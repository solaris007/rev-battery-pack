# Controller Replacement

The Trampa VESC HD-60T Twin failed in October 2026 and must be replaced.
This page collects the options, what to check before powering a new controller, and how to migrate.
Record the decision and the outcome in [log/controller.md](../log/controller.md).

## 1. What killed the HD-60T

**Root cause: regenerative braking while the BMS charge input was manually switched off.**

When the motors brake, the controller pushes current back into the battery.
With the BMS charge MOSFET off, that current has nowhere to go. The DC bus voltage rises within milliseconds, far past the HD-60T's 52 V rating, and the power stage fails.
The overvoltage fault was set to 57 V, above the 52 V rating, so it could not help. Even a lower setting may react too slowly for a spike this fast.

### Rules that prevent a repeat

- **Never ride with the BMS charge input disabled.** Check that both charge and discharge show as on in the BMS app before riding.
- **Do not regen hard on a full pack.** The BMS opens its charge MOSFET by itself at 4.25 V per cell, 51.0 V. Braking on a full pack can trigger that, with the same result as switching it off by hand.
- **Leave headroom.** Charging to 4.1 V per cell, 49.2 V, keeps regen well clear of the BMS over-charge trip.
- **Never run the BMS in bypass or charge-only mode**, see [battery.md](battery.md#battery-management-system).

### Checks before connecting the new controller

The cause is known, so these look for collateral damage, not for the cause.

- Inspect the dead board for which half failed, controller 1 or 2, and note it in the [controller log](../log/controller.md#faults).
- Spin each wheel by hand. Rough or cogging rotation can mean a shorted MOSFET dumped current into a motor winding.
- Measure phase-to-phase resistance on both motors and check phase-to-frame for shorts. The motor on ID 23 has measured about 50 % more resistance than ID 22 since 2021, so compare against that baseline.
- Check the BMS still switches charge and discharge on and off correctly, and that every cell reads normal.

## 2. Options

| | Trampa VESC HD-60T Twin | VESC Duet XS | Lacroix Stormcore 2.0 | Stormcore 60D+, for reference |
|---|---|---|---|---|
| Size L × W × H | 101 × 55 × 18 mm | 87 × 54 × 18 mm | 134 × 70 × 24 mm | 132 × 70 × 23 mm |
| Max battery | 12S | 22S | 6S–22S | 12S |
| Current per motor | – | 50 A continuous, 65 A burst | 140 A continuous, 200 A pulsed | 75 A |
| Motor leads | as before | 4 mm bullets | 4 mm female bullets | 4 mm female bullets |
| I/O connectors | as before | JST-GH | JST-PH 2 mm, USB-C | – |
| Power input | external anti-spark | – | integrated XT90, optional power switch with internal anti-spark | integrated XT90 |
| Fits the HD-60T space | yes, drop-in | yes, smaller in every dimension | only if the bay still has the 60D+ space | – |

Notes:

- **HD-60T Twin again** is the only true drop-in for the current wiring, mounting and configs. It keeps the narrow 1.6 V margin between a full pack and its 52 V rating, so the rules above matter most with it.
- **VESC Duet XS** fits anywhere the HD-60T fit and its 22S rating gives a 12S pack far more voltage headroom. No controller survives regen into a disabled BMS, so the rules above still apply. Its 50 A continuous per motor is plenty for the Rev. The hall and comms leads need new JST-GH plugs.
- **Stormcore 2.0** is much bigger than the HD-60T. It only fits if the bay was not trimmed for the HD-60T. Its holes differ from the 60D+, ⌀ 4.1 mm at about 125.5 mm spacing, so expect to redrill. Lacroix publishes no drawing of its own; the figures come from the VESC Duet datasheet, which Lacroix links as the 2.0's datasheet. It needs good heatsinking for its higher current limits.

Measure the actual bay and the actual unit before cutting anything. The pack layout leaves the controller space at one end, see [battery.md](battery.md#design).

## 3. How much controller the Rev needs

| Property | Value |
|---|---|
| Motor rating | 750 W continuous each, 1.5 kW total |
| Peak power | not published, reviewers estimate about 2–2.5 kW |
| Battery current per motor | about 17 A continuous at 43.2 V nominal |
| Current battery limit per motor | 30 A |

Every option has plenty of headroom. Motor heat limits the settings, not the controller.

## 4. Settings to change on the new controller

Fix these before the first ride. `python3 scripts/vesc_check.py check vesc/<new hardware>` flags them.

- **Overvoltage fault.** Set it below the controller's rated maximum. On a 12S-only controller, also keep regen gentle near full charge.
- **Regen current.** Keep the combined battery regen at or below 30 A, the pack's charge limit.
- **Charge level.** Charging to 4.1 V per cell, 49.2 V, leaves 1.2 V more room for regen. The X12 can set a lower charge voltage. Range drops by roughly 10 %.
- **Setup info on ID 22.** Set 40 poles, gear ratio 1, wheel 0.222 m and 20 Ah on both controllers.
- **Cut-off end.** Raise it to about 34.0 V so the VESC cuts before the BMS.

## 5. Migration steps

1. Do the collateral-damage checks in section 1.
2. Add the new hardware's rated voltage to `HARDWARE_MAX_V` in `scripts/vesc_check.py`.
3. Mount the controller and connect phases, power, CAN and throttle. Leave hall cables unplugged unless you plan to use sensored mode.
4. Power up through the anti-spark connection with the wheels off the ground.
5. Update the firmware, then run the motor wizard for both motors. Set CAN IDs 22 and 23 as before.
6. Re-create the app settings from `vesc/hd60t/id22-app.xml`. Do not load the HD-60T XML files directly onto different hardware.
7. Apply the settings from section 4.
8. Export the configs to `vesc/<new hardware>/` as `id<NN>-<motor|app>.xml` and run the checker.
9. Add the new detection results to the [detection history](../log/controller.md#motor-detection-history). Compare them with the HD-60T values.
10. Test at walking speed, then with gentle braking, before a real ride.
11. Update the hardware table in [log/controller.md](../log/controller.md#hardware) and the current hardware in [controller.md](controller.md).

## Sources

From a research conversation with Claude in October 2026, citing:

- Lacroix: Stormcore 2.0 product page
- Defiant Board Society: Stormcore 60D+ specifications
- VESC Labs: VESC Duet datasheet and Duet XS
- Trampa: VESC HD-60T Twin product page
- Electrek and EScooterNerds: Boosted Rev reviews and motor ratings
