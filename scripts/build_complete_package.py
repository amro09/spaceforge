"""Create the editable report and live walkthrough from the current game captures."""
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT=Path("generated-artifacts/mission-forge-package")
DATA=json.loads((OUT/"game-data.json").read_text())
W=json.loads(Path("artifacts/mission-forge/public/data/mission-workbook.json").read_text())
T=DATA["I18N"]
def label(key):return T.get(key,key)
def make(title,subtitle):
    d=Document();s=d.sections[0];s.top_margin=s.bottom_margin=Inches(.65)
    s.left_margin=s.right_margin=Inches(.75)
    st=d.styles["Normal"];st.font.name="Calibri";st.font.size=Pt(11);st.paragraph_format.space_after=Pt(7)
    for h in ["Title","Heading 1","Heading 2"]:d.styles[h].font.color.rgb=RGBColor.from_string("124E61")
    s.header.paragraphs[0].text="MISSION FORGE  /  PROJECT DOCUMENTATION"
    footer=s.footer.paragraphs[0];footer.add_run("Mission Forge  •  ")
    field=OxmlElement("w:fldSimple");field.set(qn("w:instr"),"PAGE");footer._p.append(field)
    d.add_heading(title,0);d.add_paragraph(subtitle)
    return d
def text(d,t):d.add_paragraph(t)
def bullets(d,items):
    for t in items:d.add_paragraph(t,"List Bullet")
def chapter(d,title):
    d.add_page_break();d.add_heading(title,1)
def shot(d,name,caption,width=6.5):
    path=OUT/"screenshots"/(name+".jpg")
    if not path.exists():raise FileNotFoundError(path)
    # Portrait images remain readable without extending beyond the page.
    from PIL import Image
    with Image.open(path) as im:width=min(width,4.1*im.width/im.height)
    d.add_picture(str(path),width=Inches(width));d.add_paragraph(caption,"Caption")
def table(d,heads,rows):
    t=d.add_table(rows=1,cols=len(heads));t.style="Light Shading Accent 1"
    for c,v in zip(t.rows[0].cells,heads):c.text=str(v)
    for row in rows:
        for c,v in zip(t.add_row().cells,row):c.text=str(v)
def link(d,title,url):
    p=d.add_paragraph();p.add_run(title+"\n")
    rel=d.part.relate_to(url,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",is_external=True)
    h=OxmlElement("w:hyperlink");h.set(qn("r:id"),rel)
    r=OxmlElement("w:r");pr=OxmlElement("w:rPr");color=OxmlElement("w:color");color.set(qn("w:val"),"086C82");pr.append(color);r.append(pr)
    t=OxmlElement("w:t");t.text=url;r.append(t);h.append(r);p._p.append(h)

d=make("Mission Forge","Detailed game report • Simple English • Current browser-game version • 15 November 2026")
text(d,"Design a spacecraft, launch it, solve problems and learn from the results. Play alone or share the work with a crew of two to four people.")
shot(d,"menu","The current Mission Forge home screen.")
text(d,"This report documents the game that is implemented in the current workspace. It does not describe a NASA-approved mission planner. Screenshots use an isolated demonstration save, not a player's personal account.")
chapter(d,"1. The idea, problem and solution")
text(d,"Space missions bring together many connected decisions. An instrument can improve science but also need more mass, power and money. A rocket must be suitable for the destination. A spacecraft must send useful data home, not only collect it.")
text(d,"Students often meet these ideas as separate facts. Mission Forge makes them connected choices in one short game. Players can try a design, see the result, discuss mistakes and try again without risking a real mission.")
bullets(d,["Goal: teach trade-offs, teamwork and evidence-based decisions.","Audience: students, teachers and people beginning to learn about space missions.","Solution: a 3D mission-design game with resource checks, unexpected events, simple explanations and educational rewards.","Challenge connection: the Space Mission Design Game challenge asks players to design, manage and simulate a mission under competing constraints."])
text(d,"The game has five playable levels: two Earth missions, two Moon missions and one Mars mission. Unlike the earlier project presentation, Moon and Mars are no longer described as future-only levels.")
shot(d,"levels","The level-selection screen. Locked cards in a fresh solo save reflect progression, not missing implementation.")
chapter(d,"2. The complete player journey")
bullets(d,["Choose solo play or a crew mode.","Choose an available level and science goal.","Select instruments, rocket, power, communications and orbit within the 90-second selection round.","Read budget, mass, power, communication, science and risk gauges. Use tooltips and information panels.","When the choices are ready, press Finish selections. This locks the design and stops the clock.","Launch mission opens Go/No-Go. Read the checks and confirm launch.","Watch the 3D launch, or skip the cinematic.","Read each mission event, choose one of three responses and review its effects.","Review the score, timeline and learning feedback. Retry, redesign or choose another level.","Full success earns the level reward. Inspect it, learn its history and equip it from the collection."])
shot(d,"design-1","Example Level 1 design with a complete set of choices.")
chapter(d,"3. Cooperative play")
text(d,"Shared-screen mode lets two to four people use one device. Players pass control between engineering stations. This is cooperative mission planning, not split-screen piloting.")
text(d,"Online mode uses a private six-character room code. The creator chooses crew size, level and science problem. Each other player opens the same game address, enters a name and joins with the code. All selected seats must be filled, connected and ready before the host starts.")
table(d,["Crew","Player 1","Player 2","Player 3","Player 4"],[
["2","Power + communications","Instruments + rocket/orbit","—","—"],
["3","Power + rocket/orbit","Instruments","Communications","—"],
["4","Power","Instruments","Communications","Rocket/orbit"]])
shot(d,"online-lobby","An actual two-browser demonstration room. The displayed code is temporary, not a permanent invitation.")
text(d,"The server restricts choices to assigned roles. Event decisions rotate by mission segment; the host continues after the explanation. The host browser runs the educational simulation. Keep its tab open and active.")
text(d,"A disconnected member pauses the mission. Refreshing the same online tab can reconnect its participant. Leaving an active crew closes the mission; rooms also end on a server restart or after 30 minutes without requests. This local version does not include host handover or account-based cloud rewards.")
chapter(d,"4. Timed selections and safe retry")
text(d,"There is one 90-second selection round per solo or shared crew design, not 90 seconds for every station. Online clients use the server's shared deadline. Reloading a guest tab does not create extra time.")
text(d,"A completion notice means the player's assigned fields are filled. The player may still change them. Finish selections is a separate confirmation by the host or solo/shared-screen player; it requires a design the game allows to launch.")
text(d,"If time runs out before finishing, selection and launch controls are blocked. Restart selections asks for confirmation, clears choices and starts a new round. In online play only the host can restart. A crew's host-selected science goal remains fixed.")
shot(d,"timeout","Timeout state. The video labels its demonstration clock advance; normal play gives the full 90 seconds.")
chapter(d,"5. Resources and scientific limits")
table(d,["Resource","What players learn"],[
["Budget","Compare known costs with the level cap. Missing costs remain unavailable, not free."],
["Mass","Add the modeled bus, instruments, power and communications mass; compare with destination capacity."],
["Power","Meet bus, payload and communication demand plus the level reserve."],
["Communication","Link quality affects the amount of data returned. Low quality is a warning, not an added launch blocker."],
["Science","Instruments that match the goal can improve science value."],
["Risk","Design choices and event responses affect modeled mission risk."]])
text(d,"Units are kilograms (kg), watts (W), million US dollars ($M), and kilometres per second (km/s) where a transfer reference is shown. Power in watts is not battery energy or mission endurance.")
text(d,"Example from the implemented lunar calculations: LROC plus LOLA has 30.5 kg instrument mass and 57.4 W instrument demand. With the game's modeled bus and support systems, total demand is 147.4 W. A 10% reserve adds 14.74 W, giving 162.14 W required. Only the instrument values are source-backed hardware values; the surrounding model settings are educational assumptions.")
text(d,"Missing electrical demand or destination capacity blocks starting the model. Missing instrument prices can allow a clearly labelled teaching run, but do not establish an affordable real mission. GTO is not silently treated as GEO. SHARAD's radio-frequency output is not treated as its total electrical input.")
shot(d,"lunar-review","Lunar checks distinguish Earth launch, transfer and insertion; unresolved information remains visible.")
chapter(d,"6. Launch, operations and decisions")
text(d,"The launch scene shows the rocket, pad, tower, lighting and engine effects. These visuals make the mission easier to understand; they do not calculate a real trajectory or prove that a rocket can fly the design.")
shot(d,"launch","A real capture of the current 3D launch sequence.")
text(d,"After launch, each segment includes an event. The mission pauses while a dialogue is open. Players compare three options, choose one, read the changes and resume. Power, communication, science, risk, collected data and returned data can change.")
shot(d,"event","An event with three choices. There is no universal best answer for every possible design.")
chapter(d,"7. Results, progression and learning")
table(d,["Score component","Maximum"],[["Science collected",35],["Data returned",30],["Energy left",15],["Risk managed",20],["Total",100]])
text(d,"Full success needs at least 70 points. Partial success needs at least 45. A forced failure or abort can prevent success regardless of a promising earlier state. Partial or full completion can open the next solo level, but only full success earns the level reward.")
text(d,"The results screen gives a score breakdown, mission timeline and learning tips. Players can retry the design, redesign, copy the design summary or return to levels. When matching mission references are configured, the results can show them.")
shot(d,"results-1","An actual recorded result. Scores vary with events and choices; the document does not guarantee a score.")
for lv in DATA["LEVELS"]:
    i=lv["id"];chapter(d,f"{7+i}. Level {i}: {label('level.'+str(i)+'.name')}")
    table(d,["Setting","Value"],[
        ["Destination",lv["mission"].title()],["Game budget cap",f"${lv['budget']}M"],
        ["Maximum instruments",lv["maxInstruments"]],["Power reserve",f"{lv['powerReserve']*100:g}%"],
        ["Mission segments",lv["segments"]],["Game seconds per segment",lv["segSeconds"]],
        ["Event penalty multiplier",lv["severity"]],["Reward",label("rw."+lv["reward"])]])
    text(d,"These level caps, timing, reserve percentages and penalty multipliers are game-balance settings, not NASA mission requirements.")
    descriptions={1:"Begin with Earth mission design. The first level introduces the tutorial, resource checks and mission events.",
    2:"A smaller budget, fewer instruments, extra power reserve and stronger event penalties require more careful choices.",
    3:"Plan a lunar survey with imported LRO instruments. Lunar shadow introduces power-management trade-offs. Lunar insertion remains unresolved when propulsion information is missing.",
    4:"Plan a Mars mission with imported MRO instruments. Communication delay is a signature event. Modeled solar output is reduced at Mars; it is a teaching factor, not a full solar-array design.",
    5:"Return to the Moon with a tighter cap, three instruments, a 15% reserve and stronger penalties. Missing instrument prices still prevent a complete real-world cost total."}
    text(d,descriptions[i]);shot(d,"design-"+str(i),f"Level {i} prepared example from the recorded demo. Later examples use an unlocked demo save.")
    if i in (3,4,5):text(d,"Important: a playable teaching run is not a verified flight plan. Check source notes and unresolved fields before making any scientific claim.")
chapter(d,"13. Event catalogue")
text(d,"This catalogue lists the current event prompts and all three response labels. Consequences are explained in the game after each response. Penalties are scaled by the level, so an option that is safe in one mission may be risky in another.")
for key in DATA["EVENTS"]:
    d.add_heading(label("ev."+key),2);text(d,label("ev."+key+".b"))
    bullets(d,[label("ev."+key+".o"+str(n)) for n in (1,2,3)])
chapter(d,"14. Rewards and collection")
table(d,["Level","Reward","Type"],[[r["level"],label("rw."+k),r["kind"]] for k,r in DATA["REWARDS"].items()])
text(d,"Newly earned rewards appear automatically after full success. The model can be inspected and the information card explains its story. Suits have different shapes and details. Rover rewards are separate from suits. Equipping an item changes the collection/equipment state but does not improve the mission score or alter engineering calculations.")
shot(d,"reward-1","The first earned reward appears automatically after full success.")
shot(d,"collection","The current collection after demonstration runs. A fresh user must earn rewards through play.")
chapter(d,"15. Controls, sound, languages and saves")
bullets(d,["Desktop: use the design tabs, buttons, tooltips and information panels. Drag the model and use camera controls or zoom.","Mobile: the interface adapts to a narrow screen; touch controls support the same choices.","Sound: master, music and effects controls plus mute; settings save in the browser. Sound starts after interaction and pauses when the tab is hidden.","English/Arabic: switch language from the header. This report and walkthrough use English.","Progress: completed levels, rewards, equipment and language save in this browser. Clearing site data removes the save; private browsing may not retain it.","Active solo missions are not restored as a running flight after refresh. Online reconnection is a temporary room/session feature, not permanent cloud storage.","Abort: the game asks for confirmation; cancelling returns to the mission. Confirming ends it with an aborted result."])
shot(d,"sound","Sound controls are in the header, away from launch actions.")
shot(d,"mobile","The real responsive layout on a narrow screen.",width=2)
chapter(d,"16. Design and implementation tools")
table(d,["Tool / component","Use in this project"],[
["Replit","Development workspace, running preview and project tooling."],
["GitHub","Source control, sharing code and merging team changes."],
["Three.js / WebGL","3D planets, spacecraft, launch visuals and reward models."],
["Web Audio API","Procedural background music and interaction/launch effects."],
["React / Vite","Browser-app host and development tooling."],
["Express / TypeScript","Co-op room API and server-side role/deadline checks."],
["Supplied Excel workbook","Imported source values, confidence labels, notes and proposed level settings."],
["Browser storage","Local progress and audio/language preferences; tab session for reconnect."],
["Playwright, Python and FFmpeg","Recorded app demonstrations, screenshot capture and document/video production."]])
text(d,"The browser game separates design calculations from the 3D view. The online server holds temporary room state and checks who may act. The host sends mission snapshots to the crew. This is an educational cooperative architecture, not a secure competitive simulation.")
text(d,"The demo recording uses isolated browser profiles. Later-level saves are unlocked for presentation, and waiting between later mission events is accelerated. Scores and event effects still come from the game engine. The video labels these shortcuts. These are recording techniques, not player-facing features.")
chapter(d,"17. Resources, references and attribution")
text(d,"Source of record: the supplied Mission Forge Data Pack, imported into the game. The following links and confidence labels are recorded in that workbook. Listing them does not mean every resource became an implemented game feature, or that all pages were independently rechecked for this report.")
text(d,"HIGH / MEDIUM / UNVERIFIED below are the workbook author's labels, not new certifications. NASA-hosted information, secondary estimates, community material and game assumptions must not be treated as equally authoritative.")
for n,s in enumerate(W["sources"],1):
    link(d,f"[{n}] {s['title']} — Workbook label: {s['confidence']}",s["url"])
d.add_heading("Project and development tools",2)
for title,url in [
("Mission Forge project repository","https://github.com/MahmoudFarah003/spaceforge"),
("GitHub","https://github.com/"),("Replit","https://replit.com/"),
("Three.js","https://threejs.org/"),
("Web Audio API documentation","https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API")]:link(d,title,url)
text(d,"Original challenge and judging requirements were also supplied by the team as screenshots. Game screenshots in this package were captured from the team's current application. No NASA endorsement or affiliation is claimed.")
chapter(d,"18. How to check a NASA-related claim")
bullets(d,["Identify exactly which value or statement you want to check.","Open its workbook source and inspect the original instrument or mission description.","Check the units and meaning: watts versus RF output, payload versus full spacecraft mass, GTO versus GEO.","Confirm whether it is a NASA primary source, secondary estimate, community suggestion or model setting.","Compare the imported value with the same field in the game. Do not fill missing values with guesses.","Label budget caps, score weights, event penalties, mission duration and rewards as educational rules.","If a source is incomplete or uncertain, keep the uncertainty visible. A playable level does not prove that the whole design is feasible."])
text(d,"Known scope limits: simplified orbital/transfer rules; incomplete costs; unresolved lunar insertion; illustrative graphics; temporary co-op rooms; local browser saves. Do not present the game as a real launch approval system.")
d.save(OUT/"Mission_Forge_Detailed_Report.docx")

walk=make("Mission Forge — Complete Live Demo","Presenter walkthrough • English • Use beside the gameplay video")
text(walk,"Purpose: demonstrate the current game's features clearly, not speed-run every level. Allow about 12–18 minutes for a live presentation; a classroom session can take longer.")
shot(walk,"menu","Start from the home screen.")
steps=[
("1. Introduce the game","Show the menu and How to play.","Mission Forge lets us design, launch and manage a mission. Every choice affects the others."),
("2. Explain progression","Open Levels. Show all five cards.","Two Earth missions, a lunar survey, a Mars mission and a harder lunar mission are implemented. Solo players unlock levels through progress."),
("3. Design Level 1","Start First Light. Use Air quality; Camera, Spectrometer, Thermal imager, Magnetometer; Falcon 9; Solar panels; High-gain antenna; LEO.","Watch the six gauges. This example balances the current learning model, but it is not a real NASA design."),
("4. Show the clock and tools","Point to the 90-second timer. Show tabs, a tooltip, model rotation and zoom. Remove and reselect an instrument if time permits.","The notice says my choices are complete, but I can still change them until I confirm Finish selections."),
("5. Confirm and review","Press Finish selections, then Launch mission. Review Go/No-Go.","Finishing stops the selection clock and locks the design. Review is separate from launching."),
("6. Launch and manage","Confirm launch. Let the animation finish. Read the first event.","There are three choices. The right trade-off depends on the situation and remaining resources."),
("7. Explain consequences","Choose an option, read the changes and press Continue/Resume. Complete the remaining segments.","We see why each decision changed science, data, power or risk."),
("8. Results and reward","Show the four score components and timeline. If full success earns a new reward, let its automatic reveal appear.","Full success needs 70 points. Partial success needs 45. Only full success earns the reward."),
("9. Collection and replay","Open Collection. Inspect an earned reward and equip it. Show retry, redesign and copy-design options on results.","The rewards teach space history. They do not make our engineering numbers stronger."),
("10. Show the other levels","Use a prepared demo save or play sequentially. Use the example designs in the next section.","Moon and Mars add different instruments and events. Missing costs and lunar insertion capability are still unknown."),
("11. Shared-screen crew","Home → Play with a crew → Shared screen. Select four players, mission and goal. Assemble crew, then Pass to next player.","Each person owns an engineering station. We share one 90-second round."),
("12. Real online crew","Use two independent browser profiles/devices. Host creates a 2-player room; guest joins using the displayed code. Both mark ready; host starts.","Player 1 controls power and communications. Player 2 controls instruments and rocket/orbit. The server rejects actions from the wrong role."),
("13. Rotating event ownership","Complete and finish the online design; host launches. Show host responding in one segment and guest in the next.","Event responsibility rotates. The host continues after the explanation. Keep the host tab active."),
("14. Timeout and restart","Start a separate fresh round and let 90 seconds pass. Press Restart selections and accept the confirmation.","The game blocks an unfinished launch. The host can start a fresh online round; a guest cannot extend the deadline."),
("15. Controls and persistence","Open Sound, adjust music/effects and toggle mute. Switch to Arabic and back. Show a narrow-screen layout. Refresh after returning to menu.","Preferences and completed rewards save in this browser, not in a cloud account. Clearing browser data removes them."),
("16. Abort and end","In a separate mission, open Abort. Cancel once, then confirm on a second attempt.","Cancelling resumes the mission; confirming ends it. Finish by explaining the source limits, not by claiming NASA certification."),
("17. Resources and closing","Show the final presentation slide and report references.","NASA resources and the supplied workbook inform selected values. GitHub supports collaboration, and we built the project with Replit.")
]
for title,do,say in steps:
    walk.add_heading(title,2);text(walk,"DO: "+do);text(walk,"SAY: “"+say+"”")
chapter(walk,"Prepared designs for all five levels")
text(walk,"Use these examples to explore the current version. Scores vary. The Moon and Mars examples can run educational scenarios with incomplete price data; they are not verified real mission designs.")
for lv,items in zip(DATA["LEVELS"],[
["Air quality","Camera, Spectrometer, Thermal imager, Magnetometer","Solar panels","LEO"],
["Air quality","Camera, Spectrometer, Magnetometer","Solar panels","LEO"],
["Crater mapping","LROC, LOLA, Diviner, LAMP","Solar panels","Lunar orbit"],
["Signs of life","CRISM, HiRISE, CTX","RTG","Hohmann transfer"],
["Regolith","Diviner, LROC, LAMP","Solar panels","Lunar orbit"]]):
    walk.add_heading(f"Level {lv['id']} — {label('level.'+str(lv['id'])+'.name')}",2)
    text(walk,f"Goal: {items[0]}. Instruments: {items[1]}. Rocket: Falcon 9. Power: {items[2]}. Communications: High-gain antenna. Orbit: {items[3]}.")
chapter(walk,"Feature coverage and presenter checklist")
table(walk,["Feature","Where to show it"],[
["Goal, instruments, rocket, power, comms, orbit","Level 1 design"],
["Six gauges, tooltips, camera controls","Design screen"],
["90-second timer, completion, finish, retry","Design and separate timeout example"],
["Go/No-Go and unresolved data","Earth review and lunar review"],
["3D launch and skip","Launch sequence"],
["Events, consequences, mission status","Solo mission and rotating crew turns"],
["Scores, timeline, retry, redesign, copy","Results"],
["All five levels and distinct reward types","Prepared level examples and Collection"],
["Shared-screen 2–4 player roles","Local crew"],
["Room code, ready, settings, synchronized choices","Two independent online clients"],
["Reconnect and temporary-room limits","Explain; refresh guest tab, not the active host"],
["Sound, language, mobile, saved progress","Header controls and fresh menu reload"],
["Abort confirmation","Separate mission; do not interrupt the main demonstration"]])
text(walk,"Before presenting: open the game, enable sound with a click, use a stable connection, prepare a second browser/device for co-op, and keep the host active. Use a separate profile if you do not want to change your personal progress. A screenshot room code from the report will not join a live room.")
text(walk,"Recording disclosure: the accompanying video uses real app screens and an isolated demo save. Later-level designs are prepared; later waiting periods are accelerated and clearly labelled. Timeout uses a labelled demo clock jump. The live game still uses its normal timings.")
link(walk,"Project source","https://github.com/MahmoudFarah003/spaceforge")
walk.save(OUT/"Mission_Forge_Live_Demo_Walkthrough.docx")
print("Created editable report and walkthrough.")
