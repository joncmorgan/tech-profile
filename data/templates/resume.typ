// ==============================================================================
// TEMPLATE: data/templates/resume.typ
// VERSION:  3.2.0
// STATUS:   A4 Professional Executive Resume Layout Blueprint
// ==============================================================================

// 1. INPUT VARIABLES (Hydrated from Python Runtime)
#let name = sys.inputs.at("name", default: "Candidate Name")
#let contact = sys.inputs.at("contact", default: "")
#let profile_summary = sys.inputs.at("profile_summary", default: "")

// Primary Heavy-Hitter Role Variables
#let job1_title = sys.inputs.at("job1_title", default: "")
#let job1_company = sys.inputs.at("job1_company", default: "")
#let job1_dates = sys.inputs.at("job1_dates", default: "")
#let job1_context = sys.inputs.at("job1_context", default: "")
// Fix: Pass the raw text string directly into the global json parsing routine
#let job1_bullets = json(bytes(sys.inputs.at("job1_bullets", default: "[]")))

// Previous Role Variables
#let job2_title = sys.inputs.at("job2_title", default: "")
#let job2_company = sys.inputs.at("job2_company", default: "")
#let job2_dates = sys.inputs.at("job2_dates", default: "")
#let job2_context = sys.inputs.at("job2_context", default: "")
// Fix: Pass the raw text string directly into the global json parsing routine
#let job2_bullets = json(bytes(sys.inputs.at("job2_bullets", default: "[]")))

// Static Section Blocks
#let collapsed_history = sys.inputs.at("collapsed_history", default: "")
#let education_block = sys.inputs.at("education_block", default: "")

// 2. DESIGN & LAYOUT SYSTEM CONFIGURATION
#let primary-color = rgb("#1a3a5f") // Deep slate corporate navy accent
#let text-color = rgb("#2d2d2d")    // Premium off-black for body copy readability
#let muted-color = rgb("#5a5a5a")   // Neutral gray for dates and metadata

#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm)
)
#set text(font: "Liberation Serif", size: 10pt, fill: text-color, lang: "en", region: "au")
#set par(justify: true, leading: 0.65em)

// 3. DOCUMENT HEADER BLOCK
#align(center)[
  #text(weight: "bold", size: 22pt, fill: primary-color)[#name] \
  #v(2pt)
  #text(size: 9pt, fill: muted-color)[#contact]
]

#v(4pt)
#line(length: 100%, stroke: 0.75pt + primary-color)
#v(8pt)

// 4. PROFESSIONAL SUMMARY SECTION
#text(weight: "bold", size: 11pt, fill: primary-color)[PROFESSIONAL SUMMARY]
#v(2pt)
#profile_summary

#v(10pt)

// 5. CORE COMPETENCIES MATRIX (Native Typst Grid Table)
#text(weight: "bold", size: 11pt, fill: primary-color)[CORE COMPETENCIES]
#v(4pt)
#table(
  columns: (1fr, 1fr, 1fr),
  fill: (x, y) => if y == 0 { primary-color.lighten(92%) } else { none },
  stroke: 0.5pt + gray.lighten(40%),
  align: left + horizon,
  inset: 7pt,
  [*Strategic Leadership*], [*Technical Execution*], [*Product & Innovation*],
  [First-Principles Thinking], [Systems & Architecture], [Product-Driven Engineering],
  [Team Scaling & Mentorship], [Iterative Development], [User Experience (UX) Focus],
  [High-Performance Culture], [Technical Roadmapping], [Cross-Functional Alignment]
)

#v(10pt)

// 6. PROFESSIONAL EXPERIENCE SECTION
#text(weight: "bold", size: 11pt, fill: primary-color)[PROFESSIONAL EXPERIENCE]
#v(6pt)

// --- CURRENT COMPANY ---
#grid(
  columns: (1fr, auto),
  [*#job1_company*],
  [#text(fill: muted-color, weight: "bold")[#job1_dates]]
)
#v(-2pt)
#text(weight: "medium", fill: primary-color)[#job1_title] \
#v(2pt)
#text(style: "italic", fill: muted-color)[#job1_context]

#v(2pt)
#for bullet in job1_bullets [
  - #eval(bullet, mode: "markup")
]

#v(12pt)

// --- PREVIOUS COMPANY ---
#grid(
  columns: (1fr, auto),
  [*#job2_company*],
  [#text(fill: muted-color, weight: "bold")[#job2_dates]]
)
#v(-2pt)
#text(weight: "medium", fill: primary-color)[#job2_title] \
#v(2pt)
#text(style: "italic", fill: muted-color)[#job2_context]

#v(2pt)
#for bullet in job2_bullets [
  - #eval(bullet, mode: "markup")
]

#v(14pt)

// 7. HISTORICAL & TIME-HORIZON SECTIONS
#text(weight: "bold", size: 11pt, fill: primary-color)[EARLY CAREER HISTORY]
#v(4pt)
#eval(collapsed_history, mode: "markup")

#v(14pt)

#text(weight: "bold", size: 11pt, fill: primary-color)[EDUCATION & CREDENTIALS]
#v(4pt)
#eval(education_block, mode: "markup")