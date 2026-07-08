# BEM Experiment 412: 35-Field Synthetic Packet Comparator-Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `411` validator with damaged variants of the run `410`
comparator smoke.

## Output

```text
outputs/bem_experiments/412_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke_validation_sensitivity
```

## Result

```text
scenarios:                            15
expected pass:                        1
observed pass:                        1
expected failures:                    14
observed failures:                    14
unexpected outcomes:                  0
sensitivity ready:                    true
accepts exact run 410:                true
rejects damaged variants:             true
paired keys:                          279
receivers:                            31
frequencies:                          9
scattered rows:                       279
scattered component cells:            1674
synthetic packet is evidence:         false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
GPU/HPC ready:                        false
```

Damaged variants fail for source-label drift, consumer-count drift,
row-count drift, receiver-count drift, source-preflight demotion,
consumer-check failure, scattered-row removal, frequency-row removal, norm
drift, coordinate drift, false evidence promotion, downstream promotion,
figure drift, and script-snapshot drift.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_packet_comparator_smoke_validation_sensitivity.py
8 passed
```

Figure validation:

```text
3545x877, dynamic range=255
```
