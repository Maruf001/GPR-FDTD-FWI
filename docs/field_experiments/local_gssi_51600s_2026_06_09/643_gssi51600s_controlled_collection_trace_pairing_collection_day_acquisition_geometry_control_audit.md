# Field Experiment 643: Collection-Day Acquisition Geometry Control Audit

Date: 2026-07-02

## Purpose

Convert the guarded BEM acquisition-geometry sensitivity result into
field-side metadata controls for the controlled collection.

The BEM geometry block shows that Tx/Rx spacing and antenna z-position can
produce much larger waveform changes than the small depth/material changes
tested in the preliminary BEM sweeps. This field run turns that result into a
collection-day control audit.

This is a CPU-only field control audit. It does not use new measured field
files, rerun the first-return acceptance gate, run field FWI, start field
3D/HPC, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/643_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit
```

## Result

```text
source field decision ready:              true
source BEM geometry ready:                true
geometry control rows:                    6
metadata-required controls:               6
currently satisfied controls:             0
geometry-sensitive blocking controls:     6
expected metadata files:                  9
expected DZT files:                       9
expected measured pairs:                  9
live files:                               0
missing files:                            18
acceptance rerun authorized now:          false
BEM peak offset span at z=0:              2.6214537950832346 dB
BEM max relative L2 across offset:        0.7099232724148534
BEM max relative L2 across antenna z:     0.4171376953084501
BEM max relative L2 across full grid:     0.9115427115447009
geometry-control metadata ready:          false
geometry-sensitive interpretation ready:  false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

Control rows:

| Priority | Control | BEM metric | Value | Metadata scope |
| ---: | --- | --- | ---: | --- |
| 1 | Tx/Rx offset lock | max relative L2 across offset | 0.7099232724148534 | all nine paired metadata JSON files |
| 2 | antenna z/standoff lock | max relative L2 across antenna z | 0.4171376953084501 | all nine paired metadata JSON files |
| 3 | phase-center track geometry | peak span across offset | 2.6214537950832346 | controlled profile metadata and profile-geometry record |
| 4 | controlled repeat geometry consistency | full-grid max relative L2 | 0.9115427115447009 | three controlled-profile metadata JSON files |
| 5 | reference scan geometry match | peak-time span across offset | 0.13190034196385092 | six reference metadata JSON files |
| 6 | metadata receipt binding | missing file count | 18 | all nine measured radar/metadata pairs |

## Interpretation

The field collection needs geometry metadata, not only radar files. The BEM
geometry result shows that small acquisition-geometry changes can dominate the
preliminary response. Therefore each controlled profile, time-zero reference,
and amplitude reference should carry paired metadata for Tx/Rx spacing,
antenna z-position or standoff, coupling/contact state, phase-center or
footprint reference, and repeat/reference geometry matching.

The current field state remains pending: all 18 first-return files are absent,
and the paired metadata files that would carry these controls are also absent.

## Decision

Use this audit as the collection-day geometry-control checklist. Keep field
evidence, field FWI, GPU escalation, and field 3D/HPC blocked until the first
return files and paired geometry metadata are present and pass the guarded
acceptance path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit.py
pass
```

Figure check:

```text
3293x872, dynamic range=255
```
