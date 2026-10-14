# Controller Log

Living record of the motor controller. Update it whenever hardware, firmware or configuration changes.
How to make a change is described in [docs/controller.md](../docs/controller.md#changing-the-configuration).
Entries before October 2026 were reconstructed from git history and the owner's email from 2021 and 2026.

## Hardware

Fields marked "unknown" are worth filling in at the next opportunity. VESC Tool shows firmware and hardware versions on connect.

| Item | Value |
|---|---|
| Status | **Failed in April 2026.** VESC Duet XS 100V with a VESC Nanolog chosen 2026-10-14, not yet ordered. See [controller-replacement.md](../docs/controller-replacement.md#3-decision-and-parts-to-order) |
| Controller | Trampa VESC HD60T Twin, board marked "MK I". Trampa order 35503 of 2021-11-18, £417.09 with shipping, bought as a backup when the Stormcore 60D+ failed |
| Serial number | unknown |
| Hardware version | unknown |
| Firmware version | unknown. The configs in `vesc/hd60t/` use config format `ConfigVersion` 2, see the note under [config history](#config-history) |
| Installed | 2021-11-20, both motors running that day |
| Bought with it | XT90 to XT60 power adapter PCB, VESC Connect dongle with integrated antenna and a 200 mm cable, Trampa power switch. The board shipped without its internal NRF Bluetooth chip because of the chip shortage. An NRF Bluetooth module, most likely the dongle, was flashed through VESC Tool's SWD programmer on 2021-11-23. |
| CAN IDs | 22 master, 23 slave |
| Throttle input | ADC on ID 22, fed by the dashboard |
| Dashboard | ReVOLT dashboard by Michael Castiau, bought 2021-10-19 for €189, fitted by 2021-11-01, unlocks with an RFID tag. Five of its six wires go to the controller: GND, 5 V, ADC, CAN H and CAN L. The throttle plugs into the dashboard. Its CAN default is 500 kbit/s. |
| Power on and off | Through the dashboard. The HD60T needed COMM pins 1 and 6, power switch and GND, bridged on both controllers for roll-to-start and full shutdown. Trampa suggested bridging the power-switch pin to the CAN GND pin instead, to keep COMM free. |
| Bluetooth module | Metr Pro, UART variant with PCB antenna. Bought 2021-11-22 from shop.metr.at, order 995. Trampa advised connecting Bluetooth to COMM on controller 1. The ADC + UART app on ID 22 suggests it was connected there, but that is not confirmed. |
| BMS | JBD 12S Smart BMS, 60 A discharge variant, because the 20 A variant was too weak. Accepts 40 A charge current. |
| Fuse | unknown |
| Anti-spark / power switch | The pack's main plug is an XT90-S anti-spark connector. Whether the Trampa power switch was fitted is unknown. |
| Spare controller | Stormcore 60D+ warranty replacement, shipped by Lacroix Europe 2021-11-22. Whether it is still on hand and unused is unknown. The failed unit came back on 2021-12-16 after Swiss customs refused the return. |

## Config history

Newest first. One line per change that was written to the controller.

Until 2026-10-14 the files in `vesc/stormcore-60d/` were taken to be Stormcore configs. Email shows the Stormcore ran only from 2021-11-15 until it failed on 2021-11-17, and the HD60T ran from 2021-11-20.
So those files hold Stormcore settings up to `26e94d6` and HD60T settings from `ad81809` on.
The `vesc/hd60t/` files were committed on 2026-04-18, an hour after the HD60T failure was reported to Trampa. They are the HD60T's last configs, after a firmware update, as the owner confirmed on 2026-10-14.
Dates in 2026-04-18 rows are commit dates. The changes may have been written to the controller any time after 2021-11-21.

| Date | Controller | Change | Commit |
|---|---|---|---|
| 2026-10-14 | HD60T | Failure recorded. No config change. Checker now flags the 57 V overvoltage fault above the 52 V rating. | – |
| 2026-10-14 | – | Config files moved to `vesc/hd60t/` and `vesc/stormcore-60d/` and renamed by CAN ID. No setting changed. | – |
| 2026-04-18, commit date | HD60T | First `ConfigVersion` 2 configs, filed under `vesc/hd60t/`. Motor current 60 A, absolute 120 A, battery 30 A, regen -15 A, motor temp cut 80–100 °C. ID 22 setup info left at defaults. | `d1f867c` |
| 2026-04-18, commit date | HD60T, filed under `stormcore-60d/` | Motor current 50 → 70 A, absolute 75 → 80 A, ID 22 app ADC → ADC + UART, throttle expo 0.75 → 0.25. The UART app most likely dates from fitting the Metr Pro in late 2021. | `d1f867c` |
| 2021-11-21 | HD60T | Regen -15 → -12 A after tuning. | `5852052` |
| 2021-11-21 | HD60T | Separate motor detection per controller. Motor current 30 → 50 A, absolute 175 → 75 A. | `ad81809` |
| 2021-11-17 | Stormcore | Absolute current 30 → 175 A, regen -12 → -15 A. Removed obsolete single-controller configs. Committed the morning the Stormcore failed. | `26e94d6`, `ef81433` |
| 2021-11-15 | Stormcore | First per-controller configs for ID 22 and ID 23 from motor detection. Motor and battery current 30 A. | `f657a7f` |
| 2021-10-24 | Stormcore | Initial config draft with placeholder motor values. | `7608d3d` |

## Motor detection history

FOC detection results per controller. Compare new results with the last line for the same controller.
A resistance rise of more than about 20 % on the same controller points to a bad phase connector, cable or winding.
Results from different controller hardware or firmware are not directly comparable.
The `ConfigVersion` 2 results read about 37 % higher in R on both motors than the 2021 HD60T results, and about 2.5 times higher in L. The same board measured both, so the shift most likely comes from the firmware update, not from motor wear.

| Date | Hardware | ID | R (Ω) | L (H) | Flux linkage (Wb) | Commit |
|---|---|---|---|---|---|---|
| 2026-04-18, commit date | HD60T, `ConfigVersion` 2 | 22 | 0.0314 | 6.769e-05 | 0.010502 | `d1f867c` |
| 2026-04-18, commit date | HD60T, `ConfigVersion` 2 | 23 | 0.0485 | 8.378e-05 | 0.010487 | `d1f867c` |
| 2026-04-18, commit date | HD60T, filed under `stormcore-60d/` | 22 | 0.0228 | 2.688e-05 | 0.010682 | `d1f867c` |
| 2021-11-21 | HD60T | 22 | 0.0229 | 2.511e-05 | 0.010632 | `ad81809` |
| 2021-11-21 | HD60T | 23 | 0.0352 | 3.538e-05 | 0.010754 | `ad81809` |
| 2021-11-15 | Stormcore | 22, 23 | 0.0385 | 3.123e-05 | 0.010824 | `f657a7f` |

## Faults

Record any fault code shown in VESC Tool, red LED, cut-out or overheating.

| Date | Odometer (km) | Controller | Fault / symptom | Cause | Fix |
|---|---|---|---|---|---|
| 2026-04, shortly before 2026-04-18 | unknown | HD60T | Controller blew while braking, and the wheels locked. Which half failed is not recorded. | The BMS charge input was switched off for the winter break and not re-enabled. Regen current had no path into the pack and the bus voltage spiked past the rating. | Trampa said on 2026-04-18 that it is likely not repairable, for lack of parts, and that the HD-60 has been out of stock for over two years. A second HD-60T, order 55161, was refunded on 2026-04-21. Replacement in [controller-replacement.md](../docs/controller-replacement.md) |
| 2021-11-20 | – | HD60T | `FAULT_CODE_ABS_OVER_CURRENT` on motor 1: -265.2 A, filtered -90.9 A, at 44.07 V. Occurred before the COMM pin 1 to 6 bridge was added. | unknown | unknown. The next day's config lowered the absolute current limit from 175 to 75 A, `ad81809`. |
| 2021-11-17 | – | Stormcore 60D+ | Accelerating after light regen while pushing the scooter out of the building, both wheels locked. The BMS reported an external short and shut its discharge port. The controller was hot. Inside, the current-sense resistor and the TI DRV gate driver were burnt. | unknown. Suspected a factory defect, or two motor phase terminals touching in plugs that were not fully insulated. The next day both motors measured 0.1–0.2 Ω on every phase pair and spun freely. The config written that morning had raised the absolute current limit from 30 to 175 A, far above the 75 A rating. Whether that played a part is unknown. | Lacroix Europe warranty replacement, shipped 2021-11-22. The HD60T, bought 2021-11-18, was fitted instead. |
