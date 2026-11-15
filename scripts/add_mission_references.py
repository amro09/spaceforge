"""Append a single editable references page without rebuilding the existing report."""
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path("generated-artifacts/mission-forge")
doc = Document(ROOT / "Mission-Forge-Complete-Guide.docx")
doc.add_page_break()
doc.add_heading("24. References and further reading", 1)

def paragraph(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1
    for run in p.runs:
        run.font.size = Pt(10)
    return p

def heading(text):
    p = doc.add_heading(text, 2)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(5)
    for run in p.runs:
        run.font.size = Pt(13)

def reference(number, title, detail, url=None):
    p = paragraph(f"[{number}] ")
    if url:
        link = OxmlElement("w:hyperlink")
        link.set(qn("r:id"), p.part.relate_to(url, RT.HYPERLINK, is_external=True))
        run = OxmlElement("w:r")
        props = OxmlElement("w:rPr")
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "124E61")
        props.append(color)
        size = OxmlElement("w:sz")
        size.set(qn("w:val"), "20")
        props.append(size)
        underline = OxmlElement("w:u")
        underline.set(qn("w:val"), "single")
        props.append(underline)
        run.append(props)
        text = OxmlElement("w:t")
        text.text = title
        run.append(text)
        link.append(run)
        p._p.append(link)
    else:
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(10)
    r = p.add_run(" — " + detail)
    r.font.size = Pt(10)

paragraph("This page separates the project's actual inputs from extra background sources added for this report. Linked titles open the public sources. Local materials were supplied by the project owner.")
heading("A. Sources and software used in the solution")
reference(1, "Supplied challenge and event screenshots.",
          "Space Mission Design Game; Judging Criteria; What Does Your Team Need to Submit? The source of the challenge, judging, and submission requirements.")
reference(2, "Supplied Mission Forge concept and revised game brief.",
          "The two uploaded text documents describing the game and requested changes. These define the project requirements; they are not published research.")
reference(3, "Mission Forge game source and captured app screens.",
          "artifacts/mission-forge/public/mission-forge.html. Primary source for this report's levels, parts, events, scores, rewards, and limitations. All report images are original app captures.")
reference(4, "Three.js r128 (0.128.0), distributed by cdnjs.",
          "The 3D rendering library loaded by the game.",
          "https://cdnjs.cloudflare.com/ajax/libs/three.js/0.128.0/three.min.js")

heading("B. Additional science and history references")
reference(5, "NASA Earth Observatory. Catalog of Earth Satellite Orbits.",
          "Background for LEO, GEO, orbit height, and observation trade-offs; report sections 5 and 21.",
          "https://science.nasa.gov/earth/earth-observatory/catalog-of-earth-satellite-orbits")
reference(6, "NASA. Basics of Space Flight, Chapter 11: Onboard Systems.",
          "Spacecraft support systems, power, and communication; sections 6–8 and 21.",
          "https://science.nasa.gov/learn/basics-of-space-flight/chapter11-1")
reference(7, "NASA. Basics of Space Flight, Chapter 5: Planetary Orbits.",
          "Orbital transfers and paths; sections 5 and 17.",
          "https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1")
reference(8, "NASA. Evaluating the Advanced Crew Escape Suit.",
          "Launch/entry suit background for the Level 1 reward; sections 14 and 19.",
          "https://www.nasa.gov/image-article/evaluating-advanced-crew-escape-suit")
reference(9, "NASA. 50 Years Ago: Certifying Apollo Spacesuits.",
          "Apollo suit protection and mobility; sections 15 and 19.",
          "https://www.nasa.gov/history/50-years-ago-certifying-apollo-spacesuits")
reference(10, "NASA NSSDCA. The Apollo Lunar Roving Vehicle.",
          "Lunar rover use during Apollo 15–17; sections 18 and 19.",
          "https://nssdc.gsfc.nasa.gov/planetary/lunar/apollo_lrv.html")
reference(11, "NASA. Mars Science Laboratory: Curiosity Rover.",
          "Mars rover science and exploration; sections 17 and 19.",
          "https://science.nasa.gov/mission/msl-curiosity")
reference(12, "NASA. Extravehicular Activity and Human Surface Mobility Program.",
          "Additional background on spacewalking suits and surface mobility; section 19.",
          "https://www.nasa.gov/suits-and-rovers")
reference(13, "Three.js documentation.",
          "Further technical reading. Current documentation may differ from the game's older r128 API.",
          "https://threejs.org/docs/index.html")
paragraph("Source note: the additional links are background reading, not a claim that each was consulted during the original build. Game costs, mass multipliers, event effects, risk indices, and scoring are original teaching rules—not NASA measurements or validated flight models. No NASA images or 3D assets were used for this report's screenshots.")

out = ROOT / "Mission-Forge-Complete-Guide-With-References.docx"
doc.save(out)
print(out)
