# Local 2D Experiment 1412: Repaired Execution CI Adoption Checklist

Date: 2026-06-28

## Purpose

Turn the repaired local 2D regression execution dry run and guarded claim
boundary into a CI adoption checklist.

This run connects:

```text
run 1406: repaired regression execution dry run
run 1411: repaired execution claim-boundary sensitivity
```

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1412_local_2d_state_consistent_repaired_execution_ci_adoption_checklist
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_adoption_rows.csv
data/local_2d_state_consistent_repaired_execution_ci_adoption_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_adoption_checklist.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ADOPTION_CHECKLIST.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_adoption_checklist.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_adoption_checklist.py
```

## Result

```text
source repaired dry run ready:              true
source claim-boundary sensitivity ready:    true
adoption routes:                            6
fast-smoke routes:                          2
full-pack-required routes:                  2
new-design-required routes:                 1
blocked-current-evidence routes:            1
locally executable routes:                  4
blocked-by-design routes:                   2
reduced sentinel rows:                      11
repaired full core rows:                    88
CI adoption checklist ready:                true
full pack remains authoritative:            true
sentinel replaces full pack:                false
physical claim ready:                       false
GPU work ready:                             false
field transfer ready:                       false
field FWI ready:                            false
ready for 3D/HPC:                           false
```

The route split is:

| Route family | Count | Action |
| --- | ---: | --- |
| Consumer smoke | 2 | Run the 11-row reduced sentinel only |
| Boundary-sensitive local 2D change | 2 | Run the repaired 88-row full core table |
| Physical or broad-radius claim | 1 | Requires a new design before support |
| GPU, field transfer, field FWI, or 3D/HPC | 1 | Blocked by current local 2D evidence |

## Interpretation

The repaired local 2D regression guard now has an actionable adoption
checklist. Consumer wiring, schema parsing, plotting, and harmless row-order
changes may use the reduced 11-row sentinel as fast smoke. Row-key,
boundary-objective, margin, or token-definition changes require the repaired
88-row full core table. Physical claims, broad-radius tolerance, GPU work,
field transfer, field FWI, and 3D/HPC remain outside the support of this local
2D guard.

## Decision

Use run `1412` as the local 2D CI adoption checklist. Keep the full 88-row core
table authoritative, keep the 11-row sentinel fast-smoke-only, and do not
promote physical claims, GPU work, field transfer, field FWI, or 3D/HPC from
this guard.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_adoption_checklist.py
5 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_adoption_checklist.png
2572x840, dynamic range=255
```
