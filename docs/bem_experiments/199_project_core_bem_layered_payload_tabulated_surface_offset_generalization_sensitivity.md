# BEM Experiment 199: Tabulated Surface Offset Generalization Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the run `198` offset-generalization validator with damaged variants
of the run `197` generalized tabulated-surface repair.

This is a CPU-only sensitivity run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/199_project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_OFFSET_GENERALIZATION_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity.py
```

## Result

```text
sensitivity scenarios:              10
expected pass scenarios:             1
observed pass scenarios:             1
expected failure scenarios:          9
observed failure scenarios:          9
unexpected outcomes:                 0
offset-generalization sensitivity:   true
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

The exact run `197` result passes. These damaged variants fail as expected:

| Scenario | Failed check family |
| --- | --- |
| Missing offset case | Case count, row count, ready row count |
| Case without ready support | Ready row count and every-case-ready check |
| Held-out extrapolation present | No-extrapolation check |
| Wrong worst best case | Worst-case identity check |
| Worst best L2 above gate | Worst-case L2 gate check |
| Negative worst best margin | Positive-margin check |
| Generalization marked not ready | Generalization/refresh state check |
| Contract refresh marked ready | Generalization/refresh state check |
| Field transfer marked ready | Field/3D/GPU blocked-state check |

## Interpretation

The run `198` validator is sensitive to the main ways the generalized
tabulated-surface repair could be corrupted or overstated: missing case
coverage, a case without a ready support, held-out extrapolation, wrong
worst-case metrics, and premature promotion flags.

This completes the guarded generalized tabulated-surface repair package for the
35 mm offset family. It still does not refresh the analytic BEM contract and
does not make field or 3D claims.

## Decision

Use runs `197`-`199` as the guarded generalized tabulated-surface repair
package. Keep analytic contract refresh, field transfer, 3D validation,
GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion blocked until
scope and claim language are refreshed deliberately.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization.py
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.py
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity.py
12 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_offset_generalization_sensitivity.png
2789x865, dynamic range=255
```
