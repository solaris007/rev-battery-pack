# VESC Configs

VESC Tool XML exports. One directory per controller hardware or config generation, one file per CAN ID and config type.

| Directory | Hardware | Status |
|---|---|---|
| `hd60t/` | Trampa VESC HD60T | Last used, failed 2026-04. Reference for the replacement |
| `hd60t-2021/` | Trampa VESC HD60T, older config format from 2021 | Previous, reference only |

The Stormcore 60D+ configs of November 2021 survive only in the git history of `hd60t-2021/`. See the note in the [config history](../log/controller.md#config-history).

A new controller gets its own directory and an entry in `HARDWARE_MAX_V` in `scripts/vesc_check.py`.

File names follow `id<CAN ID>-<motor|app>.xml`. Keep that pattern, because `scripts/vesc_check.py` relies on it.

After exporting new configs, run the checker and log the change:

```
python3 scripts/vesc_check.py check vesc/hd60t
```

See [docs/controller.md](../docs/controller.md) for the CAN layout and procedure, and [log/controller.md](../log/controller.md) for the history.
