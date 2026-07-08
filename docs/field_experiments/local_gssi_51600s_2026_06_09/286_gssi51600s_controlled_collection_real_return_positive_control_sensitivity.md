# Field Experiment 286: Positive-Control Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `285` positive-control validator with controlled damaged
variants.

Run `285` validated the saved synthetic positive-control mechanics smoke. This
run verifies that the validator rejects changes that would make the synthetic
packet incomplete, inconsistent, or falsely promoted to real field evidence.

This is a CPU-only sensitivity run. It does not stage real measured field data,
modify the real return inbox, accept provenance, accept a real archive, run
field FWI, run field 3D/HPC, or launch GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/286_gssi51600s_controlled_collection_real_return_positive_control_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_positive_control_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_positive_control_sensitivity_summary.json
figures/field_controlled_collection_real_return_positive_control_sensitivity.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_POSITIVE_CONTROL_SENSITIVITY.md
```

## Result

```text
scenarios:                    13
expected pass:                1
observed pass:                1
expected failures:            12
observed failures:            12
unexpected outcomes:          0
sensitivity ready:            true
exact run accepted:           true
damaged variants rejected:    true
real measured data present:   false
provenance acceptance ready:  false
real archive acceptance ready:false
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
gpu priority:                 none
```

## Interpretation

The validator accepts the exact positive-control smoke and rejects controlled
damage to counts, checksum matches, unexpected files, placeholders, extensions,
synthetic-only state, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `284-286` as the guarded positive-control mechanics block. The real
field archive remains blocked until actual measured DZT files, metadata, and
checksums arrive.
