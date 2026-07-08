# BEM And Field Gate Integration Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the latest local marathon block after extending the
BEM external-return handoff and the field controlled-collection archive gates.

No real 3D FDTD, field FWI, heavy GPU work, field 3D/HPC, or neural-network
training was launched.

## BEM External-Return Additions

Run `085`:

```text
external 3D FDTD return acceptance pack
required return files:              2
metadata requirements:              12
acceptance steps:                   8
gate crosswalk rows:                8
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

Run `086`:

```text
external 3D FDTD return metadata preflight
metadata requirements:              12
preflight checks:                   7
passed checks:                      0
failed checks:                      7
ready for return preflight:         false
```

Run `087`:

```text
external 3D FDTD return metadata preflight smoke
synthetic returned files:           2
metadata rows:                      12
preflight checks:                   7
passed checks:                      7
synthetic smoke only:               true
real external FDTD data present:    false
```

Run `088`:

```text
external 3D FDTD return full bundle smoke
synthetic frequency files:          2
frequency rows per run:             124
metadata preflight checks:          7
return preflight checks:            10
synthetic full bundle pass:         true
synthetic smoke only:               true
real external FDTD data present:    false
```

Interpretation:

```text
The external-return path is now acceptably specified and testable. It can fail
cleanly on missing real data and pass on complete synthetic metadata plus
frequency-bin files. Real external FDTD data are still absent, so real BEM/FDTD
comparison and 3D validation remain blocked.
```

## Field Gate Additions

Run `174`:

```text
controlled collection archive preflight smoke
preflight checks:                   23
passed checks:                      23
synthetic smoke only:               true
scientific field claim ready:       false
field FWI ready:                    false
```

Run `175`:

```text
controlled collection archive checksum bridge smoke
archive preflight checks:           23
archive blocking findings:          0
checksum ledger rows:               9
checksum accepted rows:             9
checksum blocking findings:         0
combined synthetic smoke pass:      true
synthetic smoke only:               true
field FWI ready:                    false
```

Interpretation:

```text
The field archive gate and archive-to-checksum workflow are now proven
satisfiable on synthetic archives. The real pending archive is still absent.
Measured-field claims, provenance acceptance, field FWI, heavy GPU work, and
field 3D/HPC remain blocked until real controlled-collection files pass the
same gates.
```

## Presentation Pack

Current generated pack:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
```

Current result:

```text
claims:                              37
ready scoped/design/preflight/smoke: 31
blocked:                             6
GPU/FWI/3D launch ready:             false
```

Storyboard:

```text
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
ready claims referenced:             31
blocked claims preserved:            6
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
run 088: 1564x736, dynamic range=255
run 175: 1816x772, dynamic range=255
pack 135: 2052x954, dynamic range=255
matrix 136: 2464x880, dynamic range=255
storyboard 137: 2286x851, dynamic range=255
```

## Current Decision

```text
BEM: the external-return acceptance path is ready for real returned files, but
3D validation remains blocked until those files exist and pass real gates.

Field: the archive/checksum workflow is ready as synthetic-validated
collection-day infrastructure, but measured field evidence remains blocked
until real files and metadata pass the same gates.

Local 2D: no new fixed-radius GPU/FWI branch is justified from current
evidence; use the current mechanism result in reporting until a new 2D
hypothesis is defined.
```

The marathon request remains active.
