# Field Experiment 292: Real Return Execution Readiness Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `291` real-return execution readiness validator with
controlled damaged variants.

This uses saved artifacts only. It does not ingest real DZT files, modify the
real return inbox, promote provenance acceptance, run field FWI, launch 3D/HPC
work, or use GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/292_gssi51600s_controlled_collection_real_return_execution_readiness_after_positive_control_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_execution_readiness_after_positive_control_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_execution_readiness_after_positive_control_sensitivity_summary.json
figures/field_controlled_collection_real_return_execution_readiness_after_positive_control_sensitivity.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_EXECUTION_READINESS_AFTER_POSITIVE_CONTROL_SENSITIVITY.md
```

## Result

```text
scenarios:                         17
expected pass:                     1
observed pass:                     1
expected failures:                 16
observed failures:                 16
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 290:             true
rejects damaged variants:          true
real return execution ready:       false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Interpretation

The real-return execution-readiness validator accepts the exact run `290` audit
and rejects controlled damage to gate counts, measured-requirement counts,
false real-file or metadata completion, synthetic-boundary state, downstream
readiness, blocker reasons, figure validation, and script snapshots.

## Decision

Use runs `290-292` as the guarded post-positive-control field real-return
execution gate. The next field work remains real measured artifact staging and
validation, not another synthetic mechanics run.
