# Mission Forge

**Design a spacecraft, launch it, and keep its mission alive.**

Mission Forge is an educational 3D browser game inspired by the NASA Space Apps space-mission-design challenge. Players learn how science goals, instruments, power, mass, communications, budgets, and risk affect one another.

> This is a learning game, not a NASA-certified simulator. Some specifications come from NASA and other references in the supplied data workbook. Scores, events, timers, budgets, and many balancing rules are simplified game rules—not real flight predictions.

## Contents

- [Download](#1-download-the-project)
- [Required tools](#2-required-tools)
- [Quick start](#3-quick-start-solo-and-shared-screen)
- [Online co-op](#4-enable-online-co-op)
- [How to play](#5-how-to-play)
- [Test checklist](#6-how-to-check-the-game)
- [Troubleshooting](#7-troubleshooting)
- [Developer setup](#8-developer-setup)
- [Data and resources](#9-data-references-and-tools)
- [Project files](#10-project-files)

## 1. Download the project

### Option A: Download a ZIP (no Git needed)

1. Open [MahmoudFarah003/spaceforge](https://github.com/MahmoudFarah003/spaceforge).
2. Select **Code → Download ZIP**.
3. Extract the ZIP completely.
4. Open a terminal inside the extracted project folder. This is the folder containing this README and `package.json`.

### Option B: Clone with Git

```sh
git clone https://github.com/MahmoudFarah003/spaceforge.git
cd spaceforge
```

If GitHub requests access, sign in with an account allowed to view the repository. Do not share tokens or passwords.

## 2. Required tools

| Tool | When it is needed |
| --- | --- |
| [Node.js 24 LTS](https://nodejs.org/) | Recommended for the quick launcher and full development |
| Current Chrome, Edge, Firefox, or Safari | Playing; WebGL/hardware acceleration is recommended for 3D |
| Internet connection | Downloading files/packages and loading Three.js from cdnjs |
| [Git](https://git-scm.com/) | Optional; cloning and updating instead of downloading a ZIP |
| [pnpm 10](https://pnpm.io/installation) | Online API server and React/Vite development only |
| Editor such as [VS Code](https://code.visualstudio.com/) | Optional; editing the project |

**Quick play does not need pnpm, Python, a database, NASA API keys, a GitHub integration, or a Replit account.** The online API currently uses temporary in-memory rooms, not a database.

For the full workspace, use **Linux x64 with glibc**, or **Ubuntu x64 inside WSL2 on Windows**. The current workspace intentionally excludes many native dependencies for Windows, macOS, ARM, and Alpine Linux. The dependency-free quick launcher works without those packages, including on Windows/macOS.

Check Node:

```sh
node --version
```

## 3. Quick start: solo and shared screen

From the project root:

```sh
node scripts/play-local.mjs
```

Open **http://localhost:8080** in your browser.

- No `pnpm install` or build is required for this quick route.
- It serves the actual game, including graphics, workbook data, sound, missions, and local saves.
- Solo and 2–4-player shared-screen play work without the API.
- Online rooms require the additional setup below.
- Keep the terminal running. Press **Ctrl+C** to stop.
- Do not simply double-click the HTML file: `file://` loading can block data requests.

If port 8080 is occupied:

```sh
node scripts/play-local.mjs 8081
```

Then open http://localhost:8081. Browser saves belong to a specific address/port; changing it can make an existing save appear missing.

## 4. Enable online co-op

Use the supported Linux/WSL2 environment described above. From the project root:

```sh
npm install --global pnpm@10.26.1
pnpm install --frozen-lockfile
```

Installing pnpm with npm is fine; installing this workspace's dependencies with npm is not.

### Terminal 1: start the API

```sh
PORT=3001 pnpm --filter @workspace/api-server run dev
```

Keep it running. Check **http://localhost:3001/api/healthz**: it should return `{"status":"ok"}`.

### Terminal 2: start the game

```sh
node scripts/play-local.mjs 8080 3001
```

Open http://localhost:8080. The launcher forwards `/api/` requests to the API on port 3001. Frontend and API must both stay running.

### Create and join a room

1. Select **Play with a crew · 2–4 players**.
2. The host creates an online room and selects crew size, mission, and science goal.
3. Share the six-character room code and the **same game address**.
4. Other players choose **Join a crew** and enter their names and the code.
5. All selected seats must be filled, connected, and ready.
6. The host starts. Each player controls their assigned equipment.

To test on one computer, open separate browser windows/profiles and join the same room. Keep the host visible/active during the simulation.

### Other devices on the same trusted Wi-Fi/LAN

```sh
node scripts/play-local.mjs 8080 3001 --lan
```

Players open `http://YOUR-COMPUTER-LAN-IP:8080`, not `localhost`. Allow TCP port 8080 through the host firewall only on your trusted private network. WSL2 may need Windows networking/port-forwarding configuration; testing in browser windows on the same computer is simpler.

**This does not make the game available across the internet.** Players on different networks need one publicly hosted frontend and API, with `/api/` routed to the backend and HTTPS configured. A room code alone does not connect different servers. The local launcher is for demos, not hardened public hosting; do not expose it directly to the internet.

### Co-op responsibilities

| Crew | Player 1 | Player 2 | Player 3 | Player 4 |
| --- | --- | --- | --- | --- |
| 2 | Power + communications | Instruments + rocket/orbit | — | — |
| 3 | Power + rocket/orbit | Instruments | Communications | — |
| 4 | Power | Instruments | Communications | Rocket/orbit |

In shared-screen mode, use **Pass to next player**. In online mode, assigned controls are checked by the server. Event decisions rotate through the crew; the host handles launch and continuing after outcomes.

**Session limits:** Rooms are temporary, expire after 30 minutes without requests, and disappear on server restart. A disconnection pauses play. Same-tab reload can reconnect that participant. Host departure closes the room; this version has no automatic host replacement. Keep the host tab open and active.

## 5. How to play

1. Choose solo play or a crew.
2. Select an available mission and its science goal.
3. Choose instruments, a power source, communications, a rocket, and an orbit.
4. Balance the resource gauges and read the design warnings.
5. Finish within the **90-second selection round**. Co-op players share the round, not 90 seconds each.
6. Press **Finish selections** once the design is complete and launchable. This locks the design and stops the selection timer; it does not launch automatically.
7. Review Go/No-Go checks, then launch.
8. Watch the rocket sequence and respond to mission events.
9. Read each choice's effect on science, returned data, energy, and risk.
10. Review results, collect a newly earned reward, and improve your next design.

If time expires, selections and launch are blocked. Confirm **Restart selections** to clear the design and try again. Only the online host can restart the crew's round.

### Missions and rewards

| Level | Mission | Destination | Full-success reward |
| --- | --- | --- | --- |
| 1 | First Light | Earth | Launch & Entry Suit |
| 2 | Tight Margins | Earth | Apollo-style Suit |
| 3 | Lunar Survey | Moon | Mars Rover |
| 4 | Red Horizon | Mars | EVA Suit |
| 5 | Moon on a Shoestring | Moon | Lunar Rover |

Solo progression unlocks later levels through partial or full success. Co-op training can select implemented missions without following the same solo progression.

### Scores

- Science collected: up to **35** points.
- Data returned: up to **30** points.
- Remaining energy: up to **15** points.
- Risk managed: up to **20** points.
- **70+**: full success; **45–69**: partial success.
- Aborting or a forced mission failure can override the numerical score.

Only full success earns a level's reward. Newly earned rewards have a reveal screen and can be inspected in the collection. Suits and rover rewards are educational/cosmetic; they do not boost mission scores.

### Other features

- English and Arabic interface.
- Desktop and mobile layouts.
- 3D Earth/spacecraft scenes and detailed rocket-launch visuals.
- Procedural space music, interface effects, and launch audio.
- Sound settings, mission tips, Go/No-Go explanations, retry and redesign options.
- Saved completed progress, rewards, language, and sound settings in the current browser.

**Save limits:** Clearing browser/site data removes local saves. Private browsing may discard saves. They do not automatically sync between browsers or devices. Refreshing does not restore an active solo mission. Shared-screen players use one browser collection.

## 6. How to check the game

### Manual checklist

- [ ] The menu loads and Earth is visible in 3D, or a clear fallback message explains why 3D is unavailable.
- [ ] English/Arabic switching updates the interface.
- [ ] A click enables audio; music/effects controls and mute work.
- [ ] Equipment choices update the resource gauges.
- [ ] Invalid or unresolved blocking checks prevent launch and explain why.
- [ ] The 90-second clock starts in design; Finish selections locks a valid design.
- [ ] Expiry blocks launch; restarting clears choices after confirmation.
- [ ] Launch plays, and each mission event displays choices and consequences.
- [ ] Results display the four scoring categories.
- [ ] A new full-success reward appears and is available in Collection.
- [ ] Reload after completion preserves completed progress and rewards.
- [ ] Shared-screen controls switch between assigned players.
- [ ] Online players join the same room, ready up, and see synchronized actions.
- [ ] A guest cannot edit another player's assigned systems.
- [ ] A phone-sized display remains usable.

### Automated checks

From the root after installing workspace dependencies:

```sh
pnpm --filter @workspace/mission-forge test
node artifacts/mission-forge/tests/persistence.test.cjs
```

The browser workbook script `scripts/check_workbook_game.py` needs Python, Playwright, the Replit Chromium path, and `REPLIT_DEV_DOMAIN`. It is a workspace-specific capture script, not a portable local validation command. The co-op API check in `scripts/test-coop-api.mjs` also targets the Replit development domain through `REPLIT_DEV_DOMAIN`; it is not a localhost test command as currently written.

These tests do not certify NASA accuracy, visual quality on every GPU, or real-world mission feasibility.

## 7. Troubleshooting

| Problem | What to check |
| --- | --- |
| `node` not found | Install Node.js, then reopen your terminal. |
| Port already in use | Stop the other process or choose a different launcher port. |
| Blank/limited 3D | Enable browser hardware acceleration, update the browser/GPU driver, and allow cdnjs access. The game includes a text fallback. |
| No sound | Click inside the game, check Sound/mute settings and browser volume. Background tabs may pause audio. |
| Online request fails / 502 | Start the API, check `/api/healthz`, and use the correct API port in the launcher command. |
| Room not found | Confirm both players use the same running server and exact code; expired rooms cannot be restored. |
| Timer expired | Confirm Restart selections; the online host must do this for the crew. |
| Reward not unlocked | Check full success, not just partial success; a previously earned reward may not reveal again. |
| Saves appear missing | Use the same browser profile and address/port. Check whether site data was cleared. |
| Native dependency install errors | Use Linux x64/WSL2 for the full workspace; use the dependency-free launcher for quick play on other platforms. |
| `PORT` / `BASE_PATH` required | Supply both variables for the Vite commands below. |

## 8. Developer setup

The quick launcher serves the game directly. The main application also has a React/Vite wrapper.

After `pnpm install --frozen-lockfile`, run the wrapper on Linux/WSL2:

```sh
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/mission-forge run dev
```

Open http://localhost:5173. **This Vite configuration does not proxy the online API locally.** Use the quick launcher plus API for local co-op, or configure a same-origin `/api/` reverse proxy.

Build the frontend:

```sh
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/mission-forge run build
```

The frontend output is `artifacts/mission-forge/dist/public`. A frontend build alone does not host online rooms; the API remains a separate process.

To open the editable seven-slide presentation source:

```sh
PORT=5174 BASE_PATH=/ pnpm --filter @workspace/mission-forge-presentation run dev
```

Open http://localhost:5174/slide1.

Do not commit secrets, `.env` files, `node_modules`, or generated build output. Back up changes before updating from GitHub; do not force-push over teammates' work.

## 9. Data, references, and tools

### Where the numbers come from

- [Imported workbook data](artifacts/mission-forge/public/data/mission-workbook.json): normalized data and recorded source information from the supplied Mission Forge workbook.
- [Core mission engine notes](docs/core-mission-engine.md): scientific scope, checks, and limitations.
- [Co-op documentation](docs/cooperative-play.md): roles, timing, and session behavior.

To audit a value, find its workbook row/source, open the cited reference, check units and context, then compare it with the implemented rule. A NASA instrument specification is not automatically a NASA-approved rocket capacity, mission budget, or score. Launch estimates from secondary sources must remain labelled as such. Missing data must remain unknown rather than be presented as verified.

The game has unresolved scientific constraints, including some missing instrument demand/destination capacity values and lunar insertion checks. A teaching run does not resolve those engineering gaps.

### Resources and tools used

- [NASA](https://www.nasa.gov/) and the specific references recorded in the workbook: space/instrument background and specifications.
- [NASA Space Apps Challenge](https://www.spaceappschallenge.org/): challenge context and educational motivation.
- [GitHub repository](https://github.com/MahmoudFarah003/spaceforge): source collaboration and version history.
- [Replit](https://replit.com/): development workspace.
- [Three.js](https://threejs.org/) / [cdnjs](https://cdnjs.com/libraries/three.js): browser 3D rendering and delivery of the game's Three.js runtime.
- [React](https://react.dev/), [Vite](https://vite.dev/), and [TypeScript](https://www.typescriptlang.org/): application/development tooling.
- [Node.js](https://nodejs.org/), [Express](https://expressjs.com/), and [pnpm](https://pnpm.io/): backend and workspace tooling.
- Browser Web Audio API: synthesized background music and effects.
- Playwright, Python/python-docx, LibreOffice, and FFmpeg: demo capture, editable reports, and document/video preparation.

Links to an organization are not claims of endorsement. Source entries reflect the supplied workbook; they should be reviewed before making scientific claims.

## 10. Project files

```text
artifacts/mission-forge/                React/Vite wrapper and game
  public/mission-forge.html             Main game
  public/data/mission-workbook.json     Imported data and sources
  public/coop.js                        Co-op client
  public/selection-timer.js             Selection-round controls
  tests/                               Game and persistence checks
artifacts/api-server/                   Online co-op API
artifacts/mission-forge-presentation/    Editable seven-slide deck
docs/                                  Engine and co-op explanations
scripts/play-local.mjs                  Dependency-free demo launcher
scripts/                               Data checks and documentation tools
lib/                                   Shared workspace libraries
```

Large generated MP4/PPTX/DOCX files and temporary recordings are excluded from Git history under `generated-artifacts/` and `.local/`. The editable slide source and documentation-generation scripts are included; the previously exported downloads are separate deliverables, not files automatically shipped by cloning this repository.
