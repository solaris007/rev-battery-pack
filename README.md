# Battery Pack for Boosted Rev

## Battery Specifications
Cells used: [Samsung INR21700-40T](datasheets/Samsung-INR21700-40T.pdf) ([Ordered here](https://eu.nkon.nl/samsung-inr21700-40t-4000mah-30a.html))
- Nominal voltage: 3.6
- Fully charged voltage: 4.2
- Capacity: 4 Ah (4000 mAh)

Pack:
| Description       | Value                               |
|-------------------|-------------------------------------|
| Configuration     | 12s5p                               |
| Max Voltage       | 50.4 V (12 \* 4.2 V)                |
| Nominal Voltage   | 43.2 V (12 \* 3.6 V)                |
| Min Voltage       | 30.0 V (12 \* 2.5 V)                |
| Max Capacity      | 20 Ah (5 \* 4 Ah), ~ 1 kWh (@ 50 V) |
| Max Discharge     | 175 A (C-rate = 8.75)               |
| Nominal Discharge | 20 A (C-rate = 1)                   |

- The battery power limit is 8750 W when fully charged (C-rate 8.75, 35A per cell)
- The battery power limit is 5250 W when reaching fully discharged  (C-rate 8.75, 35A per cell)

## Consumer
2 x 750 W motors.

Max power draw: 1500 W

Max continuous demand on battery:
| Throttle Pos. | State of Charge | Value                       |
|---------------|-----------------|-----------------------------|
| Full Throttle | Full Charge     | ~ 30 A (2 \* 750W) / 50.4 V |
| Full Throttle | Nominal Charge  | ~ 35 A (2 \* 750W) / 43.2 V |
| Full Throttle | Empty Charge    | ~ 50 A (2 \* 750W) / 30 V   |

- The battery will be asked to deliver max 50 A reaching fully discharged (C-rate = 2.5, 10 A per cell)
- The battery will be asked to deliver max 30 A when fully charged (C-rate = 1.5, 6A per cell)

### ECS (Stormcore) Limits:
- Battery input V: max 50.4 V
- Max Motor Power Draw: 80W for 10 minutes (is that per motor or for both motors combined?
- Motor peak at 1000W ???

## Battery Pack Design
Enclosure limitations:
- Max height:  45mm
- Max width:  115mm
- Max length: 520mm (with 7 series bottom and 5 series top to accommodate ECS)

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
- While the ESC (VESC) adds current discharge protection, but based on user-settings
- If the user (you!) makes a configuration mistake protections may be removed
- If the ESC has a fault or can't read its EEPROM, protections may be removed
- Switching out the battery is dangerous without discharge protection
- BMS cannot monitor regenerative current and adds no regen-charge protection

### Wiring & Strips
Consult [current capacity list](datasheets/current_capacity.png) to size parallel/series connections between cells.

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
