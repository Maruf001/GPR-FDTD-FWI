# Field Experiment 165: Controlled Collection Intake Manifest Preflight

Date: 2026-06-25

## Purpose

Add a reusable preflight check for the run `164` controlled-collection intake
manifest.

This run validates whether the manifest is ready for structural and provenance
gates to be rerun. It checks accepted row status, real collected values or file
paths, operator initials, UTC timestamps, expected filenames, and SHA-256
checksums for the nine measured files.

This is CPU-only validation. It does not run DZT preprocessing, FDTD, FWI, GPU
kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/165_gssi51600s_controlled_collection_intake_manifest_preflight
```

Key artifacts:

```text
data/field_controlled_collection_intake_manifest_preflight_findings.csv
data/field_controlled_collection_intake_manifest_preflight_groups.csv
data/field_controlled_collection_intake_manifest_preflight_summary.json
figures/field_controlled_collection_intake_manifest_preflight.png
docs/FIELD_COLLECTION_INTAKE_MANIFEST_PREFLIGHT.md
```

## Result

The blank run `164` template fails preflight as expected:

```text
manifest rows:                    20
accepted rows:                    0
findings:                         89
blocking findings:                89
closure groups:                   6
preflight ready:                  false
ready for structural rerun:       false
ready for provenance acceptance:  false
ready for field FWI:              false
ready for GPU work:               false
```

Group blockers:

| Closure group | Items | Accepted | Blocking findings | Ready |
| --- | ---: | ---: | ---: | --- |
| session metadata real values | 8 | 0 | 32 | false |
| target truth provenance | 2 | 0 | 8 | false |
| profile geometry provenance | 1 | 0 | 4 | false |
| acquisition profile files | 3 | 0 | 15 | false |
| time-zero reference files | 3 | 0 | 15 | false |
| amplitude reference files | 3 | 0 | 15 | false |

## Interpretation

The blank intake sheet is not accepted field evidence. That is the intended
state before collection.

Run `165` adds the missing operational guard between a filled manifest and
rerunning structural/provenance gates. After a real collection, every manifest
row must be accepted, contain a real measured value or real file path, carry
operator initials and a UTC timestamp, and all nine measured files must include
64-character SHA-256 checksums.

## Decision

Use this preflight before rerunning the packet structural validator and the
provenance gate.

Do not launch field FWI, heavy GPU work, field 3D/HPC, or neural-network
training from the current blank manifest or dry-run packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_intake_manifest_preflight.py
3 passed
```

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_gssi_field_controlled_collection_intake_manifest_preflight.py tests/test_gssi_field_controlled_collection_intake_manifest_preflight.py
pass
```

Figure check:

```text
field_controlled_collection_intake_manifest_preflight.png
2101x842, dynamic range=255
```
