# Local 2D Source-Factor X/Z/Radius Decision Boundary Audit

Date: 2026-06-25

## Scope

This checkpoint records output `194`, a CPU-light decision-boundary audit over
completed x/z/radius source-factor runs `188` and `192`.

## Output

```text
outputs/summary_tables/194_local_2d_source_factor_xzradius_decision_boundary_audit
```

Tracked note:

```text
docs/experiments/901_local_2d_source_factor_xzradius_decision_boundary_audit.md
```

## Result

```text
source executions audited:                 2
case rows audited:                         4
update cases truth depth/radius supported: 2 / 2
companion cases truth depth/radius support:1 / 2
families with all-case agreement:          1 / 2
families with mixed response:              1
truth x in tested envelope:                false
full batch ready:                          false
GPU work ready:                            false
field transfer ready:                      false
```

## Decision

The x/z/radius source-factor branch supports only a bounded local claim: the
two update cases select target-0 truth depth/radius, but one companion case
disagrees and the truth x coordinate was outside the tested envelope. Do not
launch full-batch source-factor runs, GPU work, or field transfer from this
evidence.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_xzradius_decision_boundary_audit.py
sha256: 934d30001955a39843b0c9a282fe9b1a01c6dcdd71b05496ca3e9fed299d1809

test_local_2d_source_factor_xzradius_decision_boundary_audit.py
sha256: b9c59d1b5a82589843193b6d490057fb475d1291e7e3a9372049f2a8abff5ab5
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_xzradius_decision_boundary_audit.py
3 passed
```

Figure check:

```text
local_2d_source_factor_xzradius_decision_boundary_audit.png
1847x748, dynamic range=255
```

Marathon status: active. The next branch should move away from broad
source-factor escalation unless a new targeted hypothesis is defined.
