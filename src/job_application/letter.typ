#let resume-data = json("resume_data.json")
#let letter-data = json("letter_data.json")

// Unified Design Token Hierarchy
#let brand-orange = rgb("#c2410c")
#let text-primary = rgb("#0f172a")
#let text-muted = rgb("#334155")

#set page(
  paper: "a4",
  margin: (x: 2cm, top: 2.0cm, bottom: 1.2cm),
  footer: [
    #set text(size: 8pt, fill: text-muted)
    #v(-4pt)
  ]
)

#set text(
  font: ("Liberation Sans", "Arial", "Helvetica", "sans-serif"), 
  size: 10.5pt, 
  fill: text-primary
)

#set par(justify: true, leading: 0.65em)

// --- HEADER BLOCK (Optimised Compact Layout) ---
#block(width: 100%, inset: (bottom: 10pt), stroke: (bottom: 1.5pt + text-primary))[
  #grid(
    columns: (1fr, auto),
    align: (left + bottom, right + bottom),
    [
      #text(size: 22pt, weight: "extrabold", tracking: -0.03em)[#resume-data.name] \
      #v(-2pt)
      #text(size: 9.5pt, weight: "medium", fill: text-muted)[#resume-data.post_nominals] \
      #v(2pt)
      #text(size: 10.5pt, weight: "bold", fill: brand-orange)[#resume-data.title]
    ],
    [
      #set text(size: 8.5pt, fill: text-muted)
      #resume-data.contact.location \
      #resume-data.contact.phone \
      #resume-data.contact.email \
      #resume-data.contact.linkedin
    ]
  )
]

#v(8pt)

// --- METADATA & DYNAMIC DATE ---
#align(left)[
  #text(fill: text-muted, size: 9.5pt)[
    #datetime.today().display("[day] [month repr:long] [year]")
  ]
]

#v(8pt)

// --- RECIPIENT ---
#text(weight: "bold")[#letter-data.recipient]

#v(8pt)

// --- LETTER BODY ---
#for para in letter-data.paragraphs [
  #eval(para, mode: "markup")
  #v(6pt)
]

// Safely handle missing closing property
#let closing-text = letter-data.at("closing", default: none)
#if closing-text != none [
  #v(2pt)
  #closing-text
]
#v(8pt)

Sincerely,

#v(4pt)
#image("sig-jon.png", width: 3.5cm)
#v(4pt)

*#resume-data.name*