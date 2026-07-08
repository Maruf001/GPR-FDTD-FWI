# Local 2D Experiment 1394: Reduced Sentinel Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the run `1393` reduced-sentinel validator by applying controlled
mutations to the run `1392` reduced 11-row sentinel candidate.

Run `1393` showed that the reduced sentinel is a valid optional fast-smoke
suite. This run checks the other side of that claim: the validator must reject
stale or damaged sentinel tables when a required margin row is missing, a
coverage-mandatory row is missing, a row key is duplicated, or a previously
removed redundant row is reintroduced.

This is a CPU-only table validation. It does not run FDTD, FWI, GPU work,
field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1394_local_2d_state_consistent_reduced_sentinel_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_sensitivity_rows.csv
data/local_2d_state_consistent_reduced_sentinel_sensitivity_summary.json
figures/local_2d_state_consistent_reduced_sentinel_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_SENSITIVITY.md
scripts/run_local_2d_state_consistent_reduced_sentinel_sensitivity.py
scripts/test_local_2d_state_consistent_reduced_sentinel_sensitivity.py
```

## Result

```text
scenarios:                         5
expected passing scenarios:         1
expected failing scenarios:         4
observed passing scenarios:         1
observed failing scenarios:         4
unexpected outcomes:                0
reduced sentinel sensitivity ready: true
sentinel replaces full pack:        false
full pack remains authoritative:    true
GPU ready:                          false
field FWI ready:                    false
3D/HPC ready:                       false
```

Scenario results:

| Scenario | Expected pass | Observed pass | Failing checks |
| --- | --- | --- | --- |
| exact_control | true | true | none |
| missing_margin_addon | false | false | row_count_matches_summary; required_tokens_still_covered; margin_addons_preserved |
| missing_coverage_mandatory_row | false | false | row_count_matches_summary; required_tokens_still_covered |
| duplicate_key_row | false | false | row_count_matches_summary; no_duplicate_keys |
| removed_row_reintroduced | false | false | row_count_matches_summary |

## Interpretation

The sensitivity smoke behaves as expected. The exact reduced sentinel passes,
while each intentionally damaged table fails for the expected reason.

This closes the reduced-sentinel tooling branch. The 11-row table is a useful
fast smoke guard for local state-consistency edits, but it is not a replacement
for the full 88-row core regression pack.

## Decision

Use the run `1392`/`1393` reduced sentinel plus this run `1394` sensitivity
smoke as the preferred optional fast-smoke layer. The full 88-row core pack
remains authoritative, and GPU work, field transfer, field FWI, and 3D/HPC
remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_sensitivity.py
6 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_sensitivity.png
2285x847, dynamic range=255
```
