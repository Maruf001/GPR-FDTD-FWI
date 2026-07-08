# Field Experiment 166: Controlled Collection Intake Manifest Preflight Smoke

Date: 2026-06-25

## Purpose

Verify that the run `165` intake-manifest preflight can pass when all required
fields are present.

This run fills a synthetic manifest with accepted row status, measured-looking
values, expected file basenames, operator initials, UTC timestamps, and
64-character SHA-256 checksums for the nine file rows.

The synthetic manifest is not measured field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/166_gssi51600s_controlled_collection_intake_manifest_preflight_smoke
```

Key artifacts:

```text
data/field_controlled_collection_intake_manifest_preflight_smoke_manifest.csv
data/field_controlled_collection_intake_manifest_preflight_smoke_findings.csv
data/field_controlled_collection_intake_manifest_preflight_smoke_groups.csv
data/field_controlled_collection_intake_manifest_preflight_smoke_summary.json
figures/field_controlled_collection_intake_manifest_preflight_smoke.png
docs/FIELD_COLLECTION_INTAKE_MANIFEST_PREFLIGHT_SMOKE.md
```

## Result

```text
synthetic manifest rows:            20
synthetic accepted rows:            20
synthetic findings:                 0
synthetic blocking findings:        0
synthetic preflight ready:          true
blank template blocking findings:   89
synthetic smoke only:               true
provenance acceptance ready:        false
scientific field claim ready:       false
field FWI ready:                    false
GPU work ready:                     false
```

All six closure groups pass in the synthetic smoke:

| Closure group | Items | Accepted | Blocking findings | Ready |
| --- | ---: | ---: | ---: | --- |
| session metadata real values | 8 | 8 | 0 | true |
| target truth provenance | 2 | 2 | 0 | true |
| profile geometry provenance | 1 | 1 | 0 | true |
| acquisition profile files | 3 | 3 | 0 | true |
| time-zero reference files | 3 | 3 | 0 | true |
| amplitude reference files | 3 | 3 | 0 | true |

## Interpretation

The run `165` preflight is achievable: it fails the blank template but passes a
fully populated manifest shape.

This is only a validator smoke test. It does not replace controlled collection,
real file checksums, structural validation, or provenance validation.

## Decision

Use run `165` as the real preflight guard and run `166` as a regression smoke
for the guard itself.

Do not treat the synthetic smoke manifest as measured field evidence. Field
FWI, heavy GPU work, field 3D/HPC, and neural-network training remain blocked.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_gssi_field_controlled_collection_intake_manifest_preflight_smoke.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_gssi_field_controlled_collection_intake_manifest_preflight_smoke.py
pass
```

Figure check:

```text
field_controlled_collection_intake_manifest_preflight_smoke.png
1744x774, dynamic range=255
```
