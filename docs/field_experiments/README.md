# Field Experiment Trackers

This folder tracks measured, lab, public, and benchmark-data experiments.
It is separate from the synthetic simulation tracker archive:

```text
docs/experiments/
```

Use one dataset or source-family folder per data source:

```text
docs/field_experiments/<dataset_id>/NNN_run_name.md
```

The matching output convention is:

```text
outputs/field_experiments/<dataset_id>/NNN_run_name
```

Run numbering is local to each dataset family. This keeps local GSSI DZT/DZX
work, public lab rebar datasets, public field `.dt` datasets, bridge-deck
datasets, controlled test-site radargrams, and synthetic FWI benchmarks from
sharing one flat field-data sequence.

Each tracker should include:

- Data source and raw data path or DOI.
- Import/parser status and software versions.
- Output path and command.
- Metadata extracted: traces, samples, time axis, scan spacing, antenna, labels.
- QC figures and figure notes.
- Calibration or dimensionality assumptions.
- Decision on whether the data are ready for synthetic comparison, 2D FWI, or
  only further QC.
