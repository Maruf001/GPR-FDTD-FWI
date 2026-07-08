# BEM Experiment 067: Replacement Contract Refresh

Date: 2026-06-25

## Purpose

Refresh the BEM replacement contract after the run `066` layered Sommerfeld
stress pass.

The older run `060` contract predated the scalar Sommerfeld result and treated
layered replacement as not ready. This run records the updated boundary between
supported and blocked claims.

## Output

```text
outputs/bem_experiments/067_project_core_bem_replacement_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_replacement_contract_refresh.csv
data/project_core_bem_replacement_contract_refresh_summary.json
figures/project_core_bem_replacement_contract_refresh.png
docs/PROJECT_CORE_BEM_REPLACEMENT_CONTRACT_REFRESH.md
```

## Result

```text
contract rows:                       7
homogeneous replacement ready:       true
layered Sommerfeld ready:            true
layered tabulated fallback ready:    true
compact 30mm layered ready:          false
low-order layered image ready:       false
field claim ready:                   false
3D/FWI/GPU ready:                    false
```

Contract rows:

| Item | Active method | Evidence | Value | Ready | Scope |
| --- | --- | --- | ---: | --- | --- |
| homogeneous 2D replacement | boundary_image | 057 | 0.667995713341894 | true | tested homogeneous project-core 2D envelope |
| layered 2D replacement | scalar_sommerfeld_proxy | 066 | 0.6497571611891657 | true | tested air/concrete layered project-core 2D envelope |
| layered fallback | full_10mm_tabulated_surface_cache | 062 | 0.697021169360853 | true | cached dense project-domain layered surface |
| compact layered sampling | 30mm_grid | 064 | 0.8468025283677086 | false | not promoted; epsr-12 stress fails |
| low-order layered image replacement | boundary_image | 058 | 0.9920836859251249 | false | blocked; homogeneous images do not transfer to layered case |
| measured-field claim | none | 163-166 | 0.0 | false | blocked until real controlled files and provenance pass |
| 3D/FWI/GPU escalation | none | 067 | 0.0 | false | blocked; current evidence is 2D project-core only |

## Interpretation

The active BEM replacement contract now has two scoped 2D paths:

```text
homogeneous project-core cases: boundary-image replacement
layered project-core cases:     scalar Sommerfeld proxy
```

The full 10 mm tabulated layered surface remains a fallback. Compact 30 mm
sampling and low-order layered image replacements are blocked.

## Decision

Use boundary images for homogeneous 2D BEM replacement and the scalar
Sommerfeld proxy for layered 2D BEM replacement inside the tested envelopes.

Keep measured-field, 3D, FWI, GPU, and historical `outputs/experiments` archive
claims blocked pending matched gates.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_replacement_contract_refresh.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_replacement_contract_refresh.py
pass
```

Figure check:

```text
project_core_bem_replacement_contract_refresh.png
2104x842, dynamic range=255
```
