# GSSI51600S Profile Event-Content Audit Checkpoint

## What Changed

- Added `run_gssi51600s_profile_event_content_audit.py`.
- Added unit tests for profile/window summary behavior.
- Audited the trusted GSSI 51600S local event window across profiles `0-3`.
- Compared per-profile event energy, mean amplitude, time-center index, and receiver-center index over the same five optimizer windows used in the current conservative product candidate.

## Key Numbers

- Event-content audit artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/095_gssi51600s_profile_event_content_audit_current_window/`.
- Summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/095_gssi51600s_profile_event_content_audit_current_window/data/gssi51600s_profile_event_content_summary.json`.
- Decision: `gssi51600s_profile_event_content_audit_ready`.
- Highest-energy profile: `3`.
- Latest time-center profile: `3`.
- Earliest time-center profile: `2`.
- Mean profile metrics:
  - profile `0`: mean-square energy `0.05567`, amplitude mean `0.13243`, time-center index `50.62`.
  - profile `1`: mean-square energy `0.06347`, amplitude mean `0.13867`, time-center index `51.73`.
  - profile `2`: mean-square energy `0.05749`, amplitude mean `0.12790`, time-center index `45.56`.
  - profile `3`: mean-square energy `0.06830`, amplitude mean `0.14132`, time-center index `56.54`.

## Current Decision

The profile-subset split is not explained by simple row ordering. Profile `3` carries the strongest and latest local event content, while profile `2` is earliest. That supports a profile-content/acquisition-layout explanation for why the `0-2` subset favors the shorter length branch and the `1-3` subset favors the longer branch.

This does not change the current product status by itself. It sharpens the next confirmation target: resolve profile spacing/acquisition layout and then rerun the GSSI optimizer with that geometry fixed.

## Validation

- `python -m pytest tests/test_gssi51600s_profile_event_content_audit.py -q` passed with `4 passed`.

## Next Defensible Task

Add a data-source provenance guard so 2025 public-dataset pipe rows cannot be confused with GSSI rebar product evidence, then rerun the focused product checks including the new GSSI profile-content audit.

The local marathon request remains active.
