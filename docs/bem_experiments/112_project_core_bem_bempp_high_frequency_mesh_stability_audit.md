# BEM Experiment 112: Bempp High-Frequency Mesh-Stability Audit

Date: 2026-06-27

## Purpose

Check mesh stability at the high-frequency end of the run `111` Bempp grid.

Run `106` showed that the 6x16 baseline mesh was close to the 8x20 fine mesh at
0.5 and 1.5 GHz. Run `111` then extended the locked BEM prototype to 3.0 GHz.
This run tests whether the high-frequency response is still converging under
surface-mesh refinement.

This run does not run 3D FDTD, validate against real FDTD returns, model
layered 3D GPR, use field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/112_project_core_bem_bempp_high_frequency_mesh_stability_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_high_frequency_mesh_stability_cases.csv
data/project_core_bem_bempp_high_frequency_mesh_stability_frequency_summary.csv
data/project_core_bem_bempp_high_frequency_mesh_stability_receivers.csv
data/project_core_bem_bempp_high_frequency_mesh_stability_comparisons.csv
data/project_core_bem_bempp_high_frequency_mesh_stability_audit_summary.json
figures/project_core_bem_bempp_high_frequency_mesh_stability_audit.png
docs/PROJECT_CORE_BEM_BEMPP_HIGH_FREQUENCY_MESH_STABILITY_AUDIT.md
scripts/run_project_core_bem_bempp_high_frequency_mesh_stability_audit.py
scripts/test_project_core_bem_bempp_high_frequency_mesh_stability_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
mesh cases:                         3
frequencies checked:                2
receiver rows:                      186
comparison rows:                    6
finite all responses:               true
Bempp return codes all zero:        true
baseline-to-fine max relative L2:   0.055639649360411644
baseline-to-fine max shape L2:      0.008752001112977892
fine-to-extra-fine max relative L2: 0.009408458305433572
baseline-to-extra max relative L2:  0.06551202021589525
refinement change decreases:        true
high-frequency mesh audit passed:   true
3D FDTD validation ready:           false
layered 3D GPR model ready:         false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Mesh comparisons:

| Frequency GHz | Left mesh | Right mesh | Relative L2 | Shape L2 | Peak ratio |
| ---: | --- | --- | ---: | ---: | ---: |
| 2.5 | baseline_6x16 | fine_8x20 | 0.0070932339277239055 | 0.002288571202184213 | 1.009640708824403 |
| 2.5 | fine_8x20 | extra_fine_10x24 | 0.0033092744085297713 | 0.00105754024884693 | 1.0044160628719978 |
| 2.5 | baseline_6x16 | extra_fine_10x24 | 0.010424404542687907 | 0.0033451606379378586 | 1.0140993456727 |
| 3.0 | baseline_6x16 | fine_8x20 | 0.055639649360411644 | 0.008752001112977892 | 1.0624430903149282 |
| 3.0 | fine_8x20 | extra_fine_10x24 | 0.009408458305433572 | 0.0006367040030918232 | 1.0095585117101868 |
| 3.0 | baseline_6x16 | extra_fine_10x24 | 0.06551202021589525 | 0.009263960833023761 | 1.0725984650351104 |

## Interpretation

The high-frequency BEM response is finite and refining in the right direction.
The 3.0 GHz baseline 6x16 mesh is no longer as close to the fine mesh as it was
at lower frequencies, but the 8x20 to 10x24 comparison is much smaller. That
means the high-frequency response is not obviously diverging; it is converging
with mesh refinement.

For high-frequency BEM/FDTD comparison, the 8x20 or finer mesh is the safer
reference than the 6x16 baseline. The 6x16 mesh remains useful for fast
source/receiver convention work, but 3.0 GHz validation should not rely on it
as the only BEM-side reference.

## Decision

Use run `112` as the high-frequency mesh-stability companion to run `111`.

Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR modeling, field
FWI, and GPU/HPC work blocked until real target/background FDTD returns pass
the upgraded metadata and frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_bempp_high_frequency_mesh_stability_audit.py
sha256: 7d97acf15ee7b8fd878a595fc74890ba81ea508e1f60850d4c9335cfcf36f06f

test_project_core_bem_bempp_high_frequency_mesh_stability_audit.py
sha256: 4b87a74af494e2a3e6c14d7112d765b3ef85d7381abb864d639ecefd32de9f37
```

Subsequent related BEM high-frequency experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_high_frequency_mesh_stability_audit.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_high_frequency_mesh_stability_audit.png
2644x845, dynamic range=255
```
