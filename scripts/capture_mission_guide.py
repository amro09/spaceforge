"""Capture actual English gameplay for the presentation and editable guide."""
import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("generated-artifacts/mission-forge")
SHOTS = OUT / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
    browser = pw.chromium.launch(
        executable_path="/repl/tools/bin/chromium", headless=True,
        args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    page.goto("https://" + os.environ["REPLIT_DEV_DOMAIN"] + "/mission-forge.html")
    page.wait_for_selector('[data-act="how"]')
    page.wait_for_timeout(1800)
    data = page.evaluate("({LEVELS, PARTS, GOALS, MISSIONS, EVENTS, REWARDS, I18N:I18N.en, graphics:G3.ok})")
    (OUT / "game-data.json").write_text(json.dumps(data, indent=2))
    print("3D enabled:", data["graphics"], flush=True)

    def click(act, arg=None):
        selector = f'[data-act="{act}"]' + (f'[data-arg="{arg}"]' if arg is not None else "")
        page.locator(selector).first.click()
        page.mouse.move(1438, 898)
        page.wait_for_timeout(130)

    def shot(name):
        page.screenshot(path=str(SHOTS / (name + ".jpg")), type="jpeg", quality=90)
        print("Captured", name, flush=True)

    def scroll_top():
        page.evaluate("document.querySelectorAll('*').forEach(e=>{if(e.scrollTop)e.scrollTop=0})")
        page.mouse.move(1438,898)
        page.wait_for_timeout(200)

    def design():
        for act, arg in [("pickGoal","weather"),("toggleInst","camera"),("toggleInst","thermal"),
                         ("pickRocket","condor"),("pickPower","solar"),("pickComms","hga"),("pickOrbit","GEO")]:
            click(act, arg)
        scroll_top()

    def run_mission(level):
        click("launch")
        if level == 1:
            page.wait_for_timeout(3400)
            shot("06-launch")
        page.wait_for_selector('[data-act="abort"]', timeout=20000)
        if level == 1:
            shot("07-mission")
        seen = set()
        started = time.monotonic()
        while time.monotonic() - started < 100:
            status = page.evaluate("({screen:state.screen, dialog:state.dialog, result:state.result})")
            if status["screen"] == "results":
                shot("10-results-level1" if level == 1 else "14-results-level2")
                print("Result", level, status["result"], flush=True)
                return status["result"]
            d = status["dialog"]
            if d and d["type"] == "event":
                if level == 1 and not seen:
                    shot("08-event")
                choices = {"solarStorm":1,"powerShortage":0,"instrumentDrain":1,
                           "contactLoss":1,"trajectory":0,"batteryFault":0,"opportunity":1}
                click("choose", choices[d["id"]])
                if level == 1 and not seen:
                    shot("09-consequence")
                seen.add(d["id"])
                click("resume")
            page.wait_for_timeout(200)
        raise RuntimeError("Mission did not reach results")

    shot("01-menu")
    click("go", "levels")
    shot("02-levels")
    click("playLevel", "1")
    shot("03-tutorial")
    click("tutSkip")
    design()
    shot("04-design-level1")
    click("pickRocket", "sparrow")
    scroll_top()
    shot("05-validation")
    click("pickRocket", "condor")
    scroll_top()
    result = run_mission(1)
    if result["outcome"] != "full":
        raise RuntimeError("Level 1 did not reach full success")
    click("openCard", "launchSuit")
    shot("11-reward-launch-suit")
    click("equip", "launchSuit")
    if page.locator('[data-act="closeDialog"]').count():
        click("closeDialog")
    click("go", "collection")
    shot("12-collection")
    click("go", "levels")
    click("playLevel", "2")
    design()
    shot("13-design-level2")
    result = run_mission(2)
    if result["outcome"] == "full":
        click("openCard", "apolloSuit")
        shot("15-reward-apollo")
        click("closeDialog")
        click("go", "collection")
        shot("12-collection")
    click("go", "levels")
    for n in (3,4,5):
        button = page.locator(f'[data-act="playLevel"][data-arg="{n}"]')
        card = button.locator("..")
        card.screenshot(path=str(SHOTS / f"level-{n}-planned.jpg"), type="jpeg", quality=92)
    page.set_viewport_size({"width":390,"height":844})
    click("go","menu")
    shot("16-mobile")
    browser.close()
