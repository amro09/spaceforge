"""Build an editable Word guide using reviewed game data and real screenshots."""
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT = Path("generated-artifacts/mission-forge")
DATA = json.loads((ROOT / "game-data.json").read_text())
TEXT = DATA["I18N"]
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
sec.top_margin = sec.bottom_margin = Inches(.65)
sec.left_margin = sec.right_margin = Inches(.75)
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(7)
style.paragraph_format.line_spacing = 1.08
for name in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
    doc.styles[name].font.name = "Calibri"
    doc.styles[name].font.color.rgb = RGBColor.from_string("124E61")
doc.styles["Title"].font.size = Pt(40)
doc.styles["Heading 1"].font.size = Pt(24)
doc.styles["Heading 2"].font.size = Pt(16)
doc.styles["Caption"].font.size = Pt(9)
doc.styles["Caption"].font.color.rgb = RGBColor.from_string("536274")
header = sec.header.paragraphs[0]
header.text = "MISSION FORGE   |   PLAYER & PROJECT GUIDE"
header.runs[0].font.size = Pt(9)
header.runs[0].font.color.rgb = RGBColor.from_string("536274")
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run("Mission Forge  •  ")
field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer._p.append(field)
figure = 0

def p(text, style=None):
    return doc.add_paragraph(text, style)

def title(text):
    doc.add_page_break()
    doc.add_heading(text, 1)

def sub(text):
    doc.add_heading(text, 2)

def bullets(items):
    for item in items:
        p(item, "List Bullet")

def image(name, caption, width=6.65, max_height=3.7):
    global figure
    path = ROOT / "screenshots" / (name + ".jpg")
    if not path.exists():
        raise FileNotFoundError(path)
    with Image.open(path) as img:
        w, h = img.size
    width = min(width, max_height * w / h)
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.keep_with_next = True
    par.add_run().add_picture(str(path), width=Inches(width))
    figure += 1
    caption_p = p(f"Figure {figure}. {caption}", "Caption")
    caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Shading Accent 1"
    for i, head in enumerate(headers):
        t.rows[0].cells[i].text = head
    repeat = OxmlElement("w:tblHeader")
    t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
    for row in t.rows:
        prevent = OxmlElement("w:cantSplit")
        row._tr.get_or_add_trPr().append(prevent)
        for cell in row.cells:
            for par in cell.paragraphs:
                par.paragraph_format.space_after = Pt(4)
                for run in par.runs:
                    run.font.size = Pt(10)
    p("")

doc.add_heading("Mission Forge", 0)
p("The complete game guide", "Subtitle")
p("Design a spacecraft. Launch it. Learn from every decision.", "Subtitle")
image("01-menu", "The real English main menu of Mission Forge.", max_height=4.3)
p("An editable report in simple English")
p("This guide covers the current reviewed game: two playable Earth levels and three planned levels. It explains the problem, the solution, every main screen, design choices, mission events, scoring, rewards, controls, and limits.")
p("All images are actual app screenshots. Planned levels are shown as their current cards, not as invented gameplay.")
p("Learning model only: the part names, prices, risk values, and mission rules are simplified. Mission Forge is not affiliated with NASA or any space agency.")

title("Contents")
sections = [
"1. The problem and our solution", "2. Getting started and controls",
"3. The level map", "4. The guided tutorial", "5. Mission goals and orbit choices",
"6. Science instruments", "7. Rockets, power, and communication",
"8. The six design gauges", "9. A complete example design",
"10. Launch and the live mission", "11. Events and decision feedback",
"12. All seven event types", "13. Results, scores, and replay",
"14. Level 1: First Light", "15. Level 2: Tight Margins",
"16. Planned Level 3: Lunar Survey", "17. Planned Level 4: Red Horizon",
"18. Planned Level 5: Moon on a Shoestring", "19. Rewards and the collection",
"20. Language, mobile use, and saved progress", "21. How the learning model works",
"22. Technical overview and limitations", "23. Learning activities and glossary"
]
for item in sections:
    p(item)
p("Editing this report: open it in Microsoft Word, Google Docs, or LibreOffice Writer. The headings, paragraphs, tables, and captions are editable. Screenshots are embedded pictures and can be replaced or resized. The Word navigation pane can be used to move between headings.")

title(sections[0])
sub("The problem")
p("A space mission is not only a rocket launch. A team must choose a useful science goal, the right tools, enough power, a way to send data home, and an orbit that fits the goal. The team also has limits on money and weight.")
p("These choices affect each other. A large instrument can collect more information, but it may need more electricity and a stronger rocket. A cheap antenna may save money, but less data may reach Earth. Students may learn the words without getting a safe chance to test these trade-offs.")
sub("Our solution")
p("Mission Forge turns these connected choices into a short game. The player designs a spacecraft, checks the limits, launches it, responds to problems, and reads a result that explains what happened. The player can try again with a different design.")
bullets(["Before launch: choose parts and balance money, mass, power, communication, science, and risk.",
         "After launch: respond to events. Every response has a benefit and a cost.",
         "After the mission: read the score, learn from the tips, and improve the next design.",
         "After full success: open an educational reward card about a suit or rover."])
sub("What makes this useful")
p("The game makes engineering decisions visible. It connects the science goal to the tools and orbit, and it separates collecting data from returning data. The intended benefit is better understanding through practice; this build does not include a study proving learning gains.")

title(sections[1])
image("01-menu", "Start mission planning, open the collection, or read How to play.")
table(["Action", "What to do"], [
("Start","Choose Start mission planning, then Plan mission on Level 1."),
("Choose parts","Click or tap a part card. Click a selected instrument again to remove it."),
("Read help","Hover over a choice or use its help control. Tap the ? next to a gauge."),
("Move the 3D view","Drag to rotate. Scroll or pinch to zoom. The design screen also has camera buttons."),
("Answer an event","Click or tap one of three choices, or press 1, 2, or 3."),
("Keyboard use","Use Tab to move between buttons and Enter to activate one. Dialog focus stays inside the popup."),
("Close a card","Use Close. Escape can close help/reward cards or cancel the abort prompt."),
("Navigation","Use the top Levels and Collection links. The game title returns to the menu.")
])
p("The game does not require an account. Use a modern browser. A working WebGL graphics engine is needed for the 3D scenes. If graphics cannot load, the app shows an explicit text fallback and the mission choices remain playable.")

title(sections[2])
image("02-levels", "The level map shows Ready, Locked, and Coming soon states.")
table(["Level", "Destination", "Budget", "Current status"], [
("1 · First Light","Earth","$260M","Playable from the start"),
("2 · Tight Margins","Earth","$195M","Playable after partial or full success in Level 1"),
("3 · Lunar Survey","Moon","$340M","Planned; not playable"),
("4 · Red Horizon","Mars","$470M","Planned; not playable"),
("5 · Moon on a Shoestring","Moon","$280M","Planned; not playable")
])
p("Ready means a level can be opened. Locked means an earlier level must be completed. Coming soon means the level has data and a card, but its gameplay is disabled. Completing Level 2 does not make Level 3 playable in this build.")

title(sections[3])
image("03-tutorial", "Level 1 includes a guided tutorial over the real design screen.")
p("The tutorial has eight steps. It points to the part of the screen that needs attention. Most steps move forward when the player makes the required choice.")
bullets(["1. Choose a science goal.", "2. Add at least one science instrument.",
         "3. Choose a rocket.", "4. Choose a power source.",
         "5. Choose communication equipment.", "6. Choose an orbit.",
         "7. Read the six gauges and acknowledge the explanation.",
         "8. Launch after all blocking problems are fixed."])
p("Skip tutorial removes the guide without changing the mission rules. Tutorial can reopen it. Reset design clears the current part selections. A good first learning activity is to watch how one instrument changes cost, mass, and power at the same time.")

title(sections[4])
sub("Choose a question before choosing parts")
table(["Earth goal", "Matching instruments", "Best-fit orbit"], [
("Weather watch","Camera + Thermal imager","GEO"),
("Polar ice mapping","Radar + Spectrometer","LEO"),
("Magnetic shield study","Magnetometer","LEO or GEO"),
("Air quality","Spectrometer + Camera","LEO")
])
p("FIT marks instruments that match the chosen question. GOOD FIT marks a suitable orbit. A mismatch may still allow launch, but it reduces science and increases risk. More instruments are not always better.")
sub("The orbit choices")
table(["Orbit", "Simple meaning", "Added cost", "Mass multiplier"], [
("LEO","Close to Earth; the ground moves below the spacecraft.","$0M","×1.0"),
("GEO","Keeps watching one region. More fuel is needed.","$14M","×1.6"),
("Lunar orbit — planned","Orbits the Moon.","$30M","×2.2"),
("Mars transfer — planned","A simplified Hohmann transfer to Mars.","$55M","×3.0")
])
p("The mass multiplier is a teaching shortcut for the extra effort of reaching a more distant orbit. It is not a real fuel calculation. The game does not simulate months of travel or a real navigation solution.")
sub("Goals prepared for future levels")
p("Moon: crater mapping, lunar water ice, and lunar soil. Mars: signs of past life, climate, geology, and underground water. These choices exist in the data, but their levels cannot be played yet.")

title(sections[5])
p("Instruments are the tools that answer the science question. Choose up to four in Level 1 and three in Level 2. All values below are game values, not equipment quotes or flight specifications.")
rows=[]
for key, part in DATA["PARTS"]["instruments"].items():
    rows.append([TEXT["inst."+key],f'${part["cost"]}M',part["mass"],part["power"],part["science"]])
table(["Instrument","Cost","Mass kg","Power W","Science base"], rows)
for key in DATA["PARTS"]["instruments"]:
    sub(TEXT["inst."+key])
    p(TEXT["inst."+key+".d"])
p("Science base is a starting number used by the game. A matching instrument gets a ×1.4 factor. A nonmatching instrument gets ×0.7. A poor orbit match applies another ×0.7 factor to the total. The result is compared with the level's science target and shown as a 0–100 index.")
sub("The fixed spacecraft base")
p("Every design includes a spacecraft bus: the frame, computer, and basic support systems. It always costs $30M, weighs 350 kg, and needs 60 W. This is added even before instruments are selected.")

title(sections[6])
sub("Rockets")
table(["Rocket","Cost","Level 1 capacity","Level 2 capacity","Reliability index"], [
(TEXT["rocket."+k],f'${v["cost"]}M',f'{v["payload"]} kg',f'{v["payload"]*.85:g} kg',f'{v["reliability"]*100:g}%')
for k,v in DATA["PARTS"]["rockets"].items()])
p("A larger rocket can carry more, but costs more. Reliability affects the starting risk score and the chance of a trajectory event. It is not a separately tested real-world probability of a successful launch.")
sub("Power sources")
table(["Source","Cost","Mass","Output","Added risk"], [
(TEXT["power."+k],f'${v["cost"]}M',f'{v["mass"]} kg',f'{v["output"]} W',v["risk"])
for k,v in DATA["PARTS"]["power"].items()])
p("Solar panels give strong output at a low price. A battery is cheap but has limited output and slower recovery. An RTG gives steady output but adds cost, mass, and a handling-risk value. The live mission uses a simplified recharge rule, not a real electrical system.")
sub("Communication")
table(["System","Cost","Mass","Power","Base link value"], [
(TEXT["comms."+k],f'${v["cost"]}M',f'{v["mass"]} kg',f'{v["power"]} W',v["rate"])
for k,v in DATA["PARTS"]["comms"].items()])
p("The final link quality also depends on orbit. A relay works well in LEO, but is penalized farther away. A high-gain antenna uses more power than a small antenna, but returns data more quickly.")

title(sections[7])
image("05-validation", "This real design is too heavy for the selected light rocket, so launch is blocked.")
table(["Gauge","What it means","Does it block launch?"], [
("Budget","Total selected cost compared with the level cap.","Yes, if over the cap."),
("Mass","Spacecraft mass × orbit factor compared with rocket capacity.","Yes, if too heavy."),
("Power","Required power, including the level reserve, compared with supply.","Yes, if supply is too low."),
("Communication","How effectively the link can return data.","No; weak links create an advisory."),
("Science value","How well instruments and orbit fit the science goal.","No; low science can hurt results."),
("Risk","A danger index from the selected design.","No; high risk creates an advisory.")
])
p("Missing choices also block launch. Pick a goal, at least one instrument, a rocket, a power source, a communication system, and an orbit. The mission type is fixed by the level.")
p("Red blocking items must be fixed. Advisory messages are warnings, not permission to ignore the problem. A mission can launch with weak communication and still return a poor score.")

title(sections[8])
image("04-design-level1", "A complete Level 1 weather mission design with its resource gauges.")
table(["Choice","Example selection"],[
("Goal","Weather watch"),("Instruments","Camera and Thermal imager"),
("Rocket","Condor-M"),("Power","Solar panels"),("Communication","High-gain antenna"),("Orbit","GEO")])
p("Total cost: $177M. Dry mass: 655 kg. Effective mass after the GEO multiplier: 1,048 kg. Power needed: 155 W. Solar output: 300 W. Communication: 70/100.")
p("In Level 1, this fits the $260M budget and 1,400 kg rocket limit. The design science value is 98/100 and starting risk is 28/100. The same parts also fit Level 2, but its reduced capacity and harder science target change the indices: science 84 and risk 33.")
p("This is a useful starting design, not a guaranteed winning answer. Events vary, and later decisions still change the final result.")

title(sections[9])
image("06-launch", "The actual 3D launch sequence.")
p("Launch mission starts a short sequence: countdown, ignition, liftoff, climb, stage separation, and orbit entry. It lasts about 7.6 seconds. Skip cinematic moves straight to the mission.")
sub("The live mission")
image("07-mission", "The mission screen shows the spacecraft, timeline, live resources, and mission log.", max_height=2.8)
p("Level 1 has four 7-second segments. Level 2 has five. Active mission time is about 28 or 35 seconds, but reading and answering events takes extra time because popups pause the clock.")
p("The live panel tracks power, communication, instrument health, risk, data collected, and data returned. The timeline shows progress. The log records events and choices. This is a decision game, not a manual rocket-flight game.")

title(sections[10])
image("08-event", "An actual event offers three responses while the mission clock is paused.")
p("An event appears partway through each segment. Event types are selected randomly with weights based on the design. For example, batteries make power trouble more likely. Events do not repeat within the available unused pool.")
p("Each option changes one or more live values. There is rarely an answer that improves everything. Choose by looking at the current mission, not only by memorizing an option number.")
image("09-consequence", "After a choice, the explanation shows what changed and why.", max_height=2.8)
p("Read the explanation, then choose Continue. Negative effects are 1.35 times stronger in Level 2. Positive effects keep their normal size. Values such as power and risk are limited to 0–100.")

title(sections[11])
p("The next pages list every event and all three responses. The changes are the base Level 1 values. Power, communication, instrument health, and risk changes are index points. Data changes are game data units, not bytes or real scientific measurements.")
p("In Level 2, multiply harmful changes by 1.35. A risk increase is harmful; a decrease in any other listed value is harmful. The game rounds these changes to one decimal place and keeps the final values within their allowed range.")
event_labels = {"power":"power","comms":"communication","science":"instrument health","risk":"risk","data":"collected data","returned":"returned data"}
for n, (key, event) in enumerate(DATA["EVENTS"].items()):
    if n:
        doc.add_page_break()
    sub(TEXT["ev."+key])
    p(TEXT["ev."+key+".b"])
    rows=[]
    for i, option in enumerate(event["options"], 1):
        changes = "; ".join(f"{event_labels[k]} {v:+g}" for k,v in option.items() if v)
        rows.append([str(i), TEXT[f"ev.{key}.o{i}"], changes])
    table(["Choice","Response","Base change"], rows)
    for i in range(1,4):
        p(f'{i}. {TEXT[f"ev.{key}.e{i}"]}')
    if key=="solarStorm":
        p("More likely with GEO or a small antenna.")
    elif key=="powerShortage":
        p("More likely with a battery or a small power margin.")
    elif key=="instrumentDrain":
        p("More likely with more instruments or a very small power margin.")
    elif key=="contactLoss":
        p("More likely with a small antenna or LEO.")
    elif key=="trajectory":
        p("More likely with a less reliable rocket.")
    elif key=="batteryFault":
        p("More likely with a battery; solar also adds some weight.")
    else:
        p("A useful science opportunity can appear for any design.")

title(sections[12])
image("10-results-level1", "A real result screen explains the score and offers next actions.", max_height=2.9)
table(["Score part","Maximum","Simple meaning"],[
("Science collected","35","How much data was collected compared with the level's expected amount."),
("Data returned","30","The share of collected data that safely reached Earth."),
("Energy left","15","How much power remains at the end."),
("Risk managed","20","Lower final risk earns more points.")])
table(["Outcome","Rule","Progress and reward"],[
("Full success","Normal completion with score 70 or higher.","Records success, opens the next playable level, and grants its reward."),
("Partial success","Normal completion with score 45–69.","Opens the next playable level, but no reward."),
("Failure","Normal score below 45, power reaches 0, or risk reaches 100.","No new unlock or reward. Resource failure caps score at 40."),
("Aborted","Player confirms Abort mission.","Score 0; no new unlock or reward.")])
p("Retry with this design lets you reuse your choices. Redesign returns to planning. Level select returns to the map. Earlier earned rewards are not removed by a later failed attempt. Repeating a full success does not create a duplicate reward.")
p("Learning tips point to problems such as weak communication, little spare power, high risk, or a poor goal/orbit match. The game shows up to two tips.")

title(sections[13])
image("04-design-level1", "First Light is the guided Earth mission.", max_height=2.7)
table(["Setting","Value"],[
("Budget","$260M"),("Rocket capacity","100% of the chosen rocket's base capacity"),
("Required extra power","0%"),("Instrument limit","4"),
("Science target","60"),("Mission segments","4 × 7 seconds"),
("Event penalty multiplier","1.0"),("Reward for full success","Launch & Entry Suit")])
p("Purpose: learn the design screen, read the gauges, launch, and experience mission events. The larger budget gives room to explore different choices.")
p("First attempt: choose Weather watch, pick fitting instruments, compare LEO and GEO, then review the warnings. After the mission, explain why data returned and data collected are different.")
image("11-reward-launch-suit", "Full success opens the Launch & Entry Suit learning card.", max_height=1.9)

title(sections[14])
image("13-design-level2", "Tight Margins uses the same design workflow with stricter limits.", max_height=2.7)
table(["Setting","Value"],[
("Budget","$195M"),("Rocket capacity","85% of the chosen rocket's base capacity"),
("Required extra power","10% above normal need"),("Instrument limit","3"),
("Science target","70"),("Mission segments","5 × 7 seconds"),
("Event penalty multiplier","1.35"),("Reward for full success","Apollo-style Moon Suit")])
p("Purpose: make a focused design rather than buying every strong part. A design must now leave extra electrical capacity. The same rocket can lift less, and harmful event effects are stronger.")
image("14-results-level2", "An actual Level 2 result. Outcomes depend on both design and decisions.", max_height=1.9)

for level_num, sec_idx, explanation in [
(3,15,"The planned Moon mission adds a longer route, a larger mass multiplier, and weaker communication. Its prepared goals include craters, water ice, and lunar soil."),
(4,16,"The planned Mars mission uses a simplified Hohmann transfer. Prepared goals include past-life chemistry, climate, geology, and underground water. No real travel time or landing is simulated in the current playable build."),
(5,17,"This planned return to the Moon uses a smaller budget than Lunar Survey, a lower rocket allowance, and stronger penalties. It is intended as a harder resource-planning exercise.")]:
    lv=DATA["LEVELS"][level_num-1]
    title(sections[sec_idx])
    image(f"level-{level_num}-planned", "Actual Coming soon card. This is not a gameplay screenshot.", width=3.4, max_height=4.0)
    p("Status: planned only. The level cannot be launched in this version.")
    p(explanation)
    table(["Prepared setting","Value"],[
    ("Budget",f'${lv["budget"]}M'),("Rocket allowance",f'{lv["payloadFactor"]*100:g}%'),
    ("Required power reserve",f'{lv["powerReserve"]*100:g}%'),("Instrument limit",lv["maxInstruments"]),
    ("Science target",lv["scienceTarget"]),("Segments",f'{lv["segments"]} × {lv["segSeconds"]} seconds'),
    ("Event penalty multiplier",lv["severity"]),("Planned reward",TEXT["rw."+lv["reward"]])])
    p("These are prepared data settings, not proof of implemented gameplay. They may change when the level is built.")

title(sections[18])
image("12-collection", "The collection shows earned items and locked future rewards.")
p("Full success grants a level-linked reward once. Open the card to read its history, where it was used, and its main features. A 3D model can be rotated when graphics are available. Equip or Display changes appearance only; it never changes cost, mass, power, risk, or score.")
for key in ["launchSuit","apolloSuit","marsRover","evaSuit","lunarRover"]:
    if key in ["apolloSuit","marsRover"]:
        doc.add_page_break()
    sub(TEXT["rw."+key])
    if key == "apolloSuit":
        image("15-reward-apollo", "The earned Apollo-style Moon Suit card in the real game.", max_height=2.8)
    p(("Available reward. " if DATA["REWARDS"][key]["level"]<=2 else "Planned reward only. ") + TEXT["rw."+key+".h"])
    p("Where used: " + TEXT["rw."+key+".w"])
    p("Features: " + TEXT["rw."+key+".f"].replace("|","; ") + ".")

title(sections[19])
image("16-mobile", "The English game on a narrow display. Scroll to reach content below the screen.", width=2.4, max_height=4.9)
sub("English and Arabic")
p("The language button switches the interface between English and Arabic. Arabic uses a right-to-left layout. Goals, choices, help, mission events, results, and reward cards have translated text. Switching language does not require restarting the mission.")
sub("Mobile and desktop")
p("Buttons support click or touch. Narrow layouts stack content and use scrolling. Drag and zoom controls work with the 3D view; text decisions are still used to play the mission.")
sub("Progress is temporary")
p("Progress, earned rewards, equipped items, and the current mission live only in the open page's memory. Refreshing or closing the page resets them. There is no account, cloud save, or saved resume point in this build. For a demonstration, keep the game tab open.")

title(sections[20])
sub("Before launch")
table(["Rule","Calculation in plain words"],[
("Budget","$30M base spacecraft + instruments + rocket + power + communication + orbit cost."),
("Dry mass","350 kg base spacecraft + instrument mass + power-source mass + communication mass."),
("Effective mass","Dry mass × orbit mass multiplier."),
("Capacity","Rocket base capacity × level rocket allowance."),
("Power need","60 W base spacecraft + instrument power + communication power."),
("Power check","Supply must be at least need × (1 + level reserve)."),
("Power margin","(Supply − normal need) ÷ supply."),
("Communication","Antenna base value × orbit link factor; relay also gets the orbit relay factor."),
("Science index","Sum adjusted instrument science; apply orbit-fit factor; divide by science target; multiply by 100 and limit to 100.")
])
sub("Risk is an index, not a measured probability")
p("Starting risk begins at 8. It adds (1 − rocket reliability) × 180, the power-source risk, and orbit risk. It adds 12 if mass use is above 90%, or 5 if above 75%. It adds 10 for power margin below 10%, 8 for communication below 45, 6 for a poor orbit match, and 1.5 per instrument. The total is rounded and limited to 0–100.")
sub("Orbit link factors")
table(["Orbit","Link factor","Extra relay factor","Base orbit risk"],[
("LEO","0.80","1.0","4"),("GEO","1.00","0.6","8"),
("Lunar — planned","0.70","0.8","14"),("Mars — planned","0.45","0.7","22")])

doc.add_page_break()
sub("During the mission")
p("Live power starts from the spare-power margin: 60 + margin × 60, limited to 40–95. Instrument health starts at 85. Communication and risk start from the design indices.")
p("Power recovery uses the source's recharge value plus 0.8 × positive power margin. Base recharge values are 0.55 for solar, 0.15 for a battery, and 0.60 for an RTG. Every second, power changes by recharge minus 0.75 × level severity. Risk rises by 0.12 × severity per second.")
p("Communication gradually moves back toward its design value. Collection per second is 3 × instrument health/100 × design science/100. If live power is 15 or less, collection is reduced to 35% of that rate. Data returns at 2 × communication/100 units per second, never more than has been collected.")
p("On a normal finish, a final transmission returns some remaining data: remaining data × communication/100 × 0.5. This final pass does not run after abort or resource failure.")
sub("Exact score calculation")
table(["Part","Calculation"],[
("Expected data","Segments × seconds per segment × 3 × 0.9"),
("Science points","35 × the smaller of 1 and collected data ÷ expected data"),
("Return points","30 × returned data ÷ collected data; 0 if no data was collected"),
("Power points","15 × final power ÷ 100"),
("Risk points","20 × (1 − final risk ÷ 100)"),
("Final score","Round the sum of the four parts; apply failure/abort rules described earlier.")
])
p("Budget is a launch limit, not a direct score bonus. Unspent money does not itself give points. The final score rewards useful science, returning it, remaining power, and low risk.")

title(sections[21])
sub("What the app contains")
p("The game is a browser-based single HTML document with its styles, interface text, data, and game logic included. Three.js r128 provides the 3D scenes and is loaded from cdnjs. The main web app displays this game in a full-screen frame.")
bullets(["The design interface recalculates values when choices change.",
         "The launch sequence is a visual animation, not a rocket-physics test.",
         "The mission is a timed rule-based simulation with weighted random events.",
         "Reward models use simplified shapes rather than flight-accurate engineering models.",
         "The current game does not save player progress to a server or browser storage."])
sub("Graphics and connection")
p("The 3D library needs to load, and the browser needs WebGL. If either is unavailable, the app displays a notice and text panels instead of silently failing. The screenshots in this report were captured from the app with software-rendered WebGL enabled.")
sub("What this game does not claim")
bullets(["It does not predict whether a real spacecraft will survive.",
         "It does not calculate real fuel, radiation, temperature, orbital mechanics, or launch dynamics.",
         "Part prices, capacities, reliability numbers, and risk indices are teaching values.",
         "A high score is evidence of success under the game's rules, not proof of a valid real mission.",
         "Moon and Mars cards are a roadmap, not completed levels.",
         "The game is not a NASA product and does not claim NASA approval."])
sub("Source of this guide")
p("Gameplay details were checked against the current Mission Forge HTML source and actual browser screens. Reward history is described as presented in the game's educational cards. All screenshots show this reviewed build; no future-level gameplay images have been invented.")

title(sections[22])
sub("A simple classroom activity")
bullets(["Ask each player to choose a science question and explain why it matters.",
         "Build one design and write down the six gauge values before launch.",
         "Predict the weakest system, then play the mission.",
         "Compare the prediction with the result and the learning tips.",
         "Change one design choice, replay, and explain what improved or got worse.",
         "Discuss why a good design can still face a difficult event."])
sub("Questions for the discussion")
p("Why did you choose this orbit? Which instrument could you remove? Was all collected data returned? What did a decision cost you? Why is spare power useful? Did an educational reward change the score?")
sub("Plain-English glossary")
table(["Word","Meaning"],[
("Spacecraft bus","The frame, computer, and basic support systems."),
("Instrument","A tool that measures something in space."),
("Payload","The weight a rocket is allowed to carry."),
("Orbit","The path a spacecraft follows around a body."),
("LEO","Low Earth Orbit: a path close to Earth."),
("GEO","An orbit that keeps the spacecraft above one region."),
("RTG","A power source that turns heat from radioactive material into electricity."),
("Reserve / margin","Extra capacity left after normal needs are met."),
("Communication / downlink","Sending information from the spacecraft to Earth."),
("Trade-off","Gaining something while giving up something else."),
("Risk index","A simplified danger number, not a real flight probability."),
("Cosmetic reward","An appearance change that does not improve game performance.")
])
p("The main lesson: a mission succeeds when its systems work together. The best next design is based on what the player learned, not simply on buying the largest parts.")

out = ROOT / "Mission-Forge-Complete-Guide.docx"
doc.save(out)
print(f"Saved {out}; {figure} embedded figures; {len(doc.paragraphs)} paragraphs; {len(doc.tables)} editable tables")
