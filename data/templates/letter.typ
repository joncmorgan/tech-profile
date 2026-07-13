// ==============================================================================
// TEMPLATE: data/templates/letter.typ
// VERSION:  2.4.1
// STATUS:   Styled Executive Cover Letter Blueprint (A4 Standard)
// ==============================================================================

#let name = sys.inputs.at("name", default: "Candidate")
#let sender_address = sys.inputs.at("sender_address", default: "")
#let sender_contact = sys.inputs.at("sender_contact", default: "")
#let date = sys.inputs.at("date", default: "")

#let company_name = sys.inputs.at("company_name", default: "Target Organization")
#let hiring_manager = sys.inputs.at("hiring_manager", default: "Hiring Committee")
#let department = sys.inputs.at("department", default: "")
#let body_text = sys.inputs.at("body_text", default: "")

// Corporate Palette Definition
#let primary-color = rgb("#1a3a5f") // Deep slate blue/navy accent
#let text-color = rgb("#2d2d2d")    // Soft off-black for premium readability
#let muted-color = rgb("#5a5a5a")   // Clean neutral gray for secondary details

// Global Formatting Rules (Configured to A4 Metric Scales)
#set page(
  paper: "a4", 
  margin: (top: 2.5cm, bottom: 2.5cm, left: 3cm, right: 3cm)
)
#set text(font: "Liberation Serif", size: 10.5pt, fill: text-color, lang: "en", region: "au")
#set par(justify: true, leading: 0.75em) // Slightly opened leading for breathing room

// 1. Elegant Geometric Header Block
#grid(
  columns: (1fr, auto),
  gutter: 10pt,
  align(left + bottom)[
    #text(weight: "bold", size: 20pt, fill: primary-color)[#name]
  ],
  align(right + bottom)[
    #text(size: 9pt, fill: muted-color)[
      #sender_address \
      #sender_contact
    ]
  ]
)

// Structural Accent Rule
#v(-4pt)
#line(length: 100%, stroke: 0.75pt + primary-color.lighten(30%))
#v(20pt)

// 2. Formal Dateline & Addressed Target
#text(fill: muted-color)[#date]
#v(14pt)

#text(size: 11pt)[
  To, \
  #hiring_manager \
  #if department != "" [
    #department \
  ]
  *#text(fill: primary-color)[#company_name]*
]

#v(24pt)

// 3. Dynamic Letter Prose Hydration Block
#eval(body_text, mode: "markup")