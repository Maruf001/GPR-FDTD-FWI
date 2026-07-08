# Field Experiment 167: Controlled Collection Day Checklist Pack

Date: 2026-06-25

## Purpose

Turn the controlled-collection closure and intake-manifest artifacts from runs
`163-166` into an operator-facing collection-day checklist pack.

This is a no-data operational artifact. It does not create measured field
evidence, run DZT preprocessing, launch field FWI, use GPU/HPC, or train neural
networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/167_gssi51600s_controlled_collection_day_checklist_pack
```

Key artifacts:

```text
data/field_controlled_collection_day_checklist.csv
data/field_controlled_collection_day_file_manifest.csv
data/field_controlled_collection_day_gate_sequence.csv
data/field_controlled_collection_day_checklist_pack_summary.json
figures/field_controlled_collection_day_checklist_pack.png
docs/FIELD_COLLECTION_DAY_CHECKLIST_PACK.md
```

## Result

```text
checklist items:                     20
metadata items:                      11
real file items:                     9
controlled profile files:            3
time-zero reference files:           3
amplitude reference files:           3
gate count:                          6
synthetic preflight smoke passed:    true
blank template blocking findings:    89
ready for collection-day use:        true
ready for provenance acceptance:     false
ready for structural rerun:          false
field FWI ready:                     false
GPU work ready:                      false
field 3D/HPC ready:                  false
```

The checklist includes the exact nine required real files:

```text
3 controlled profile-repeat DZT files
3 time-zero reference DZT files
3 amplitude-reference DZT files
```

It also carries six collection gates: fill manifest, record operator/UTC,
hash nine files, run intake preflight, confirm the synthetic smoke rule still
passes, and rerun structural plus provenance gates on real data.

## Interpretation

The field-side blocker is now operationally packaged. The current archive still
cannot become measured field evidence by relabeling, but the collection-day work
is reduced to 20 checklist rows and six explicit gates.

## Decision

Use this pack during controlled collection. Do not treat it as measured field
evidence; provenance acceptance, field FWI, GPU work, and field 3D/HPC remain
blocked until real files and metadata pass the gates.

## Validation

Figure check:

```text
2283x841, dynamic range=255
```
