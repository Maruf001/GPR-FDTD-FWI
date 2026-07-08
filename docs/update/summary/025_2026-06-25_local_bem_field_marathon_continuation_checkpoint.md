# Local BEM And Field Marathon Continuation Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the continuation after the local 20-hour marathon rule
was tightened. It covers the new local marathon skill, BEM runs `071-084`, field
run `167-172`, the local 2D next-experiment design matrix, the refreshed
presentation evidence pack, and the presentation storyboard.

The marathon request remains active; this checkpoint is not a stop condition.

## Skill

New local skill:

```text
/home/lam002/.codex/skills/gpr-local-20h-marathon
```

The skill scopes marathon behavior to:

```text
/home/lam002/Documents/GPR-FDTD-FWI
outputs/bem_experiments
outputs/experiments
outputs/field_experiments
docs/bem_experiments
docs/experiments
docs/field_experiments
```

It explicitly says not to stop at clean checkpoints while the requested
active-session duration remains.

## BEM 3D Progression

Run `071`:

```text
matched 3D FDTD comparison contract
contract items:                  10
ready / partial / blocked:       7 / 1 / 2
launch blockers:                 3
ready for 3D FDTD launch:        false
ready for 3D validation claim:   false
```

Finding:

```text
run 070 was a homogeneous y-polarized plane-wave Bempp reference, so a fair
FDTD comparison must either match that plane wave or create a GPR-like Bempp
source first.
```

Run `072`:

```text
Bempp point-dipole source probe
source position:                 [-0.04, 0.0, 0.09] m
dipole moment:                   [0.0, 1.0, 0.0]
frequencies checked:             4
finite all responses:            true
Bempp dipole reference ready:    true
ready for 3D FDTD validation:    false
```

Run `073`:

```text
paired FDTD manifest contract
manifest templates:              2
receiver count:                  31
frequency count:                 4
missing external FDTD runs:      2
paired FDTD data ready:          false
3D validation claim ready:       false
```

Run `074`:

```text
paired FDTD manifest validator
validation checks:               9
passed checks:                   9
failed checks:                   0
manifest templates valid:        true
paired FDTD data ready:          false
3D validation claim ready:       false
```

Run `075`:

```text
FDTD pair-comparator preflight
schema columns:                  12
preflight checks:                22
passed checks:                   1
failed checks:                   21
target expected frequency rows:  124
background expected rows:        124
target FDTD rows present:        0
background FDTD rows present:    0
comparison ready:                false
3D validation claim ready:       false
```

Run `076`:

```text
FDTD pair-comparator synthetic smoke
target synthetic rows:           124
background synthetic rows:       124
comparator checks:               22
comparator failed checks:        0
max scattered recovery error:    3.694567826668716e-12
synthetic comparator pass:       true
real FDTD data ready:            false
3D validation claim ready:       false
```

Run `077`:

```text
FDTD frequency-bin import template
target template rows:            124
background template rows:        124
required schema columns:         12
component columns to fill:       6
blank component cells:           1488
import templates ready:          true
real FDTD data ready:            false
comparison ready:                false
3D validation claim ready:       false
```

Run `078`:

```text
FDTD import-template synthetic smoke
target synthetic rows:           124
background synthetic rows:       124
comparator checks:               22
comparator failed checks:        0
synthetic import smoke pass:     true
real FDTD data ready:            false
comparison ready:                false
3D validation claim ready:       false
```

Run `079`:

```text
3D FDTD execution readiness audit
readiness checks:                10
pass / partial / fail:           6 / 1 / 3
blocking gaps:                   3
blocking gap checks:             local_3d_fdtd_engine, frequency_bin_extractor, paired_real_fdtd_outputs
local 3D FDTD launch ready:      false
real comparison ready:           false
3D validation claim ready:       false
```

Run `080`:

```text
3D FDTD frequency-bin extractor contract
requirements:                    7
ready / implementation / blocked: 4 / 2 / 1
time-trace schema columns:       9
frequency-bin schema columns:    12
extractor contract ready:        true
extractor implemented:           false
real comparison ready:           false
3D validation claim ready:       false
```

Run `081`:

```text
3D FDTD frequency-bin extractor synthetic smoke
synthetic trace rows:            7936
extracted target rows:           124
extracted background rows:       124
comparator checks:               22
comparator failed checks:        0
extractor smoke pass:            true
real FDTD data ready:            false
real comparison ready:           false
3D validation claim ready:       false
```

Run `082`:

```text
3D FDTD engine candidate audit
candidate paths:                 6
preferred next candidates:       1
supporting tooling candidates:   1
blocked research candidates:     2
reference-only candidates:       2
top candidate:                   external_3d_fdtd_import
external data request ready:     true
local 3D FDTD launch ready:      false
real comparison ready:           false
3D validation claim ready:       false
```

Run `083`:

```text
external 3D FDTD data request pack
requested FDTD runs:             2
request artifacts:               7
receiver count:                  31
frequency count:                 4
frequency rows per run:          124
total frequency rows expected:   248
acceptance gates:                7
external request ready:          true
real external FDTD data present: false
real comparison ready:           false
3D validation claim ready:       false
```

Run `084`:

```text
external 3D FDTD return preflight
preflight checks:                10
passed checks:                   0
failed checks:                   10
blocking findings:               10
paired frequency return ready:   false
real external FDTD data present: false
real comparison ready:           false
3D validation claim ready:       false
```

Run `085`:

```text
external 3D FDTD return acceptance pack
required return files:           2
current required files present:  0
metadata requirements:           12
acceptance steps:                8
gate crosswalk rows:             8
expected total frequency rows:   248
ready to accept external return: true
real external FDTD data present: false
real comparison ready:           false
3D validation claim ready:       false
```

Run `086`:

```text
external 3D FDTD return metadata preflight
metadata requirements:           12
preflight checks:                7
passed checks:                   0
failed checks:                   7
blocking findings:               7
metadata preflight ready:        false
return file hashes verified:     false
ready for return preflight:      false
real comparison ready:           false
3D validation claim ready:       false
```

Run `087`:

```text
external 3D FDTD return metadata preflight smoke
synthetic returned files:        2
metadata rows:                   12
preflight checks:                7
passed checks:                   7
failed checks:                   0
blocking findings:               0
synthetic metadata smoke pass:   true
synthetic smoke only:            true
real external FDTD data present: false
real comparison ready:           false
3D validation claim ready:       false
```

Run `088`:

```text
external 3D FDTD return full bundle smoke
synthetic frequency files:       2
frequency rows per run:          124
metadata preflight checks:       7
metadata blocking findings:      0
return preflight checks:         10
return blocking findings:        0
synthetic full bundle pass:      true
synthetic smoke only:            true
real external FDTD data present: false
real comparison ready:           false
3D validation claim ready:       false
```

Current BEM decision:

```text
The 3D BEM branch is ready through backend/source/manifest/validator/comparator
contracts, the comparator has a synthetic pass-case smoke, and strict
target/background import templates exist with a synthetic fill smoke. Local
execution is blocked by the absence of a 3D FDTD engine and paired real
target/background outputs. The extractor contract is explicit and has a
synthetic direct-DFT smoke, and the engine-candidate audit now selects external
full-Maxwell 3D FDTD import as the preferred validation-data path. The request
pack now defines two paired runs, seven artifacts, and seven acceptance gates.
The return preflight is executable and currently fails because no returned
target/background files exist. The return acceptance handoff is now exact, with
two required files, 12 metadata fields, eight acceptance steps, and eight gate
crosswalk rows. The metadata preflight makes that ledger executable and
currently fails because no metadata ledger or hash-verifiable returned files
exist. The synthetic metadata smoke proves this gate can pass when the ledger
and hashes are complete. The full return-bundle smoke proves the metadata and
frequency-bin gates can pass together on a complete synthetic bundle, but real
traces are still missing.
It is still not a 3D validation result because paired target/background FDTD
outputs do not exist yet.
```

## Field Progression

Run `167`:

```text
controlled collection-day checklist pack
checklist items:                 20
metadata items:                  11
real file items:                 9
controlled profile files:        3
time-zero reference files:       3
amplitude reference files:       3
gate count:                      6
ready for collection-day use:    true
provenance acceptance ready:     false
field FWI ready:                 false
GPU/HPC ready:                   false
```

Run `168`:

```text
controlled collection checksum ledger template
ledger rows:                     9
command rows:                    9
controlled profile files:        3
time-zero reference files:       3
amplitude reference files:       3
ready for collection-day use:    true
provenance acceptance ready:     false
field FWI ready:                 false
GPU/HPC ready:                   false
```

Run `169`:

```text
controlled collection checksum ledger preflight
ledger rows:                     9
accepted rows:                   0
blocking findings:               45
blocking findings per file role: 15
preflight ready:                 false
provenance acceptance ready:     false
field FWI ready:                 false
GPU/HPC ready:                   false
```

Run `170`:

```text
checksum ledger preflight synthetic smoke
synthetic ledger rows:            9
synthetic accepted rows:          9
synthetic blocking findings:      0
synthetic preflight ready:        true
synthetic smoke only:             true
scientific field claim ready:     false
field FWI ready:                  false
GPU/HPC ready:                    false
```

Run `171`:

```text
controlled collection archive layout contract
real file layout rows:            9
metadata artifact rows:           6
archive directories:              7
command templates:                31
ready for collection-day use:     true
provenance acceptance ready:      false
field FWI ready:                  false
GPU/HPC ready:                    false
```

Run `172`:

```text
controlled collection operator handoff pack
operator sequence steps:          8
file handoff rows:                9
metadata value handoff rows:      11
gate crosswalk rows:              6
ready for operator handoff:       true
provenance acceptance ready:      false
field FWI ready:                  false
GPU/HPC ready:                    false
```

Run `173`:

```text
controlled collection archive preflight
archive preflight checks:          23
passed checks:                     0
failed checks:                     23
blocking findings:                 23
archive ready:                     false
provenance acceptance ready:       false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Run `174`:

```text
controlled collection archive preflight smoke
preflight checks:                  23
passed checks:                     23
failed checks:                     0
blocking findings:                 0
synthetic archive smoke pass:      true
synthetic smoke only:              true
scientific field claim ready:      false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Run `175`:

```text
controlled collection archive checksum bridge smoke
archive preflight checks:          23
archive blocking findings:         0
checksum ledger rows:              9
checksum accepted rows:            9
checksum blocking findings:        0
combined synthetic smoke pass:     true
synthetic smoke only:              true
scientific field claim ready:      false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Current field decision:

```text
The field branch now has an operator-facing collection-day checklist and a
checksum ledger template plus preflight, synthetic pass-case smoke,
archive-layout contract, operator handoff pack, and archive preflight. These
are not measured field evidence. The archive-preflight smoke proves the archive
gate can pass on a complete synthetic archive, but Field FWI, heavy GPU, field
3D/HPC, and provenance acceptance remain blocked. The archive-checksum bridge
smoke proves archived files can hash into accepted ledger rows, but real files
and metadata must still fill the archive layout and pass intake, checksum,
structural, archive, and provenance gates.
```

## Presentation Pack

Refreshed pack:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
```

Current result:

```text
claims:                          37
ready scoped/design/preflight:    31
blocked:                         6
field FWI/GPU/3D validation:      false
storyboard slides:                8
```

Headline:

```text
We have a scoped homogeneous 2D BEM replacement candidate, a reusable layered
scalar Sommerfeld proxy, a 3D Bempp finite-rebar/dipole-source design path with
paired FDTD manifests, a validator, a comparator schema, synthetic smokes, and
strict import templates, an execution-gap audit, an extractor contract, and an
extractor smoke, plus an external-FDTD-import decision, data-request pack, and
return preflight, return handoff, metadata preflight, metadata smoke, full return-bundle smoke, a guarded field intake/checklist/checksum/preflight/smoke/
archive-layout/operator-handoff/archive-preflight/archive-smoke/archive-checksum-bridge path, and no defensible field
FWI/GPU/3D validation claim from the current evidence.
```

Storyboard:

```text
1. current evidence boundary
2. local 2D detector result
3. 2D BEM replacement evidence
4. blocked BEM shortcuts
5. 3D BEM path
6. field collection gate
7. no-go claims
8. decision requests
```

## Local 2D Matrix

Run `136` / docs experiment `871`:

```text
candidate branches:                7
ready branches:                    3
blocked branches:                  3
design-needed branches:            1
presentation claim count:          37
new local 2D GPU ready:            false
broad GPU queue ready:             false
detector-seeded FWI ready:          false
field transfer ready:              false
```

Current local 2D decision:

```text
Do not launch a new local 2D GPU/FWI branch from the fixed-radius result. Use
the mechanism result in reporting, and require a new acquisition/source/material
hypothesis before future 2D compute.
```

## Validation

Compile checks:

```text
run_project_core_bem_3d_fdtd_comparison_contract.py
run_project_core_bem_bempp_dipole_source_probe.py
run_project_core_bem_3d_fdtd_manifest_contract.py
run_project_core_bem_3d_fdtd_manifest_validator.py
run_project_core_bem_3d_fdtd_pair_comparator_preflight.py
run_project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke.py
run_project_core_bem_3d_fdtd_frequency_bin_import_template.py
run_project_core_bem_3d_fdtd_frequency_bin_import_template_smoke.py
run_project_core_bem_3d_fdtd_execution_readiness_audit.py
run_project_core_bem_3d_fdtd_frequency_bin_extractor_contract.py
run_project_core_bem_3d_fdtd_frequency_bin_extractor_smoke.py
run_project_core_bem_3d_fdtd_engine_candidate_audit.py
run_project_core_bem_3d_fdtd_external_data_request_pack.py
run_project_core_bem_3d_fdtd_external_return_preflight.py
run_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
run_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
run_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
run_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
run_gssi_field_controlled_collection_day_checklist_pack.py
run_gssi_field_controlled_collection_checksum_ledger_template.py
run_gssi_field_controlled_collection_checksum_ledger_preflight.py
run_gssi_field_controlled_collection_checksum_ledger_preflight_smoke.py
run_gssi_field_controlled_collection_archive_layout_contract.py
run_gssi_field_controlled_collection_operator_handoff_pack.py
run_gssi_field_controlled_collection_archive_preflight.py
run_gssi_field_controlled_collection_archive_preflight_smoke.py
run_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
run_bem_field_2d_presentation_evidence_pack.py
run_local_2d_next_experiment_design_matrix.py
run_bem_field_2d_presentation_storyboard.py
tests/test_project_core_bem_3d_fdtd_manifest_validator.py
tests/test_project_core_bem_3d_fdtd_pair_comparator_preflight.py
tests/test_project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template_smoke.py
tests/test_project_core_bem_3d_fdtd_execution_readiness_audit.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_contract.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_smoke.py
tests/test_project_core_bem_3d_fdtd_engine_candidate_audit.py
tests/test_project_core_bem_3d_fdtd_external_data_request_pack.py
tests/test_project_core_bem_3d_fdtd_external_return_preflight.py
tests/test_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
tests/test_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
tests/test_gssi_field_controlled_collection_day_checklist_pack.py
tests/test_gssi_field_controlled_collection_checksum_ledger_template.py
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight.py
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight_smoke.py
tests/test_gssi_field_controlled_collection_archive_layout_contract.py
tests/test_gssi_field_controlled_collection_operator_handoff_pack.py
tests/test_gssi_field_controlled_collection_archive_preflight.py
tests/test_gssi_field_controlled_collection_archive_preflight_smoke.py
tests/test_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
tests/test_local_2d_next_experiment_design_matrix.py
pass
```

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_manifest_validator.py
tests/test_project_core_bem_3d_fdtd_pair_comparator_preflight.py
tests/test_project_core_bem_3d_fdtd_pair_comparator_synthetic_smoke.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_import_template_smoke.py
tests/test_project_core_bem_3d_fdtd_execution_readiness_audit.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_contract.py
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_smoke.py
tests/test_project_core_bem_3d_fdtd_engine_candidate_audit.py
tests/test_project_core_bem_3d_fdtd_external_data_request_pack.py
tests/test_project_core_bem_3d_fdtd_external_return_preflight.py
tests/test_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_smoke.py
tests/test_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
tests/test_gssi_field_controlled_collection_day_checklist_pack.py
tests/test_gssi_field_controlled_collection_checksum_ledger_template.py
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight.py
tests/test_gssi_field_controlled_collection_checksum_ledger_preflight_smoke.py
tests/test_gssi_field_controlled_collection_archive_layout_contract.py
tests/test_gssi_field_controlled_collection_operator_handoff_pack.py
tests/test_gssi_field_controlled_collection_archive_preflight.py
tests/test_gssi_field_controlled_collection_archive_preflight_smoke.py
tests/test_gssi_field_controlled_collection_archive_checksum_bridge_smoke.py
tests/test_local_2d_next_experiment_design_matrix.py
69 passed
```

Full test suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1109 passed in 30.33s
```

Figure checks:

```text
run 071: 2500x808, dynamic range=255
run 072: 2500x845, dynamic range=255
run 073: 2104x840, dynamic range=255
run 074: 2106x844, dynamic range=255
run 075: 2104x844, dynamic range=255
run 076: 2104x845, dynamic range=255
run 077: 1997x808, dynamic range=255
run 078: 1924x810, dynamic range=255
run 079: 2032x810, dynamic range=255
run 080: 1996x808, dynamic range=255
run 081: 1924x810, dynamic range=255
run 082: 2140x854, dynamic range=255
run 083: 2105x808, dynamic range=255
run 084: 1924x772, dynamic range=255
run 085: 1996x772, dynamic range=255
run 086: 1924x772, dynamic range=255
run 087: 1492x738, dynamic range=255
run 088: 1564x736, dynamic range=255
run 167: 2283x841, dynamic range=255
run 168: 1564x807, dynamic range=255
run 169: 1816x807, dynamic range=255
run 170: 1744x774, dynamic range=255
run 171: 1888x807, dynamic range=255
run 172: 2142x845, dynamic range=255
run 173: 1996x790, dynamic range=255
run 174: 1996x790, dynamic range=255
run 175: 1816x772, dynamic range=255
run 136: 2464x880, dynamic range=255
pack 135: 2052x954, dynamic range=255
pack 137: 2286x851, dynamic range=255
```

Resource state stayed within limits; no heavy GPU, field FWI, field 3D/HPC, or
neural-network training was launched.

## Next Branch

Continue with one of:

```text
1. 2D-side claim/report cleanup using the refreshed BEM/field evidence pack.
2. BEM-side FDTD-output import/validator scaffolding for future paired data.
3. Field-side real-collection artifact polish while provenance remains blocked.
```
