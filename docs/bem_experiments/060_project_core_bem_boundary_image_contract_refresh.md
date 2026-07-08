# BEM Experiment 060: Boundary-Image Contract Refresh

Date: 2026-06-25

## Purpose

Refresh the BEM replacement contract after the homogeneous stress pass in run
`057` and the layered failures in runs `058` and `059`.

This is a CPU-only synthesis over existing summaries. It does not run FDTD,
field preprocessing, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/060_project_core_bem_boundary_image_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_boundary_image_contract_refresh.csv
data/project_core_bem_boundary_image_contract_refresh_summary.json
figures/project_core_bem_boundary_image_contract_refresh.png
docs/PROJECT_CORE_BEM_BOUNDARY_IMAGE_CONTRACT_REFRESH.md
```

## Result

```text
contract rows:                            8
homogeneous boundary-image candidate:     ready
layered boundary-image replacement:       not ready
dense layered surface required:           true
field claim ready:                        false
historical outputs/experiments claim:     false
3D/FWI/GPU escalation ready:              false
```

Contract rows:

| Claim | Evidence | Value | Ready | Decision |
| --- | --- | ---: | --- | --- |
| homogeneous field-table replacement | 055 | 0.3301113956330722 | true | supported inside the tested homogeneous project-core field-table gate |
| homogeneous contrast scattering replay | 056 | 0.5620892946687726 | true | supported for the tested epsr ladder |
| homogeneous geometry and offset stress replay | 057 | 0.667995713341894 | true | supported for saved lateral, depth/radius, and Tx/Rx-offset stress cases |
| layered dense project-domain surface | 047 | 0.697021169360853 | true | conditionally supported only with dense project-domain surface sampling |
| layered boundary-image replacement | 058 | 0.9920836859251249 | false | not supported; homogeneous replacement does not transfer to layered media |
| layered low-order interface basis | 059 | 1.0946737347877629 | false | not supported; simple optical/interface images do not repair the layered failure |
| field archive claim | 163 | 9.0 | false | blocked until real field files and provenance replace the dry-run packet |
| 3D/FWI/GPU escalation | 060 | 0.0 | false | blocked; no matched 3D or field validation gate exists for the BEM replacement |

## Interpretation

The boundary-image replacement is validated only for the tested homogeneous
project-core 2D envelope. Layered media remain conditional on dense
project-domain surface sampling. Low-order layer-aware analytic surrogates did
not repair the layered failure.

## Decision

Use the boundary-image model for homogeneous 2D BEM replacement experiments
only.

Keep layered, field, 3D, FWI, GPU, and historical `outputs/experiments` archive
claims blocked until their own matched gates pass.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_boundary_image_contract_refresh.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_boundary_image_contract_refresh.py
pass
```

Figure check:

```text
project_core_bem_boundary_image_contract_refresh.png
1888x846, dynamic range=255
```
