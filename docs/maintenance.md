# Maintenance

Schedule and procedures for the Rev with the DIY pack and VESC controller.
Record what you do in [log/maintenance.md](../log/maintenance.md). Record controller changes in [log/controller.md](../log/controller.md).

## Schedule

### Before every ride

- [ ] Pack voltage is above 36 V. Below that, charge first.
- [ ] Both charge and discharge are switched on in the BMS app. Regen with charge off destroys the controller.
- [ ] No warning or red LED on the controller.
- [ ] Throttle returns to zero and brakes work at walking speed.
- [ ] No new rattles, smells or visible damage on the deck and enclosure.

### Monthly or every 250 km

- [ ] Check cell voltages in the BMS app at rest. The spread between the highest and lowest cell should stay under 30 mV.
- [ ] Look at the enclosure seal and cable glands for cracks or water marks.
- [ ] Check that every bolt on the enclosure, stem and motor mounts is tight.
- [ ] Clear the VESC Tool fault log and note any faults in the controller log.

### Every 3 months or 1000 km

- [ ] Do a full balance charge with the X12 and let it finish balancing.
- [ ] Measure pack internal resistance with the X12. Add the reading to the battery health table.
- [ ] Read the BMS cycle count and full-charge voltage. Add them to the battery health table.
- [ ] Open the enclosure if it can be done without breaking the seal. Look for chafed wires, discoloured nickel strip, loose phase connectors and swollen cells.
- [ ] Back up the VESC configs and compare them with the repo, see below.

### Yearly

- [ ] Do a capacity test: ride the pack down to about 3.0 V per cell at rest, then charge to full with the X12 and record the Ah it put in.
- [ ] Re-run motor detection in VESC Tool **without writing the result**. Compare R, L and flux linkage with the detection history.
- [ ] Check for VESC firmware updates and read the release notes before updating.
- [ ] Replace the enclosure seal with fresh RTV162 if it has hardened or lifted.

## Thresholds

| Measurement | OK | Investigate | Stop riding |
|---|---|---|---|
| Cell spread at rest | < 30 mV | 30–100 mV | > 100 mV |
| Any cell at rest | 3.0–4.2 V | 2.8–3.0 V | < 2.8 V or > 4.25 V |
| Capacity | > 16 Ah | 14–16 Ah | < 14 Ah, end of life at 60 % |
| Motor resistance vs. last detection on the same hardware | < +20 % | +20–50 % | > +50 % |
| Pack temperature after a ride | < 45 °C | 45–60 °C | > 60 °C |

The capacity limits come from the cell datasheet. It defines end of life as 60 % of rated capacity after 250 full cycles.

## Procedures

### Cell balance check

1. Let the pack rest for at least an hour after riding or charging.
2. Connect the JBD / Xiaoxiang app over Bluetooth.
3. Note the highest cell, lowest cell and spread.
4. If the spread exceeds 30 mV, charge to full and leave the charger connected until balancing finishes. The BMS balances above 4.0 V per cell at only 50–60 mA, so this takes hours.
5. If the same P-group is always lowest, note its number. It may have a weak cell or a poor weld.

### Controller config backup

1. Connect VESC Tool and read the motor and app configs of both controllers.
2. Export them over the files in `vesc/hd60t/`.
3. Run `git status`. If nothing changed, the controller matches the repo.
4. If something changed, find out why, then commit and log it.

```
python3 scripts/vesc_check.py check vesc/hd60t
```

### Storage

- Store at 3.7–3.8 V per cell. The X12 storage mode does this.
- Store indoors, between 10 and 25 °C, away from anything flammable.
- Check the voltage every month and top up to storage level if needed.
- Disconnect the power switch or anti-spark loop so the controller does not drain the pack.

### After a controller failure

1. Disconnect the pack from the controller.
2. Find the cause before connecting a new controller. Check the BMS charge state first, then phase wires and motors, see [controller-replacement.md](controller-replacement.md#1-what-killed-the-hd-60t).
3. Log the fault in the [controller log](../log/controller.md#faults).

### After a crash or water exposure

1. Do not charge.
2. Check the pack voltage and every cell voltage in the BMS app.
3. Open the enclosure and look for dents, water and damaged insulation.
4. Only charge again once all cells read within 30 mV of each other and nothing is damaged. Charge supervised, outdoors or on a fire-safe surface.
