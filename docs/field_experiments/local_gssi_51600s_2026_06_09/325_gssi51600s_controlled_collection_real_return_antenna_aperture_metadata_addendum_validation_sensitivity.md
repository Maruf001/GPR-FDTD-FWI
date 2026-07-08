# Field Experiment 325: Antenna Aperture Metadata Addendum Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `324` validator for the run `323` controlled-field antenna
aperture metadata addendum.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/325_gssi51600s_controlled_collection_real_return_antenna_aperture_metadata_addendum_validation_sensitivity
```

## Result

```text
scenario count:                     14
expected pass count:                1
observed pass count:                1
expected failure count:             13
observed failure count:             13
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 323:    true
validator rejects damaged variants: true
updated packet items:               61
updated metadata requirements:      36
antenna aperture metadata items:    4
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The exact run `323` artifacts pass. Thirteen damaged variants fail as expected:
source identity drift, packet-count drift, metadata-count drift, antenna-row
loss, antenna-item drift, antenna blocking drift, false packet-row readiness,
BEM aperture motivation drift, false contract demotion, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift.

## Interpretation

Runs `323-325` form a guarded field antenna aperture metadata-addendum block.
The packet contract is updated, but field evidence remains blocked until real
measured files and metadata are staged and validated.

## Decision

Use runs `323-325` as the guarded field antenna aperture metadata-addendum
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_antenna_aperture_metadata_addendum_validation_sensitivity.py
3 passed
```

Figure check:

```text
3545x895, dynamic range=255
```
