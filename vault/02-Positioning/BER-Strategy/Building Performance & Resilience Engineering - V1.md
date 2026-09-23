# Director of Building Performance & Resilience Engineering

## Business Case & 3-Year Strategy — JFS Engineers

**Contents**: 1. The Opportunity · 2. Candidate Fit Assessment · 3. Quick Wins (0–6 months) · 4. Three-Year Strategy · 5. What the Director Role Needs to Own · 5a. Professional Indemnity & Liability Considerations · 6. Open Questions · 7. Recommended Technical Pipeline (Appendix)

---

## 1. The Opportunity

[[JFS Engineers]] has an established façade/envelope engineering practice (20–100 staff) with real technical depth already in place — System Thermal Assessment, Condensation Risk Assessment, Cladding Pressure Assessment, CFD Wind Assessment, and Overall Building Energy Modeling all already appear on JFS's current service list. What's missing isn't the underlying technical capability from scratch — it's the repositioning of that capability into a named, marketed resilience service; the methodological upgrade from code-compliance-grade analysis to resilience-grade (design-day/heatwave, dynamic hygrothermal) analysis; and the commercial connection to climate-risk disclosure. That's a materially smaller build than "start from zero," and it's a better business case for it.

Three forces are converging right now:

- **Regulatory**: Mandatory climate-related financial disclosure (AASB S2 / ASRS) is already in force for large entities (Group 1, since Jan 2025), expands to more businesses in July 2026 (Group 2), and again in July 2027 (Group 3). Property owners, developers, and their financiers now have to explain — in financial-reporting terms — how climate hazards affect their assets. Façades are one of the most exposed, most legible parts of that story: water ingress, wind/storm damage, thermal underperformance, corrosion, bushfire exposure.
- **Technical**: Firms like Arup, Buro Happold, Inhabit and AECOM compete on deep physics-based analysis — energy/thermal simulation, thermal bridging, condensation/hygrothermal modelling, daylight/glare, wind/CFD, structural movement, and physical testing. That is the credibility bar for "market leader" — but it's a service list, not a moat. Most of it is buildable.
- **Operational**: The tooling to deliver that analysis at scale now exists outside the big firms' walls — Speckle/BHoM as a data exchange and schema layer, OpenStudio/EnergyPlus as an open simulation backbone, with human-in-the-loop QA (including offshored model production). A mid-size firm can build a governed, repeatable analysis pipeline without carrying Arup-scale headcount.

**Not every physics-based service is equally resilience-relevant, and the build-out should follow that.** Splitting the competitive-benchmark service list by how directly each ties to physical climate hazard (rather than treating it as one undifferentiated "advanced analysis" list):

|Tier|Capabilities|Why|
|:--|:--|:--|
|**Core (build first, together)**|Thermal bridging & condensation/hygrothermal · Wind pressure, wind-driven rain & water penetration · Overheating & thermal performance under **design-day/heatwave/peak-condition scenarios**|Each maps directly to an intensifying physical hazard (heat, storm/wind, extreme rainfall) named in the ASRS/AASB S2 material — these are resilience capabilities, not general design-quality services|
|**Secondary / distinct sale**|Embodied & whole-life carbon|ASRS-material, but as a _transition_-risk / decarbonisation-financing conversation, not physical resilience — keep it in the offer but don't fold it into "resilience"|
|**Lead-in / pipeline (distinct purpose)**|JV3 (NCC Section J energy compliance) · Daylight compliance for DA (NSW planning approval — e.g. ADG-type solar access/daylight requirements) · **NSW embodied-carbon/materials-index reporting** (BASIX Materials Index for residential, NABERS Embodied Emissions Materials Form for non-residential, at ≥80% of materials by quantity, DA and CC stages)|Not a resilience or ASRS sale at all — this is how JFS gets _invited onto a project_ at the DA stage, before façade documentation exists. All three are well-trodden, mandatory-or-near-mandatory compliance pathways in NSW, fast to deliver, and create the relationship that later pulls through the higher-value core-resilience and disclosure work|
|**Deprioritise for this positioning**|Daylight/glare/solar reflection (occupant comfort/design-quality framing) · Acoustics · Seismic/structural movement (non-thermal)|Amenity- or design-quality-driven, only loosely coupled (if at all) to climate hazard exposure in the Australian context|

Worth noting the overlap rather than treating these as four unrelated lists — but the overlap is in **software and modelling skillset, not methodology or output**. JV3 compliance modelling and resilience-grade overheating analysis both use the same simulation engines (EnergyPlus/IES/DesignBuilder-class), and building capability in one gives JFS a real head start on the other — but they ask different questions and need different inputs:

||JV3 (lead-in/compliance)|Core resilience capability|
|:--|:--|:--|
|Weather input|Standard/reference year (TMY-type) file|Design-day, heatwave, and future/extreme weather files|
|Question asked|Annual energy consumption vs. a compliance benchmark|Will occupants and the building survive/perform under peak and future extreme conditions?|
|Typical outputs|kWh/m²/annum, compliance pass/fail|Peak operative temperature, overheating-hour exceedance, indoor temperature under sustained heatwave|
|Client/audience|Certifier, DA approval process|Risk/asset owner, insurer, ASRS disclosure|

So the honest framing for JFS is: build JV3 delivery capability now for the lead-in service (it's needed regardless, and it's the faster win) — but treat the resilience-grade overheating capability as a **distinct methodology built on the same software platform**, not an automatic by-product of doing JV3 work. The modelling skill and tooling investment carries across; the weather files, scenario design, and output metrics do not.

Daylight has the same "same word, different service" trap: DA daylight compliance (ADG-type solar-access checks) is narrow and lead-in-only, distinct from the "daylight/glare" architectural-comfort/occupant-experience work that's deprioritised above for resilience purposes — worth keeping the two separate internally so the deprioritised one doesn't quietly creep back in.

Embodied carbon has the same split. **NSW Materials Index reporting** (BASIX/NABERS Embodied Emissions Materials Form) is a narrow, mandatory, DA/CC-stage compliance deliverable — lead-in work, and it's an easy one to add given existing embodied-carbon quantification experience (Section 2a). The broader **whole-of-life carbon advisory** service in the secondary/transition tier is a different, larger conversation about decarbonisation strategy and financing — same underlying technical skill, materially different scope and sale.

**The build order this implies**: the three Core capabilities together (clients exposed to one hazard usually have exposure to the others, so a joint offer sells better than a single-issue one), with the JV3/daylight/materials-index lead-in triad standing alongside as a separate, simpler front door — not part of the resilience pitch, but how JFS earns the right to make it on the next project.

**The position to claim**: JFS becomes the mid-market specialist that connects façade engineering, physics-based building performance analysis, and climate-risk disclosure into one service — faster and leaner than the multidisciplinary giants, more technically rigorous than compliance-only competitors. Against Tier-1 firms specifically, the durable counter-position isn't claiming they can't do this work — it's agility, senior-level access, proportionate fixed fees for mid-market decisions, and independent technical assurance, rather than trying to match their headcount or breadth.

### 1a. Reality-Checked Against JFS's Current Book (17 projects)

Worth revising the earlier framing here: across the current project sample, only **one** project has a confirmed AASB S2-grade owner — One One One Eagle Street, owned by the ASX-listed GPT Group. That means "target Group 1 entities" isn't the volume play in JFS's _existing_ book that it was framed as earlier — it's real, but narrow, and GPT is close to a named-account strategy rather than a market segment.

The larger, already-live demand in the current book actually sits in two other channels:

- **Government/statutory-procured projects (7 of 17)** — CIT Woden, the AWM redevelopment (×2 packages), Cowra Hospital, Cross River Rail, Logan Hospital, and the Carseldine Village/SGCH work. These clients aren't driven by AASB S2 at all — they're driven by jurisdictional climate targets (ACT net zero 2045, Queensland's Clean Economy Jobs Act, the NSW Health Net Zero Roadmap, Commonwealth Climate Disclosure) that convert directly into **contractual rating obligations on the façade package**: Green Star targets (6 Star at CIT Woden), IS Rating "Excellent" at Cross River Rail, NABERS/Green Star minimums under Queensland government building policy, plus ethical-supplier and modern-slavery contract clauses. This is a bigger and more immediate revenue channel for JFS today than ASRS disclosure support.
- **NSW planning law (Sustainable Buildings SEPP)** — mandatory embodied-emissions reporting at DA and CC stage for _every_ NSW development, residential and non-residential, regardless of AASB S2 status. This bites on the private NSW developers in the book (e.g. Deicorp, Beldev/IP Property) who otherwise carry no mandatory climate-reporting duty at all — the requirement comes from where the project is, not who owns it.

**Practical implication**: the near-term revenue engine for Year 1 isn't primarily "sell ASRS disclosure support" — the current book doesn't have enough Group 1-grade clients to make that a volume business yet. It's "be the façade consultant whose technical output already satisfies Green Star / IS Rating / NABERS-linked contractual requirements, and who handles NSW embodied-emissions reporting as standard." AASB S2/ASRS positioning is the medium-term growth story as Group 2 (July 2026) and Group 3 (July 2027) phase in and the client base widens beyond the current book — worth keeping both threads visible rather than betting Year 1 entirely on the disclosure narrative.

### 1b. A Fourth Channel: CRREM-Linked Retrofit via ESG-Consultant Partnerships

The three channels above all assume JFS is either the owner's direct consultant or wins new-build DA/design work directly. There's a fourth, structurally different channel worth adding: existing-building retrofit driven by CRREM (Carbon Risk Real Estate Monitor) transition-risk assessments — sold not directly to owners, but via partnership with the ESG consultants, sustainability advisors, and NABERS assessors who run the CRREM modelling in the first place.

The logic: CRREM identifies which assets face carbon "stranding" risk and roughly when — but it can't say whether the façade is actually the cause, what's technically achievable, what it costs, what embodied carbon it adds, or whether the existing structure can carry the proposed intervention. That's a façade-engineering question, not an ESG-advisory one, and most ESG consultancies don't employ that expertise in-house. JFS becomes the technical delivery partner turning "this building may strand in 2029" into a costed, buildable, whole-life-carbon-aware retrofit pathway — while the ESG advisor keeps the client relationship and portfolio strategy.

This maps directly onto JFS's existing **Remediation & Diagnostics** service line (Façade Audits, Water Ingress Investigation and Testing, Structural Assessment and Risk Profiling, Existing Asset Material Life Forecasting) — arguably a _better_ existing anchor for this channel than the new-build services are for the DA lead-in triad. Put together, JFS already has technical footholds at both ends of the building lifecycle: new-build lead-in via Façade Consulting/Building Physics, and retrofit lead-in via Remediation & Diagnostics. This channel is how the retrofit end gets commercialised and connected to a financial (not just physical) risk narrative.

Structurally, it's a lower-commitment, channel-partnership play rather than a direct-sales one: build a small number of formal relationships with ESG consultancies/NABERS assessors/energy modellers, offer a fixed-fee, low-cost entry product (a desktop triage translating a CRREM stranding-date flag into a preliminary façade-risk score), and let staged, fixed-scope packages pull the relationship deeper only where warranted. It's deliberately lean — JFS doesn't need to build ESG/CRREM expertise in-house, only enough literacy to speak the same language as the partner.

**Worth flagging as new territory**: this channel introduces a liability dimension the other three don't carry in the same way — the risk that a CRREM-derived planning target gets treated by a client as an implied guarantee of a physical-project outcome. Addressed in Section 5a.

This is the case for a dedicated Director role: someone who can own that connection commercially and technically, and isn't just running BAU delivery. Note that everything above is the market case on its own terms — it holds regardless of who fills the role. Section 2 addresses candidate fit separately.

---

## 2. Candidate Fit Assessment (Separate from the Business Case)

This is deliberately kept apart from Section 1. The market opportunity is true regardless of who holds the role; whether this candidate is the right person to execute it is a different question, and collapsing the two weakens both arguments if either is challenged. Four honest categories:

### 2a. Existing capability — bring this in on day one

Against the candidate's own project history, several strategy pillars are already proven, hands-on delivery experience rather than a build risk:

- **Design-day/heatwave overheating (Core)** — mined Bureau of Meteorology historical data against official heatwave definitions and spliced the sequences into EnergyPlus weather files to stress-test a government-backed resilient housing prototype under extreme heat; separately, applied synthetic future-climate weather files to quantify overheating risk in free-running buildings for adaptation planning and ESG reporting. This is precisely the design-day/heatwave methodology distinguished from JV3's annual-consumption approach elsewhere in this document.
- **Thermal bridging (steady-state) (Core)** — direct THERM/WINDOW-based façade heat-transfer analysis (transoms, mullions, glazing configurations under NFRC reference conditions), producing linear thermal transmittance, frame U-values and SHGC outputs.
- **Wind/water penetration (Core)** — integrated physical wind-tunnel pressure data with CFD onto structural meshes to evaluate cladding suction loads against safety compliance criteria.
- **JV3 (NCC Section J performance-solution modelling) (lead-in)** — dozens to hundreds of JV3 calculations delivered, on top of over a decade of high-fidelity EnergyPlus modelling supporting NABERS Commitment Agreements (including degraded-performance and off-axis risk scenarios, subject to independent regulatory audit). This was previously flagged as an open question in this document; it's now confirmed direct, high-volume capability.
- **Daylight compliance + comfort (lead-in and deprioritised-for-resilience, respectively)** — dozens of daylight/solar-access/visual-comfort assessments spanning commercial, aged care and residential projects, covering both statutory compliance metrics and human-centric comfort.
- **Embodied carbon (lead-in and secondary/transition line)** — formal NABERS upfront (embodied) carbon accreditation, plus whole-of-building upfront embodied carbon quantification for a major builder feeding a formal Green Star submission. This is credentialed capability, not just project experience — strengthens both the NSW materials-index lead-in service and the broader transition-risk advisory line.
- **The data pipeline itself (Year 1 operational build)** — designed and built a central documentation engine consolidating around 10 report types, a single-source-of-truth database, and automated simulation-to-deliverable pipelines.
- **Offshoring/delegation infrastructure (Year 2 scale-up)** — led an infrastructure risk audit specifically to map functions suitable for delegation or offshoring and produced the resulting delegation matrix and role SOPs.
- **Municipal-scale resilience strategy (Year 3 positioning)** — lead technical sub-consultant on a City of Melbourne project embedding climate adaptation and heatwave-refuge criteria across council-owned assets.
- **Regulatory fluency on the assessor's side (supports the lead-in service)** — delivered multi-year training for Victorian statutory planners on auditing energy-modelling submissions.

### 2b. Genuine gaps — worth naming plainly rather than glossing over

- **Dynamic hygrothermal / interstitial moisture modelling (WUFI-class).** The track record shows steady-state 2D thermal bridging (THERM/WINDOW), not dynamic hygrothermal simulation, and no personal WUFI accreditation. There's a reasonable chance someone within JFS already holds this — worth checking internally (Section 2e) before assuming an external hire or partner is needed. Since the Core condensation capability includes interstitial moisture accumulation over time — not just surface condensation — this stays a real gap for the Director personally either way.
- **Physical wind-tunnel test commissioning (narrower than first thought).** JFS's own service list already includes CFD Wind Assessment, so the computational side of this leg is covered at the firm level, not just by the Director's resume. The remaining gap is specifically commissioning _physical_ wind-tunnel testing and owning the test-house relationship — matters mainly for tall/complex buildings — worth confirming whether that relationship already exists rather than assuming it needs building from nothing.
- **Commercial/BD ownership.** The technical delivery record is very strong; the Director role also carries P&L ownership, pricing, and new-client sales. The one commercial project on record is participation in a repositioning exercise (engaging branding consultants), not direct evidence of running client acquisition personally. Worth being honest about whether this is a genuine strength, a growth area, or something JFS's existing BD function should own with the Director as the technical face.

### 2c. New organisational requirements — not a personal gap, needs building regardless of who's Director

- A documented methodology/QA standard for climate-risk assessment (consistency now, audit-defensibility later).
- Evidence-retention and disclosure-support templates (hazard screens, vulnerability assessments, metrics frameworks) — don't exist as JFS assets yet.
- The canonical data schema/pipeline architecture built for JFS's own systems and data — prior experience building something similar elsewhere de-risks this, but it still has to be built fresh here, not ported.
- The named, marketed service line and capability statement (Quick Win 3).

### 2d. Keeping it lean — hire considerations, deliberately minimal

Given the stated preference to stay lean, the instinct to resist is hiring broadly in Year 1. Two targeted additions are worth considering, not a team build:

- **One mid-level analyst/modeller** (new hire or an existing JFS staff member upskilled) to absorb JV3 lead-in volume once that pathway is proven — this frees the Director for core/strategic work rather than being consumed by compliance-volume delivery, which is the single most likely way a lean plan quietly fails (the Director's time gets eaten by the lead-in service instead of the resilience build it's meant to fund).
- **A specialist partner or subcontractor relationship — check internally first.** For dynamic hygrothermal (WUFI) modelling specifically, there's a reasonable chance someone within JFS already holds this accreditation (Section 2e) — confirm before committing to an external partner. Physical wind-tunnel test commissioning is more likely to need an external relationship regardless. Either way, pay for access rather than headcount — both are used on a subset of projects, not enough to justify an FTE.

Everything else in Year 1 — positioning, quick wins, the pipeline MVP, governance — can plausibly run through the Director plus existing JFS staff being redirected or trained, without new hires.

### 2e. Where JFS's Existing Capability Actually Stands

This was originally a speculative audit ("check whether anyone does X"). JFS's own current service list answers most of it directly — the picture is considerably stronger than assumed, and the open items are about depth and methodology, not existence:

|Core hazard capability|Confirmed on JFS's current service list|What's actually left to check|
|:--|:--|:--|
|**Thermal bridging & condensation**|System Thermal Assessment and Condensation Risk Assessment (both full and preliminary-stage) are already named services|Depth: is this steady-state, code-compliance-level assessment, or does it reach dynamic hygrothermal/interstitial moisture modelling (the genuine gap flagged in 2b)? Likely the former — the upgrade path is methodological, not a build from zero.|
|**Wind / water penetration**|Cladding Pressure Assessment, CFD Wind Assessment, and Water Ingress Investigation and Testing are all already named services — this is the most mature of the three legs at the firm level|Whether physical wind-tunnel test commissioning (vs. CFD) is already an established relationship, or needs building (2b).|
|**Overheating / thermal performance**|Overall Building Energy Modeling is already a named service, alongside Performance Solution Reports, Performance Based Design Brief, and Technical Performance Specification — NCC performance-solution/verification-method language JFS already operates in|Whether existing energy modelling is calibrated to annual/compliance metrics (JV3-type, most likely) or already touches design-day/heatwave scenarios — almost certainly the former, which means the Core resilience methodology (2a, 2b) is a genuine and valuable addition on top of real existing capability, not a parallel build.|

Two additional findings worth folding into the JV3/lead-in service specifically: the presence of **Performance Solution Reports**, **Performance Based Design Brief**, and **Technical Performance Specification** on JFS's list strongly suggests JFS already operates in the NCC performance-solution space in some form — Quick Win 6 is likely closer to "formalise and extend an existing capability" than "stand up something new." Separately, **Solar Assessment** and **Glare Assessment** are already services, which may already cover some of the DA daylight-compliance ground — worth confirming whether that's ADG-type solar-access compliance or façade-design solar heat gain analysis, since those are different deliverables despite the overlap in tools.

Not currently on the list, consistent with the gap already identified: any embodied-carbon or materials-index service (2b/2c) — this remains a genuine build, not something to assume exists.

Practical first step, now narrower than before: rather than a broad discovery interview, a focused conversation with whoever delivers System Thermal Assessment, CFD Wind Assessment, and Overall Building Energy Modeling today — to confirm methodology depth (steady-state vs. dynamic, annual vs. design-day) and whether "Performance Solution Reports" already includes JV3 specifically.

---

## 3. Quick Wins (0–6 months)

Low-capex, fast-to-market moves that generate revenue and credibility while the longer build happens in the background.

1. **Climate-risk register add-on to existing façade scopes.** For current and recent clients, offer a structured façade climate-risk assessment (hazard screen + vulnerability assessment, using the checklist format regulators expect) as an extension to existing condition surveys, remedial scopes, and new-build design reviews. Minimal new capability required — mostly repackaging and structuring what the team already assesses informally.
2. **Target the two channels with real, current pull-through.** Rather than a generic "Group 1 entities" search: (a) GPT/111 Eagle Street is the one confirmed AASB S2-grade relationship in the current book — worth a specific, named account plan; (b) the government-procured cohort (NSW Health Infrastructure, Cross River Rail Delivery Authority, Metro South Health, AWM, CIT/Major Projects Canberra) already carries live Green Star / IS Rating / NABERS-linked contractual obligations that JFS's façade technical output feeds directly — position climate-resilience input as protecting those existing rating commitments, not as a new ASRS-disclosure pitch.
3. **A named service line and one-page capability statement.** Formalise "Building Performance & Resilience Engineering" as a distinct, marketed service — even before the full technical build-out is complete. Naming and packaging it creates the sales conversation.
4. **Remedial-works reframe.** For live and upcoming remedial projects, shift the framing from "what failed, how do we fix it" to "what failed, why, and will the fix hold under the future hazard profile" — a differentiated, defensible scope addition that's a natural extension of work already being quoted.
5. **The three core hazard capabilities, not one flagship — and lower-risk than first framed.** JFS's current service list already confirms System Thermal Assessment, Condensation Risk Assessment, Cladding Pressure Assessment, and CFD Wind Assessment as existing services. The build isn't three capabilities from scratch — it's upgrading two legs from code-compliance-grade to resilience-grade methodology (dynamic hygrothermal, design-day/heatwave) and confirming the depth of what already exists (Section 2e) before selling it as a joint "resilience core."
6. **Formalise JV3 + DA daylight compliance + NSW materials-index reporting as the lead-in offer.** JV3 itself is now confirmed, not hedged: dozens to hundreds of calculations already delivered directly (Section 2a) — this can be marketed and scaled immediately, not piloted first. JFS's own service list (Performance Solution Reports, Performance Based Design Brief, Overall Building Energy Modeling) suggests the firm already operates in this space too, which is worth confirming to understand how much is genuinely new vs. consolidation. Materials-index reporting is a credentialed capability as well (NABERS upfront carbon accreditation, Section 2a), so all three legs of this lead-in triad are lower-risk than originally scoped. The platform recommended for the pipeline build (Better Building — see Section 7) has a purpose-built NCC 2022 J1V3 workflow, which helps scale this beyond one person.
7. **Launch the CRREM-to-Façade Desktop Triage and initiate 2–3 channel-partner relationships.** A fixed-fee, low-cost product that converts an ESG consultant's CRREM stranding-date flag into a preliminary façade-risk score — the entry point for the fourth channel (Section 1b). Approach ESG consultancies, sustainability advisors, and independent NABERS assessors as partners, not competitors: they keep the client relationship and portfolio strategy, JFS supplies the façade-engineering evidence. Anchors on JFS's existing Remediation & Diagnostics service line, so — like Quick Win 5 — this is formalising existing capability more than building from scratch. Sequence the PI/liability setup in Section 5a before this goes to market.

---

## 4. Three-Year Strategy

### Year 1 — Establish the position

The first six months are Quick Wins 1–7 above. Across the full year, that work extends into:

- Full stand-up of the three core hazard capabilities as one connected, sellable service (Quick Win 5) — not just piloted — ready to sell into both the government-procured cohort and the GPT-style named account (Quick Win 2).
- Deepen the 2–3 channel-partner relationships from Quick Win 7 into a repeatable referral flow, rather than one-off introductions — this is a structurally different, lower-commitment channel from the direct/government/DA-lead-in channels above, and worth tracking separately.
- The data pipeline MVP: pilot Better Building against DesignBuilder for the offshore-modelling platform decision — see Section 7 for the full architecture, the offshore/local work boundary, and the pilot plan.
- Formalise governance: who at JFS owns climate-risk methodology, how it's QA'd, how evidence is retained — this becomes sellable IP and later audit-defensible track record.

### Year 2 — Build out the technical scope and delivery engine

- Deepen the core three (e.g. moving from steady-state to dynamic hygrothermal modelling, CFD-based wind studies for higher-complexity projects) rather than broadening into the deprioritised list. Add daylight/glare, acoustics, or seismic/structural-movement services only opportunistically — client-requested, partnered, or bundled — not as a strategic build.
- Add embodied/whole-life carbon as a distinct second service line (separate sales motion — decarbonisation/financing-linked, not resilience-linked).
- Scale the data pipeline: template libraries, automated QA gates, and — if volume justifies it — an offshore production capability for model conversion/preparation, freeing senior staff for judgement-heavy review rather than manual model-building.
- Target Group 2 entities entering scope from July 2026 as a defined sales campaign, using Year 1 case studies as proof.
- Develop reusable disclosure-support artefacts (hazard screens, vulnerability assessment templates, metrics frameworks) that can be repriced and resold across clients rather than rebuilt each time.
- Build out staged CRREM-linked retrofit packages beyond the desktop triage — a Façade Carbon Feasibility Study and a Retrofit Options and Carbon-Capex Plan — for partner-referred assets, and begin a proprietary project-experience benchmark database (typology, climate zone, intervention type, capex/m², embodied carbon/m²). This becomes a genuine moat as it accumulates — more durable than CRREM familiarity alone, which any competitor can acquire.

### Year 3 — Market leadership positioning

- Publicly position JFS as the tech-enabled, mid-market alternative to the big multidisciplinary consultancies for façade climate resilience — differentiated on speed, cost, and specialisation rather than trying to match their headcount or breadth.
- Ahead of the Group 3 wave (July 2027), run structured outreach to the newly in-scope mid-size businesses — a segment the big firms are less likely to prioritise but that fits JFS's existing size and relationships well.
- Evaluate whether the internal pipeline/tooling itself becomes a productised offering (e.g. a portal or reporting tool) — an additional revenue line beyond consulting hours.
- Review and refresh: by year 3, some of today's differentiators will be commoditised — use the accumulated project evidence base and methodology track record as the next moat (auditability and demonstrated outcomes matter increasingly as ASRS assurance requirements tighten over time).
- Productise an **Independent Façade Retrofit Assurance Review** — a second-opinion service testing whether a Tier-1 firm's proposed retrofit strategy is technically feasible, structurally viable, moisture-safe, and properly costed. A way to enter high-value assignments without competing for the whole project. Add **post-occupancy reconciliation** (comparing modelled vs. measured outcomes) as a recurring revenue line, distinguishing JFS from consultants who stop at the design report.

---

## 5. What the Director Role Needs to Own

- **Commercial**: service-line P&L, client targeting (the government-procured cohort, the GPT-style named AASB S2 account, and the widening Group 2/3 pool as it phases in), pricing of new offers.
- **Technical governance**: methodology standards for climate-risk assessment and physics-based analysis, QA framework, evidence retention.
- **Delivery infrastructure**: sponsorship of the data pipeline build (schema, tooling, potential offshore capability) — not hands-on-keyboard, but the decision-maker on architecture and investment.
- **Positioning**: the external face of "JFS does building performance and resilience" — content, case studies, conference/industry presence.

---

## 5a. Professional Indemnity & Liability Considerations

This wasn't a live issue for the first three channels in the same way, but the CRREM/retrofit channel (Section 1b) — and to a lesser extent ASRS-disclosure-linked work generally — introduces a distinct risk: a planning-level output (a CRREM stranding date, an ASRS disclosure metric) being treated by a client as an implied guarantee of a physical-project outcome (energy savings, carbon reduction, a NABERS rating, a valuation uplift). The Director should own this as a governance matter before the channel is marketed, not after the first claim.

Practical requirements before Quick Win 7 goes to market:

- **Confirm PI insurance scope** with JFS's broker specifically for remedial/retrofit advisory work: coverage for water-ingress, condensation, and thermal-performance claims; any cladding/combustible-cladding exclusions; whether design-and-construct or novated roles are excluded.
- **Appointment language**: explicitly state that energy, carbon, NABERS, CRREM, and valuation outcomes are modelling estimates, not guarantees; define named reliance parties only; require written sign-off for contractor substitutions post-design.
- **Scope discipline**: resist being asked for a definitive retrofit recommendation from a CRREM stranding date alone — that's a planning signal, not an engineering scope, and needs the staged feasibility work in between.

This is a one-off setup cost — a broker conversation, a contract-language update — not an ongoing burden. Worth sequencing into the first 90 days alongside Quick Win 7, before the first partner-referred engagement rather than after.

---

## 6. Open Questions to Sharpen This Further

- Whether "Performance Solution Reports" / "Performance Based Design Brief" on JFS's service list already includes JV3 work at the firm level (separate from the Director's personal track record, now confirmed in Section 2a), or NCC Section J performance solutions more generally — determines how much of Quick Win 6 is scaling an individual capability into a firm-wide one vs. genuinely new to JFS.
- Whether "Solar Assessment" on JFS's service list already covers ADG-type DA daylight compliance, or is façade-design solar heat gain analysis only (Section 2e).
- Whether existing System Thermal Assessment / Condensation Risk Assessment / Overall Building Energy Modeling work is steady-state/annual (most likely) or already touches dynamic hygrothermal and design-day/heatwave methodology (Section 2e).
- Whether anyone within JFS currently holds WUFI/dynamic hygrothermal accreditation — worth checking before assuming an external partner is needed (Section 2b/2d).
- Is the 17-project list the full current book or a sample — and what proportion of JFS's overall work is NSW-based (determines how central the NSW lead-in service and SEPP-driven materials-index work should be to the Year 1 plan)?
- Are GPT (111 Eagle Street), NSW Health Infrastructure, Cross River Rail Delivery Authority, and AWM active ongoing relationships to build on, or one-off single-project engagements?
- Is there appetite/budget for the data pipeline build, or does Year 1 need to be self-funding from quick wins first?
- What's the competitive set locally (Melbourne/Victoria) — are Arup/Buro Happold/AECOM active in this specific niche regionally, or is the real competition smaller specialist façade consultancies without the physics depth?
- Whether JFS has an existing BD/client-acquisition function the Director would work alongside, or whether commercial ownership sits with the Director alone (Section 2b).
- Whether a physical wind-tunnel test-house relationship already exists at JFS or needs establishing (Section 2b/2d).
- Whether JFS already has any relationships with ESG consultancies, sustainability advisors, or independent NABERS assessors to build the Section 1b channel-partner strategy on, or whether this is a cold-start business-development effort.
- Current PI insurance scope — does it already cover remedial/retrofit advisory claims (water ingress, condensation, thermal performance), or does this need confirming before Quick Win 7 is marketed (Section 5a)?

---

## 7. Recommended Technical Pipeline (Appendix)

This is the concrete answer to "what does the Year 1 data pipeline MVP actually run on," based on a comparison of building-simulation geometry tools against JFS's specific use case: take architectural PDFs, send them to an offshore model-build team with a clear brief, get back an analytical model, then enrich it with NCC compliance data and HVAC before it feeds downstream façade and design workflows.

**Platform choice**: pilot **Better Building** as the primary platform — it's browser-based (simplifying offshore deployment), has purpose-built Australian NCC/J1V3 workflows already, and exports EnergyPlus epJSON as a clean escape hatch into custom tooling. Run **DesignBuilder** in parallel as the alternative for cases needing deeper bidirectional editing (it returns a richer, more editable handoff format but carries a heavier training burden). Neither needs to be "won" definitively before starting — the pilot recommendation below tests both on the same two projects.

**The pipeline, end to end**:

PDF intake → automated sheet preparation (split, rasterise, name by sheet/revision/level) → offshore analytical modelling → structured export (IDF/epJSON/dsbXML) → canonical model with provenance → automated QA → NCC/HVAC enrichment → EnergyPlus compliance model → façade data products.

**The offshore/local boundary — this is the governance decision that matters most**: the offshore team should build the _observed_ geometry only — zones, surfaces, openings, shading, levels, all traceable back to a specific drawing sheet — never make engineering judgement calls. Deterministic enrichment (construction references copied from a schedule, HVAC templates selected from a prescribed decision table) can move offshore once the brief is unambiguous. Everything requiring judgement stays with the local Australian technical team: NCC interpretation, thermal-bridge methodology, façade U-value and SHGC acceptance, infiltration assumptions, performance-solution conclusions, and final sign-off. This boundary is what keeps the lean-hire model in Section 2d viable — it's what one local analyst can credibly review and sign off on, rather than needing to re-derive.

**Four canonical layers**, kept separate so an engineering assumption change never forces a geometry rebuild: Source (drawings, revisions, extracted labels), Geometry (levels, zones, surfaces, openings, shading), Engineering (constructions, glazing, schedules, loads, HVAC), Compliance (proposed/reference rules, NCC assumptions, reporting metadata).

**Handoff discipline**: never accept just a native project file back from offshore. Require a structured submission bundle — source drawings, calibrated underlays, the native authoring file, exchange formats (IDF/epJSON/gbXML), and a review package (assumptions log, object register, QA results, marked-up plans) — plus a manifest recording model identifiers, drawing revision, tool/version, and known exclusions. Every zone and envelope object should carry a stable ID traceable to its source drawing, so downstream façade analysis can reference source objects rather than fragile auto-generated surface names.

**Where to actually spend development effort**: not on building another geometry editor — on automated QA. First scripts to write: closed-volume checks, matching adjacent surfaces, no incorrectly-adiabatic exterior walls, no duplicate/zero-area surfaces, floor areas reconciling with the model summary, every significant object mapped to a drawing reference or a logged assumption. This is the actual moat — nominally valid exchange files routinely contain omitted or fragmented geometry that only structured validation catches.

**Pilot plan**: run the same two test projects — one Class 1 dwelling (pitched roof, garage, roofspace, mixed glazing) and one small Class 5–9 building (several levels, perimeter/core zoning, non-trivial façade) — through Better Building and DesignBuilder in parallel, with separate offshore modellers working from the same brief. Measure brief-preparation time, modelling time, clarification requests, first-pass QA failure count, local correction time, and time to produce the façade schedule and proposed/reference compliance models. Optimise the decision for total local review time, not raw offshore modelling speed — that's the real cost driver in a lean model.