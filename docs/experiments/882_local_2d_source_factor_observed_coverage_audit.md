# Experiment 882: Local 2D Source-Factor Observed Coverage Audit

Date: 2026-06-25

## Purpose

Audit whether the six-variant source-factor design from run `167` covers the
source-factor signatures already visible in the cached matched pair deltas from
run `159`.

This is a cached coverage audit only. It does not run new FDTD, GPU work, field
transfer, field FWI, or neural-network training.

## Output

```text
outputs/summary_tables/169_local_2d_source_factor_observed_coverage_audit
```

Key artifacts:

```text
data/local_2d_source_factor_observed_coverage_rows.csv
data/local_2d_source_factor_full_factorial_variants.csv
data/local_2d_source_factor_observed_coverage_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_OBSERVED_COVERAGE_AUDIT.md
figures/local_2d_source_factor_observed_coverage_audit.png
scripts/run_local_2d_source_factor_observed_coverage_audit.py
scripts/test_local_2d_source_factor_observed_coverage_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitive cases:                         2
pair rows audited:                       16
current design variants per case:        6
recommended variants per case:           8
full-factorial variant count:            8
incomplete current-design cases:         2
cached factorial-gap cases:              2
cases with observed outside-design row:  1
observed variants outside current design:1
cache has all factorial variants:        false
current design full factorial complete:  false
revised design needed:                   true
cached execution ready:                  false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Coverage

| Case | Pairs | Current variants | Observed variants | Observed outside current design | Missing current-design variants |
| --- | ---: | ---: | --- | --- | --- |
| max amplitude stress | 6 | 6 | amplitude_frequency_only, combined_observed | none | time_amplitude_only, time_frequency_only |
| max geometry instability | 10 | 6 | amplitude_frequency_only, combined_observed, time_frequency_only | time_frequency_only | time_amplitude_only, time_frequency_only |

## Interpretation

The six-variant source-factor contract is undercomplete for a true three-factor
isolation. A full design over time shift, amplitude scale, and frequency/source
scale has eight variants per case:

```text
nominal_replay
time_shift_only
amplitude_only
frequency_only
time_amplitude_only
time_frequency_only
amplitude_frequency_only
combined_observed
```

The cached pair deltas already show a `time_frequency_only` signature in the
`max_geometry_instability` case, which the six-variant contract did not include.
The cache also lacks full factorial coverage, so this is not an executed
factorial isolation result.

## Decision

Revise the next local 2D source-factor design to the full eight-variant
factorial before claiming execution readiness. Keep cached execution, new FDTD,
GPU work, field transfer, broad source robustness, and time-zero-only
explanation blocked.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_observed_coverage_audit.py
sha256: 3953ad476d3ce9cb7990f3d63b129643d08c83d1474842d789cd94f5e864deeb

test_local_2d_source_factor_observed_coverage_audit.py
sha256: 53f4f5c8b646cac484a8d1a8931ada125fa37b6e697d1c866f9d9fe29e773906
```

Subsequent local 2D source-factor experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_observed_coverage_audit.py
3 passed
```

Figure check:

```text
local_2d_source_factor_observed_coverage_audit.png
1816x771, dynamic range=255
```
