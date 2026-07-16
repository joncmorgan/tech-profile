#let resume-data = json("resume_data.json")
#let letter-data = json("letter_data.json")

// Unified Design Token Hierarchy
#let brand-orange = rgb("#c2410c")
#let text-primary = rgb("#0f172a")
#let text-muted = rgb("#334155")

#set page(
  paper: "a4",
  margin: (x: 2cm, top: 2.5cm, bottom: 2.5cm)
)

#set text(
  font: ("Liberation Sans", "Arial", "Helvetica", "sans-serif"), 
  size: 10.5pt, 
  fill: text-primary
)

#set par(justify: true, leading: 0.75em)

// --- HEADER BLOCK (Identical Branded Layout) ---
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

#v(20pt)

// --- METADATA & DYNAMIC DATE ---
#align(left)[
  #text(fill: text-muted, size: 9.5pt)[
    #resume-data.contact.location \
    #datetime.today().display("[day] [month repr:long] [year]")
  ]
]

#v(20pt)

// --- RECIPIENT ---
#text(weight: "bold")[#letter-data.recipient]

#v(12pt)

// --- LETTER BODY ---
#for para in letter-data.paragraphs [
  #para
  #v(12pt)
]

#v(6pt)
#letter-data.closing

#v(30pt)

Sincerely,

#v(8pt)
#image("sig-jon.png", width: 3.5cm)
#v(8pt)

*#resume-data.name*