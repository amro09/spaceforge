# Mission Forge Project Map

## Scope and Runtime Truth

This repository is a pnpm monorepo. The interactive game users currently play is a standalone vanilla-JavaScript game in `artifacts/mission-forge/public/mission-forge.html`. The Vite/React host in `artifacts/mission-forge/src` renders that file in a full-screen iframe (`App.tsx`); the host's React `Station` page and its React mission/scoring libraries are a separate implementation and are not the current embedded game's source of truth.

The standalone game consists of the HTML document (including its CSS, data, translations, renderers, state machine, and Three.js scene code), `public/mission-engine.js` (pure resource calculations), `public/workbook-adapter.js` (merges imported workbook values and reports), and `public/data/mission-workbook.js` (imported data). `mission-workbook.json` is the readable source-data export. Three.js r128 is loaded from cdnjs; without it or WebGL the game provides text fallbacks.

## Repository Inventory

The lists below cover the workspace files and directories, excluding `.git`, installed `node_modules`, and generated build output. `components/ui` entries are individual reusable shadcn/Radix-style components; the `mission-forge` and `mockup-sandbox` lists intentionally show their copies separately.

### Root

- `.git/` — version-control metadata (not application source; excluded from the recursive inventory).
- `.gitignore` — Git ignore rules.
- `.npmrc` — pnpm package age policy, workspace package overrides and build/install policy; keep the minimum release-age protection intact.
- `.replit`, `.replitignore` — Replit run and ignore configuration.
- `package.json` — root scripts and shared TypeScript/Prettier dependencies.
- `pnpm-lock.yaml` — locked dependency graph for pnpm.
- `pnpm-workspace.yaml` — workspace package globs, shared dependency catalog and overrides.
- `pyproject.toml`, `uv.lock` — Python scripts' environment/dependency metadata and lock.
- `replit.md` — workspace run/operate notes (currently mostly starter-template placeholders).
- `tsconfig.json`, `tsconfig.base.json` — root TypeScript project references and shared compiler options.
- `PROJECT_MAP.md` — this document.
- `artifacts/` — runnable application artifacts.
- `attached_assets/` — supplied source material.
- `docs/` — engineering notes and decisions.
- `lib/` — shared API, generated client/schema and database packages.
- `scripts/` — workbook import, browser checks, capture and document-generation scripts.

### `artifacts/api-server/`

Small Express API package, separate from the current browser game's gameplay.

- `.replit-artifact/artifact.toml` — Replit artifact metadata.
- `build.mjs` — server build/bundle script.
- `package.json`, `tsconfig.json` — package dependencies/scripts and compiler settings.
- `src/app.ts` — Express middleware and `/api` router setup.
- `src/index.ts` — requires `PORT` and starts the server.
- `src/lib/logger.ts` — shared server logger.
- `src/lib/.gitkeep`, `src/middlewares/.gitkeep` — retain otherwise empty source directories.
- `src/routes/index.ts` — API route aggregation.
- `src/routes/health.ts` — health endpoint.
- `src/middlewares/` — reserved middleware directory; no implementation files currently.

### `artifacts/mission-forge/`

The Vite package serving the live game iframe, plus a parallel React implementation.

- `.replit-artifact/artifact.toml` — artifact metadata.
- `components.json` — shadcn component generator configuration.
- `index.html` — Vite/React host document and metadata, not the game's internal HTML.
- `package.json`, `tsconfig.json`, `vite.config.ts` — package scripts/dependencies, TS settings, host/build config.
- `public/favicon.svg` — app icon.
- `public/robots.txt` — crawler policy.
- `public/mission-forge.html` — **live game**: complete single-document UI, CSS, game data, translations, screen renderers, timers, event simulation, results and 3D scene.
- `public/mission-engine.js` — pure mission resource calculation module used by the live page and tests.
- `public/workbook-adapter.js` — injects workbook-backed parts and level budgets, adjusts validation and supplies source/readiness/timeline/results reports.
- `public/data/mission-workbook.js` — workbook data published as `window.MISSION_WORKBOOK` for the browser.
- `public/data/mission-workbook.json` — JSON export of workbook tables, source notes and qualifiers.
- `src/main.tsx` — React root and error-boundary mount.
- `src/App.tsx` — full-viewport iframe wrapper loading `public/mission-forge.html`.
- `src/index.css` — Tailwind v4/shadcn theme and utilities for the React implementation; it does not style the HTML inside the iframe.
- `src/pages/station.tsx` — large, separate React mission station with its own phases and UI.
- `src/pages/not-found.tsx` — React not-found screen.
- `src/lib/mission.ts` — separate React implementation's options, config and design evaluation/scoring.
- `src/lib/operations.ts` — separate React implementation's operations events, score, XP/levels and rewards.
- `src/lib/storage.ts` — localStorage persistence/sanitization used by the React station, not the active HTML game's in-memory progress.
- `src/lib/utils.ts` — class-name utility.
- `src/components/scene.tsx` — React Three Fiber scene for the React station.
- `src/components/rewards.tsx` — React station rewards dialog/cards/level bar.
- `src/components/reward-preview.tsx` — reward preview model/content.
- `src/components/error-boundary.tsx` — React error boundary.
- `src/hooks/use-mobile.tsx`, `src/hooks/use-toast.ts` — React mobile and toast hooks.
- `src/components/ui/` — reusable UI component wrappers, all separate files: `accordion.tsx`, `alert-dialog.tsx`, `alert.tsx`, `aspect-ratio.tsx`, `avatar.tsx`, `badge.tsx`, `breadcrumb.tsx`, `button-group.tsx`, `button.tsx`, `calendar.tsx`, `card.tsx`, `carousel.tsx`, `chart.tsx`, `checkbox.tsx`, `collapsible.tsx`, `command.tsx`, `context-menu.tsx`, `dialog.tsx`, `drawer.tsx`, `dropdown-menu.tsx`, `empty.tsx`, `field.tsx`, `form.tsx`, `hover-card.tsx`, `input-group.tsx`, `input-otp.tsx`, `input.tsx`, `item.tsx`, `kbd.tsx`, `label.tsx`, `menubar.tsx`, `navigation-menu.tsx`, `pagination.tsx`, `popover.tsx`, `progress.tsx`, `radio-group.tsx`, `resizable.tsx`, `scroll-area.tsx`, `select.tsx`, `separator.tsx`, `sheet.tsx`, `sidebar.tsx`, `skeleton.tsx`, `slider.tsx`, `sonner.tsx`, `spinner.tsx`, `switch.tsx`, `table.tsx`, `tabs.tsx`, `textarea.tsx`, `toast.tsx`, `toaster.tsx`, `toggle-group.tsx`, `toggle.tsx`, `tooltip.tsx`.
- `tests/levels.test.cjs` — Node regression suite that executes the inline game source and tests levels, events, scoring, localization, workbook-backed calculations and edge cases.

### `artifacts/mission-forge-presentation/`

Separate slide deck/editor artifact that presents the project; it is not the game UI.

- `.replit-artifact/artifact.toml` — artifact metadata.
- `index.html`, `package.json`, `tsconfig.json`, `vite.config.ts` — web entry, package scripts/dependencies, TS and Vite configuration.
- `public/favicon.svg` — presentation icon.
- `public/screenshots/` — screenshots used by slides: `01-menu.jpg`, `02-levels.jpg`, `03-tutorial.jpg`, `04-design-level1.jpg`, `05-validation.jpg`, `06-launch.jpg`, `07-mission.jpg`, `08-event.jpg`, `09-consequence.jpg`, `10-results-level1.jpg`, `11-reward-launch-suit.jpg`, `12-collection.jpg`, `13-design-level2.jpg`, `14-results-level2.jpg`, `15-reward-apollo.jpg`, `16-mobile.jpg`, `level-3-planned.jpg`, `level-4-planned.jpg`, `level-5-planned.jpg`.
- `src/main.tsx`, `src/App.tsx`, `src/index.css` — slide app mount, navigation/editor shell and styling. `App.tsx` contains an explicit platform contract; avoid restructuring its slide/router contract casually.
- `src/slideLoader.ts` — resolves the manifest to slide components or SDM documents.
- `src/data/slides-manifest.json` — slide order, metadata and source paths.
- `src/pages/slides/` — individual authored slides: `Design.tsx`, `Introduction.tsx`, `Learning.tsx`, `Levels.tsx`, `Manage.tsx`, `Problem.tsx`, `Resources.tsx`, `Results.tsx`, `Rewards.tsx`, `Solution.tsx`.
- `src/widgets/ImportedChart.tsx` — chart widget used by the presentation.
- `src/.sdm/` — slide-document-model editor/runtime implementation: `editingState.ts`, `fileDragGuard.ts`, `fontCss.ts`, `geometry.ts`, `motion.ts`, `render.tsx`, `sdm.schema.yaml`, `SdmInteractionLayer.tsx`, `sdmRuntime.ts`, `SdmSlide.tsx`, `SdmTextEditor.tsx`, `sdmVitePlugin.ts`, `selectionGestures.ts`, `session.ts`, `shapePaths.ts`, `snapping.ts`, `style.ts`, `textAutofit.ts`, `textColorGestures.ts`.
- `src/.sdm/core/` — shared SDM schema/serialization/operations: `fonts.ts`, `layoutValidation.ts`, `motion.ts`, `operations.ts`, `protocol.ts`, `schema.ts`, `selectionGeometry.ts`, `serialization.ts`, `slidesManifest.ts`.
- `src/.sdm/core/text/` — ProseMirror-backed text editing helpers: `formattingContinuity.ts`, `index.ts`, `inlineStyles.ts`, `inputRules.ts`, `listStyles.ts`, `paragraphMarkers.ts`, `pmCommands.ts`, `pmDoc.ts`, `pmSchema.ts`, `selectionFormatting.ts`, `styleUtils.ts`.
- `scripts/sdmRepair.ts`, `scripts/sdmValidation.ts`, `scripts/validate-slides.ts` — SDM repair, validation and slide-manifest validation scripts.
- `src/data/slides/` — intended SDM YAML document directory; currently no tracked YAML document is present in the workspace inventory.

### `artifacts/mockup-sandbox/`

Separate Vite component-preview utility, not a Mission Forge runtime dependency.

- `.replit-artifact/artifact.toml` — artifact metadata.
- `components.json`, `index.html`, `package.json`, `tsconfig.json`, `vite.config.ts` — preview UI config and project setup.
- `mockupPreviewPlugin.ts` — Vite preview plugin.
- `src/main.tsx`, `src/App.tsx`, `src/index.css` — React mount, dynamically discovered component preview/gallery and preview styles.
- `src/.generated/mockup-components.ts` — generated preview module registry.
- `src/hooks/use-mobile.tsx`, `src/hooks/use-toast.ts`, `src/lib/utils.ts` — shared hooks and class-name utility.
- `src/components/mockups/` — intended user mockup components; currently no files are present.
- `src/components/ui/` — component wrappers, individual files: `accordion.tsx`, `alert-dialog.tsx`, `alert.tsx`, `aspect-ratio.tsx`, `avatar.tsx`, `badge.tsx`, `breadcrumb.tsx`, `button-group.tsx`, `button.tsx`, `calendar.tsx`, `card.tsx`, `carousel.tsx`, `chart.tsx`, `checkbox.tsx`, `collapsible.tsx`, `command.tsx`, `context-menu.tsx`, `dialog.tsx`, `drawer.tsx`, `dropdown-menu.tsx`, `empty.tsx`, `field.tsx`, `form.tsx`, `hover-card.tsx`, `input-group.tsx`, `input-otp.tsx`, `input.tsx`, `item.tsx`, `kbd.tsx`, `label.tsx`, `menubar.tsx`, `navigation-menu.tsx`, `pagination.tsx`, `popover.tsx`, `progress.tsx`, `radio-group.tsx`, `resizable.tsx`, `scroll-area.tsx`, `select.tsx`, `separator.tsx`, `sheet.tsx`, `sidebar.tsx`, `skeleton.tsx`, `slider.tsx`, `sonner.tsx`, `spinner.tsx`, `switch.tsx`, `table.tsx`, `tabs.tsx`, `textarea.tsx`, `toast.tsx`, `toaster.tsx`, `toggle-group.tsx`, `toggle.tsx`, `tooltip.tsx`.

### `lib/`

- `lib/api-client-react/package.json`, `tsconfig.json` — generated React API client package setup.
- `lib/api-client-react/src/index.ts` — exports generated API hooks/schemas and fetch configuration.
- `lib/api-client-react/src/custom-fetch.ts` — API fetch/base URL/auth-token helpers.
- `lib/api-client-react/src/generated/api.ts`, `api.schemas.ts` — generated client functions and schemas.
- `lib/api-spec/package.json`, `orval.config.ts` — OpenAPI package and Orval code-generation config.
- `lib/api-spec/openapi.yaml` — API contract; currently only health-check route.
- `lib/api-zod/package.json`, `tsconfig.json` — generated Zod/types package config.
- `lib/api-zod/src/index.ts` — generated API/types exports.
- `lib/api-zod/src/generated/api.ts` — generated Zod API schemas.
- `lib/api-zod/src/generated/types/index.ts`, `healthStatus.ts` — generated response types.
- `lib/db/package.json`, `tsconfig.json`, `drizzle.config.ts` — database package scripts, TS and Drizzle config.
- `lib/db/src/index.ts` — creates PostgreSQL pool/Drizzle instance; requires `DATABASE_URL`.
- `lib/db/src/schema/index.ts` — schema barrel/starter placeholder; no concrete tables currently defined.
- `lib/integrations/` — included by workspace globs; no tracked files currently present.

### `scripts/`

- `package.json`, `tsconfig.json` — TypeScript scripts package setup.
- `post-merge.sh` — post-merge helper.
- `src/hello.ts` — starter/sample TypeScript script.
- `add_mission_references.py` — append an editable references page to an existing report.
- `build_mission_proposal_ar.py` — produce an Arabic proposal document with app screenshots and RTL layout.
- `build_mission_report.py` — build an editable Word guide from reviewed game data/screenshots.
- `capture_mission_guide.py` — capture English gameplay for the presentation and guide.
- `check_workbook_game.py` — exercise workbook-backed game flow in Chromium using Playwright.
- `import_mission_workbook.py` — repeatable XLSX-to-JSON/browser-data import; preserves missing values.

### `attached_assets/` and `docs/`

- `attached_assets/Mission_Forge_Data_Pack_1794689600166.xlsx` — supplied workbook used as the source for imported hardware/reference data.
- `docs/core-mission-engine.md` — engineering note for the pure resource engine, workbook assumptions, readiness semantics, validation and scope.

## Screen Flow and Render Ownership

The active app screen is a state value, not a URL route. `go(screen)` clears timers/dialogs, changes the 3D scene, and calls the global `render()`. `render()` updates document language/direction, rebuilds the top bar and invokes `SCREENS[state.screen]()`.

1. **Home/menu:** `SCREENS.menu()` in `public/mission-forge.html`. Starts planning, opens collection, or opens the how-to dialog.
2. **Level select:** `SCREENS.levels()`. Five cards; `levelStatus()` and `state.progress` determine readiness/locks. A successful or partial prior level unlocks the next.
3. **Spacecraft design and instrument selection:** `SCREENS.design()`. The left panel is sectioned mission, goal, instruments, rocket, power, communications and orbit selection. Instruments are multi-select up to the level cap; workbook data determines Moon/Mars instruments. The middle area shows the Three.js assembly or text schematic. The right panel shows six live gauges, validation messages, the embedded Go/No-Go report and launch control.
4. **Go/No-Go:** not a separate screen. It is the validation/report section of `SCREENS.design()`, combining `evaluateDesign()` with `window.workbookGoNoGo()` from `workbook-adapter.js`. It distinguishes game-allowed launch (`canLaunch`) from readiness (`GO`, `NO_GO`, `UNRESOLVED`); a teaching run may be playable with unresolved real-data checks.
5. **Launch:** `startLaunch()` switches to `SCREENS.launch()` for a roughly 7.6-second cinematic/countdown; `skipLaunch` bypasses to the mission. `setScene()`/`buildLaunchScene()` provide the 3D visual, with a staged text fallback.
6. **Mission Control/HUD:** `startMission()` initializes a live simulation and `SCREENS.mission()` renders six gauges, segment timeline, optional workbook timeline, event/decision log and abort control. `updateHud()` updates values without rebuilding the screen. Events appear in dialogs over the HUD and pause the clock.
7. **Mission Results/Debrief:** `finishMission()` computes outcome/score/progression and navigates to `SCREENS.results()`, which shows the score breakdown, takeaways, unlock/next-level state, optional workbook comparison, retry/redesign/level navigation and reward claim.
8. **Collection:** `SCREENS.collection()` is a separate navigable screen; `renderDialog()` shows how-to, event, consequence, abort and reward-card dialogs. Rewards can be inspected/equipped cosmetically.

The React `src/pages/station.tsx` has its own station screen with design/countdown/ascent/orbit/operations/debrief states, but it does not render inside `App.tsx`'s iframe flow. Its `src/lib/mission.ts`, `operations.ts`, `storage.ts`, `components/scene.tsx` are therefore a second, currently separate game implementation.

## State, Rules, Levels, Parts and Events

### Active game state

`state` in the inline script of `public/mission-forge.html` owns the current screen/language/level/design, progress map, reward collection/equipment, tutorial flags, active mission, latest result, dialog, launch timer and interval IDs. It is in memory only. There is no save/load path for active-game progress: reload/close resets levels and collection, and the UI explicitly tells the player this. The React alternative uses browser `localStorage` in `src/lib/storage.ts`, but this is not active game persistence.

The active simulation ticks every 100 ms with `dt = 0.1`. It updates power, communication, risk, science data collection and downlink; one event is offered at about 45% through each timed segment. Abort is a distinct result and grants no progress/reward. Full success grants that level's cosmetic reward; partial or full success unlocks the next level.

### Levels and parts

- `LEVELS` in the inline data section defines five playable experiences: Earth Levels 1–2, Moon Levels 3 and 5, Mars Level 4. Each record controls budget, payload factor, power reserve, instrument cap, science target, number/duration of segments, event severity, reward and tutorial.
- `MISSIONS` maps destination to allowed goals/orbits, first level, solar output factor, downlink rate and event pool; Moon/Mars add a guaranteed signature event.
- `GOALS` maps a science goal to fitting instruments and preferred orbit.
- `BUS`, `PARTS` and `EVENTS` define the always-included spacecraft bus, legacy teaching instruments/rockets/power/comms/orbits and event weights/effects.
- `workbook-adapter.js` merges workbook instruments/rockets into `PARTS`, updates level budget values from workbook levels, defines valid destination part lists and provides source/unknown-data notes. `mission-workbook.js` is generated from the attached XLSX via `scripts/import_mission_workbook.py`; JSON counterpart contains the broader workbook sheets and sources. Missing prices/specifications are intentionally represented as unavailable, not zero.
- `REWARDS` lists visual models and level unlock thresholds; it does not affect calculation inputs.

### Calculations and scoring

The active legacy calculation functions are `calculateBudget`, `calculateMass`, `powerOutput`, `calculatePower`, `calculateComms`, `calculateRisk`, `calculateScience` and `evaluateDesign` in the inline script. Workbook adapter wraps/replaces selected calculations with `MissionEngine.resources()` in `public/mission-engine.js`, preserving missing values and separating launch-to-LEO, TLI and unresolved lunar orbit insertion. `docs/core-mission-engine.md` explains the semantics and intentional modeling limits.

Pre-launch checks include all selected part costs against level budget, dry mass against destination rocket capacity (legacy teaching orbit multiplier remains only for legacy parts), instrument/bus/comms power plus reserve versus output, and communication/science/risk advisories. Goal/instrument/orbit fit affect science and risk. Calculations are deterministic for a fixed design.

Post-launch final score is a weighted 100-point sum, rounded to integer:

- science collected: up to 35 points, normalized against expected collection;
- returned data: up to 30 points, based on the fraction of collected data transmitted;
- remaining power: up to 15 points;
- managed risk: up to 20 points, inverse of final risk.

At 70+ the outcome is full success; at 45–69, partial; below 45, failure. Power depletion or risk reaching 100 also forces failure and caps score at 40. Abort scores zero and earns no unlock/reward. Takeaways are selected from weak communications/power, high risk, bad orbit/goal fit, then general balance/events.

### Random events

`pickEvent()` selects an unused event from the mission pool using a weighted random draw. Weights depend on design properties (e.g. battery, power margin, orbit, antenna and rocket reliability), and event severity scales harmful option deltas. Moon/Mars signature events are forced first (`lunarShadow`/`marsDelay`). Each event pauses the simulation and presents three choices; `chooseOption()` applies the choice's power/comms/science/risk/data/returned deltas, with severity scaling harmful changes, and shows a consequence dialog. The event is marked used so it is not repeated until the pool is exhausted. This makes resource math deterministic while event sequences are random; the regression suite seeds `Math.random` for reproducibility.

## English/Arabic Localization

- The active dictionary is the large inline `I18N` object in `public/mission-forge.html`, with parallel `en` and `ar` keys for screens, labels, descriptions, validation, events, results, tutorials and rewards.
- `t(key, vars)` looks up the current language, falls back to English, then to the key itself, and interpolates `{name}` placeholders.
- The top-bar language control dispatches `ACTIONS.lang`; it flips `state.lang` and rerenders. Language is not persisted across reloads (state starts at `en`).
- Each render sets `document.documentElement.lang` to `en` or `ar` and `dir` to `ltr` or `rtl`; the button's `lang` attribute describes the language it switches to.
- Workbook data may provide part names/descriptions in English only; the adapter copies these into both dictionaries at runtime, while its explanatory/report text uses explicit English/Arabic pairs. Thus not every workbook-sourced dynamic string is necessarily translated.
- Not every displayed fragment is dictionary-driven: some markup/labels, tooltips, camera aria-labels, inline language ternaries and fallback punctuation remain literal. New user-visible strings should be added in both dictionary branches and verified in both languages.
- The React alternative has no equivalent complete EN/AR interface/language switch; do not infer its localization from the active standalone page.

## CSS Organization and Directionality

The active game's CSS is an inline `<style>` block near the start of `public/mission-forge.html`, split by comments into top bar, menu, levels, design, launch, mission HUD, dialogs, results and collection. Root custom properties define the dark navy surface, panel/line/text colors, amber/teal/coral status colors, font stacks and common radius. Layout is primarily flex/grid; animation uses `rise` and `flash`; a reduced-motion media query disables animations/transitions.

Responsive rules are mainly one `@media (max-width: 900px)` block: the three-column design becomes a vertical stack, the 3D view moves above the panels, the HUD changes from six to three columns, results/reward layouts stack, and menu/launch get minimum height. There is no separate narrow-phone breakpoint. HTML has viewport-fit metadata and the UI scrolls on mobile.

Logical properties are used in many RTL-sensitive places (`inset-inline-*`, `padding-inline-*`, `border-inline-start`, `text-align:start`, `inset-inline`, `padding-inline-start`) and specific RTL rules suppress Latin tracking and reverse timeline transform origin. Physical-direction leftovers include checkmark `left:4px`, left-origin gauge bars, physical left/right in camera/tooltip positioning and translateX centering overrides. Some physical values are intentional for visual coordinates, but they deserve RTL review rather than blind replacement.

`src/index.css` is a separate Tailwind v4/shadcn stylesheet for the React host/alternative station. It defines light theme tokens (and a `.dark` block that currently repeats the light values), fonts/radius, and generated utility layers. It does not cascade into the iframe document.

## Risks and Existing Issues to Respect

### Code that is easy to break

- The actual play path is the iframe URL in `src/App.tsx` plus the public HTML's relative script URLs. Moving/renaming the HTML or its `data/` and JS siblings breaks gameplay even if React compiles.
- Script load order matters: workbook data, core engine, workbook adapter, then the inline game. The adapter monkey-patches/wraps calculations and actions after the core definitions; preserve these boundaries and re-run the game test after edits.
- The inline HTML script intentionally has access to global lexical declarations used by the adapter and VM test. Converting it to modules or changing globals affects both runtime and tests.
- Keep `MissionEngine` pure and maintain its distinction between missing, zero, game-playable and verified readiness. In particular, do not claim lunar orbit insertion is verified without propulsion/propellant inputs.
- `I18N` key parity, dynamically added workbook translations and RTL direction updates are regression-sensitive. `tests/levels.test.cjs` checks dictionary keys, event strings, both-language screen generation and numeric edge cases.
- The slide deck's `src/App.tsx` has an explicit platform contract and `src/slideLoader.ts` expects manifest/file consistency; avoid casually restructuring the presentation app.
- Root `.npmrc` includes an intentional one-day minimum package release age for supply-chain defense.

### Duplication and source-of-truth hazards

- The React station (`pages/station.tsx` + `lib/mission.ts`/`operations.ts`/`storage.ts`) duplicates a substantial game model, but the live app embeds the standalone HTML. Features/fixes placed only in React will not change the current gameplay.
- Game styles, dictionaries, level/part/event data and most UI logic are all concentrated inside one 1,700+ line HTML file, while calculation/data adaptation is split across two JS files and two workbook exports. The single-file approach is portable but easy to desynchronize.
- `public/data/mission-workbook.js` and `.json` are generated representations of the attached workbook; update/regenerate them through the importer, not by editing only one copy.
- Both the game and mockup sandbox contain a large near-identical generated `components/ui` set. Treat these as generated/shared-pattern copies, not evidence that the game uses those components.
- Documentation, screenshots, project pitch copy and presentation slides can also repeat the game's claims; verify all copies if gameplay scope or model semantics change.

### Hardcoded text and model caveats

- The active UI has some English literals outside the translation dictionary (including accessibility labels and a few render/adapter strings). The dictionary's “every visible string” comment is an intent, not a guarantee.
- Workbook-provided source names/notes and part descriptions are injected without a full Arabic translation; adapter strings use a local two-language helper separate from `t()`.
- Legacy Earth model values and many budget/science/risk/event/power/comms settings are educational proposals; actual Moon/Mars hardware inputs are incomplete. Instrument prices are missing, some electrical demand/capacity data is unavailable, published rocket figures have qualifiers, and a lunar insertion requirement is not spacecraft capability.
- Browser game state is intentionally not saved. Reloading abandons a run and erases in-memory level/reward progress; the separate React localStorage implementation can mislead developers into expecting persistence.

### Layout/accessibility concerns visible in source

- At widths up to 900px the main three-column design becomes a long vertical page. Fixed/viewport-height areas, top bar wrapping, lengthy Arabic labels and the event/reward dialogs need narrow-screen testing, especially around 320px and browser zoom.
- The same mobile rule sets `body` overflow hidden while enabling scrolling on `#ui`; verify that keyboard focus, dialog focus trapping and nested scroll areas remain reachable on touch and keyboard.
- Six mission HUD gauges become three columns but still include labels, values and tooltip buttons; this can be tight on small phones and Arabic text.
- Some non-translated accessibility text and physical-direction styles can make an otherwise translated RTL screen read or align inconsistently.
- Camera controls use English-only aria labels; 3D errors and external Three.js CDN failure are handled, but the live game still depends on network access for the CDN unless its load fails gracefully.
- The app has no separate Go/No-Go route/screen; the readiness report is embedded below the design gauges. Be explicit about this when discussing flows or implementing a requested screen.

## Verification Performed

Read-only review only, except for adding this requested document. Ran `node artifacts/mission-forge/tests/levels.test.cjs`: it passed. Output included 100 runs per level (500 total), core-engine boundary checks, localized screen/event checks, constraints, abort/failure and reward progression. No application source or configuration was changed for this map.