// Resume template. Data comes from a YAML file passed as --input data=<path>.
#let data = yaml(sys.inputs.at("data", default: "resume.yml"))
#let accent = rgb("#1f4e8c")
#let muted = rgb("#555555")

#set document(title: data.header.name + " — Resume", author: data.header.name)
#set page(paper: "us-letter", margin: (x: 0.6in, top: 0.5in, bottom: 0.5in))
#set text(font: "Liberation Sans", size: 10pt, fill: rgb("#1a1a1a"))
#set par(leading: 0.58em, justify: false)
#set list(indent: 0.6em, body-indent: 0.45em, spacing: 0.7em, marker: [•])
#show link: set text(fill: accent)

#let section(name) = {
  v(0.9em)
  text(size: 10.5pt, weight: "bold", fill: accent, tracking: 0.08em, upper(name))
  v(-0.6em)
  line(length: 100%, stroke: 0.8pt + accent)
  v(0.25em)
}

// Header
#text(size: 19pt, weight: "bold", tracking: 0.06em, upper(data.header.name)) \
#v(-0.35em)
#text(size: 11pt, fill: accent, data.header.title) \
#v(-0.3em)
#{
  let parts = (link("mailto:" + data.header.email, data.header.email), text(fill: muted, data.header.location))
  for l in data.header.links { parts.push(link(l.url, l.label)) }
  text(size: 8.5pt, parts.join(text(fill: muted, "   |   ")))
}

#section("Professional Summary")
#data.summary

#section("Experience")
#for job in data.experience [
  #block(breakable: true, above: 0.9em)[
    #grid(columns: (1fr, auto),
      [*#job.title* #text(fill: muted)[ | ] #text(fill: accent, job.company)],
      text(size: 9pt, fill: muted, job.dates))
    #if "intro" in job [ #v(-0.35em) #text(style: "italic", fill: muted, size: 9pt, job.intro) ]
    #v(-0.2em)
    #for b in job.bullets [
      - *#b.label:* #b.text
    ]
    #if "tech" in job [ #v(-0.1em) #text(size: 8pt, style: "italic", fill: muted, job.tech.join(" · ")) ]
  ]
]

#if "earlier" in data and data.earlier.len() > 0 [
  #section("Earlier Experience")
  #for e in data.earlier [
    #block(above: 0.55em)[*#e.title* #text(fill: muted)[ | ] #text(fill: accent, e.company) #text(fill: muted)[ (#e.years)] — #e.text]
  ]
]

#section("Technical Skills")
#for s in data.skills [
  #block(above: 0.62em)[*#s.category:* #s.items]
]

#if "certifications" in data and data.certifications.len() > 0 [
  #section("Certifications")
  #for c in data.certifications [
    - #c.name #text(fill: muted, style: "italic")[ — #c.dates]
  ]
]
