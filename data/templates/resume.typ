// data/templates/resume.typ
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "Liberation Sans", size: 10pt)

#let name = sys.inputs.name
#let contact_line = sys.inputs.contact

= #name
#text(size: 9pt, fill: gray)[#contact_line]
#line(length: 100%, stroke: 0.5pt)

== Executive Summary
#sys.inputs.summary

== Professional Experience
#sys.inputs.history