# Experiment 69: Single-Rebar Shallow r=4 Reporting Handoff

## Purpose

Package the shallow single-rebar r=4 mm reporting decision into a compact
artifact. This branch is location-correct and nominal-radius-correct, but the
radius should remain interval-supported under material/source uncertainty.

## 536: Shallow r=4 Reporting Handoff

Output:

```text
outputs/experiments/536_single_rebar_shallow_r4_reporting_handoff
```

Artifacts:

```text
README.md
data/shallow_r4_reporting_handoff.json
run_manifest.json
```

Decision:

```text
nominal point radius: 4.0 mm
packaged material/source-aware interval: 3.95-4.05 mm
broader fine-grid diagnostic interval: about 3.925-4.100 mm
high-precision point-radius claim without nuisance calibration: rejected
```

Evidence summary:

| Evidence | r=4 result | r=8 control |
| --- | --- | --- |
| Run 197 | nominal r=4.0 mm; material best r=4.05 mm; material interval 3.95-4.10 mm | nominal/material best r=8.0 mm; material interval 8.0-8.05 mm |
| Run 201 | final r=4.0 mm; material/source interval 3.95-4.05 mm | final r=8.0 mm; material/source interval 8.0-8.05 mm |

Interpretation:

```text
The shallow r=4 point estimate is stable under the nominal high-band stage, but
material/source nuisance profiling shifts the reporting radius enough to require
an interval. The deeper r=8 control is less sensitive.
```

## Next Decision

Use run 536 as the compact citation for shallow/small-radius single-rebar
interval reporting. Future work should extend nuisance-aware interval reporting
only where ambiguity appears, not make free material parameters a default
optimizer dimension.
