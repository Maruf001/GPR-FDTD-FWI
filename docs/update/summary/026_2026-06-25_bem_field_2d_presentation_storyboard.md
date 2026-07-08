# BEM, Field, And Local 2D Presentation Storyboard

Date: 2026-06-25

## Scope

This checkpoint turns the current evidence pack into a concise presentation
order. It does not change any scientific gate.

Output:

```text
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
```

Key artifacts:

```text
data/bem_field_2d_presentation_storyboard.csv
data/bem_field_2d_presentation_storyboard_summary.json
figures/bem_field_2d_presentation_storyboard.png
docs/BEM_FIELD_2D_PRESENTATION_STORYBOARD.md
```

## Result

```text
slide count:                        8
tracks covered:                     7
blocked claims preserved:           7
ready claims referenced:            36
GPU/FWI/3D launch ready:            false
```

## Slide Order

1. Current evidence boundary
2. Local 2D detector result
3. 2D BEM replacement evidence
4. Project-core payload boundary
5. 3D BEM path: finite-rebar backend, dipole source, manifests, validator, comparator schema, synthetic smokes, import templates, execution-gap audit, extractor contract, extractor smoke, engine-candidate decision, external data-request pack, return preflight, return handoff, metadata preflight, metadata smoke, and full return-bundle smoke
6. Field collection gate: intake, checklist, checksum ledger, checksum preflight, synthetic smoke, archive layout, operator handoff, archive preflight, archive-preflight smoke, and archive-checksum bridge
7. No-go claims
8. Decision requests: real field collection, paired 3D FDTD data, or presentation/report packaging around the payload contract

## Decision

Use this as a presentation ordering aid. Keep the no-go claims explicit: no
field FWI, heavy GPU, field 3D/HPC, neural-network training, or 3D validation
claim follows from the current evidence.

## Validation

Figure check:

```text
2286x851, dynamic range=255
```
