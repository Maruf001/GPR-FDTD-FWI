# Local 2D Experiment 1395: Reduced Sentinel Adoption Contract

Date: 2026-06-27

## Purpose

Define the safe-use boundary for the reduced 11-row local 2D
state-consistency sentinel suite.

Runs `1392` through `1394` produced, validated, and stress-tested the reduced
sentinel. This run converts that result into an explicit adoption contract so
the reduced sentinel is not mistaken for a replacement of the full 88-row core
regression pack.

This is a CPU-only contract audit. It does not run FDTD, FWI, GPU work, field
transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1395_local_2d_state_consistent_reduced_sentinel_adoption_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_adoption_contract_rows.csv
data/local_2d_state_consistent_reduced_sentinel_adoption_contract_summary.json
figures/local_2d_state_consistent_reduced_sentinel_adoption_contract.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_ADOPTION_CONTRACT.md
scripts/run_local_2d_state_consistent_reduced_sentinel_adoption_contract.py
scripts/test_local_2d_state_consistent_reduced_sentinel_adoption_contract.py
```

## Result

```text
contract items:                       6
contract passes:                      6
blocking failures:                    0
reduced sentinel rows:                11
required coverage tokens:             32
sensitivity scenarios:                5
fast-smoke adoptable:                 true
full pack required for boundaries:    true
sentinel replaces full pack:          false
broad radius tolerance promoted:      false
GPU ready:                            false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

Contract items:

| Contract item | Status | Allowed use | Blocked use |
| --- | --- | --- | --- |
| reduced_candidate_validated | pass | optional fast smoke for local state-consistency table consumers | none beyond the validator result |
| sensitivity_guard_ready | pass | guard against stale, duplicated, or incomplete sentinel tables | none beyond the sensitivity result |
| full_pack_remains_authoritative | pass | fast precheck before the full pack | replacement of the 88-row core regression pack |
| boundary_changes_require_full_pack | pass | consumer wiring, table parsing, plotting, and schema smoke | acceptance-boundary, objective-support, margin-threshold, or token-definition changes |
| gpu_field_3d_promotion_blocked | pass | local CPU smoke only | GPU queue, field transfer, field FWI, or 3D/HPC escalation |
| reduced_row_count_fixed_for_current_pack | pass | current 11-row fast smoke suite | silent row additions or deletions without rerunning validation and sensitivity |

## Interpretation

The reduced 11-row sentinel is safe to adopt as an optional fast-smoke suite
for local state-consistency consumers. It is not an acceptance boundary and
does not replace the 88-row core regression pack.

## Decision

Use the reduced sentinel for CPU-only fast smoke on consumer wiring, schema,
parsing, and plotting changes. Run the full core pack for boundary, objective,
margin, token-definition, GPU, field-transfer, field-FWI, or 3D/HPC decisions.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_adoption_contract.py
4 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_adoption_contract.png
2285x838, dynamic range=255
```
