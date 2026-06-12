# Experiment 77: Decision Figure Readiness Audit

## Purpose

Audit the run 542 decision-figure map after adding the compact run 543
objective summary. The goal is to decide whether more compact replacement
figures are needed before report assembly.

## 544: Figure Readiness Audit

Output:

```text
outputs/experiments/544_decision_figure_readiness_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
CPU-only image-stat audit of the run 542 mapped PNG files, using grayscale
dimension, dynamic-range, and aspect-ratio checks.
PY
```

Artifacts:

```text
data/decision_figure_readiness_audit.csv
data/decision_figure_readiness_audit.json
README.md
run_manifest.json
```

Audited figures:

```text
run 498: coordinate_confidence_aggregate.png
run 498: coordinate_ambiguity_widths.png
run 543: compact_objective_summary.png
run 531: coordinate_objective_diagnostic_ratios.png
run 507: coordinate_objective_diagnostic_ratios.png
run 201: two_stage_margin_summary.png
run 201: two_stage_stage_confidence_summary.png
run 201: two_stage_material_uncertainty_summary.png
run 201: two_stage_interval_runtime_summary.png
run 534: coordinate_confidence_aggregate.png
run 534: coordinate_ambiguity_widths.png
```

Metrics:

```text
figures checked: 11
report-ready candidates: 10
detail-only too-wide figures: 1
dynamic range: 255 for all audited figures
```

The only layout flag is the run 531 fitted-ringdown objective detail plot:

```text
4762x1005 px, aspect ratio 4.738, grayscale std 73.2677
```

## Interpretation

The mapped report figure set is usable after run 543. The run 531 objective
plot remains valuable as a detailed audit figure, but it is too wide to be the
primary report graphic. Run 543 should carry the objective-summary slot, with
run 532 and run 531 kept as row-level/detail audit artifacts.

The run 507 source-shape transfer plot is readable enough as-is, and the run
498, run 201, and run 534 figures all pass the basic report-readiness checks.

## Next Decision

Proceed to report assembly or citation packaging. Do not create more compact
figures unless a specific manuscript layout requires them.
