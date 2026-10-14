#!/usr/bin/env python3
"""Summarise, compare and sanity-check VESC Tool XML config exports.

Usage:
  python3 scripts/vesc_check.py summary vesc/hd60t        # key settings as a Markdown table
  python3 scripts/vesc_check.py diff A.xml B.xml           # every setting that differs
  python3 scripts/vesc_check.py check vesc/hd60t           # check limits against the pack

A config set is a directory holding id<NN>-motor.xml and id<NN>-app.xml for
each controller on the CAN bus. Only the Python standard library is used.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# --- Pack and hardware limits (keep in sync with docs/battery.md) -----------
SERIES = 12
PARALLEL = 5
CAPACITY_AH = 20
CELL_MAX_V = 4.2
CELL_MAX_DISCHARGE_A = 35      # Samsung 40T, continuous, no temp cut
CELL_MAX_CHARGE_A = 6          # Samsung 40T, rated charge
BMS_UNDERVOLT_CELL_V = 2.7     # JBD default, tolerance +/- 0.1 V
BMS_UNDERVOLT_TOL_V = 0.1
CONTROLLER_MAX_V = 52          # VESC HD60T input range 11-52 V
MOTOR_POLES = 40               # hub motor, 20 pole pairs
GEAR_RATIO = 1                 # direct drive hub motor

MOTOR_KEYS = [
    ("l_current_max", "Motor current max (A)"),
    ("l_current_min", "Motor current brake (A)"),
    ("l_in_current_max", "Battery current max (A)"),
    ("l_in_current_min", "Battery current regen (A)"),
    ("l_abs_current_max", "Absolute current max (A)"),
    ("l_max_erpm", "Max ERPM"),
    ("l_battery_cut_start", "Battery cutoff start (V)"),
    ("l_battery_cut_end", "Battery cutoff end (V)"),
    ("l_temp_fet_start", "MOSFET temp start (C)"),
    ("l_temp_fet_end", "MOSFET temp end (C)"),
    ("l_temp_motor_start", "Motor temp start (C)"),
    ("l_temp_motor_end", "Motor temp end (C)"),
    ("foc_motor_r", "Motor resistance (Ohm)"),
    ("foc_motor_l", "Motor inductance (H)"),
    ("foc_motor_flux_linkage", "Flux linkage (Wb)"),
    ("si_motor_poles", "Motor poles"),
    ("si_gear_ratio", "Gear ratio"),
    ("si_wheel_diameter", "Wheel diameter (m)"),
    ("si_battery_cells", "Battery cells (S)"),
    ("si_battery_ah", "Battery capacity (Ah)"),
]

APP_KEYS = [
    ("controller_id", "CAN controller ID"),
    ("app_to_use", "App to use"),
    ("can_baud_rate", "CAN baud rate (enum)"),
    ("send_can_status", "CAN status messages (enum)"),
    ("send_can_status_rate_hz", "CAN status rate (Hz)"),
    ("shutdown_mode", "Shutdown mode (enum)"),
    ("app_adc_conf.ctrl_type", "ADC control type (enum)"),
    ("app_adc_conf.throttle_exp", "ADC throttle expo"),
    ("app_adc_conf.throttle_exp_brake", "ADC brake expo"),
    ("app_uart_baudrate", "UART baud rate"),
]

APP_TO_USE = {
    "0": "None", "1": "PPM", "2": "ADC", "3": "UART", "4": "PPM + UART",
    "5": "ADC + UART", "6": "Nunchuk", "7": "NRF", "8": "Custom", "9": "Balance",
}


def load(path):
    """Return a flat {tag: text} dict for a VESC Tool XML export."""
    root = ET.parse(path).getroot()
    return {child.tag: (child.text or "").strip() for child in root}


def num(conf, key):
    try:
        return float(conf[key])
    except (KeyError, ValueError):
        return None


def config_set(directory):
    """Map controller id -> {'motor': dict, 'app': dict, 'files': [...]}."""
    controllers = {}
    for path in sorted(Path(directory).glob("id*-*.xml")):
        cid, kind = path.stem[2:].split("-", 1)
        entry = controllers.setdefault(cid, {"files": []})
        entry[kind] = load(path)
        entry["files"].append(path.name)
    if not controllers:
        sys.exit(f"no id<NN>-motor.xml / id<NN>-app.xml files in {directory}")
    return controllers


def fmt(value):
    return "–" if value is None or value == "" else value


def cmd_summary(directory):
    ctrls = config_set(directory)
    ids = sorted(ctrls)
    header = "| Setting | " + " | ".join(f"ID {i}" for i in ids) + " |"
    print(header)
    print("|" + "---|" * (len(ids) + 1))
    for kind, keys in (("app", APP_KEYS), ("motor", MOTOR_KEYS)):
        for key, label in keys:
            row = []
            for i in ids:
                value = ctrls[i].get(kind, {}).get(key)
                if key == "app_to_use" and value is not None:
                    value = f"{value} ({APP_TO_USE.get(value, '?')})"
                row.append(fmt(value))
            print(f"| {label} | " + " | ".join(row) + " |")


def cmd_diff(a, b):
    left, right = load(a), load(b)
    changed = [k for k in sorted(set(left) | set(right)) if left.get(k) != right.get(k)]
    if not changed:
        print("identical")
        return
    width = max(len(k) for k in changed)
    for k in changed:
        print(f"{k:<{width}}  {fmt(left.get(k)):>14}  ->  {fmt(right.get(k))}")


def cmd_check(directory):
    ctrls = config_set(directory)
    n = len(ctrls)
    problems = []   # (level, message)

    def warn(msg):
        problems.append(("WARN", msg))

    def fail(msg):
        problems.append(("FAIL", msg))

    pack_max_v = SERIES * CELL_MAX_V
    if pack_max_v > CONTROLLER_MAX_V:
        fail(f"full pack {pack_max_v:.1f} V exceeds controller rating {CONTROLLER_MAX_V} V")

    total_in = total_regen = 0.0
    ids_seen = set()
    for cid, c in sorted(ctrls.items()):
        m, a = c.get("motor"), c.get("app")
        tag = f"ID {cid}"
        if m is None or a is None:
            fail(f"{tag}: needs both a motor and an app config (found {c['files']})")
            continue

        app_id = a.get("controller_id")
        if app_id != cid:
            fail(f"{tag}: file name says ID {cid} but app config has controller_id {app_id}")
        if app_id in ids_seen:
            fail(f"{tag}: duplicate CAN controller_id {app_id}")
        ids_seen.add(app_id)

        cut_start, cut_end = num(m, "l_battery_cut_start"), num(m, "l_battery_cut_end")
        if cut_start is not None and cut_end is not None:
            if cut_start <= cut_end:
                fail(f"{tag}: battery cutoff start {cut_start} V must be above end {cut_end} V")
            bms_worst = SERIES * (BMS_UNDERVOLT_CELL_V + BMS_UNDERVOLT_TOL_V)
            if cut_end <= SERIES * BMS_UNDERVOLT_CELL_V:
                fail(f"{tag}: cutoff end {cut_end} V is at or below the BMS cutoff "
                     f"{SERIES * BMS_UNDERVOLT_CELL_V:.1f} V; the BMS will cut power first")
            elif cut_end < bms_worst:
                warn(f"{tag}: cutoff end {cut_end} V ({cut_end / SERIES:.2f} V/cell) is within the "
                     f"BMS tolerance (up to {bms_worst:.1f} V); the BMS may cut power before the VESC")

        t_start, t_end = num(m, "l_temp_motor_start"), num(m, "l_temp_motor_end")
        if t_start is not None and t_end is not None and t_start >= t_end:
            fail(f"{tag}: motor temp start {t_start} must be below end {t_end}")

        total_in += num(m, "l_in_current_max") or 0
        total_regen += abs(num(m, "l_in_current_min") or 0)

        expected = {
            "si_battery_cells": SERIES,
            "si_battery_ah": CAPACITY_AH,
            "si_motor_poles": MOTOR_POLES,
            "si_gear_ratio": GEAR_RATIO,
        }
        for key, want in expected.items():
            got = num(m, key)
            if got is not None and got != want:
                warn(f"{tag}: {key} is {fmt(m.get(key))}, expected {want} "
                     "(affects speed, range and battery % in VESC Tool)")

    max_discharge = PARALLEL * CELL_MAX_DISCHARGE_A
    max_charge = PARALLEL * CELL_MAX_CHARGE_A
    if total_in > max_discharge:
        fail(f"combined battery current {total_in:.0f} A exceeds pack rating {max_discharge} A")
    if total_regen > max_charge:
        fail(f"combined regen current {total_regen:.0f} A exceeds pack charge rating {max_charge} A")
    elif total_regen == max_charge:
        warn(f"combined regen current {total_regen:.0f} A is exactly the pack charge rating "
             f"{max_charge} A; avoid hard braking on a full pack")

    wheels = {num(c["motor"], "si_wheel_diameter") for c in ctrls.values() if "motor" in c}
    if len(wheels) > 1:
        warn(f"controllers disagree on wheel diameter: {sorted(w for w in wheels if w is not None)}")

    print(f"Checked {n} controller(s) in {directory}")
    print(f"  combined battery current: {total_in:.0f} A (pack limit {max_discharge} A)")
    print(f"  combined regen current:   {total_regen:.0f} A (pack limit {max_charge} A)")
    for level, msg in problems:
        print(f"{level}: {msg}")
    if not problems:
        print("OK: no problems found")
    return 1 if any(level == "FAIL" for level, _ in problems) else 0


def main(argv):
    if len(argv) == 3 and argv[1] == "summary":
        cmd_summary(argv[2])
        return 0
    if len(argv) == 4 and argv[1] == "diff":
        cmd_diff(argv[2], argv[3])
        return 0
    if len(argv) == 3 and argv[1] == "check":
        return cmd_check(argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
