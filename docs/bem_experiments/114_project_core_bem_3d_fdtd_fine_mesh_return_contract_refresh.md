# BEM Experiment 114: Fine-Mesh External Return Contract Refresh

Date: 2026-06-27

## Purpose

Refresh the external 3D FDTD return contract after the run `113` fine-mesh BEM
frequency-grid audit.

The existing external FDTD request from run `100` asks for four frequencies and
31 receivers for each of two runs: target-present and background. Run `113`
shows that the BEM-side high-frequency reference should use the 8x20 mesh,
especially at 3.0 GHz. This run converts that finding into an updated return
contract without invalidating the original four-bin handoff.

This run does not run FDTD, install returned files, perform BEM/FDTD
comparison, make a 3D validation claim, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/114_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_frequency_plan.csv
data/project_core_bem_3d_fdtd_fine_mesh_return_options.csv
data/project_core_bem_3d_fdtd_fine_mesh_contract_updates.csv
data/project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_RETURN_CONTRACT_REFRESH.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
original request frequencies:        4
fine-mesh grid frequencies:          9
optional added frequencies:          5
receiver count:                      31
minimal rows per file:               124
minimal paired target/background rows:248
full rows per file:                  279
full paired target/background rows:  558
3 GHz 6x16-to-8x20 relative L2:      0.055639649360411644
combined metadata fields required:   25
contract updates:                    5
blocking contract updates:           4
minimal return contract ready:       true
preferred full-grid contract ready:  true
real external FDTD data present:     false
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
local 3D FDTD launch ready:          false
GPU/HPC ready:                       false
```

Return options:

| Option | Frequencies | Rows per file | Paired rows | Status |
| --- | ---: | ---: | ---: | --- |
| minimal original four-bin return | 4 | 124 | 248 | acceptable if real files pass gates |
| preferred full fine-mesh grid return | 9 | 279 | 558 | preferred if external FDTD cost allows |

Contract updates:

| Update | Blocking | Requirement |
| --- | --- | --- |
| BEM reference mesh | true | Use the 8x20 BEM mesh as the comparison reference for returned frequency bins. |
| Minimal return still valid | false | Do not invalidate the original four-bin external request. |
| Strict metadata gate | true | Keep the 25-field metadata ledger gate. |
| Paired target/background | true | Target and background files must contain the same receiver and frequency keys. |
| Real return boundary | true | No BEM/FDTD validation claim before real returned FDTD files pass all gates. |

## Interpretation

The original four-bin external FDTD request remains valid as the minimal return
surface. If those real files arrive and pass the upgraded metadata and
frequency-bin gates, they can be used for comparison.

The preferred return is now clearer: if external FDTD cost allows, ask for all
nine run `113` fine-mesh frequencies. This would provide a denser validation
curve with 558 paired target/background rows instead of 248.

In both cases, the 3.0 GHz BEM-side reference should be the 8x20 mesh, not the
faster 6x16 mesh. The 6x16-to-8x20 relative L2 at 3.0 GHz is
0.055639649360411644, which is large enough to matter for validation.

## Decision

Use this as the current external-return contract refresh:

```text
Accept a real four-bin return if it passes all gates.
Prefer a nine-bin return if external FDTD cost allows.
Use the 8x20 BEM reference mesh for returned frequency-bin comparison.
```

Keep BEM/FDTD comparison, 3D validation, local 3D FDTD launch, and GPU/HPC work
blocked until real target/background files pass the 25-field metadata gate and
frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.py
sha256: 656e02ea99b9f3ebc4a390b86a64f23228dc1797058d9a24d26b8845076a1938

test_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.py
sha256: c3386cf432697af9e4c6d4181335d359846b61d10613f06e97f9829829b38b2f
```

Subsequent related BEM 3D return-intake experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.py
3 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.png
2680x827, dynamic range=255
```
