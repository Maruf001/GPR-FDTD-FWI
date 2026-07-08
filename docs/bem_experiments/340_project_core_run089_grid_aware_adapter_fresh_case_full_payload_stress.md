# BEM Experiment 340: Fresh-Case Full-Payload Stress

Date: 2026-06-28

## Purpose

Duplicate the run `094` fresh homogeneous stress path and save the full
formula-replay payload for each fresh case.

Runs `337-339` showed that run `094` passed numerically but could not be
independently replayed from the saved arrays because three formula inputs were
missing. This run closes that artifact gap by saving Tx background fields, Rx
background fields, and the source spectrum for each fresh case, along with the
existing adapter and FDTD comparison arrays.

This is a CPU-only project-core BEM/FDTD adapter run. It does not launch GPU or
HPC work, use field data, use the synthetic 2D archive, run field FWI, or make a
field-transfer claim.

## Output

```text
outputs/bem_experiments/340_project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress_case_summary.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress_payload_completeness.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress_payload_shapes.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress_arrays.npz
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress_summary.json
figures/project_core_run089_grid_aware_adapter_fresh_case_full_payload_stress.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_FRESH_CASE_FULL_PAYLOAD_STRESS.md
```

## Expected Result

The run is expected to reproduce the run `094` three-case numerical pass while
saving all replay items for each case:

```text
selected_indices
selected_frequencies_hz
target_x_m
target_z_m
target_weights
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
adapter_output_frequency_bins
fdtd_scattered_frequency_bins
adapter_band
fdtd_band
```

## Decision Rule

If all three fresh cases pass and all required replay items are saved for every
case, the next branch should independently replay the saved run `340` payloads.
No field transfer, 3D validation, GPU escalation, or field FWI is justified by
this run alone.
