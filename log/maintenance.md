# Maintenance Log

Record every inspection, repair and measurement here. Newest first.
The schedule and procedures are in [docs/maintenance.md](../docs/maintenance.md).
Controller config changes and faults go in [controller.md](controller.md).
Entries before October 2026 were reconstructed from git history and the owner's email from 2021 and 2026.

## Work log

| Date | Odometer (km) | Work done | Notes |
|---|---|---|---|
| 2026-04, shortly before 2026-04-18 | unknown | HD60T controller failed from regen braking with the BMS charge input still off after the winter break. Scooter out of service until the controller is replaced. | Prevention and checks in [controller-replacement.md](../docs/controller-replacement.md#1-what-killed-the-hd-60t) |
| 2022-07-07, reported | about 250 | Top-balanced the pack once with the iCharger X12. About 5.7 kWh used in total, about 23 Wh/km. | Cells 2 and 3 lagged, see battery health |
| 2021-11-23, about | – | Ordered a spare front and a spare rear motor. | – |
| 2021-11-20 | – | Fitted a Trampa VESC HD60T in place of the failed Stormcore. Both motors running. Detection and tuning followed on 2021-11-21. | See controller log |
| 2021-11-17 | – | Stormcore 60D+ failed. | See controller log faults |
| 2021-11-15 | – | Pack, Stormcore 60D+, ReVOLT dashboard, throttle and both motors working together. Controllers detected and tuned. | – |
| by 2021-11-01 | – | ReVOLT dashboard fitted. | – |

## Battery health

Take these readings every 3 months and after any incident. Trends matter more than single values.

| Date | Odometer (km) | Full-charge voltage (V) | Max cell delta (mV) | Pack internal resistance (mΩ) | Measured capacity (Ah) | BMS cycle count | Notes |
|---|---|---|---|---|---|---|---|
| 2022-07-07, reported | about 250 | unknown | 40 | unknown | unknown | unknown | Imbalance 10–40 mV, cells 2 and 3 lagging. One top balance with the X12. |
| 2021-11 | 0 | – | 10 | – | 20, rated | 0 | New cells measured at 3.450 V ± 0.01 V before assembly |
