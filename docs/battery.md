# Battery Pack

12S5P pack built from Samsung INR21700-40T cells to replace the stock Boosted Rev battery.

## Cells

Cells: [Samsung INR21700-40T](../datasheets/samsung-inr21700-40t.pdf), ordered from [NKON](https://eu.nkon.nl/samsung-inr21700-40t-4000mah-30a.html).

| Property | Value |
|---|---|
| Nominal voltage | 3.6 V |
| Max voltage | 4.2 V |
| Cut-off voltage | 2.5 V |
| Capacity | 4 Ah |
| Max continuous discharge | 35 A, or 45 A with an 80 °C cut |
| Standard charge | 2 A CC/CV to 4.2 V |
| Max charge | 6 A CC/CV to 4.2 V |
| Charge temperature | 0 to 45 °C ambient |
| Discharge temperature | -20 to 60 °C ambient |

## Pack

| Property | Value |
|---|---|
| Configuration | 12S5P, 60 cells |
| Energy | 864 Wh |
| Max voltage | 50.4 V |
| Nominal voltage | 43.2 V |
| Cut-off voltage | 30.0 V |
| Capacity | 20 Ah |
| Max discharge | 225 A with 80 °C cut-off |
| Nominal discharge | 175 A |
| Max charge current | 30 A |
| Standard charge current | 10 A |

The stock Boosted Rev battery holds 370 Wh. This pack holds more than twice that.
If 370 Wh gives about 25 km of range, this pack should give a theoretical 55 km.
Real range depends on riding style, rider weight and road conditions.

## Load

The Rev keeps its original 2 × 750 W hub motors. Each is rated 750 W continuous, 1.5 kW in total.
Boosted never published a peak figure. Reviewers estimate about 2–2.5 kW.
The stock battery was also 43.2 V nominal, so this 12S pack matches the motors. At 43.2 V one motor draws about 17 A continuous.

| Throttle | State of charge | Battery current |
|---|---|---|
| Full | Full, 50.4 V | ~30 A for both motors |
| Full | Nominal, 43.2 V | ~35 A |
| Full | Empty, 30 V | ~50 A |

These values are indicative. Hills and acceleration draw more current than the steady-state numbers.
The controller limits battery current in software, see [controller.md](controller.md).

## Design

Enclosure limits:

| Dimension | Max |
|---|---|
| Height | 45 mm |
| Width | 115 mm |
| Length | 520 mm |

The pack uses 7 P-groups on the bottom layer and 5 on the top layer to leave room for the controller.

![Pack layout](../diagrams/battery-pack-v0.6.png)

- [Layout v0.6 (PDF)](../diagrams/battery-pack-v0.6.pdf), current.
- [Layout v0.5 (PDF)](../diagrams/battery-pack-v0.5.pdf), earlier draft.
- [OmniGraffle source](../diagrams/battery-pack.graffle).

The diagram still labels the controller as Stormcore. The VESC HD60T took its place in November 2021.
The diagram's "12 × 4.5 V" note is a typo for 12 × 4.2 V.

## Build Steps

1. Measure each cell. Mine measured a consistent 3.450 V with a maximum deviation of 0.01 V.
2. Glue fish paper insulation rings on the positive end of every cell.
3. Glue the 5 cells of each P-group together with room-temperature epoxy.
4. After curing, wrap each P-group in fish paper.
5. Spot weld the nickel strips, see below.
6. Seal with [Momentive RTV162](../datasheets/momentive-rtv162.pdf) electronics-grade silicone.

## Wiring and Strips

Size series and parallel connections with the [wire current capacity table](../datasheets/wire-current-capacity.png).

### Nickel strip

Check what you order. The strip from Alibaba turned out to be nickel-plated steel, not pure nickel.
Plated steel has about 4 times the resistance of pure nickel and heats up under load.

I used [10 m of 0.2 × 50 mm pure nickel strip from NKON](https://eu.nkon.nl/accessories/packaccessoires/battery-solder-strip/1-meter-nikkel-batterijsoldeerstrip-50mm-0-20mm.html).
Each strip connects all cells of a P-group and folds over as a full-width series connection to the next group.
Folded, the strip is about 86 mm wide. At 0.2 mm thick that carries roughly 150 A, which keeps the series joints cool.

### BMS sense wires

24 AWG UL1007 white single-core wire, rated 105 °C and 300 V.

## Battery Management System

[JBD 12S Smart BMS](https://www.aliexpress.com/item/32819508078.html), with [specifications](../datasheets/jbd-bms-specifications.webp) and [wiring diagram](../manuals/jbd-bms-wiring.webp).

| Protection | Default value |
|---|---|
| Over-charge | 4.25 V per cell |
| Over-charge release | 4.15 V per cell |
| Balance start | 4.0 V per cell |
| Balance current | 50–60 mA |
| Over-discharge | 2.7 ± 0.1 V per cell, 32.4 V pack |
| Over-discharge release | 2.9 V per cell |
| Over-temperature | 75 °C |

The installed BMS is the 60 A discharge variant, because the 20 A variant was too weak. It accepts up to 40 A charge current.
The pack's main lead ends in an XT90-S anti-spark plug.

**Never ride with the BMS charge input switched off.** Regen braking then has no path into the pack, the bus voltage spikes and the controller dies. This destroyed the HD60T in April 2026.
The BMS also opens its charge path by itself at 4.25 V per cell, so avoid hard regen on a full pack.

The BMS protects both charging and discharging. **Do not run the BMS in bypass mode**, i.e. only for charging:

- The ESC's current protection is an extra layer. It does not replace the BMS's discharge and undervoltage protection.
- A configuration mistake on the ESC can remove protections, because they are a simple memory setting.
- An ESC fault or corrupted EEPROM can remove protections.
- Swapping the battery is dangerous without discharge protection. Battery terminals should always be protected.
- Most ESCs monitor regenerative current poorly.
- **An ESC provides no over-voltage protection and no correct Li-ion charge algorithm.**

## Charging

Chargers and power supplies are listed in [tools.md](tools.md).

- Charge between 0 and 45 °C. Let a cold pack warm up first.
- Use 10 A for normal charging. Never exceed 30 A.
- Charging to 4.1 V per cell, 49.2 V, leaves room for regen braking right after a charge. It costs roughly 10 % of range.
- For storage longer than a couple of weeks, leave the pack at 3.7–3.8 V per cell.
