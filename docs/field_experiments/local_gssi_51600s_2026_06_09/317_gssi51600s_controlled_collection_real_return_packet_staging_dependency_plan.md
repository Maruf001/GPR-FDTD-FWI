# Field Experiment 317: Real-Return Packet Staging Dependency Plan

Date: 2026-06-29

## Purpose

Convert the guarded controlled-field return-packet worksheet into a
dependency-ordered staging plan.

This run clarifies which measured files, metadata records, checksums, and
acceptance results must be produced before the controlled field packet can be
accepted. It does not stage measured files, run provenance acceptance, run
archive acceptance, promote controlled field evidence, run field FWI, launch
GPU work, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/317_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_stage_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_dependency_edges.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan.png
scripts/
```

## Result

```text
staging plan ready:                 true
stage count:                        7
dependency edges:                   9
missing packet items:               57
missing measured DZT files:         9
missing metadata requirements:      32
missing checksum rows:              9
missing acceptance results:         7
first required stage:               stage_controlled_profile_repeats
last required stage:                rerun_acceptance_gates
acceptance gate can pass now:        false
provenance acceptance ready:         false
controlled field evidence ready:     false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The seven-stage dependency plan is:

| Order | Stage | Missing items |
| ---: | --- | ---: |
| 1 | controlled profile repeats | 3 |
| 2 | time-zero references | 3 |
| 3 | amplitude references | 3 |
| 4 | global metadata values | 11 |
| 5 | per-file metadata values | 21 |
| 6 | SHA-256 checksum rows | 9 |
| 7 | acceptance-result files | 7 |

## Interpretation

The 57 missing controlled-field return-packet items form a seven-stage
dependency graph. The measured DZT files must be collected first, then measured
metadata and checksums can be completed, and only then can the structural,
provenance, archive, evidence, and escalation gates be rerun.

The current archive still has zero measured packet items, so provenance,
archive, evidence, field FWI, and field 3D/HPC work remain blocked.

## Decision

Use run `317` as the controlled field return-packet staging sequence. Do not
run provenance acceptance, archive acceptance, field FWI, GPU work, or field
3D/HPC until real measured packet items pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan.py
3 passed
```

Figure validation:

```text
3760x967, dynamic range=255
```
