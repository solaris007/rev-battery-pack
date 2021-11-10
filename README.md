# Battery Pack for Boosted Rev

## Battery Specifications
Cells used: [Samsung INR21700-40T](datasheets/Samsung-INR21700-40T.pdf) ([Ordered here](https://eu.nkon.nl/samsung-inr21700-40t-4000mah-30a.html))
- Nominal voltage: +3.6V
- Max voltage: +4.2V
- Cut-off voltage: +2.5V 
- Max capacity: 4 Ah (4000 mAh)

Pack:

| Description                | Value                               |
|----------------------------|-------------------------------------|
| Configuration              | 12S5P                               |
| Capacity                   | 864 Wh                              |
| Max Voltage                | 50.4 V                              |
| Nominal Voltage            | 43.2 V                              |
| Cut-off Voltage            | 30.0 V                              |
| Discharge Capacity (Rated) | 20 Ah                               |
| Max Discharge              | 225 A (80°C cut-off)                |
| Nominal Discharge          | 175 A                               |

> ### Comparison with the stock Boosted Rev battery
> The original battery has a capacity of 370Wh. This new battery pack
> thus increases that capacity by more than 2 times.
> If a 370Wh battery provides a range of appr. 25kmh, the new
> battery should be able to provide a (theoretical) range of 55kmh.
> 
> This calculation is of course an indication and may vary based on riding style, weight of the rider
> and road conditions.

## Consumer
2 x 750 W motors.

Max power draw: 1500 W

Max continuous demand on battery:

| Throttle Pos. | State of Charge | Value                       |
|---------------|-----------------|-----------------------------|
| Full Throttle | Full Charge     | ~ 30 A (2 \* 750W) / 50.4 V |
| Full Throttle | Nominal Charge  | ~ 35 A (2 \* 750W) / 43.2 V |
| Full Throttle | Empty Charge    | ~ 50 A (2 \* 750W) / 30 V   |

These values are indicative and not representative of real-word conditions.
(for ex. if you are going up a hill, even if the battery is fully charged, the motor will consume more than 30A)

### VECS (Stormcore 60D+) Limits:
- Battery input V: max 50.4 V
- Max power rating: 80A for a couple of minutes (peak: 100A for a couple of seconds)
- Max Motor power draw: 30A per motor => 60A combined

## Battery Pack Design
Enclosure limitations:
- Max height:  45mm
- Max width:  115mm
- Max length: 520mm (with 7 series bottom and 5 series top to accommodate VECS)

[Cell Configuration Diagram](diagrams/battery-pack-v0.5.pdf)

### Battery Manufacture
- Measure each cell. I measured a consistent 3.450 V with a maximum deviation of 0.01V.
- Glue fish paper isolation rings on the positive end of the cells
- Use room temperature epoxy to glue the 5 cells of a parallel group (P-group) together
- After curing, wrap the P-group with fish paper

### Battery Management System (BMS)
[JBD 12s Smart BMS](https://www.aliexpress.com/item/32819508078.html?spm=a2g0s.12269583.0.0.290022f9etByly) [Specifications](datasheets/jbd-bms-specifications.webp), [Wiring diagram](manuals/jbd-bms-wiring.webp)

The BMS will be used for monitoring charging and discharging the battery.

DO NOT USE THE BMS IN BY-PASS MODE (i.e. only for charging the battery):

- The ESC adds additional current discharge protection, but it's exactly that: additional. It's not meant to replace the robust discharge/undervoltage protection of a BMS.
- If the user (you!) makes a configuration mistake protections may be removed, since this is a simple memory setting
- If the ESC has a fault or EEPROM gets corrupted (by age or external factors), protections may be removed
- Switching out the battery is dangerous without discharge protection. Battery terminals should always be protected.
- Most ESCs perform poor regenerative current monitoring
- **An ESC won't provide over-voltage protection, or provide correct Li-ion charge algorithms**

### Wiring & Strips
Consult [current capacity list](datasheets/current_capacity.png) to size parallel/series connections between cells.

#### Nickel Strips
Be careful where you order. From Alibaba I got nickel-plated steel instead of pure nickel. Plated steel has 4 times higher resistance than pure nickel with associated heat development during operation.

I finally ordered [10 meters of 0.2mm x 50mm strip from NKON](https://eu.nkon.nl/accessories/packaccessoires/battery-solder-strip/1-meter-nikkel-batterijsoldeerstrip-50mm-0-20mm.html).

From the nickel roll I cut strips that connect all cells in a P-group as well as provide a full-width series connection to the next p-group.

The strip is ~86mm wide when folded up/down to the next p-group in series. 0.2mm thickness with 86mm width should give a decent optimal ampere rating of ~150A, therefore curbing heat between p-groups.

#### BMS
- 24AWG 1007 white single-core, 105°C / 300V

## Tools
| Name | Description | Manual |
|------|-------------|--------|
| [kWeld](https://www.keenlab.de/index.php/product/kweld-complete-kit/) | Spot welder kit | [Assembly Manual](https://www.keenlab.de/wp-content/uploads/2018/07/kWeld-assembly-manual-r5.0.pdf), [Operation Manual](https://www.keenlab.de/wp-content/uploads/2018/07/kWeld-operation-manual-r3.0.pdf) |
| kCap | Ultracapacitor for kWeld | [Manual](https://www.keenlab.de/wp-content/uploads/2020/04/kCap-manual-r2.0.pdf) |
| kSupply | High current voltage regulator and charger for kWeld | [Manual](https://www.keenlab.de/wp-content/uploads/2019/06/kSupply-manual.pdf) |
| [HP PSU HSTNS-PR01](https://www.ebay.ch/itm/114295259966?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649) | HP Power Supply HSTNS-PR01 ATSN 7001044 380622-001 379124-001 for kWeld | - |


## Sources / Inspiration
- https://michael-castiau.blogspot.com
- https://forum.freesk8.org/t/mod-a-boosted-rev-battery-esc-and-more/942
- https://www.electricbike.com/introduction-battery-design-2/
- https://www.eboardsperu.com/product/12s4p-battery-pack-for-12s-universal-enclosure/
- https://lacroixboards.com/products/stormcore
- https://vesc-project.com/
