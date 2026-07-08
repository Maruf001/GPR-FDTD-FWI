# Field Experiment 323: Antenna Aperture Metadata Addendum

Date: 2026-06-29

## Purpose

Add antenna aperture, footprint, coupling, and positioning metadata
requirements to the controlled field return packet contract.

This run does not stage measured DZT files, accept provenance, accept a real
archive, promote controlled field evidence, run field FWI, launch 3D/HPC work,
or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/323_gssi51600s_controlled_collection_real_return_antenna_aperture_metadata_addendum
```

## Result

```text
source packet items:                      57
source metadata requirements:             32
antenna aperture metadata items:          4
updated packet items:                     61
updated acceptance checks:                201
updated measured requirements:            54
updated metadata requirements:            36
updated global metadata values:           15
updated file metadata values:             21
real DZT files:                           9
checksum rows:                            9
acceptance gates:                         7
BEM 3-sample aperture relative L2:        0.08009547612144642
antenna aperture metadata required:       true
antenna coupling metadata required:       true
updated packet contract ready:            true
real return execution ready:              false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
GPU priority:                             none
```

The four new metadata records are:

| Item | Purpose |
| --- | --- |
| `antenna_model_serial_and_nominal_frequency` | Identify the GSSI antenna and acquisition hardware. |
| `antenna_footprint_and_phase_center_geometry` | Record footprint, phase-center convention, Tx/Rx offset convention, and orientation. |
| `antenna_ground_coupling_and_lift_condition` | Record surface contact, lift-off, spacer/sled state, and coupling condition. |
| `antenna_positioning_and_polarization_control` | Record polarization, scan direction, encoder contact, and repeat positioning control. |

## Interpretation

The controlled field packet needs explicit antenna aperture and coupling
metadata. The BEM receiver-aperture audit shows that finite aperture can
materially change scattered responses, and the GSSI field antenna is a
finite-footprint instrument rather than a point receiver.

## Decision

Use this addendum as the current field-side packet-contract update. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked until the updated measured
packet is staged and validated.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_antenna_aperture_metadata_addendum.py
4 passed
```

Figure check:

```text
3329x880, dynamic range=255
```
