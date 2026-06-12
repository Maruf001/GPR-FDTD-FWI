# Field Experiment Archive

This archive is for measured, lab, public, and benchmark data experiments.
It is intentionally separate from the synthetic simulation archive:

```text
outputs/experiments/
```

The matching field tracker archive is:

```text
docs/field_experiments/
```

Use one dataset or source-family folder per data source:

```text
outputs/field_experiments/<dataset_id>/NNN_run_name
```

Run numbering is local to each dataset family. This keeps a local GSSI scan,
a public bridge-deck dataset, a lab rebar benchmark, and a synthetic FWI
benchmark from competing for one flat field-data sequence.

Raw data stay under `data/` and should not be copied into this archive.
Generated artifacts belong here: inventories, import summaries, QC figures,
minimal processed arrays, calibration reports, and field-to-synthetic bridge
experiments.

Keep three levels separate:

- Raw data: original vendor or downloaded files under `data/`.
- Minimal processed data: parser output with trace/time axes and reversible
  corrections only.
- Analysis-ready data: background removal, gain, picks, velocity estimates,
  labels, or other derived products.

Do not use these field outputs as direct 2D or 3D FWI evidence until metadata,
geometry, time-zero, velocity, and dimensionality assumptions have been
validated for the specific dataset family.
