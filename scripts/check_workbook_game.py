"""Exercise the user-visible workbook design and mission flows in Chromium."""
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

out=Path("generated-artifacts/workbook-check")
out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path="/repl/tools/bin/chromium",headless=True,
        args=["--no-sandbox","--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    page=browser.new_page(viewport={"width":1440,"height":1000})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto("https://"+os.environ["REPLIT_DEV_DOMAIN"]+"/mission-forge.html")
    page.wait_for_selector('[data-act="how"]')
    def click(action,arg=None):
        selector=f'[data-act="{action}"]'+(f'[data-arg="{arg}"]' if arg is not None else "")
        page.locator(selector).first.click()
        page.mouse.move(1400,980)
    def fill(goal,inst,orbit):
        click("pickGoal",goal)
        for id in inst:click("toggleInst",id)
        click("pickPower","solar")
        click("pickComms","hga")
        click("pickOrbit",orbit)
        click("pickRocket","falcon9")
    def play():
        click("launch")
        click("skipLaunch")
        start=time.monotonic()
        policy={"lunarShadow":1,"marsDelay":0,"solarStorm":1,"powerShortage":0,"instrumentDrain":1,"contactLoss":0,"trajectory":0,"batteryFault":2,"opportunity":1}
        while time.monotonic()-start<120:
            s=page.evaluate("({screen:state.screen,dialog:state.dialog,result:state.result})")
            if s["screen"]=="results":
                assert s["result"]["outcome"] in ("full","partial"),s
                print("Completed",page.evaluate("state.levelId"),s["result"]["score"],flush=True)
                return
            if s["dialog"] and s["dialog"]["type"]=="event":
                click("choose",str(policy[s["dialog"]["id"]]))
                click("resume")
            page.wait_for_timeout(150)
        raise AssertionError("Mission timed out")
    click("go","levels")
    for level in [1,2]:
        click("playLevel",str(level))
        if page.locator('[data-act="tutSkip"]').count():click("tutSkip")
        fill("air",["camera","spectrometer","magnetometer"],"LEO")
        assert page.locator("#launchBtn").is_enabled()
        play()
        click("go","levels")
    click("playLevel","3")
    fill("craters",["lroc","lola"],"LUNAR")
    assert page.locator('[aria-label="Go/No-Go"]').inner_text().find("30.5 kg / 57.4 W")>=0
    click("pickRocket","falconHeavy")
    assert page.locator("#launchBtn").is_disabled()
    assert "unresolved" in page.locator(".vals").inner_text()
    click("pickRocket","falcon9")
    assert "checks unresolved" in page.locator("#launchBtn").inner_text()
    assert "Lunar orbit insertion (LOI): Unresolved" in page.locator('[aria-label="Go/No-Go"]').inner_text()
    for locator in [page.locator('[data-scroll="parts"]'),page.locator('[data-scroll="hud"]')]:
        locator.evaluate("(e)=>e.scrollTop=0")
    page.screenshot(path=str(out/"lunar-design.jpg"),type="jpeg",quality=90)
    click("toggleInst","lola")
    assert "19.2 kg / 24 W" in page.locator('[aria-label="Go/No-Go"]').inner_text()
    click("toggleInst","lola")
    source=page.locator("#sec-instruments").locator("xpath=following-sibling::*").count()
    assert page.locator('a[href*="spaceflightnow.com"]').count()>0
    click("lang")
    assert page.locator("html").get_attribute("dir")=="rtl"
    assert "فحوص غير محسومة" in page.locator("#launchBtn").inner_text()
    page.set_viewport_size({"width":390,"height":844})
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
    page.screenshot(path=str(out/"lunar-mobile-ar.jpg"),type="jpeg",quality=90)
    page.set_viewport_size({"width":1440,"height":1000})
    click("lang")
    play()
    assert "Lunar Reconnaissance Orbiter" in page.locator("#ui").inner_text()
    assert "11.3 kg and 33.4 W" in page.locator("#ui").inner_text()
    page.screenshot(path=str(out/"lunar-results.jpg"),type="jpeg",quality=90)
    click("go","levels")
    click("playLevel","4")
    fill("marsWater",["sharad","crism"],"HOHMANN")
    assert page.locator("#launchBtn").is_disabled()
    assert "electrical demand is unavailable" in page.locator(".vals").inner_text()
    assert "Unavailable" in page.locator('[aria-label="Go/No-Go"]').inner_text()
    assert not errors,errors
    print("Browser passed: Earth 1/2, lunar completion, null capacity/power, LROC/LOLA totals, source links, Arabic/mobile; no JS errors.",flush=True)
    browser.close()
