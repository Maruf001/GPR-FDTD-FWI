# BEM Experiment 126: Fine-Mesh Comparator Mismatch Audit

Date: 2026-06-27

## Purpose

Audit the preferred nine-frequency fine-mesh BEM/FDTD comparator across
schema-valid synthetic mismatch modes.

Run `118` proved exact reconstruction, a small scattered-field scale error,
and a large scattered-field scale error. This run broadens that check to
amplitude, frequency-localized, phase, component, receiver-key, frequency-key,
common-mode, and background-subtraction mismatches.

This is a synthetic comparator audit. It does not install real FDTD returns,
run local 3D FDTD, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/126_project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_scenario_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_frequency_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_metric_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_validation_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_COMPARATOR_MISMATCH_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenario count:                  10
frequency count:                 9
receiver count:                  31
rows per scenario:               279
target synthetic rows:           2790
background synthetic rows:       2790
validation checks:               180
validation failed checks:        0
expected pass scenarios:         3
expected fail scenarios:         7
observed pass scenarios:         3
observed fail scenarios:         7
unexpected outcomes:             0
pass threshold relative L2:      0.1
mismatch audit ready:            true
real FDTD data ready:            false
real BEM/FDTD comparison ready:  false
3D validation claim ready:       false
gpu/hpc ready:                   false
```

Scenario summary:

| Scenario | Class | Max relative L2 | Expected pass | Observed pass |
| --- | --- | ---: | --- | --- |
| exact_control | control | 8.942279382796571e-15 | true | true |
| small_scattered_scale_error | amplitude | 0.0500000000000035 | true | true |
| bad_scattered_scale_error | amplitude | 0.30000000000000254 | false | false |
| localized_high_frequency_scale_error | localized_frequency | 0.300000000000001 | false | false |
| quadrature_phase_error | phase | 1.4142135623730971 | false | false |
| ey_component_sign_error | component | 1.999999944539111 | false | false |
| receiver_reverse_scatter_assignment | geometry_keying | 1.3888444346290052 | false | false |
| frequency_shift_scatter_assignment | frequency_keying | 5.205076894730209 | false | false |
| common_mode_background_bias_cancels | common_mode | 8.942279382796571e-15 | true | true |
| background_only_bias_error | background_subtraction | 1.0716891488389093 | false | false |

## Interpretation

The fine-mesh comparator catches the schema-valid mismatch modes that should
change the recovered scattered field: large amplitude error, high-frequency
localized amplitude error, phase rotation, component sign error, receiver-key
assignment error, frequency-key assignment error, and target/background
background-subtraction bias.

The common-mode bias scenario passes because the same incident-field bias is
added to both target and background, so target-minus-background subtraction
cancels it. That is expected comparator behavior, not real 3D validation.

## Decision

Use this audit as mismatch-mode evidence for the preferred nine-bin BEM/FDTD
comparison gate. Keep real BEM/FDTD comparison and 3D validation blocked until
returned external FDTD target, background, and metadata files pass the real
preflight.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit.png
3130x912, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit.py
sha256=5af301731445f804df454203c8824100b0c88e5853299230ec696080cd587af2

tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_mismatch_audit.py
sha256=78fcaf23c54739e676e35e802f25d4ed65468f49def53e12b6408be670f94071
```
