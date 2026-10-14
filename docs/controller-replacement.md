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

The ReVOLT dashboard and the Metr Pro both work with it after config and wiring changes, see below. The one open point is switching it on.

**Check before ordering:** ask VESC Labs whether the Duet XS can wake on wheel rotation or from an external line. Without that, roll-to-start is lost and its power button needs a spot within reach, see [ReVOLT dashboard](#revolt-dashboard).

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

### Duet XS plugs

Both add-ons and the dashboard share two Duet XS plugs.

| Plug | Pin | Signal | Used by |
|---|---|---|---|
| IO, 8-pin | 1 | 5 V | dashboard |
| IO, 8-pin | 2 | 3.3 V, 0.3 A | Metr Pro |
| IO, 8-pin | 3 | GND | dashboard, Metr Pro |
| IO, 8-pin | 4 | ADC1 | throttle from the dashboard |
| IO, 8-pin | 5 | UART TX | Metr Pro |
| IO, 8-pin | 6 | UART RX, 5 V tolerant | Metr Pro |
| IO, 8-pin | 7, 8 | ADC2, ADC3 | – |
| CAN, 4-pin | 1 | 5 V | Nanolog |
| CAN, 4-pin | 2, 3 | CAN H, CAN L | dashboard, Nanolog |
| CAN, 4-pin | 4 | GND | Nanolog |

Every 5 V pin is rated 1 A, 2 A in total. The dashboard draws up to about 300 mA.
Build one harness from the 8-pin IO pigtail and splice the dashboard's CAN H and CAN L into the 4-pin CAN cable to the Nanolog.

### Metr Pro on the Duet XS

It should work. No report of a Metr Pro on a Duet or Duet XS turned up, so treat the first ride as the test.

- **Firmware.** Run VESC firmware 7.00, the stable Duet XS release, with Metr app 4.30.0 or later, which added VESC 7.0 support in July 2026. Avoid the 7.01 beta. Live data and logging have survived past firmware changes; config editing in the app breaks first. On 6.06 the app's Modes page did not work as of April 2026.
- **Both motors.** The Duet XS runs both motors from one MCU and reports motor 2 under its CAN ID + 1. With ID 22 the Metr app sees 22 and 23, as on the HD-60T.
- **Wiring.** The Metr Pro UART must not be powered from 5 V. Pin 1 next to its 3.3 V pin carries 5 V, so check the harness with a meter before plugging the Metr in. Move each Metr wire by the VESC signal it used on the old plug, so the wire on the HD-60T's TX pin goes to pin 5. The Metr's stock cable is a 7-pin JST-PH, so the harness is new.
- **App setting.** ADC and UART. The Metr finds the baud rate by itself; 115200 is the default. A solid green LED on the Metr means the UART link is up, a blinking one means it is not.
- **Updates and account.** Module firmware updates run in the Metr app over Bluetooth, not through the closed shop. The app needs no account.

### ReVOLT dashboard

The throttle runs through a ReVOLT dashboard by Michael Castiau. It works with the Duet XS after config and wiring changes, but roll-to-start is most likely lost.
Its firmware is closed source. These findings come from the [build post](https://michael-castiau.blogspot.com/2021/05/boosted-rev-custom-dashboard-vesc.html), the user manual and analysis of release binaries 1.2.0 and 2.1.0 in [MichaelCastiau/boosted-revolt-dashboard](https://github.com/MichaelCastiau/boosted-revolt-dashboard).
The last firmware, 2.1.0, dates from 2022-10-24. The author stopped selling Rev products in November 2022.

How it works:

- It reads CAN status messages 1 and 5 from IDs 22 and 23, for speed and pack voltage. The VESC ID 22 is hard-coded, and speed assumes 40 motor poles.
- It passes the throttle through to the controller's ADC as an analog signal, only while unlocked. It never sends current or brake commands.
- The only thing it sends is a broadcast CAN shutdown, on a long press and 10 s after power-up without a valid RFID key.
- CAN runs at a fixed 500 kbit/s.
- The status message layouts it reads are unchanged up to VESC firmware 7.01.

On the Duet XS:

- **Controller ID 22.** Motor 2 then reports as 23 by itself. Firmware 6.x and later picks a random ID by default, so set it by hand.
- **CAN status messages 1 and 5 on.** Firmware 6.x and later sends none by default. The HD-60T sent 1 to 5 at 50 Hz from ID 22.
- **Throttle range.** The Duet XS reads the ADC on a 0–3.3 V scale. The HD-60T throttle map of 1.86–3.1 V fits.
- **CAN termination.** No datasheet says where the bus is terminated. With power off, measure between CAN H and CAN L. About 60 Ω means two terminators, as it should be.
- **Power on and off.** The dashboard has no power output, and its manual says its button does not turn on the scooter. Roll-to-start came from the controller. The Duet XS toggles on and off with a momentary button across MOM1 and MOM2, and its datasheet mentions no wake on motion. Shutdown from the dashboard should still work, because the Duet XS firmware accepts the broadcast shutdown. Do not copy the HD-60T's pin 1 to 6 bridge onto MOM1 and MOM2. A permanent bridge either keeps the unit on for good or turns it off after 1.5 s.
- **Setup.** The ReVOLT Tool's "Configure Automatically" writes a VESC 5.x app config. Set the Duet XS by hand in VESC Tool instead.
- **Dashboard commands.** The manual gives CAN ID 0x16 for dashboard config frames, but the firmware listens on 0x40. A frame sent to 0x16 is a set-duty command for VESC 22 and can spin motor 1. Only use 0x40.

Every device on CAN needs its own ID. The motors use 22 and 23. The Nanolog defaults to ID 2, which is free. Keep it off 22, 23 and 64, the ID of the dashboard's config frames.

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
- **CAN for the dashboard.** Controller ID 22, CAN status messages 1 and 5 on, 500 kbit/s. See [ReVOLT dashboard](#revolt-dashboard).

## 6. Migration steps

1. Do the collateral-damage checks in section 1.
2. Add the new hardware's rated voltage to `HARDWARE_MAX_V` in `scripts/vesc_check.py`.
3. Mount the controller and its power button, and connect phases, power through the pack's XT90-S plug, the dashboard, the Nanolog and the Metr Pro as in section 3. Measure about 60 Ω between CAN H and CAN L with the power off. Leave hall cables unplugged unless you plan to use sensored mode.
4. Power up through the anti-spark connection with the wheels off the ground.
5. Update the firmware to 7.00, then run the motor wizard for both motors. Set the controller ID to 22, so motor 2 reports as 23.
6. Re-create the app settings from `vesc/hd60t/id22-app.xml` by hand. Do not load the HD-60T XML files or the ReVOLT Tool's automatic config onto different hardware.
7. Apply the settings from section 5.
8. Export the configs to `vesc/<new hardware>/` as `id<NN>-<motor|app>.xml` and run the checker.
9. Add the new detection results to the [detection history](../log/controller.md#motor-detection-history). Compare them with the HD-60T values.
10. Connect VESC Tool over the Nanolog and the Metr app over the Metr Pro. Both should show IDs 22 and 23. Check that the dashboard shows speed and battery, and that a long press shuts the controller down.
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
- VESC firmware source and firmware archive: dual-motor CAN IDs, CAN status defaults, shutdown handling, Duet XS builds
- esk8.news forum: Metr app and Metr Pro threads on firmware 6.x and 7.x
- Michael Castiau: ReVOLT dashboard build post, user manual and release binaries 1.2.0 and 2.1.0

History, parts owned and the failure date come from the owner's email: Trampa orders 35503 and 55161, Lacroix Europe order 4895, shop.metr.at order 995, and the ReVOLT dashboard thread from 2021 and 2022.
