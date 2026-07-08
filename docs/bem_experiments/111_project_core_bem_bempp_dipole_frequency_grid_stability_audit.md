# BEM Experiment 111: Bempp Dipole Frequency-Grid Stability Audit

Date: 2026-06-27

## Purpose

Audit the locked 3D Bempp dipole prototype over a denser frequency grid.

Runs `106`-`108` fixed the current BEM-side mesh, source, and receiver
conventions. Run `110` made those conventions part of the external-return
metadata gate. This run checks whether the locked BEM prototype remains finite
and numerically usable from 0.4 GHz to 3.0 GHz.

This run does not run 3D FDTD, validate against real FDTD returns, model
layered 3D GPR, use field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/111_project_core_bem_bempp_dipole_frequency_grid_stability_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_dipole_frequency_grid_rows.csv
data/project_core_bem_bempp_dipole_frequency_grid_receiver_rows.csv
data/project_core_bem_bempp_dipole_frequency_grid_adjacent_comparison.csv
data/project_core_bem_bempp_dipole_frequency_grid_stability_audit_summary.json
figures/project_core_bem_bempp_dipole_frequency_grid_stability_audit.png
docs/PROJECT_CORE_BEM_BEMPP_DIPOLE_FREQUENCY_GRID_STABILITY_AUDIT.md
scripts/run_project_core_bem_bempp_dipole_frequency_grid_stability_audit.py
scripts/test_project_core_bem_bempp_dipole_frequency_grid_stability_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frequencies tested:                  9
receiver rows:                       279
adjacent frequency comparisons:      8
finite frequencies:                  9
all frequencies finite:              true
max adjacent relative L2:            3.36970569842619
max adjacent normalized shape L2:    0.06658931539243934
mean adjacent normalized shape L2:   0.021373160110717757
peak receiver y min:                 -0.005333333333333343 m
peak receiver y max:                 0.0 m
peak receiver span:                  0.005333333333333343 m
Bempp return code:                   0
frequency grid numerically usable:   true
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
layered 3D GPR model ready:          false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Adjacent frequency comparisons:

| Left GHz | Right GHz | Relative L2 | Shape L2 | Peak ratio |
| ---: | ---: | ---: | ---: | ---: |
| 0.4 | 0.5 | 1.342777140018468 | 0.010987846295814839 | 2.374722576188969 |
| 0.5 | 0.75 | 3.36970569842619 | 0.008525102045543076 | 4.415249047782024 |
| 0.75 | 1.0 | 1.548332964672885 | 0.0016356948004357743 | 2.544755735614069 |
| 1.0 | 1.25 | 0.8406160630085359 | 0.006326838612866349 | 1.8283103714068718 |
| 1.25 | 1.5 | 0.537149720976866 | 0.007432384763152285 | 1.5248829755193327 |
| 1.5 | 2.0 | 1.053373880016817 | 0.014903616698516763 | 2.0179549490074753 |
| 2.0 | 2.5 | 0.36439347320017046 | 0.06658931539243934 | 1.2515032085345779 |
| 2.5 | 3.0 | 0.3420084194952919 | 0.05458448227697363 | 1.4447882780800372 |

## Interpretation

The locked 3D Bempp dipole prototype is numerically stable over the tested
0.4-3.0 GHz grid: all nine solves return finite receiver responses.

The response amplitude changes strongly with frequency, which is expected for
this point-dipole BEM proxy and means amplitude normalization must remain a
formal comparison requirement. The receiver-line shape changes much less than
the amplitude, with maximum adjacent normalized shape L2 of about 0.0666.

This is BEM-side numerical evidence only. It does not validate BEM against 3D
FDTD or field data.

## Decision

Use this run to inform future external FDTD frequency-bin choices and BEM-side
normalization checks.

Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR modeling, field
FWI, and GPU/HPC work blocked until real target/background FDTD returns pass
the upgraded run `110` metadata gate and the frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_bempp_dipole_frequency_grid_stability_audit.py
sha256: a018b9880e1198763ed6ab75fd1ec4618ebae4ea62c05b6195c358f0ef959800

test_project_core_bem_bempp_dipole_frequency_grid_stability_audit.py
sha256: 76e972327189f6285422cfa38c0a3f2326b0c8e5172cd1737362ee671fc446e9
```

Subsequent related BEM frequency-grid experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_dipole_frequency_grid_stability_audit.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_dipole_frequency_grid_stability_audit.png
2680x846, dynamic range=255
```
