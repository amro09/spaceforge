"""Supplementary real-screen footage for validation, abort and replay controls."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path("generated-artifacts/mission-forge-package")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/repl/tools/bin/chromium",headless=True,args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    c=b.new_context(viewport={"width":1280,"height":800},record_video_dir=str(OUT/"controls-raw"),record_video_size={"width":1280,"height":800})
    pg=c.new_page();pg.goto("https://"+os.environ["REPLIT_DEV_DOMAIN"]+"/mission-forge.html")
    pg.wait_for_selector('[data-act="how"]')
    def act(a,v=None):pg.evaluate("([a,v])=>ACTIONS[a](v)",[a,v]);pg.wait_for_timeout(300)
    def cap(s,t=5):
        pg.evaluate("""s=>{let el=document.getElementById('demo-caption');if(!el){el=document.createElement('div');el.id='demo-caption';document.body.append(el)}el.style.cssText='position:fixed;bottom:0;left:0;right:0;background:#061223f5;color:white;z-index:99999;border-top:2px solid #4fe0c3;padding:12px;text-align:center;font:16px Arial;pointer-events:none';el.textContent=s}""",s)
        pg.wait_for_timeout(t*1000)
    act("playLevel","1");act("tutSkip")
    pg.evaluate("()=>{state.design={mission:'earth',goal:'air',instruments:['camera','spectrometer','thermal','magnetometer'],rocket:'falcon9',power:'battery',comms:'hga',orbit:'LEO'};render();rebuildAssembly()}")
    cap("MORE CONTROLS | A prepared low-power design: red resource checks prevent finishing and launching.")
    pg.screenshot(path=str(OUT/"screenshots"/"validation.jpg"),type="jpeg")
    act("designTab","support")
    cap("Design tabs group the choices. Click a selected instrument to remove it; choose another power system to fix a shortage.")
    act("pickPower","solar")
    for a in ["l","r","in","out"]:act("cam",a)
    cap("Camera controls rotate and zoom the 3D assembly. Desktop dragging and touch controls also work.")
    act("finishSelections");act("launch");act("confirmLaunch")
    pg.wait_for_timeout(1800);cap("Skip cinematic moves straight to the mission. It does not skip engineering checks.",1);act("skipLaunch")
    act("abort");cap("Abort asks for confirmation. Cancel returns to the mission without ending it.");act("abortNo")
    act("abort");act("abortYes");cap("Confirming Abort ends the run with an aborted result, not a successful mission.");pg.screenshot(path=str(OUT/"screenshots"/"abort.jpg"),type="jpeg")
    act("copyDesign");cap("Copy design copies the design summary when the browser permits clipboard access.")
    act("retry");cap("Retry uses the same design for another launch.",2);act("skipLaunch");act("abort");act("abortYes")
    act("redesign");cap("Redesign returns to engineering choices so the next attempt can improve the design.")
    cap("DEMO COMPLETE | Full instructions, all level examples and source links are in the editable report and walkthrough.",6)
    v=pg.video;c.close();v.save_as(str(OUT/"controls.webm"));b.close()
