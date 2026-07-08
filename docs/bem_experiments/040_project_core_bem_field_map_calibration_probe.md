# BEM Experiment 040: Field-Map Calibration Probe

Date: 2026-06-25

## Purpose

Test whether the run `039` BEM-compatible analytic-field gap can be closed by a
low-dimensional mixture of analytic field products under leave-one-scan-position
validation.

This is a CPU-only calibration probe using saved run `036` arrays and the
colleague-provided `scarep` analytic Green function. It does not run FDTD time
stepping, field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/040_project_core_bem_field_map_calibration_probe
```

Key artifacts:

```text
data/project_core_bem_field_map_calibration_probe.csv
data/project_core_bem_field_map_calibration_probe_summary.json
figures/project_core_bem_field_map_calibration_probe.png
docs/PROJECT_CORE_BEM_FIELD_MAP_CALIBRATION_PROBE.md
```

## Result

```text
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
cases checked:                      3
mixture variants:                   analytic_product_div_source+analytic_receiver_conjugate_div_source
worst best-single analytic L2:      0.8309901396143111
worst all-scan mixture L2:          0.6280658438481003
worst leave-one-scan mixture L2:    0.9869554402632811
field-map calibration ready:        false
project-grid best worst L2:         0.44601690298659386
uses colleague scarep Green:        true
gpu required:                       false
```

Metrics:

| epsr | Project-grid L2 | Best single analytic L2 | All-scan mixture L2 | Leave-one-scan mixture L2 | Ready |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1.25 | 0.0989465314024021 | 0.8309901396143111 | 0.6280658438481003 | 0.9869554402632811 | false |
| 2.0 | 0.23018542478328735 | 0.784781796009896 | 0.5937429054816376 | 0.9639936912388861 | false |
| 4.0 | 0.44601690298659386 | 0.5743454280440946 | 0.4625721668098588 | 0.7639130639563865 | false |

## Interpretation

The all-scan mixture can fit below the 0.75 adapter gate, but the held-out
scan-position test fails. This means the run `039` gap is not just a simple
two-term field convention problem that transfers across nearby scan positions.

The active BEM/project-core blocker is a deeper finite-domain or project-grid
Green-field mismatch at the target cells.

## Decision

Do not promote the analytic field-map. The next branch should construct or
learn a project-domain Green surface at target cells, then retest the same
adapter gates.

## Validation

```text
python -m py_compile run_project_core_bem_field_map_calibration_probe.py
python run_project_core_bem_field_map_calibration_probe.py
```

Figure check:

```text
project_core_bem_field_map_calibration_probe.png: 1925x769, dynamic range=255
```
