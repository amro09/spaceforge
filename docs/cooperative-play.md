# Cooperative Mission Forge

## Start a crew mission

1. On the home screen choose **Play with a crew · 2–4 players**.
2. Choose **Shared screen**, **Create online room**, or **Join a crew**.
3. The host selects 2, 3, or 4 players, an implemented mission level, and its science goal.
4. For online play, share the same app URL and the six-character room code. Each participant enters their own name and joins.
5. Everyone presses **Toggle ready**. The host starts only after all selected seats are filled, connected, and ready.

## Crew responsibilities

| Crew size | Player 1 | Player 2 | Player 3 | Player 4 |
| --- | --- | --- | --- | --- |
| 2 | Power + communications | Instruments + rocket/orbit | — | — |
| 3 | Power + rocket/orbit | Instruments | Communications | — |
| 4 | Power | Instruments | Communications | Rocket/orbit |

The host chooses the mission and science problem, launches the mission, and continues after the crew has read an event's outcome. Mission-event decisions rotate through players by mission segment.

In shared-screen mode, use **Pass to next player** to hand over the design controls. During events, the game selects the responsible player's turn automatically. This is cooperative planning on one device, not split-screen flight control.

In online mode, the server checks membership and assigned controls. Every participant sees the host's synchronized mission. The host's browser runs the educational simulation; this is not a competitive, cheat-proof leaderboard. Keep the host tab open and active.

## Timed selections

Entering design starts a 90-second round. Online crews share the server's deadline; reloading a guest tab does not restart it. Shared-screen crews share one round across all stations.

The completion notice appears when a player's assigned fields are filled. Players can still adjust their choices until the host (or solo/shared-screen player) presses **Finish selections** with a launchable design. This stops the selection clock and locks the design for Go/No-Go review; it does not automatically launch.

If the timer expires before finishing, edits and launch are blocked. **Restart selections** asks for confirmation, clears the design, and starts a new 90-second round. Only the online host can restart. The mission's fixed host-selected science goal remains in co-op.

Low communication quality remains a learning trade-off, not an extra launch prohibition added by the review screen. Unknown mass/power/capacity and other existing blocking checks still apply.

## Session lifetime

- A disconnected crew pauses mission simulation until everyone reconnects.
- Refreshing an online tab reconnects the same participant using that tab's session.
- Leaving as host, or deliberately leaving an active mission, closes the room for everyone after confirmation. A disconnected participant can reconnect in the same tab session; replacements cannot take over a seat mid-flight.
- Rooms are temporary in the game server's memory. They expire after 30 minutes without requests and end if the server restarts.
- Completed progress and rewards save separately in each participant's browser. Clearing browser data removes those saves.
- Shared-screen participants share one browser collection.
- Cooperative training can begin at any implemented mission. This does not mean the workbook contains complete engineering data for every mission.

## Scientific scope

Cooperative play does not change workbook specifications or turn unresolved checks into verified approvals. Cost omissions, missing SHARAD electrical demand, missing destination capacities, and unresolved lunar insertion retain their existing meaning. Graphics are illustrative rather than flight dynamics predictions.

## Checks

- `pnpm --filter @workspace/mission-forge test`
- `node artifacts/mission-forge/tests/persistence.test.cjs`
- `node scripts/test-coop-api.mjs` (against the running development preview)

The room test creates and deletes isolated 2-, 3-, and 4-player rooms, checks permissions, capacity, readiness, assigned actions, snapshots, and duplicate event rejection.
