"""Record current gameplay in an isolated browser; never change player saves or game code."""
import base64, json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT=Path("generated-artifacts/mission-forge-package")
SHOTS=OUT/"screenshots"
SHOTS.mkdir(parents=True,exist_ok=True)
DESIGNS=[
 dict(goal="air",instruments=["camera","spectrometer","thermal","magnetometer"],rocket="falcon9",power="solar",comms="hga",orbit="LEO"),
 dict(goal="air",instruments=["camera","spectrometer","magnetometer"],rocket="falcon9",power="solar",comms="hga",orbit="LEO"),
 dict(goal="craters",instruments=["lroc","lola","diviner","lamp"],rocket="falcon9",power="solar",comms="hga",orbit="LUNAR"),
 dict(goal="life",instruments=["crism","hirise","ctx"],rocket="falcon9",power="rtg",comms="hga",orbit="HOHMANN"),
 dict(goal="regolith",instruments=["diviner","lroc","lamp"],rocket="falcon9",power="solar",comms="hga",orbit="LUNAR")]
POLICY=dict(lunarShadow=1,marsDelay=0,solarStorm=1,powerShortage=0,instrumentDrain=1,contactLoss=0,trajectory=0,batteryFault=2,opportunity=1)
chapters=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path="/repl/tools/bin/chromium",headless=True,args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    ctx=browser.new_context(viewport={"width":1280,"height":800},record_video_dir=str(OUT/"raw"),record_video_size={"width":1280,"height":800})
    # Tee the game's actual Web Audio output to a recording; no new audio is composed.
    ctx.add_init_script("""
      const Original=window.AudioContext;
      window.AudioContext=class extends Original {
        constructor(...args){super(...args);
          const dest=this.createMediaStreamDestination(), orig=AudioNode.prototype.connect;
          const context=this;
          AudioNode.prototype.connect=function(target,...rest){
            if(this.context===context && target===context.destination)orig.call(this,dest);
            return orig.call(this,target,...rest);
          };
          window.demoChunks=[];window.demoRecorder=new MediaRecorder(dest.stream);
          window.demoRecorder.ondataavailable=e=>{if(e.data.size)window.demoChunks.push(e.data)};
          window.demoRecorder.start(1000);
        }
      };
    """)
    page=ctx.new_page(); errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    url="https://"+os.environ["REPLIT_DEV_DOMAIN"]+"/mission-forge.html"
    page.goto(url);page.wait_for_selector('[data-act="how"]')
    started=time.monotonic()
    data=page.evaluate("({LEVELS,PARTS,GOALS,MISSIONS,EVENTS,REWARDS,I18N:I18N.en,graphics:G3.ok})")
    (OUT/"game-data.json").write_text(json.dumps(data,indent=2))
    def act(name,arg=None):
        page.evaluate("([a,v])=>ACTIONS[a](v)",[name,arg])
        page.wait_for_timeout(250)
    def caption(text,seconds=4):
        chapters.append({"seconds":round(time.monotonic()-started,1),"text":text})
        page.evaluate("""text=>{let el=document.getElementById('demo-caption');if(!el){el=document.createElement('div');el.id='demo-caption';document.body.append(el);}
          el.style.cssText='position:fixed;bottom:0;left:0;right:0;background:#061223f5;color:white;border-top:2px solid #4fe0c3;z-index:99999;padding:12px 22px;font:16px/1.4 Arial;pointer-events:none;text-align:center';el.textContent=text;}""",text)
        page.wait_for_timeout(seconds*1000)
    def shot(name):
        page.evaluate("document.getElementById('demo-caption')?.remove()")
        page.screenshot(path=str(SHOTS/(name+".jpg")),type="jpeg",quality=86)
        print("Captured",name,flush=True)
    page.mouse.click(700,40)
    caption("MISSION FORGE | A complete guided demo of the current game",5);shot("menu")
    act("how");caption("Learn by balancing connected choices: budget, mass, power, communications, science and risk.",5);shot("help");act("closeDialog")
    act("go","levels");caption("Five playable levels: Earth, Moon and Mars. Solo progression unlocks the next mission.",5);shot("levels")
    act("playLevel","1");act("tutSkip")
    caption("A 90-second design round starts here. Tutorial and tooltips explain the choices.",4);shot("empty-design")
    # Apply the same public actions used by controls; automatic tab navigation is omitted in this guided recording.
    for actname,arg in [("pickGoal","air"),("toggleInst","camera"),("toggleInst","spectrometer"),("toggleInst","thermal"),("toggleInst","magnetometer"),("pickRocket","falcon9"),("pickPower","solar"),("pickComms","hga"),("pickOrbit","LEO")]:
        act(actname,arg)
    caption("Choose a science goal, instruments, rocket, power, communication system and orbit. Watch the six gauges.",7)
    shot("design-1")
    act("finishSelections");caption("Finish selections stops the clock and locks the design. Review comes before launch.",4)
    act("launch");caption("Go / No-Go reviews the model. A game-ready design is not real flight certification.",5);shot("gonogo")
    act("confirmLaunch");page.wait_for_timeout(2200);shot("launch")
    page.wait_for_function("state.screen==='mission'",timeout=25000)
    caption("The launch leads to mission operations. Each event offers three responses.",2);shot("mission")
    def finish_run(level):
        seen=0
        while page.evaluate("state.screen")!="results":
            s=page.evaluate("({dialog:state.dialog,over:state.mission?.over})")
            if s["dialog"] and s["dialog"]["type"]=="event":
                event=s["dialog"]["id"]
                caption("Mission event: read the problem and compare the three choices.",4 if seen==0 else 1.5)
                if level==1 and seen==0:shot("event")
                act("choose",POLICY[event])
                caption("The game explains what changed. Choices affect data, power, communications, science and risk.",3 if seen==0 else 1)
                if level==1 and seen==0:shot("consequence")
                act("resume");seen+=1
            else:
                page.wait_for_timeout(200)
        page.wait_for_timeout(1700)
        result=page.evaluate("state.result")
        print("Level result",level,result["score"],result["outcome"],flush=True)
        if page.evaluate("state.dialog?.type==='card'"):
            caption("Full success unlocks a new reward automatically. Inspect the 3D model and read its history.",4);shot("reward-"+str(level));act("equip",data["LEVELS"][level-1]["reward"]);act("closeDialog")
        caption("Results: science 35 + returned data 30 + energy 15 + risk management 20. Full success needs 70 points.",4)
        shot("results-"+str(level))
        return result
    results=[finish_run(1)]
    # Other mission examples use fresh scenario setup and faster simulation ticks, disclosed onscreen.
    for level in range(2,6):
        page.evaluate("()=>{state.dialog=null;state.progress[1]='full';state.progress[2]='full';state.progress[3]='full';state.progress[4]='full';}")
        act("playLevel",str(level))
        page.evaluate("d=>{state.design={...d,mission:currentLevel().mission};render();rebuildAssembly();}",DESIGNS[level-1])
        caption(f"Level {level} | Prepared demo design. Remaining levels use an unlocked demo save; mission time is accelerated.",5)
        shot("design-"+str(level))
        act("finishSelections");act("launch")
        if level==3:
            caption("Moon: launch and TLI checks are separate from lunar insertion. Missing costs and propulsion data stay unresolved.",6);shot("lunar-review")
        act("confirmLaunch");page.wait_for_function("state.screen==='mission'",timeout=25000)
        # Preserve the calculations and decisions, accelerate only the waiting between events.
        page.evaluate("()=>{clearTimers();state.timers.mission=setInterval(()=>{for(let i=0;i<5;i++)missionTick()},100)}")
        results.append(finish_run(level))
    act("go","collection");caption("Collection: inspect earned suits and rovers, read their history and equip them. Rewards do not change scores.",6);shot("collection")
    act("go","menu")
    page.locator(".audio-controls summary").click()
    caption("Sound controls: master, music and effect levels, plus mute. Audio starts after your first click.",5);shot("sound")
    page.locator(".audio-controls summary").click()
    act("lang");caption("The same game supports Arabic and English.",4);shot("arabic");act("lang")
    act("crewMenu");caption("Co-op supports 2–4 players on one shared screen or online with a private room code.",5);shot("crew-menu")
    act("crewSetup","local");page.locator("#crewSize").select_option("4")
    act("crewSubmit");caption("Shared-screen mode: pass control between power, instruments, communications and rocket/orbit stations.",5);shot("local-crew")
    for i in range(3):act("crewPass");page.wait_for_timeout(1200)
    page.on("dialog",lambda d:d.accept())
    act("crewLeave")
    act("crewMenu");act("crewSetup","create")
    page.locator("#crewName").fill("Demo Commander")
    act("crewSubmit");page.wait_for_function("missionCoop.room?.code")
    code=page.evaluate("missionCoop.room.code")
    guestctx=browser.new_context(viewport={"width":1280,"height":800});guest=guestctx.new_page();guest.goto(url);guest.wait_for_selector('[data-act="how"]')
    guest.evaluate("()=>{ACTIONS.crewMenu();ACTIONS.crewSetup('join')}")
    guest.locator("#crewName").fill("Demo Engineer");guest.locator("#crewCode").fill(code)
    guest.evaluate("ACTIONS.crewSubmit()")
    page.wait_for_function("missionCoop.room.players.length===2")
    caption("Online: share this room code. Each player joins separately; the host chooses settings and the science goal.",6);shot("online-lobby")
    act("crewReady");guest.evaluate("ACTIONS.crewReady()");page.wait_for_timeout(1200);act("crewStart");page.wait_for_timeout(1000)
    act("pickPower","solar");act("pickComms","hga")
    guest.evaluate("()=>ACTIONS.toggleInst('camera')");page.wait_for_timeout(1000)
    guest.evaluate("()=>ACTIONS.pickRocket('falcon9')");page.wait_for_timeout(1000)
    guest.evaluate("()=>ACTIONS.pickOrbit('LEO')");page.wait_for_timeout(1500)
    caption("Two players: host handles power + communications; partner handles instruments + rocket/orbit. Changes synchronize.",6);shot("online-design")
    act("finishSelections");page.wait_for_timeout(1000);act("launch");act("confirmLaunch")
    page.wait_for_function("state.screen==='mission'",timeout=25000)
    page.wait_for_function("state.dialog?.type==='event'",timeout=20000)
    caption("Event decisions rotate through the crew. Only the assigned player can choose; the host continues.",6);shot("online-event")
    act("choose",POLICY[page.evaluate("state.dialog.id")]);act("resume")
    page.wait_for_function("state.dialog?.type==='event'",timeout=20000)
    guest.wait_for_function("state.dialog?.type==='event'",timeout=5000)
    guest.evaluate("i=>ACTIONS.choose(i)",POLICY[page.evaluate("state.dialog.id")])
    page.wait_for_timeout(1200);caption("Partner decision received. The room pauses if a crew member disconnects. Keep the host tab active.",5)
    act("crewLeave");guestctx.close()
    act("playLevel","1");act("tutSkip")
    caption("Expiry example: fast-forwarding the demo clock only. Real players receive the full 90 seconds.",4)
    page.evaluate("()=>{window.realNow=Date.now;Date.now=()=>realNow()+95000}")
    page.wait_for_timeout(600);caption("When time expires, choices and launch are blocked. Restart selections offers a fresh round.",4);shot("timeout")
    page.evaluate("Date.now=window.realNow");act("restartSelections");caption("Restart clears choices. No incomplete mission is launched automatically.",3)
    act("go","menu")
    page.set_viewport_size({"width":390,"height":844});page.wait_for_timeout(600);shot("mobile")
    caption("Responsive layout supports mobile and desktop. Progress and equipped rewards save in this browser.",5)
    page.set_viewport_size({"width":1280,"height":800})
    caption("NASA resources + supplied workbook inform the learning model. GitHub stores the code; Replit powers development.",6)
    caption("MISSION FORGE | Design. Decide. Learn. | Educational simulation, not NASA approval or a real flight predictor.",6)
    # Save captured sound if a Web Audio context was initialized.
    audio=page.evaluate("""async()=>{if(!window.demoRecorder)return null;
      await new Promise(r=>{demoRecorder.onstop=r;demoRecorder.stop()});
      const b=new Blob(demoChunks,{type:'audio/webm'});return await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(b)})}""")
    if audio:(OUT/"game-audio.webm").write_bytes(base64.b64decode(audio))
    video=page.video;ctx.close()
    video.save_as(str(OUT/"gameplay-raw.webm"))
    browser.close()
    (OUT/"chapters.json").write_text(json.dumps(chapters,indent=2))
    (OUT/"results.json").write_text(json.dumps({"results":results,"errors":errors},indent=2))
    print("COMPLETE",len(chapters),"chapters",errors,flush=True)
