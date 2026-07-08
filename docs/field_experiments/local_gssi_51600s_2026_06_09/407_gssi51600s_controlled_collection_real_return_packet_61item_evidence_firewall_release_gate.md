# Field Experiment 407: Evidence-Firewall Release Gate

Date: 2026-06-29

## Purpose

Convert the synthetic-acceptance evidence firewall from run `401` into a
release-gate checklist for future real packet returns.

This run does not promote any synthetic row to measured field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/407_gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_release_gate_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_release_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_dependency_edges.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source firewall ready:                       true
source claim boundary ready:                 true
release gate ready:                          true
release-gate rows:                           49
direct real-input release rows:              33
generated follow-up release rows:            16
release actions:                             6
dependency edges:                            6
release-ready rows now:                      0
release-blocked rows now:                    49
real replacements required:                  49
current release can promote evidence:        false
synthetic only:                              true
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The release gate has six ordered actions:

| Order | Release action |
| ---: | --- |
| 1 | replace direct real inputs |
| 2 | regenerate follow-up outputs |
| 3 | rerun intake parser contract |
| 4 | rerun provenance gate |
| 5 | rerun archive acceptance gate |
| 6 | evaluate field FWI, GPU, and 3D/HPC only after acceptance |

## Decision

Use this gate before allowing any parser-accepted field row to become measured
evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate.py
4 passed
```

Figure check:

```text
2645x864, dynamic range=255
```
