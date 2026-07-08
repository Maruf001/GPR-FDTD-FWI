# Field Experiment 401: Synthetic Acceptance Evidence Firewall

Date: 2026-06-29

## Purpose

Add an evidence firewall around the synthetic worksheet acceptance smoke from
run `395`.

This run keeps accepted synthetic rows useful for parser-regression testing but
explicitly blocks them from measured field evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, and field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/401_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_firewall_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_firewall_rule_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source smoke ready:                         true
evidence firewall ready:                    true
firewall rows:                              49
synthetic parser accepted rows:             49
parser-regression allowed rows:             49
measured-evidence allowed rows:             0
provenance-acceptance allowed rows:         0
archive-acceptance allowed rows:            0
field-FWI allowed rows:                     0
real-replacement required rows:             49
synthetic only:                             true
real packet files present:                  false
provenance acceptance ready:                false
real archive acceptance ready:              false
controlled field evidence ready:            false
field FWI ready:                            false
field 3D/HPC ready:                         false
gpu priority:                               none
```

## Decision

Use this firewall before any future filled worksheet can be promoted to field
evidence. Synthetic accepted rows are parser-regression artifacts only.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall.py
4 passed
```

Figure check:

```text
2609x864, dynamic range=255
```
