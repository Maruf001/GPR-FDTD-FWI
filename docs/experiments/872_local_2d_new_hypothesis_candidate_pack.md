# Experiment 872: Local 2D New-Hypothesis Candidate Pack

Date: 2026-06-25

## Purpose

Turn the design-needed local 2D branch from run `136` into concrete next
hypotheses, while preserving the current no-go gates for broad GPU work,
detector-seeded FWI, field transfer, and field FWI.

This is a CPU-only design artifact. It does not run FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/138_local_2d_new_hypothesis_candidate_pack
```

Key artifacts:

```text
data/local_2d_new_hypothesis_candidate_pack.csv
data/local_2d_new_hypothesis_candidate_pack_summary.json
figures/local_2d_new_hypothesis_candidate_pack.png
docs/LOCAL_2D_NEW_HYPOTHESIS_CANDIDATE_PACK.md
scripts/run_local_2d_new_hypothesis_candidate_pack.py
scripts/test_local_2d_new_hypothesis_candidate_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
hypothesis candidates:               7
run-next CPU candidates:             4
design-first candidates:             2
field-blocked candidates:            1
CPU-design-ready candidates:         7
CPU-adapter-ready candidates:        2
recommended next hypothesis:         matched_2d_bem_fdtd_dielectric_cylinder_adapter
new local 2D GPU ready:              false
broad GPU queue ready:               false
detector-seeded FWI ready:           false
field transfer ready:                false
field FWI ready:                     false
GPU work ready:                      false
```

Ranked next hypotheses:

| Rank | Hypothesis | Status | Score | Immediate use |
| ---: | --- | --- | ---: | --- |
| 1 | matched_2d_bem_fdtd_dielectric_cylinder_adapter | run_next_cpu | 23.0 | Compare colleague 2D BEM against project FDTD on one matched receiver-line observable. |
| 2 | layered_halfspace_loss_and_time_zero_sensitivity | run_next_cpu | 15.0 | Quantify layer, loss, and time-zero effects before new FDTD sweeps. |
| 3 | receiver_aperture_windowing_stability_map | run_next_cpu | 15.0 | Separate acquisition/windowing effects from target-inversion effects. |
| 4 | source_amplitude_time_zero_perturbation_replay | run_next_cpu | 15.0 | Stress current 2D claims against amplitude and time-zero perturbations. |
| 5 | field_packet_to_2d_prior_replay | blocked_by_field_data | 8.0 | Wait for real field files to pass archive/provenance gates. |
| 6 | variable_radius_depth_stress_outside_fixed_lock | design_first | 6.0 | Design a new stress branch before proposing any GPU run. |
| 7 | shape_material_variant_probe_design | design_first | 3.0 | Scope non-circular/material-variant physics before compute. |

## Interpretation

The highest-value local 2D improvement is not another fixed-radius GPU probe.
It is a CPU-only matched 2D BEM/FDTD dielectric-cylinder adapter that compares
the colleague BEM reference against the project FDTD observable under the same
geometry, material, source, receiver line, and measured quantity.

Source/time-zero, receiver-window, and layered sensitivity work are also useful
CPU branches. None of those branches opens a broad GPU, detector-FWI,
field-transfer, or field-FWI gate.

## Decision

Start the next local 2D branch from a duplicated matched-adapter script and keep
it CPU-scoped until the observable, tolerance, and BEM/FDTD comparison pass. Do
not launch a new GPU/FWI branch from the fixed-radius result.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test used
for this result:

```text
scripts/run_local_2d_new_hypothesis_candidate_pack.py
scripts/test_local_2d_new_hypothesis_candidate_pack.py
```

The snapshot manifest SHA-256 entries match the frozen files.

## Validation

Focused tests:

```text
tests/test_local_2d_new_hypothesis_candidate_pack.py
4 passed
```

Figure check:

```text
2637x954, dynamic range=255
```
