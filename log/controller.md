# Controller Log

Living record of the motor controller. Update it whenever hardware, firmware or configuration changes.
How to make a change is described in [docs/controller.md](../docs/controller.md#changing-the-configuration).
Entries before October 2026 were reconstructed from git history.

## Hardware

Fields marked "unknown" are worth filling in at the next opportunity. VESC Tool shows firmware and hardware versions on connect.

| Item | Value |
|---|---|
| Status | **Failed, replacement pending.** See [controller-replacement.md](../docs/controller-replacement.md) |
| Controller | Trampa VESC HD60T, dual, board marked "MK I" |
| Serial number | unknown |
| Hardware version | unknown |
| Firmware version | unknown, config format `ConfigVersion` 2 |
| Installed | 2026-04, approximate |
| CAN IDs | 22 master, 23 slave |
| Throttle input | ADC on ID 22 |
| BMS | JBD 12S Smart BMS, current rating unknown |
| Fuse | unknown |
| Anti-spark / power switch | unknown |

## Config history

Newest first. One line per change that was written to the controller.

| Date | Controller | Change | Commit |
|---|---|---|---|
| 2026-10-14 | HD60T | Controller failed from regen with the BMS charge input off. No config change. Checker now flags the 57 V overvoltage fault above the 52 V rating. | – |
| 2026-10-14 | – | Config files moved to `vesc/hd60t/` and `vesc/stormcore-60d/` and renamed by CAN ID. No setting changed. | – |
| 2026-04-18 | HD60T | First HD60T configs. Motor current 60 A, absolute 120 A, battery 30 A, regen -15 A, motor temp cut 80–100 °C. ID 22 setup info left at defaults. | `d1f867c` |
| 2026-04-18 | Stormcore | Last Stormcore update. Motor current 50 → 70 A, absolute 75 → 80 A, ID 22 app ADC → ADC + UART, throttle expo 0.75 → 0.25. | `d1f867c` |
| 2021-11-21 | Stormcore | Regen -15 → -12 A after tuning. | `5852052` |
| 2021-11-21 | Stormcore | Separate motor detection per controller. Motor current 30 → 50 A, absolute 175 → 75 A. | `ad81809` |
| 2021-11-17 | Stormcore | Absolute current 30 → 175 A, regen -12 → -15 A. Removed obsolete single-controller configs. | `26e94d6`, `ef81433` |
| 2021-11-15 | Stormcore | First per-controller configs for ID 22 and ID 23 from motor detection. Motor and battery current 30 A. | `f657a7f` |
| 2021-10-24 | Stormcore | Initial config draft with placeholder motor values. | `7608d3d` |

## Motor detection history

FOC detection results per controller. Compare new results with the last line for the same controller.
A resistance rise of more than about 20 % on the same controller points to a bad phase connector, cable or winding.
Results from different controller hardware are not directly comparable.

| Date | Hardware | ID | R (Ω) | L (H) | Flux linkage (Wb) | Commit |
|---|---|---|---|---|---|---|
| 2026-04-18 | HD60T | 22 | 0.0314 | 6.769e-05 | 0.010502 | `d1f867c` |
| 2026-04-18 | HD60T | 23 | 0.0485 | 8.378e-05 | 0.010487 | `d1f867c` |
| 2026-04-18 | Stormcore | 22 | 0.0228 | 2.688e-05 | 0.010682 | `d1f867c` |
| 2021-11-21 | Stormcore | 22 | 0.0229 | 2.511e-05 | 0.010632 | `ad81809` |
| 2021-11-21 | Stormcore | 23 | 0.0352 | 3.538e-05 | 0.010754 | `ad81809` |
| 2021-11-15 | Stormcore | 22, 23 | 0.0385 | 3.123e-05 | 0.010824 | `f657a7f` |

## Faults

Record any fault code shown in VESC Tool, red LED, cut-out or overheating.

| Date | Odometer (km) | Controller | Fault / symptom | Cause | Fix |
|---|---|---|---|---|---|
| 2026-10, reported 2026-10-14 | unknown | HD60T | Controller blown. Which half failed is not recorded. | Regen braking while the BMS charge input was manually disabled. Regen current had no path into the pack and the bus voltage spiked past the rating. | Replace the controller, see [controller-replacement.md](../docs/controller-replacement.md) |
