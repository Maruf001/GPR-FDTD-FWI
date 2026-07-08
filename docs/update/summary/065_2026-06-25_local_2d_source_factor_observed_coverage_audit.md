# Local 2D Source-Factor Observed Coverage Audit

Date: 2026-06-25

## Scope

This checkpoint records output `169`, a cached audit of whether the run `167`
six-variant source-factor design covers the observed factor signatures in run
`159`.

## Output

```text
outputs/summary_tables/169_local_2d_source_factor_observed_coverage_audit
```

Tracked note:

```text
docs/experiments/882_local_2d_source_factor_observed_coverage_audit.md
```

## Result

```text
sensitive cases:                         2
pair rows audited:                       16
current design variants per case:        6
recommended variants per case:           8
incomplete current-design cases:         2
cached factorial-gap cases:              2
cases with observed outside-design row:  1
observed variants outside current design:1
revised design needed:                   true
cached execution ready:                  false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Run `167` was useful but undercomplete. The next local 2D source-factor design
must use the full eight-variant factorial, including `time_amplitude_only` and
`time_frequency_only`. Cached pair deltas are not enough to execute the full
isolation, and no new FDTD, GPU work, field transfer, broad source robustness,
or time-zero-only explanation is justified from this result.

## Milestone Snapshot

This milestone froze:

```text
run_local_2d_source_factor_observed_coverage_audit.py
sha256: 3953ad476d3ce9cb7990f3d63b129643d08c83d1474842d789cd94f5e864deeb

test_local_2d_source_factor_observed_coverage_audit.py
sha256: 53f4f5c8b646cac484a8d1a8931ada125fa37b6e697d1c866f9d9fe29e773906
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_observed_coverage_audit.py
3 passed
```

Python compile check:

```text
run_local_2d_source_factor_observed_coverage_audit.py: pass
tests/test_local_2d_source_factor_observed_coverage_audit.py: pass
```

Figure check:

```text
local_2d_source_factor_observed_coverage_audit.png
1816x771, dynamic range=255
```

Marathon status: active. The next branch should duplicate the design-contract
script into a revised eight-variant source-factor contract.
