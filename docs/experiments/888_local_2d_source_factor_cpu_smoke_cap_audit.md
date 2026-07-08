# Experiment 888: Local 2D Source-Factor CPU Smoke Cap Audit

Date: 2026-06-25

## Purpose

Record the capped execution attempt for the first numbered CPU source-factor
command from run `175`.

This is an execution-cost audit. It does not complete the optimizer run, run the
full command batch, use GPU, transfer to field, run field FWI, or train neural
networks.

## Output

```text
outputs/summary_tables/177_local_2d_source_factor_cpu_smoke_cap_audit
```

Key artifacts:

```text
data/local_2d_source_factor_cpu_smoke_cap_audit.csv
data/local_2d_source_factor_cpu_smoke_cap_audit_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_SMOKE_CAP_AUDIT.md
figures/local_2d_source_factor_cpu_smoke_cap_audit.png
scripts/run_local_2d_source_factor_cpu_smoke_cap_audit.py
scripts/test_local_2d_source_factor_cpu_smoke_cap_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
attempted command index:                 1
attempted experiment ID:                 1359
cap seconds:                             3600
observed elapsed seconds at cap:         3666
exit code:                               130
capped by agent:                         true
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

## Interpretation

The first numbered CPU command did not complete within a one-hour smoke cap and
produced no output folder. The command used one CPU core continuously and stayed
within RAM/GPU limits, but the current full optimizer command is too expensive
as a smoke test.

## Decision

Do not run the full nine-command CPU batch. Design a cheaper micro-smoke with a
smaller geometry/objective workload before attempting source-factor execution
again.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_smoke_cap_audit.py
sha256: e9f67d4b50ba08c9c6ba3cf970072eac83bc18c77334ca4c1e2d8a76e0d2be45

test_local_2d_source_factor_cpu_smoke_cap_audit.py
sha256: 27d4534d5992f819ce6675ce9160851f2553bb78ce16da922402bed935dbc918
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script and should reduce the smoke workload before any full
command batch.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_smoke_cap_audit.py
2 passed
```

Figure check:

```text
local_2d_source_factor_cpu_smoke_cap_audit.png
1276x738, dynamic range=255
```
