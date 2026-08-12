#let resume-data = json("resume_data.json")
#let letter-data = json("letter_data.json")

// Design Token Layout Definitions
#let brand-orange = rgb("#c2410c")
#let text-primary = rgb("#0f172a")
#let text-muted = rgb("#334155")
#let bg-box = rgb("#f8fafc")
#let border-grey = rgb("#cbd5e1")

//#set page(
//  paper: "a4",
//  margin: (x: 2cm, y: 2.5cm),
//  footer: align(center)[
//    #text(size: 8.5pt, fill: text-muted)[
//      #resume-data.contact.phone  |  #resume-data.contact.email  |  #resume-data.contact.linkedin
//    ]
//  ]
//)

#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.5cm)
)

// Font stack array automatically falls back safely if a font is missing
#set text(
  font: ("Liberation Sans", "Arial", "Helvetica", "sans-serif"), 
  size: 10pt, 
  fill: text-primary
)

#set par(justify: true, leading: 0.65em)

// Styled Section Heading Definition
#show heading.where(level: 2): it => block(
  width: 100%,
  stroke: (bottom: 0.5pt + border-grey),
  inset: (bottom: 8pt),
  above: 2em,
  below: 1em,
)[
  #grid(
    columns: (auto, 1fr),
    gutter: 8pt,
    box(width: 4pt, height: 1.1em, fill: brand-orange, radius: 2pt),
    text(size: 12pt, weight: "bold", fill: text-primary)[#it.body]
  )
]

// --- HEADER BLOCK ---
#block(width: 100%, inset: (bottom: 15pt), stroke: (bottom: 2pt + text-primary))[
  #text(size: 24pt, weight: "extrabold", tracking: -0.03em)[#resume-data.name] \
  #v(2pt)
  #text(size: 10pt, weight: "medium", fill: text-muted)[#resume-data.post_nominals] \
  #v(4pt)
  #text(size: 11pt, weight: "bold", fill: brand-orange)[#resume-data.title] \
  #v(6pt)
  #text(size: 8.5pt, fill: text-muted)[
    #resume-data.contact.location  |  #resume-data.contact.phone  |  #resume-data.contact.email  |  #resume-data.contact.linkedin
  ]
]

#v(10pt)

// --- ABOUT/THESIS BOX ---
#rect(
  fill: bg-box,
  stroke: (left: 4pt + brand-orange),
  radius: (right: 4pt),
  inset: 12pt,
  width: 100%
)[
  #set par(leading: 0.7em)
  #text(style: "italic", size: 9.5pt)[#resume-data.about]
]

// --- CORE CAPABILITIES ---
== Core Capabilities

#for cap in resume-data.capabilities [
  #block(below: 12pt)[
    *#cap.title:* #text(fill: text-muted)[#cap.description]
  ]
]

// --- PROFESSIONAL EXPERIENCE ---
== Professional Experience

#for exp in resume-data.experience [
  #block(width: 100%, breakable: false, below: 18pt)[
    #grid(
      columns: (1fr, auto),
      text(weight: "bold", size: 11pt)[#exp.company],
      text(weight: "semibold", size: 9pt, fill: text-muted)[#exp.period]
    )
    #v(-2pt)
    #text(weight: "semibold", fill: text-muted, size: 9.5pt)[#exp.role]
    #v(4pt)
    #text(size: 9.5pt)[#exp.summary]
    
    #if "highlights" in exp [
      #v(4pt)
      #set list(marker: text(fill: brand-orange)[•])
      #for highlight in exp.highlights [
        - #text(fill: text-muted, size: 9.5pt)[#highlight]
      ]
    ]
  ]
]

// --- EDUCATION & ACCREDITATIONS ---
== Education & Accreditations

#for edu in resume-data.education [
  #block(width: 100%, breakable: false, below: 14pt)[
    #grid(
      columns: (1fr, auto),
      text(weight: "bold", size: 10.5pt)[#edu.institution],
      if edu.period != "" [ #text(weight: "semibold", size: 9pt, fill: text-muted)[#edu.period] ]
    )
    #v(-2pt)
    #if edu.role != "" [
      #text(weight: "semibold", fill: text-muted, size: 9.5pt)[#edu.role]
      #v(2pt)
    ]
    
    #if "summary" in edu [
      #text(fill: text-muted, size: 9.5pt)[#edu.summary]
    ]
    #if "highlights" in edu [
      #v(4pt)
      #set list(marker: text(fill: brand-orange)[•])
      #for highlight in edu.highlights [
        - #text(fill: text-muted, size: 9.5pt)[#highlight]
      ]
    ]
  ]
]

// --- TECHNICAL SKILLS APPENDIX ---
== Technical Toolkit & Systems Infrastructure

#for skill in resume-data.technical_skills [
  #block(below: 12pt)[
    *#skill.title:* #text(fill: text-muted)[#skill.description]
  ]
]