import argparse
import json
import logging
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
import requests
from bs4 import BeautifulSoup

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("EcosystemJobHunter")


class EcosystemJobHunter:
    """Modular, fault-tolerant job-hunting, career page scraping, network mapping,

    and recruiter intelligence framework.
    """

    def __init__(self, company_manifest: List[Dict[str, str]]):
        self.manifest = company_manifest
        self.home_dir = Path.home()
        self.data_dir = Path("data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.html_output_path = self.home_dir / "job_hunting_summary.html"
        self.direct_json_path = self.data_dir / "direct_career_jobs.json"
        self.recruiter_json_path = self.data_dir / "recruiter_leads.json"
        self.launchpad_json_path = self.data_dir / "company_launchpad.json"

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.career_keywords = [
            "career",
            "careers",
            "vacancies",
            "work-with-us",
            "join-us",
            "join-our-team",
            "open-roles",
            "positions",
            "opportunities",
            "jobs",
        ]
        self.exclude_keywords = [
            "grant",
            "grants",
            "scholarship",
            "blog",
            "news",
            "press",
            "article",
            "townhouse",
            "donor",
        ]
        self.job_title_pattern = re.compile(
            r"\b(Director|Manager|Specialist|Advisor|Officer|Lead|Analyst|Coordinator|Consultant|Associate|Executive|Head of|Project Manager)\b",
            re.IGNORECASE,
        )

        self.specialized_agencies = [
            {"name": "Capstone Recruitment", "focus": "Property & Infrastructure"},
            {"name": "Macdonald & Company", "focus": "Real Estate & Development"},
            {"name": "Gough Recruitment", "focus": "Property & Real Asset Management"},
            {"name": "SHK Asia Pacific", "focus": "Executive & Government/NFP"},
            {"name": "Davidson", "focus": "Public Sector & Community Housing"},
        ]

        # In-memory storage for incremental renders
        self.discovered_jobs: List[Dict[str, str]] = []
        self.network_dorks: Dict[str, str] = {}
        self.recruiter_dorks: Dict[str, str] = {}

    def _fetch_url(self, url: str, timeout: int = 6) -> requests.Response | None:
        """Helper to fetch URLs with short timeout to prevent blocking."""
        try:
            res = requests.get(
                url, headers=self.headers, timeout=timeout, allow_redirects=True
            )
            return res if res.status_code == 200 else None
        except requests.RequestException as e:
            logger.debug(f"Request skipped for {url}: {e}")
            return None

    def extract_job_titles_from_page(
        self, page_url: str, company_name: str
    ) -> List[Dict[str, str]]:
        """Parses a career page HTML to identify active job vacancy titles."""
        found_jobs = []
        res = self._fetch_url(page_url)
        if not res:
            return found_jobs

        soup = BeautifulSoup(res.text, "html.parser")
        candidate_elements = soup.find_all(
            ["h1", "h2", "h3", "h4", "a", "li", "div", "p"]
        )
        seen_titles: Set[str] = set()

        for elem in candidate_elements:
            text = elem.get_text().strip()
            text_clean = " ".join(text.split())

            if (
                len(text_clean) > 5
                and len(text_clean) < 100
                and self.job_title_pattern.search(text_clean)
            ):
                if not any(
                    ex in text_clean.lower() for ex in self.exclude_keywords
                ):
                    if text_clean.lower() not in seen_titles:
                        seen_titles.add(text_clean.lower())

                        href = (
                            elem["href"]
                            if elem.name == "a" and elem.has_attr("href")
                            else page_url
                        )
                        full_link = urllib.parse.urljoin(page_url, href)

                        found_jobs.append(
                            {
                                "company": company_name,
                                "title": text_clean,
                                "source": "Direct Career Page",
                                "snippet": f"Active vacancy detected on {company_name} career portal.",
                                "url": full_link,
                            }
                        )

        return found_jobs

    def scan_direct_career_pages(self):
        """Identifies career page URLs and extracts open job listings."""
        logger.info("--- STEP 1: SCANNING DIRECT CAREER PAGES ---")

        for company in self.manifest:
            name = company["name"]
            url = company["url"]
            fallback_career_url = company.get("career_url")

            logger.info(f"Polling {name}")
            career_page_url = None

            res = self._fetch_url(url)
            if res:
                soup = BeautifulSoup(res.text, "html.parser")
                for link in soup.find_all("a", href=True):
                    href = link["href"].strip()
                    anchor_text = link.get_text().strip().lower()
                    href_lower = href.lower()

                    if any(
                        ex in href_lower or ex in anchor_text
                        for ex in self.exclude_keywords
                    ):
                        continue

                    if any(
                        kw in anchor_text or kw in href_lower
                        for kw in self.career_keywords
                    ):
                        career_page_url = urllib.parse.urljoin(url, href)
                        logger.info(f"  [+] Found Career Page: {career_page_url}")
                        break

            if not career_page_url and fallback_career_url:
                career_page_url = fallback_career_url

            if career_page_url:
                jobs = self.extract_job_titles_from_page(career_page_url, name)
                if jobs:
                    for j in jobs:
                        logger.info(f"      * Discovered Role: {j['title']}")
                    self.discovered_jobs.extend(jobs)

            # Incremental save after each company
            self._save_json(self.direct_json_path, self.discovered_jobs)
            self.render_html_report()

        logger.info(
            f"Step 1 Complete: {len(self.discovered_jobs)} direct roles saved to {self.direct_json_path}"
        )

    def generate_launchpads_and_dorks(self):
        """Constructs deterministic search URLs for LinkedIn, SEEK, and Executive Search."""
        logger.info("--- STEP 2: GENERATING NETWORK & RECRUITER SEARCH LAUNCHPADS ---")

        company_names = [f'"{c["name"]}"' for c in self.manifest]
        grouped_names = " OR ".join(company_names)

        # 1. Network Connections Dorks
        decision_makers_dork = f'site:linkedin.com/in ("Head of People" OR "Talent Acquisition" OR "Head of Development" OR "Investment Director" OR "Managing Director") ({grouped_names}) "Melbourne"'
        bridge_dork = f'site:linkedin.com/in "Melbourne" ("formerly" OR "ex-") ({grouped_names})'

        self.network_dorks = {
            "decision_makers_url": f"https://www.google.com/search?q={urllib.parse.quote_plus(decision_makers_dork)}",
            "bridge_connections_url": f"https://www.google.com/search?q={urllib.parse.quote_plus(bridge_dork)}",
        }

        # 2. Recruiter & TA Dorks
        internal_ta_dork = f'site:linkedin.com/in ("Talent Acquisition" OR "Recruitment Partner" OR "People & Culture Director") ({grouped_names}) "Melbourne"'
        agency_sector_dork = 'site:linkedin.com/in ("Recruiter" OR "Search Consultant" OR "Principal Consultant" OR "Talent Partner") ("Property" OR "Real Estate" OR "Affordable Housing" OR "ESG" OR "Impact Investment") "Melbourne"'
        agency_client_dork = f'site:linkedin.com/in ("Recruiter" OR "Executive Search" OR "Consultant") ({grouped_names}) "Melbourne"'

        self.recruiter_dorks = {
            "internal_ta_url": f"https://www.google.com/search?q={urllib.parse.quote_plus(internal_ta_dork)}",
            "agency_sector_url": f"https://www.google.com/search?q={urllib.parse.quote_plus(agency_sector_dork)}",
            "agency_client_url": f"https://www.google.com/search?q={urllib.parse.quote_plus(agency_client_dork)}",
        }

        # 3. Company Search Launchpad Data
        launchpad_data = []
        for comp in self.manifest:
            name = comp["name"]
            c_url = comp.get("career_url", comp["url"])
            seek_url = f"https://www.seek.com.au/jobs?keywords={urllib.parse.quote_plus(f'\"{name}\"')}"
            linkedin_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(f'site:linkedin.com/jobs \"{name}\" \"Melbourne\"')}"

            launchpad_data.append(
                {
                    "company": name,
                    "career_url": c_url,
                    "seek_search_url": seek_url,
                    "linkedin_search_url": linkedin_url,
                }
            )

        self._save_json(self.launchpad_json_path, launchpad_data)
        self._save_json(
            self.recruiter_json_path,
            {
                "recruiter_dorks": self.recruiter_dorks,
                "agencies": self.specialized_agencies,
            },
        )

        self.render_html_report()
        logger.info(f"Step 2 Complete: Search shortcuts saved to {self.launchpad_json_path}")

    def _save_json(self, path: Path, data):
        """Helper to save data to JSON safely."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to write to {path}: {e}")

    def render_html_report(self):
        """Renders the HTML summary report using currently available data."""
        timestamp = datetime.now().strftime("%B %d, %Y - %H:%M")

        # Deduplicate job listings
        seen_keys = set()
        unique_listings = []
        for item in self.discovered_jobs:
            key = f"{item['company']}-{item['title'].lower()}"
            if key not in seen_keys:
                seen_keys.add(key)
                unique_listings.append(item)

        rows_html = ""
        for job in unique_listings:
            rows_html += f"""
            <tr>
                <td><strong>{job['company']}</strong></td>
                <td><span class="job-title-text">{job['title']}</span></td>
                <td><span class="badge direct-career-page">{job['source']}</span></td>
                <td class="snippet">{job['snippet']}</td>
                <td><a href="{job['url']}" target="_blank" rel="noopener noreferrer" class="btn-link">Open Listing ↗</a></td>
            </tr>
            """

        company_rows_html = ""
        for comp in self.manifest:
            name = comp["name"]
            c_url = comp.get("career_url", comp["url"])
            seek_url = f"https://www.seek.com.au/jobs?keywords={urllib.parse.quote_plus(f'\"{name}\"')}"
            linkedin_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(f'site:linkedin.com/jobs \"{name}\" \"Melbourne\"')}"

            company_rows_html += f"""
            <tr>
                <td><strong>{name}</strong></td>
                <td><a href="{c_url}" target="_blank" class="btn-link-sec">Career Page ↗</a></td>
                <td><a href="{seek_url}" target="_blank" class="btn-link-seek">SEEK Jobs ↗</a></td>
                <td><a href="{linkedin_url}" target="_blank" class="btn-link-li">LinkedIn Jobs ↗</a></td>
            </tr>
            """

        agency_rows_html = ""
        for agency in self.specialized_agencies:
            a_name = agency["name"]
            a_focus = agency["focus"]
            agency_linkedin_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(f'site:linkedin.com/in \"{a_name}\" \"Melbourne\" (\"Consultant\" OR \"Recruiter\")')}"

            agency_rows_html += f"""
            <tr>
                <td><strong>{a_name}</strong></td>
                <td>{a_focus}</td>
                <td><a href="{agency_linkedin_url}" target="_blank" class="btn-link-recruiter">Find {a_name} Consultants ↗</a></td>
            </tr>
            """

        dec_url = self.network_dorks.get("decision_makers_url", "#")
        bridge_url = self.network_dorks.get("bridge_connections_url", "#")
        ta_url = self.recruiter_dorks.get("internal_ta_url", "#")
        sec_url = self.recruiter_dorks.get("agency_sector_url", "#")
        cli_url = self.recruiter_dorks.get("agency_client_url", "#")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ecosystem Job & Recruiter Intelligence Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            background-color: #f7fafc;
            margin: 0;
            padding: 2rem;
        }}
        .container {{
            max-width: 1150px;
            margin: 0 auto;
            background: #ffffff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        h1 {{ color: #2d3748; margin-bottom: 0.2rem; }}
        h2 {{ color: #4a5568; margin-top: 2rem; border-bottom: 2px solid #edf2f7; padding-bottom: 0.5rem; }}
        .meta {{ color: #718096; font-size: 0.9rem; margin-bottom: 1.5rem; }}
        .actions {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.5rem; }}
        .btn {{
            display: inline-block;
            background: #3182ce;
            color: #ffffff;
            padding: 0.55rem 1.1rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .btn:hover {{ background: #2b6cb0; }}
        .btn-purple {{ background: #805ad5; }}
        .btn-purple:hover {{ background: #6b46c1; }}
        .btn-teal {{ background: #319795; }}
        .btn-teal:hover {{ background: #2c7a7b; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        th, td {{
            padding: 0.75rem 0.85rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
            font-size: 0.9rem;
        }}
        th {{ background-color: #edf2f7; color: #4a5568; font-size: 0.8rem; text-transform: uppercase; }}
        .job-title-text {{ font-weight: 600; color: #2d3748; }}
        .snippet {{ color: #4a5568; font-size: 0.85rem; }}
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge.direct-career-page {{ background: #c6f6d5; color: #22543d; }}
        
        .btn-link {{
            display: inline-block;
            background: #2b6cb0;
            color: #ffffff !important;
            padding: 0.35rem 0.7rem;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .btn-link:hover {{ background: #2c5282; }}
        .btn-link-sec {{ color: #319795; font-weight: 600; text-decoration: none; }}
        .btn-link-seek {{ color: #d69e2e; font-weight: 600; text-decoration: none; }}
        .btn-link-li {{ color: #3182ce; font-weight: 600; text-decoration: none; }}
        .btn-link-recruiter {{ color: #805ad5; font-weight: 600; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Melbourne Real Estate, Impact & Housing Job Intelligence</h1>
        <div class="meta">Last Updated: {timestamp} | Total Direct Roles Found: <strong>{len(unique_listings)}</strong></div>
        
        <h2>1. Network Connections & Warm Lead Launchpad</h2>
        <div class="actions">
            <a href="{dec_url}" target="_blank" class="btn">Find Decision-Makers on LinkedIn ↗</a>
            <a href="{bridge_url}" target="_blank" class="btn">Find Former Employee Bridge Leads ↗</a>
        </div>

        <h2>2. Recruiter & Executive Search Intelligence</h2>
        <div class="actions">
            <a href="{ta_url}" target="_blank" class="btn btn-purple">Find In-House TA & HR Leads ↗</a>
            <a href="{sec_url}" target="_blank" class="btn btn-purple">Find Property/ESG Agency Recruiters ↗</a>
            <a href="{cli_url}" target="_blank" class="btn btn-teal">Find Recruiters Mentioning Ecosystem Clients ↗</a>
        </div>

        <h3>Specialized Melbourne Recruitment Agencies</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 35%;">Agency Name</th>
                    <th style="width: 40%;">Primary Sector Focus</th>
                    <th style="width: 25%;">Search Action</th>
                </tr>
            </thead>
            <tbody>
                {agency_rows_html}
            </tbody>
        </table>

        <h2>3. Active Discovered Job Listings (Parsed from Career Pages)</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Company</th>
                    <th style="width: 28%;">Role Title</th>
                    <th style="width: 15%;">Source</th>
                    <th style="width: 23%;">Snippet</th>
                    <th style="width: 12%;">Action</th>
                </tr>
            </thead>
            <tbody>
                {rows_html if rows_html else '<tr><td colspan="5">Scanning career pages or no open roles detected... Use the company search launchpad below.</td></tr>'}
            </tbody>
        </table>

        <h2>4. 1-Click Company Search Launchpad</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 40%;">Company Name</th>
                    <th style="width: 20%;">Direct Website</th>
                    <th style="width: 20%;">SEEK Search</th>
                    <th style="width: 20%;">LinkedIn Search</th>
                </tr>
            </thead>
            <tbody>
                {company_rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        with open(self.html_output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def execute_hunt(self, direct_only: bool = False):
        """Runs the complete automation suite with incremental saving."""
        logger.info("Starting Ecosystem Automated Job & Recruiter Hunting Process")

        # Step 1: Generate 100% reliable launchpads first so user immediately has working HTML
        self.generate_launchpads_and_dorks()

        # Step 2: Direct Career Page Web Scraping
        if not direct_only:
            self.scan_direct_career_pages()

        logger.info(f"Execution complete. Output generated at: {self.html_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ecosystem Job & Network Hunter")
    parser.add_argument(
        "--launchpad-only",
        action="store_true",
        help="Generate launchpads and dorks instantly without web scraping.",
    )
    args = parser.parse_args()

    COMPANY_MANIFEST = [
        {
            "name": "Conscious Investment Management",
            "url": "https://www.consciousinvest.com.au/",
            "career_url": "https://www.consciousinvest.com.au/",
        },
        {
            "name": "Impact Investment Group",
            "url": "https://www.impact-group.com.au/",
            "career_url": "https://www.impact-group.com.au/",
        },
        {
            "name": "Assemble",
            "url": "https://assemble.com.au/",
            "career_url": "https://assemble.com.au/careers/",
        },
        {
            "name": "Future Super",
            "url": "https://www.futuresuper.com.au/",
            "career_url": "https://www.futuresuper.com.au/careers/",
        },
        {
            "name": "Nightingale Housing",
            "url": "https://www.nightingalehousing.org/",
            "career_url": "https://www.nightingalehousing.org/careers",
        },
        {
            "name": "MAKE Property Group",
            "url": "https://makeventures.com.au/",
            "career_url": "https://makeventures.com.au/about/",
        },
        {
            "name": "Habitat for Humanity Victoria",
            "url": "https://www.habitatvic.org.au/",
            "career_url": "https://www.habitatvic.org.au/careers",
        },
        {
            "name": "Nexus Developments",
            "url": "https://nexusdevelopments.com.au/",
            "career_url": "https://nexusdevelopments.com.au/",
        },
        {
            "name": "Sefa",
            "url": "https://sefa.com.au/",
            "career_url": "https://sefa.com.au/join-us",
        },
        {
            "name": "Lord Mayor's Charitable Foundation",
            "url": "https://www.greatermelbournefoundation.org.au/",
            "career_url": "https://www.greatermelbournefoundation.org.au/about/careers",
        },
        {
            "name": "Australian Impact Investments",
            "url": "https://australianimpactinvestments.com.au/",
            "career_url": "https://australianimpactinvestments.com.au/",
        },
        {
            "name": "Fontic",
            "url": "https://www.fontic.com.au/",
            "career_url": "https://www.fontic.com.au/",
        },
        {
            "name": "Housing Australia",
            "url": "https://www.housingaustralia.gov.au/",
            "career_url": "https://www.housingaustralia.gov.au/careers",
        },
        {
            "name": "Development Victoria",
            "url": "https://www.development.vic.gov.au/",
            "career_url": "https://www.development.vic.gov.au/careers",
        },
        {
            "name": "Homes Victoria",
            "url": "https://www.homes.vic.gov.au/",
            "career_url": "https://www.homes.vic.gov.au/jobs-and-opportunities",
        },
        {
            "name": "Housing Choices Australia",
            "url": "https://www.housingchoices.org.au/",
            "career_url": "https://www.housingchoices.org.au/about-us/careers/",
        },
        {
            "name": "SGCH",
            "url": "https://www.sgch.com.au/",
            "career_url": "https://www.sgch.com.au/join-our-team/",
        },
        {
            "name": "HousingFirst",
            "url": "https://www.housingfirst.org.au/",
            "career_url": "https://www.housingfirst.org.au/work-with-us",
        },
        {
            "name": "Slattery",
            "url": "https://slattery.com.au/",
            "career_url": "https://slattery.com.au/about/careers",
        },
        {
            "name": "Impact Investing Australia",
            "url": "https://impactinvestingaustralia.com/",
            "career_url": "https://impactinvestingaustralia.com/",
        },
    ]

    hunter = EcosystemJobHunter(COMPANY_MANIFEST)
    hunter.execute_hunt(direct_only=args.launchpad_only)