# BEM Experiment 026: Project-Core Arrival-Window Direct-Wave Audit

Date: 2026-06-24

## Purpose

Test whether the direct-wave transfer failure from run `023` is mostly caused
by late-time finite-domain or boundary content in the saved project-core FDTD
traces.

This run applies Gaussian windows centered on the expected direct arrival and
recomputes source-scale transfer metrics. It does not launch a new FDTD solve.

## Output

```text
outputs/bem_experiments/026_project_core_arrival_window_direct_wave_audit
```

Key artifacts:

```text
data/arrival_window_direct_wave_summary.json
data/arrival_window_direct_wave_metrics.csv
figures/arrival_window_direct_wave_metrics.png
docs/ARRIVAL_WINDOW_DIRECT_WAVE_AUDIT.md
```

## Result

```text
source run:                    outputs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit
full all-pair symmetric L2:    1.6206668574552758
best all-pair symmetric L2:    1.6206668574552758
full reference-transfer L2:    1.346364319602316
best reference-transfer L2:    1.3229455481578225
arrival window improves gate:  false
```

Window diagnostics:

| Window | Sigma (ns) | All-pair symmetric L2 | Reference-transfer symmetric L2 |
| --- | ---: | ---: | ---: |
| full | 0.0 | 1.6206668574552758 | 1.346364319602316 |
| gaussian arrival | 0.2 | 1.6472933942179502 | 1.3229455481578225 |
| gaussian arrival | 0.35 | 1.6517367973628811 | 1.3265125713408745 |
| gaussian arrival | 0.5 | 1.6532054833503376 | 1.3283225469085913 |
| gaussian arrival | 0.75 | 1.6555219857958354 | 1.3304330265766386 |
| gaussian arrival | 1.0 | 1.6594946241150086 | 1.3326904402030912 |
| gaussian arrival | 1.5 | 1.6682973055216317 | 1.3377716980248473 |
| gaussian arrival | 2.0 | 1.6722836254206648 | 1.342199673549215 |

## Interpretation

Arrival-windowing does not repair the direct-wave transfer gate. The mismatch
is therefore not mainly explained by late-time finite-domain or boundary
content in the saved traces.

## Decision

Keep the bridge blocker assigned to source/receiver formulation or
scattered-field calibration, not to simple time-window cleanup.

## Validation

```text
python -m py_compile run_project_core_arrival_window_direct_wave_audit.py
conda run -n gpr-fdtd-fwi python run_project_core_arrival_window_direct_wave_audit.py
```

Figure check:

```text
1 PNG figure, nonblank dynamic range, 1492x738
```
