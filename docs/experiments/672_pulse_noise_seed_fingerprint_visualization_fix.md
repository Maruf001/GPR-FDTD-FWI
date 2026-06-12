# Pulse/Noise Seed Fingerprint Visualization Fix

Date: 2026-06-10 19:08 PDT

## Purpose

The original `source_pulse_noise_context.png` panels made seed-labelled runs
look too similar because the noise proxy was normalized independently from the
source and combined traces. That hid the actual noise scale and did not give a
clear visual handle for what a seed changes.

The reusable script now separates the concepts:

- Source pulse and spectrum panels: normalized for pulse/ringdown shape.
- Pulse plus noise panel: clean source, noise, and combined proxy on one
  source-peak amplitude scale.
- Seed fingerprint panel: Gaussian noise divided by its configured standard
  deviation, with fixed y limits.
- Distribution panel: standardized sample histogram against an ideal normal
  density.

The metadata summary now records `schema_version: 2`, the seed role, the first
16 standardized fingerprint samples, percentiles, and validation sampling
details. The seed meaning shown in the figure is: the seed selects a repeatable
Gaussian sample realization; it does not change the source pulse shape or the
Gaussian noise distribution.

## Commands

Sample regenerated for the user-inspected run:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --summary outputs/experiments/850_coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown049375_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

The first broad refresh was interrupted after some compatible runs were already
rewritten with the improved figure design. After the user clarified that
existing figures can be kept, the refresh process was stopped and a
skip-existing audit was run instead:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --backfill-root outputs/experiments \
  --max-run-number 1133 \
  --audit-json outputs/visualization_audits/20260610/pulse_noise_seed_fingerprint_skip_existing_audit_20260610.json \
  --audit-csv outputs/visualization_audits/20260610/pulse_noise_seed_fingerprint_skip_existing_audit_20260610.csv
```

Run 1134 was excluded because a coordinate optimizer was active while this
audit was run.

## Results

- Compatible runs with `source_pulse_noise_context.png`: 538.
- Compatible runs with `source_pulse_noise_context_summary.json`: 538.
- Summaries already rewritten with the new seed-fingerprint schema: 55.
- Existing summaries intentionally kept from the earlier design: 483.
- Skip-existing audit rows through run 1133: 1133.
- Audit status counts: `skipped=1133`.
- Skip reasons: 538 existing valid pulse/noise artifacts, 595 no compatible
  coordinate optimizer summary.

Audit files:

- `outputs/visualization_audits/20260610/pulse_noise_seed_fingerprint_skip_existing_audit_20260610.json`
- `outputs/visualization_audits/20260610/pulse_noise_seed_fingerprint_skip_existing_audit_20260610.csv`

## Validation

Focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_experiment_context_visualizations.py
```

Result: `7 passed`.

The pulse/noise PNG validator now samples pixels for unique-color and nonwhite
checks to keep batch audits practical for hundreds of large figures while still
catching blank or degenerate outputs.
