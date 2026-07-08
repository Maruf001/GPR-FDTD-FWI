# Experiment 873: Local 2D New-Hypothesis Candidate Pack, Field-176 Refresh

Date: 2026-06-25

## Purpose

Refresh the local 2D next-hypothesis queue after the field run `176`
real-archive acceptance contract and the run `139` presentation evidence-pack
refresh.

This is a CPU-only design artifact. It does not run FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/142_local_2d_new_hypothesis_candidate_pack_field176_refresh
```

Key artifacts:

```text
data/local_2d_new_hypothesis_candidate_pack.csv
data/local_2d_new_hypothesis_candidate_pack_summary.json
figures/local_2d_new_hypothesis_candidate_pack.png
docs/LOCAL_2D_NEW_HYPOTHESIS_CANDIDATE_PACK.md
scripts/run_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
scripts/test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
hypothesis candidates:               7
run-next CPU candidates:             4
design-first candidates:             2
field-blocked candidates:            1
CPU-design-ready candidates:         6
CPU-adapter-ready candidates:        2
recommended next hypothesis:         matched_2d_bem_fdtd_dielectric_cylinder_adapter
new local 2D GPU ready:              false
broad GPU queue ready:               false
detector-seeded FWI ready:           false
field transfer ready:                false
field FWI ready:                     false
GPU work ready:                      false
field real archive acceptance ready: false
presentation claim count:            44
```

Ranked next hypotheses:

| Rank | Hypothesis | Status | CPU design ready | Immediate use |
| ---: | --- | --- | --- | --- |
| 1 | matched_2d_bem_fdtd_dielectric_cylinder_adapter | run_next_cpu | true | Compare colleague 2D BEM against project FDTD on one matched receiver-line observable. |
| 2 | layered_halfspace_loss_and_time_zero_sensitivity | run_next_cpu | true | Quantify layer, loss, and time-zero effects before new FDTD sweeps. |
| 3 | receiver_aperture_windowing_stability_map | run_next_cpu | true | Separate acquisition/windowing effects from target-inversion effects. |
| 4 | source_amplitude_time_zero_perturbation_replay | run_next_cpu | true | Stress current 2D claims against amplitude and time-zero perturbations. |
| 5 | variable_radius_depth_stress_outside_fixed_lock | design_first | true | Design a new stress branch before proposing any GPU run. |
| 6 | field_packet_to_2d_prior_replay | blocked_by_field_data | false | Wait for run-176 real archive acceptance before using field priors. |
| 7 | shape_material_variant_probe_design | design_first | true | Scope non-circular/material-variant physics before compute. |

## Interpretation

The highest-value local 2D improvement remains a CPU-only matched 2D BEM/FDTD
dielectric-cylinder adapter. The field-176 refresh tightens the field bridge:
field-to-2D prior replay is no longer design-ready merely because a synthetic
archive/checksum bridge passes. It is blocked until the real archive acceptance
contract passes.

Source/time-zero, receiver-window, and layered sensitivity work remain useful
CPU branches. None of these branches opens a broad GPU, detector-FWI,
field-transfer, field-FWI, or 3D/HPC gate.

## Decision

Start the next local 2D branch from a duplicated matched-adapter script and
keep it CPU-scoped until the observable, tolerance, and BEM/FDTD comparison
pass. Do not launch a new GPU/FWI branch from the fixed-radius result, and do
not use field priors until the run `176` real archive acceptance contract
passes.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test used
for this result:

```text
scripts/run_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
scripts/test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
```

The snapshot manifest SHA-256 entries match the frozen files.

## Validation

Focused tests:

```text
tests/test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
5 passed
```

Figure check:

```text
2637x954, dynamic range=255
```

Script snapshots:

```text
run_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
sha256=e4e523307d18932c304ff49fc9a0c2cda8a9614c1ce26d2d73b93f13d0269f03

test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
sha256=8b43582645b14980dad45eb55ff31f85cbcab32fbcebb2e71046957eb0fd51f4
```
