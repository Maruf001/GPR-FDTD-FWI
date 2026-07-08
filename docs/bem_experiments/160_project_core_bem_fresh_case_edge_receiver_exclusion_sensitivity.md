# BEM Experiment 160: Fresh-Case Edge Receiver Exclusion Sensitivity

Date: 2026-06-27

## Purpose

Test whether the receiver-6 residual identified in run `159` can be handled by
simply excluding edge receivers.

Run `159` showed that receiver `6` is the largest residual-energy receiver in
all three fresh project-core cases. This run checks whether dropping receiver
`6` or dropping both edge receivers closes the fresh-case comparison gap.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/160_project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity
```

Key artifacts:

```text
data/project_core_bem_fresh_case_edge_receiver_exclusion_rows.csv
data/project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity_summary.json
figures/project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity.png
docs/PROJECT_CORE_BEM_FRESH_CASE_EDGE_RECEIVER_EXCLUSION_SENSITIVITY.md
scripts/run_project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity.py
scripts/test_project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity.py
```

## Result

```text
fresh cases:                         3
receiver subsets:                    4
subset rows:                         12
strict-gate passes:                  0
all best subsets pass gate:          false
worst best case:                     shifted_deeper_epsr4
worst best subset:                   drop_receiver_6
worst best relative L2:              0.5439481056909283
edge exclusion promotes bridge:      false
receiver-edge modeling needed:       true
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Best observations:

| Case | All receivers L2 | Best deployable subset | Best subset L2 |
| --- | ---: | --- | ---: |
| lower_contrast_radius_25mm | 0.18685792461171655 | drop_edge_receivers_0_6 | 0.17570038083249712 |
| shifted_deeper_epsr4 | 0.5997321402926066 | drop_receiver_6 | 0.5439481056909283 |
| larger_high_contrast_epsr6 | 0.5119171157297535 | drop_edge_receivers_0_6 | 0.4883770407808971 |

## Interpretation

Dropping receiver `6` or both edge receivers lowers some fresh-case errors, but
no deployable subset reaches the strict `0.1` gate. Receiver exclusion would
hide part of the residual without promoting the bridge.

## Decision

Keep the project-core bridge blocked. Use the edge localization as a target for
receiver-edge modeling, not as permission to exclude receivers or promote 3D
validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity.py
3 passed
```

Figure validation:

```text
project_core_bem_fresh_case_edge_receiver_exclusion_sensitivity.png
2392x842, dynamic range=255
```
