# Local 2D Source-Factor Full-Factorial Design Contract

Date: 2026-06-25

## Scope

This checkpoint records output `170`, the corrected full-factorial local 2D
source-factor design contract after run `169`.

## Output

```text
outputs/summary_tables/170_local_2d_source_factor_full_factorial_design_contract
```

Tracked note:

```text
docs/experiments/883_local_2d_source_factor_full_factorial_design_contract.md
```

## Result

```text
sensitive cases:                         2
design rows:                             16
variant count per case:                  8
cached pair-observed design rows:        5
cached available design rows:            7
required counterfactual design rows:     9
new variant rows added after audit:      4
full-factorial design ready:             true
CPU execution contract ready:            true
cached execution ready:                  false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Run `170` supersedes the six-variant run `167` contract for future local 2D
source-factor execution. The corrected design has all eight source-factor
combinations per sensitive case and explicitly separates cached inputs from the
nine required counterfactual diagnostics.

No new FDTD, GPU work, field transfer, broad source robustness, or
time-zero-only explanation is justified until those counterfactual diagnostics
exist and pass the matched 1 mm geometry/radius gate.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_full_factorial_design_contract.py
sha256: 5ef15ddc921bc3236ab763c7aecf17222aaed35274b114d25fc555d5e83169cb

test_local_2d_source_factor_full_factorial_design_contract.py
sha256: f13a7829c876fb8635c5e401e4d0f49da6456c7a8da96728158da826d599a1f3
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_full_factorial_design_contract.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_full_factorial_design_contract.py: pass
tests/test_local_2d_source_factor_full_factorial_design_contract.py: pass
```

Figure check:

```text
local_2d_source_factor_full_factorial_design_contract.png
1780x771, dynamic range=255
```

Marathon status: active. The next branch should refresh the milestone snapshot
audit and then determine whether the nine required counterfactual diagnostics
can be generated from cached optimizer artifacts or require a new bounded CPU
diagnostic executor.
