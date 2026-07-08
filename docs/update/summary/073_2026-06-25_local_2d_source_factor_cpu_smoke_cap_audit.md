# Local 2D Source-Factor CPU Smoke Cap Audit

Date: 2026-06-25

## Scope

This checkpoint records output `177`, the capped execution-cost audit for the
first numbered local 2D source-factor CPU command.

## Output

```text
outputs/summary_tables/177_local_2d_source_factor_cpu_smoke_cap_audit
```

Tracked note:

```text
docs/experiments/888_local_2d_source_factor_cpu_smoke_cap_audit.md
```

## Result

```text
attempted command index:                 1
attempted experiment ID:                 1359
cap seconds:                             3600
observed elapsed seconds at cap:         3666
exit code:                               130
output folder exists after cap:          false
residual process after cap:              false
single CPU smoke completed:              false
single CPU smoke practical:              false
micro-smoke needed:                      true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Do not run the full nine-command CPU batch. The current full optimizer command
is not a practical smoke path. The next useful branch is a cheaper micro-smoke
design with reduced geometry/objective workload, followed by another static
parse gate before execution.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_smoke_cap_audit.py
sha256: e9f67d4b50ba08c9c6ba3cf970072eac83bc18c77334ca4c1e2d8a76e0d2be45

test_local_2d_source_factor_cpu_smoke_cap_audit.py
sha256: 27d4534d5992f819ce6675ce9160851f2553bb78ce16da922402bed935dbc918
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_smoke_cap_audit.py
2 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_smoke_cap_audit.py: pass
tests/test_local_2d_source_factor_cpu_smoke_cap_audit.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_smoke_cap_audit.png
1276x738, dynamic range=255
```

Marathon status: active. The next branch should design a reduced micro-smoke
instead of running the full CPU wrapper command.
