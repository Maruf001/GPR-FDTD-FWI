# Local 2D Source-Factor CPU Smoke Partial Output Correction

Date: 2026-06-25

## Scope

This checkpoint records output `179`, the correction to the capped CPU
source-factor smoke audit after detecting the optimizer runner's auto-prefixed
partial output folder.

## Output

```text
outputs/summary_tables/179_local_2d_source_factor_cpu_smoke_partial_output_correction
```

Tracked note:

```text
docs/experiments/889_local_2d_source_factor_cpu_smoke_partial_output_correction.md
```

## Result

```text
source run:                              177_local_2d_source_factor_cpu_smoke_cap_audit
cap summary said output folder exists:   false
partial output exists:                   true
candidate CSV count:                     2
run manifest exists:                     false
summary JSON exists:                     false
confidence CSV exists:                   false
objective diagnostics CSV exists:        false
figure file count:                       0
complete optimizer output:               false
usable evidence ready:                   false
runner auto-prefix detected:             true
future run name should omit numeric ID:  true
micro command naming refresh needed:     true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

The capped run remains non-evidence. It has only partial candidate CSVs and no
manifest, summary, confidence table, objective diagnostics, or figures.

The correction changes the execution procedure: future optimizer `--run-name`
values should omit numeric prefixes, because the runner allocates and prepends
the experiment ID itself.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_cpu_smoke_partial_output_correction.py
sha256: c2474eb6c162ec7c44ae0ecef7088c0431b11df9f2bafc5299143019f953fa51

test_local_2d_source_factor_cpu_smoke_partial_output_correction.py
sha256: ccf48c8a4731e14b83b468d161a4fdf4e22834d79f8603143ce768eb3d633aae
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_smoke_partial_output_correction.py
2 passed
```

Python compile check:

```text
run_local_2d_source_factor_cpu_smoke_partial_output_correction.py: pass
tests/test_local_2d_source_factor_cpu_smoke_partial_output_correction.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_smoke_partial_output_correction.png
1456x736, dynamic range=255
```

Marathon status: active. The next branch is a corrected micro-smoke command
design that starts from a duplicated run-specific script and omits numeric
prefixes from optimizer run names.
