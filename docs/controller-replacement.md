# Controller Replacement

The Trampa VESC HD-60T Twin failed in April 2026 and must be replaced. Trampa said it is likely not repairable.
This page collects the options, the chosen replacement and parts to order, what to check before powering it, and how to migrate.
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

- **HD-60T Twin again** is the only true drop-in for the current wiring, mounting and configs. Trampa said in April 2026 that the HD-60 had been out of stock for over two years, so it is likely unavailable. It keeps the narrow 1.6 V margin between a full pack and its 52 V rating, so the rules above matter most with it.
- **VESC Duet XS** fits anywhere the HD-60T fit and its 22S rating gives a 12S pack far more voltage headroom. No controller survives regen into a disabled BMS, so the rules above still apply. Its 50 A continuous per motor is plenty for the Rev. The hall and comms leads need new JST-GH plugs.
- **Stormcore 2.0** is much bigger than the HD-60T. It only fits if the bay was not trimmed for the HD-60T. Its holes differ from the 60D+, ⌀ 4.1 mm at about 125.5 mm spacing, so expect to redrill. Lacroix publishes no drawing of its own; the figures come from the VESC Duet datasheet, which Lacroix links as the 2.0's datasheet. It needs good heatsinking for its higher current limits.

Measure the actual bay and the actual unit before cutting anything. The pack layout leaves the controller space at one end, see [battery.md](battery.md#design).

## 3. Decision and parts to order

**Chosen on 2026-10-14: VESC Duet XS 100V.** Not yet ordered.
It fits the HD-60T space, and its 100 V rating leaves about 50 V of headroom above a full pack, against 1.6 V on the HD-60T.

**Check before ordering:** ask ReVOLT whether the dashboard works with the Duet XS, see [ReVOLT dashboard](#revolt-dashboard). The throttle runs through the dashboard, so the scooter does not ride without it.

Order everything from VESC Labs in one go, because the add-on prices only apply on the Duet XS product page.
Prices are ex VAT, as of October 2026.

| Item | Price | Why |
|---|---|---|
| VESC Duet XS 100V | €199.99 | Replacement controller |
| VESC Nanolog | €34.99 as add-on, €44.99 alone | Bluetooth and Wi-Fi link for VESC Tool, onboard logging |
| XT90S connector, female | €2.49 | Probably not needed. The pack already ends in an XT90-S anti-spark plug. Check that it mates with the Duet XS's XT90 male input before ordering. The Duet XS datasheet requires an XT90S or a precharge switch when the BMS has none. |

The Duet XS comes with an RGB momentary power button, six 4 mm male bullets, and 500 mm JST-GH pigtails with 2, 3, 4, 5, 6, 6 and 8 pins, so these are not on the list.

A spare Stormcore 60D+, the 2021 warranty replacement, may still be on hand. It is no stopgap: its 50.4 V rating equals a full pack, so any regen spike exceeds it, the failure that killed the HD-60T.

### Wireless and logging

The Duet XS has no radio of its own.

- **VESC Nanolog, new.** An ESP32-C3 running VESC Express firmware. It gives VESC Tool a Bluetooth LE and 2.4 GHz Wi-Fi link, stores logs in 500 MB of onboard memory, and updates over the air. It plugs into the Duet XS CAN port with its included 4-pin JST-GH cable and accepts 3–15 V, so the port's 5 V output powers it. It measures 23 × 25 mm and weighs 4.3 g.
- **Metr Pro UART, already owned.** Bought 2021-11-22 as "Metr Pro - PCB Antenna", the UART variant. A Bluetooth LE module for the Metr app's live dashboard and ride records. VESC Tool reaches it only through the Metr app's TCP bridge. Metr has closed its shop and sells no new modules. It says the app and web services keep working "for the foreseeable future".

The two overlap on phone access. The Nanolog is the long-term link, because its firmware is maintained and it logs without a phone.
Keep the Metr Pro for the Metr app's ride stats. Nothing else depends on it.

Metr's own pages name no supported VESC firmware. A mirror of the App Store listing shows VESC 7.0 support added in app version 4.30.0, July 2026.
Check that the Metr app reads both motors after the Duet XS firmware update.

The Metr Pro UART needs 3.3 V, GND, TX and RX and must not be powered from 5 V. On the Duet XS these sit on the 8-pin IO plug next to the throttle input: 3.3 V on pin 2, GND on pin 3, TX on pin 5 and RX on pin 6, with the throttle on ADC1, pin 4. Build one harness from the 8-pin pigtail that carries both. Move each Metr wire by the VESC signal it used on the old plug, so the wire on the old TX pin goes to pin 5. The 3.3 V output is rated 0.3 A. Keep ID 22 on the ADC + UART app.

### ReVOLT dashboard

The throttle runs through a ReVOLT dashboard by Michael Castiau, so the Duet XS must work with it.
Five of its six wires go to the controller: GND, 5 V, ADC, CAN H and CAN L. The dashboard passes the throttle on as an ADC signal.

- **ADC and GND** go to the 8-pin IO plug, ADC1 on pin 4 and GND on pin 3, in the same harness as the Metr Pro.
- **CAN and 5 V.** The Duet XS has one CAN port, and the Nanolog needs it too. Split the port's 4-pin cable to feed both, and check that its 5 V output can supply both. Keep the CAN rate at 500 kbit/s, the dashboard's default.
- **Power on and off.** The HD-60T needed COMM pins 1 and 6 bridged for the dashboard's roll-to-start and full shutdown. The Duet XS has a momentary power button instead. How the dashboard switches it is unknown.
- **Firmware.** The dashboard was set up in 2021 against the VESC firmware of that time. Whether it works with current firmware is unknown.

Ask ReVOLT about power switching and firmware before ordering.

Every device on CAN needs its own ID. Keep 22 and 23 for the motors, check which ID the dashboard uses, and change the Nanolog's ID on VESC Tool's VESC Express page if it clashes.

## 4. How much controller the Rev needs

| Property | Value |
|---|---|
| Motor rating | 750 W continuous each, 1.5 kW total |
| Peak power | not published, reviewers estimate about 2–2.5 kW |
| Battery current per motor | about 17 A continuous at 43.2 V nominal |
| Current battery limit per motor | 30 A |

Every option has plenty of headroom. Motor heat limits the settings, not the controller.

## 5. Settings to change on the new controller

Fix these before the first ride. `python3 scripts/vesc_check.py check vesc/<new hardware>` flags them.

- **Overvoltage fault.** Set it below the controller's rated maximum. On a 12S-only controller, also keep regen gentle near full charge.
- **Regen current.** Keep the combined battery regen at or below 30 A, the pack's charge limit.
- **Charge level.** Charging to 4.1 V per cell, 49.2 V, leaves 1.2 V more room for regen. The X12 can set a lower charge voltage. Range drops by roughly 10 %.
- **Setup info on ID 22.** Set 40 poles, gear ratio 1, wheel 0.222 m and 20 Ah on both controllers.
- **Cut-off end.** Raise it to about 34.0 V so the VESC cuts before the BMS.

## 6. Migration steps

1. Do the collateral-damage checks in section 1.
2. Add the new hardware's rated voltage to `HARDWARE_MAX_V` in `scripts/vesc_check.py`.
3. Mount the controller and connect phases, power through the pack's XT90-S plug, the dashboard, the Nanolog and the Metr Pro as in section 3. Leave hall cables unplugged unless you plan to use sensored mode.
4. Power up through the anti-spark connection with the wheels off the ground.
5. Update the firmware, then run the motor wizard for both motors. Set CAN IDs 22 and 23 as before.
6. Re-create the app settings from `vesc/hd60t/id22-app.xml`. Do not load the HD-60T XML files directly onto different hardware.
7. Apply the settings from section 5.
8. Export the configs to `vesc/<new hardware>/` as `id<NN>-<motor|app>.xml` and run the checker.
9. Add the new detection results to the [detection history](../log/controller.md#motor-detection-history). Compare them with the HD-60T values.
10. Connect VESC Tool over the Nanolog and the Metr app over the Metr Pro. Both should show IDs 22 and 23. Check that the dashboard shows live data and switches the controller on and off.
11. Test at walking speed, then with gentle braking, before a real ride.
12. Update the hardware table in [log/controller.md](../log/controller.md#hardware) and the current hardware in [controller.md](controller.md).

## Sources

From a research conversation with Claude in October 2026, citing:

- Lacroix: Stormcore 2.0 product page
- Defiant Board Society: Stormcore 60D+ specifications
- VESC Labs: VESC Duet datasheet, Duet XS product page and add-ons, VESC Nanolog
- Metr: shop notice, FAQ and setup page, and a mirror of the Metr app's App Store listing
- Trampa: VESC HD-60T Twin product page
- Electrek and EScooterNerds: Boosted Rev reviews and motor ratings

History, parts owned and the failure date come from the owner's email: Trampa orders 35503 and 55161, Lacroix Europe order 4895, shop.metr.at order 995, and the ReVOLT dashboard thread from 2021 and 2022.
