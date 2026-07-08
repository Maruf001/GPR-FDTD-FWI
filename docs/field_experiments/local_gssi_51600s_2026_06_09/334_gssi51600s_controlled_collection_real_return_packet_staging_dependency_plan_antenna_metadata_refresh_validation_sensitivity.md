# Field Experiment 334: Antenna-Aware Staging Dependency Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `333` artifact validator with controlled damaged variants.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/334_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          17
expected pass:                      1
observed pass:                      1
expected failures:                  16
observed failures:                  16
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 332:              true
rejects damaged variants:           true
packet items required:              61
metadata requirements:              36
antenna metadata addendum items:    4
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The validator accepts the exact run `332` artifacts and rejects damaged variants
for source-gate drift, packet-count drift, stage-count drift, stage-order drift,
metadata-count drift, antenna-row drift, readiness promotion, dependency-graph
drift, downstream promotion, GPU-priority drift, figure-validation drift, and
script-snapshot drift.

## Decision

Use runs `332-334` as the guarded antenna-aware staging dependency block. The
field branch remains blocked at measured-packet acquisition: the 61-item packet
must exist and pass the refreshed acceptance gate before provenance acceptance,
archive acceptance, field evidence, field FWI, GPU work, or field 3D/HPC can
be justified.

## Validation

Focused sensitivity test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3725x922, dynamic range=255
```
