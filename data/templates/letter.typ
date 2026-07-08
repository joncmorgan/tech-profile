// data/templates/letter.typ
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
#set text(font: "Liberation Sans", size: 11pt)

= #sys.inputs.name
#text(size: 9pt, fill: gray)[#sys.inputs.contact]
#v(10pt)
#align(right)[#sys.inputs.date]

To the Hiring Team,

#v(10pt)
#sys.inputs.body

#v(20pt)
Sincerely,

#sys.inputs.name