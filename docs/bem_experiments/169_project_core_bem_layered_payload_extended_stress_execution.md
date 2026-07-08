# BEM Experiment 169: Layered Payload Extended Stress Execution

Date: 2026-06-27

## Purpose

Execute the run `168` extended layered stress ladder for the scoped layered
payload branch.

This run reruns local CPU project-core FDTD/BEM adapter comparisons for the
four extended layered cases. It does not compare against field data, launch
GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/169_project_core_bem_layered_payload_extended_stress_execution
```

Key artifacts:

```text
data/project_core_bem_layered_payload_extended_stress_cases.csv
data/project_core_bem_layered_payload_extended_stress_all_scan_metrics.csv
data/project_core_bem_layered_payload_extended_stress_leave_one_metrics.csv
data/project_core_bem_layered_payload_extended_stress_execution_summary.json
figures/project_core_bem_layered_payload_extended_stress_execution.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_EXTENDED_STRESS_EXECUTION.md
scripts/run_project_core_bem_layered_payload_extended_stress_execution.py
scripts/test_project_core_bem_layered_payload_extended_stress_execution.py
```

## Result

```text
source design ready:                 true
case count:                          4
passed cases:                        3
failed cases:                        1
worst case:                          larger_radius_epsr9
worst leave-one L2:                  0.7745663063852277
extended layered stress ready:       false
field transfer ready:                false
3D validation ready:                 false
GPU required:                        false
```

| Case | Target cells | Best leave-one L2 | Ready | Note |
| --- | ---: | ---: | --- | --- |
| shallow_z_epsr9 | 526 | 0.678333487523724 | true | passes |
| larger_radius_epsr9 | 1013 | 0.7745663063852277 | false | fails the 0.75 gate |
| low_contrast_epsr6 | 0 | 0.0 | true | degenerate zero-target case |
| high_interface_epsr12 | 533 | 0.5738072739328918 | true | passes |

## Interpretation

The extended layered payload branch does not pass as designed. The larger-
radius case fails the leave-one-scan gate, and the low-contrast case is
degenerate because target permittivity equals the lower-halfspace permittivity,
producing zero target cells.

## Decision

Do not promote the layered payload beyond the previous scoped stress boundary.
Repair the extended stress design before drawing a broader layered conclusion.
Keep measured-field transfer, project-core bridge promotion, 3D validation,
GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_extended_stress_execution.py
3 passed
```

Figure validation:

```text
project_core_bem_layered_payload_extended_stress_execution.png
2579x721, dynamic range=255
```
