# CLAUDE.md

Documentation and config repo for a DIY 12S5P battery pack and dual VESC controller in a Boosted Rev scooter.
There is no application code. The only script is `scripts/vesc_check.py`, which uses the Python standard library.

## Git workflow

- **Commit and push directly to `main`.** The owner allows this for this repo. No feature branch or pull request is needed.
- Use conventional commit prefixes as in the existing history: `feat:`, `fix:`, `doc:`, `chore:`, `refactor:`.
- Rename binaries with `git mv` so history follows them.

## Layout

- `docs/`: reference docs. `battery.md`, `controller.md`, `maintenance.md`, `tools.md`.
- `log/`: dated records. `controller.md` holds hardware, config history, motor detection history and faults. `maintenance.md` holds work done and battery health.
- `vesc/<hardware>/id<CAN ID>-<motor|app>.xml`: VESC Tool exports. `hd60t/` is current, `stormcore-60d/` is the previous controller.
- `diagrams/`, `datasheets/`, `manuals/`, `images/`: binary reference material. File names are lowercase and hyphenated.

## Conventions

- VESC XML files are exported by VESC Tool. Do not hand-edit them. Describe a suggested setting change in `docs/controller.md` instead and let the owner write it to the controller.
- When VESC configs change, run `python3 scripts/vesc_check.py check vesc/hd60t` and add a line to the config history in `log/controller.md`. If motor detection values changed, add a line to the detection history too.
- Pack and hardware limits live in two places: `docs/battery.md` and the constants at the top of `scripts/vesc_check.py`. Keep them in sync.
- Logs are newest first. Mark unknown values as "unknown" rather than guessing.
- Diagram PNGs are rendered from the PDF with `pdftoppm -r 60 -png -singlefile diagrams/<name>.pdf diagrams/<name>`.
