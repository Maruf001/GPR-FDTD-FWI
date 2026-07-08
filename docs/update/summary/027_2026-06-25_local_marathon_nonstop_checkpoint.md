# Local Marathon Nonstop Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the continuation after the local 20-hour marathon skill
was tightened to treat clean checkpoints as progress artifacts, not stop
conditions.

The marathon request remains active; this file is not a stop condition.

## Skill

Updated and validated:

```text
/home/lam002/.codex/skills/gpr-local-20h-marathon
```

The skill now includes explicit early-stop violation recovery: if Codex stops
before the requested duration, it must acknowledge the mistake, preserve the
active marathon, re-read state, and continue in commentary instead of ending at
an apology.

## BEM 3D Additions

Run `077`:

```text
FDTD frequency-bin import template
target template rows:                  124
background template rows:              124
required schema columns:               12
component columns to fill:             6
blank component cells:                 1488
import templates ready:                true
real FDTD data ready:                  false
3D validation claim ready:             false
```

Run `078`:

```text
FDTD import-template synthetic smoke
target synthetic rows:                 124
background synthetic rows:             124
comparator checks:                     22
comparator failed checks:              0
synthetic import smoke pass:           true
real FDTD data ready:                  false
3D validation claim ready:             false
```

Run `079`:

```text
3D FDTD execution readiness audit
readiness checks:                      10
pass / partial / fail:                 6 / 1 / 3
blocking gaps:                         3
blocking gap checks:                   local_3d_fdtd_engine, frequency_bin_extractor, paired_real_fdtd_outputs
local 3D FDTD launch ready:            false
real BEM/FDTD comparison ready:        false
3D validation claim ready:             false
```

Run `080`:

```text
3D FDTD frequency-bin extractor contract
requirements:                         7
ready / implementation / blocked:     4 / 2 / 1
time-trace schema columns:            9
frequency-bin schema columns:         12
extractor contract ready:             true
extractor implemented:                false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `081`:

```text
3D FDTD frequency-bin extractor synthetic smoke
synthetic trace rows:                 7936
extracted target rows:                124
extracted background rows:            124
comparator checks:                    22
comparator failed checks:             0
extractor smoke pass:                 true
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `082`:

```text
3D FDTD engine candidate audit
candidate paths:                      6
preferred next candidates:            1
supporting tooling candidates:        1
blocked research candidates:          2
reference-only candidates:            2
top candidate:                        external_3d_fdtd_import
external data request ready:          true
local 3D FDTD launch ready:           false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `083`:

```text
external 3D FDTD data request pack
requested FDTD runs:                  2
request artifacts:                    7
receiver count:                       31
frequency count:                      4
frequency rows per run:               124
total frequency rows expected:        248
acceptance gates:                     7
external request ready:               true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `084`:

```text
external 3D FDTD return preflight
preflight checks:                     10
passed checks:                        0
failed checks:                        10
blocking findings:                    10
paired frequency return ready:        false
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `085`:

```text
external 3D FDTD return acceptance pack
required return files:                2
current required files present:       0
metadata requirements:                12
acceptance steps:                     8
gate crosswalk rows:                  8
expected total frequency rows:        248
ready to accept external return:      true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `086`:

```text
external 3D FDTD return metadata preflight
metadata requirements:                12
preflight checks:                     7
passed checks:                        0
failed checks:                        7
blocking findings:                    7
metadata preflight ready:             false
return file hashes verified:          false
ready for return preflight:           false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `087`:

```text
external 3D FDTD return metadata preflight smoke
synthetic returned files:             2
metadata rows:                        12
preflight checks:                     7
passed checks:                        7
failed checks:                        0
blocking findings:                    0
synthetic metadata smoke pass:        true
synthetic smoke only:                 true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Run `088`:

```text
external 3D FDTD return full bundle smoke
synthetic frequency files:            2
frequency rows per run:               124
metadata preflight checks:            7
metadata blocking findings:           0
return preflight checks:              10
return blocking findings:             0
synthetic full bundle pass:           true
synthetic smoke only:                 true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

Current BEM decision:

```text
The BEM-side acceptance surface is ready through manifests, validation,
comparator schema, import templates, and synthetic smokes.

The local execution side is still blocked: no local 3D FDTD engine and no
paired target/background real FDTD outputs exist. The extractor contract now
has a synthetic direct-DFT smoke, and the engine-candidate audit selects
external full-Maxwell 3D FDTD import as the preferred validation-data path.
The external request pack now defines the two paired runs, request artifacts,
and acceptance gates needed before real comparison can reopen. The return
preflight is executable and currently fails because no returned target/
background files exist. The return acceptance handoff now defines the exact two
files, 12 metadata fields, eight acceptance steps, and eight gate crosswalk rows
needed when files arrive. The metadata preflight now makes that ledger
machine-checkable and currently fails because no metadata ledger or
hash-verifiable returned files exist. The synthetic metadata smoke proves the
gate can pass when the ledger and hashes are complete, but it is not real
external FDTD data. The full return-bundle smoke proves metadata and
frequency-bin gates can pass together on a synthetic bundle, but it is still
not real external FDTD data.
```

## Field Additions

Run `169`:

```text
checksum ledger preflight
ledger rows:                           9
accepted rows:                         0
blocking findings:                     45
preflight ready:                       false
field FWI ready:                       false
```

Run `170`:

```text
checksum ledger synthetic pass smoke
synthetic ledger rows:                 9
synthetic accepted rows:               9
synthetic blocking findings:           0
synthetic preflight ready:             true
scientific field claim ready:          false
field FWI ready:                       false
```

Run `171`:

```text
controlled collection archive layout contract
real file layout rows:                 9
metadata artifact rows:                6
archive directories:                   7
command templates:                     31
ready for collection-day use:          true
provenance acceptance ready:           false
field FWI ready:                       false
```

Run `172`:

```text
controlled collection operator handoff pack
operator sequence steps:               8
file handoff rows:                     9
metadata value handoff rows:           11
gate crosswalk rows:                   6
ready for operator handoff:            true
provenance acceptance ready:           false
field FWI ready:                       false
```

Run `173`:

```text
controlled collection archive preflight
archive preflight checks:              23
passed checks:                         0
failed checks:                         23
blocking findings:                     23
archive ready:                         false
field FWI ready:                       false
```

Run `174`:

```text
controlled collection archive preflight smoke
preflight checks:                      23
passed checks:                         23
failed checks:                         0
blocking findings:                     0
synthetic archive smoke pass:          true
synthetic smoke only:                  true
scientific field claim ready:          false
field FWI ready:                       false
```

Run `175`:

```text
controlled collection archive checksum bridge smoke
archive preflight checks:              23
archive blocking findings:             0
checksum ledger rows:                  9
checksum accepted rows:                9
checksum blocking findings:            0
combined synthetic smoke pass:         true
synthetic smoke only:                  true
scientific field claim ready:          false
field FWI ready:                       false
```

Current field decision:

```text
The checksum ledger gate is mechanically ready and has both blank-fail and
synthetic-pass evidence. The archive layout and operator handoff are also
defined, and the archive preflight now fails cleanly against the empty real
archive. The archive-preflight smoke passes on a complete synthetic archive.
The archive-checksum bridge smoke proves archived files can hash into accepted
ledger rows. These are still not measured field evidence. Real controlled-
collection files and metadata must fill the archive layout and pass checksum,
intake, structural, archive, and provenance gates before any field FWI, heavy
GPU work, field 3D/HPC, or neural-network training.
```

## Presentation Pack

Current generated pack:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
```

Current result:

```text
claims:                               37
ready scoped/design/preflight/smoke:  31
blocked:                              6
GPU/FWI/3D launch ready:              false
```

Storyboard:

```text
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
ready claims referenced:              31
blocked claims preserved:             6
```

Local 2D matrix:

```text
outputs/summary_tables/136_local_2d_next_experiment_design_matrix
presentation claim count:             37
new local 2D GPU ready:               false
broad GPU queue ready:                false
detector-seeded FWI ready:            false
field transfer ready:                 false
```

## Validation

Focused tests:

```text
69 passed
```

Full suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1109 passed in 30.33s
```

Figure checks:

```text
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
run 169: 1816x807, dynamic range=255
run 170: 1744x774, dynamic range=255
run 171: 1888x807, dynamic range=255
run 172: 2142x845, dynamic range=255
run 173: 1996x790, dynamic range=255
run 174: 1996x790, dynamic range=255
run 175: 1816x772, dynamic range=255
pack 135: 2052x954, dynamic range=255
matrix 136: 2464x880, dynamic range=255
storyboard 137: 2286x851, dynamic range=255
```

## Next Defensible Work

Continue with one of:

```text
1. BEM: define a real 3D FDTD engine/import implementation contract that can fill run 077.
2. Field: add an operator-handoff acceptance rehearsal/preflight over the real-archive checklist.
3. Local 2D: refine report claim boundaries using the 37-claim evidence pack.
```
