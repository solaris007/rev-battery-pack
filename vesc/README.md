# VESC Configs

VESC Tool XML exports. One directory per controller hardware, one file per CAN ID and config type.

| Directory | Hardware | Status |
|---|---|---|
| `hd60t/` | Trampa VESC HD60T | Current |
| `stormcore-60d/` | Stormcore 60D+ | Previous, reference only |

File names follow `id<CAN ID>-<motor|app>.xml`. Keep that pattern, because `scripts/vesc_check.py` relies on it.

After exporting new configs, run the checker and log the change:

```
python3 scripts/vesc_check.py check vesc/hd60t
```

See [docs/controller.md](../docs/controller.md) for the CAN layout and procedure, and [log/controller.md](../log/controller.md) for the history.
