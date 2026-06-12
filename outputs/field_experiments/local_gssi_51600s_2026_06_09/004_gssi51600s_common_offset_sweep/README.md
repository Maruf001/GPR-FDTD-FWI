# GSSI 51600S Common-Offset Hyperbola Sweep

CPU-only field-data sensitivity run for:

```text
data/2026-06-09_GSSI_model_51600S
```

This run sweeps effective transmitter/receiver offset values from 0 to 120 mm
for the short profiles 014 and 016. It is a model-sensitivity check, not a
confirmed instrument calibration.

Best profile fits:

- `PROJECT001C__014.DZT`: offset=60 mm, v=0.098 m/ns, epsr=9.45, median depth=6.5 mm, boundary warning=False
- `PROJECT001C__016.DZT`: offset=60 mm, v=0.090 m/ns, epsr=11.10, median depth=21.2 mm, boundary warning=True
