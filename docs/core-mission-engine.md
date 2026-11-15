# Mohammad — Core Mission Engine (Task 03)

Branch: `mohammad/core-mission-engine`. Base: `5e2a2c8`.

This change extends the existing workbook-backed game. It does not replace the game, change its science/reward balance, or merge into main.

## What changed

- Added `artifacts/mission-forge/public/mission-engine.js`, a pure calculation module shared by the browser adapter and tests. It does not change inputs or depend on graphics, timers, network requests, or the DOM.
- Mass now exposes the bus, instrument payload, power system, communications, total model mass, destination capacity, and result. Published launch capacities do not use an orbit mass multiplier or a level payload penalty. The existing fictional GEO model remains explicitly educational; GTO is never substituted for GEO.
- Power now exposes instrument load, bus load, communications, total demand, output, required reserve in W, total demand including reserve, and spare output. Reserve is `demand × level.powerReserve`; the existing margin remains `(output − demand) / output`. These are power calculations, not battery energy or endurance calculations.
- Budget exposes the known subtotal, number of unavailable cost entries, total cost, remaining budget, and result. Missing prices keep total and remaining budget unavailable. A known subtotal above the cap fails immediately. Actual zero prices remain distinct from missing prices.
- Go/No-Go now returns `GO`, `NO_GO`, or `UNRESOLVED`. Definite failures take priority over missing data. Missing capacity or electrical demand blocks starting the game; missing instrument prices retain the existing explicitly labeled teaching-run behavior.
- Lunar checks separately report Earth launch using LEO capacity, TLI using TLI capacity, and lunar orbit insertion. The workbook's approximate 3.2 km/s TLI and 0.9 km/s LOI references retain their confidence and source metadata. Neither value is treated as a measured spacecraft capability.
- The English and Arabic report now shows the breakdowns, reserve, overall readiness, separate lunar stages, and limitations. A lunar teaching run never reports that insertion has passed.
- Added boundary and missing-data assertions to the existing regression test, an application `test` command, and updated the existing browser-check expectations for the revised launch label.

## Sources and scope

The proposal and all 13 workbook tabs were read before implementation. The attached workbook and repository workbook have the same SHA-256:

`9608231cc6b9ca987152be1933ee940cab67b6c75025821e1d00e193be13bce8`

No external scientific source or new hardware number was added. The imported workbook data and original attachments are unchanged.

| Calculation | Workbook location | Treatment |
| --- | --- | --- |
| Launch capacities | `2_Launch_Vehicles`, rows 4–9 | Per destination; blanks remain unknown; medium confidence |
| Lunar instrument mass and power | `3_Moon_Instruments`, rows 4–10 | Individual instrument values; LROC + LOLA = 30.5 kg / 57.4 W |
| Mars instrument mass and power | `4_Mars_Instruments`, rows 4–9 | SHARAD electrical demand remains unknown; 10 W RF is not electrical input |
| TLI / LOI reference requirements | `5_Orbits_Transfers`, rows 5–6 | Approximate, medium confidence; not propulsion capability |
| Instrument costs | Workbook README and blank imported costs | Unavailable; never silently zero |

Bus, power-source and communications specifications, level power reserve fractions, budget caps, science, risk, event timing and the legacy GEO model remain existing teaching settings. The workbook's CubeSat budget-reserve guidance is distinct from a power reserve and has not been imposed across unrelated levels.

## API and meaning of readiness

`MissionEngine.resources(design, level, bus, parts, solarFactor)` returns `{mass, power, budget}`. Missing, non-finite, negative or nonnumeric resource specifications produce an unresolved total rather than being coerced into a number.

`MissionEngine.lunarStages(design, mass, parts, workbook)` returns `{launch, tli, insertion}` for Moon designs, otherwise `null`. Insertion is unresolved because the workbook supplies no spacecraft propulsion/propellant capability. Spacecraft model mass does not claim to include engineered propellant, adapters or integration margins.

`evaluateDesign()` retains its existing fields and adds `budgetDetails`, `stages`, `readiness` and `verifiedGo`. `canLaunch` means the educational game may start. `verifiedGo` means all implemented model checks returned Go; it is never a real flight-readiness certification. For a lunar design, `canLaunch` may be true while `readiness` is unresolved and `verifiedGo` is false. New callers must use the appropriate field rather than equating a playable simulation with complete readiness.

Example, Level 3 with LROC, LOLA, Falcon 9, solar panels, high-gain communications and lunar orbit:

- Instrument payload: 30.5 kg and 57.4 W.
- Model mass: 490.5 kg. Falcon 9 workbook limits: 22,800 kg LEO and 3,500 kg TLI.
- Demand: 147.4 W; 10% reserve: 14.74 W; required with reserve: 162.14 W; modeled output: 300 W.
- Known cost subtotal: $160M. Full cost and remaining budget: unavailable because both instrument prices are missing.
- Earth launch and TLI: Go in the model. LOI and overall readiness: unresolved. Educational run remains available.

## Validation and review

Run from the repository root:

```sh
node artifacts/mission-forge/tests/levels.test.cjs
```

The suite exercises 100 deterministic mission runs per level (500 total), reward progression, abort/failure behavior, bilingual screen generation, destination constraints, LROC/LOLA removal, missing SHARAD power and missing capacities. Added checks cover exact mass/power sums, reserve boundaries, zero and missing capacities, invalid mass data, known/unknown/zero costs, over-budget known subtotals, immutability, unresolved readiness, separate LEO/TLI/LOI and English/Arabic report content.

Baseline and updated gameplay score ranges and success counts matched. A local browser check confirmed the complete Earth design, enabled launch button, and English/Arabic resource report layout. Lunar calculations and bilingual lunar report content were verified in the automated suite. The existing Replit-specific Chromium script was updated but was not run locally. No full monorepo dependency installation/build was performed; this change targets the portable HTML game and its scripts.

## Review and merge

Review this branch against `main`. Merge it yourself after review. The change does not alter server, database, React host, presentation, source workbook, generated workbook data, mission events or reward definitions.
