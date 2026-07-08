# BEM Experiment 717: Producer Input Strict Contract-Hash Policy Audit

Date: 2026-07-01

## Purpose

Audit the `input_contract_sha256` rule for the matched-FDTD producer input
files.

Runs `714-716` showed that blank producer-input templates are correctly
rejected. This run asks a narrower acceptance-gate question: does the exporter
only require a syntactically valid hash, or does it require the exact hash of
the saved input contract?

This is CPU-only acceptance-policy auditing. It does not run FDTD, execute the
exporter on real files, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/717_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_contract_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_current_exporter_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
producer input file keys:               2
required producer rows:               558
canonical contract hashes:              2
probe cases:                            8
arbitrary hex64 hashes accepted now:    2
exact hash enforcement active now:  false
strict-policy pass cases:               2
strict-policy fail cases:               6
ready for hardening patch:           true
exporter execution ready:           false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                       false
```

## Interpretation

The current exporter rejects blank or non-hex contract hashes, but it accepts a
valid-looking arbitrary 64-character hash. That means the hash field is a syntax
gate today, not a true binding to the saved input contract.

This run defines two canonical per-file contract hashes, one for
`fdtd_source_hash_manifest` and one for `fdtd_scattered_norm_values`.

## Decision

Use this audit as the basis for a guarded exporter hardening patch. Do not
accept real matched-FDTD producer input until the acceptance path requires the
exact canonical contract hash.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_contract_hash_policy_audit.py
4 passed
```

Figure check:

```text
2644x850, dynamic range=255
```
