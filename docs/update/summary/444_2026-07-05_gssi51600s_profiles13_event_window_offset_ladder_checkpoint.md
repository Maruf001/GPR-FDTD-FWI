# 444 2026-07-05 GSSI51600S Profiles 1/3 Event-Window Offset Ladder Checkpoint

## What changed

- Tested the earlier event-window family on additional profiles 1/3 crossline-offset variants.
- Isolated right-offset and left-offset effects around the current nonuniform coordinate hypothesis.
- Compared these against the fully uniform earlier-window run that had produced the shallow cover-depth branch.

## Key numbers

Profiles 1/3 earlier-window offset ladder:

- `[-0.20, 0.00, 0.14]`:
  - field L1 loss: `0.9608709216117859`
  - objective loss: `0.9750060439109802`
  - cover depth: `0.1380164921283722 m`
  - diameter: `17.33890362083912 mm`
  - length: `0.18456555902957916 m`
- `[-0.20, 0.00, 0.18]`:
  - field L1 loss: `0.9610996246337891`
  - objective loss: `0.9751166701316833`
  - cover depth: `0.13799713551998138 m`
  - diameter: `17.33960583806038 mm`
  - length: `0.1847650408744812 m`
- `[-0.20, 0.00, 0.22]`:
  - field L1 loss: `0.9610714912414551`
  - objective loss: `0.9750823378562927`
  - cover depth: `0.1381007730960846 m`
  - diameter: `17.33972504734993 mm`
  - length: `0.18476656079292297 m`
- `[-0.22, 0.00, 0.14]`:
  - field L1 loss: `0.9608632922172546`
  - objective loss: `0.974998414516449`
  - cover depth: `0.13803528249263763 m`
  - diameter: `17.33885519206524 mm`
  - length: `0.1845645308494568 m`
- Fully uniform `[-0.22, 0.00, 0.22]` earlier-window reference:
  - field L1 loss: `0.9704806208610535`
  - objective loss: `0.9938139915466309`
  - cover depth: `0.10122688114643097 m`
  - diameter: `17.217664048075676 mm`
  - length: `0.18371789157390594 m`

## Current decision

The profiles 1/3 earlier-window shallow cover-depth branch appears only in the fully uniform `[-0.22, 0.00, 0.22]` geometry among the variants tested here. The nonuniform variants tested so far all remain near `0.138 m` cover depth and fit the field data better than the fully uniform earlier-window shallow case.

This reinforces the latest bundle decision: event-window timing and y geometry interact, and the earlier event window should not be promoted as a release default without a joint timing/geometry rule.

## What remains blocked

- The current local offset ladder does not yet identify a geometry/timing pair that gives both shallow x/z consistency and the best waveform fit.
- Measured crossline profile coordinates remain the cleanest way to break this ambiguity.
- If measured coordinates are unavailable, the next optimizer should jointly search a small y-offset and event-window grid instead of changing one factor at a time.

## Validation and resource checks

- GPU runs completed for IDs `509`, `510`, and `511`.
- No code changes were required for this ladder.
- Prior bundle/query validation remains: latest expanded focused suite passed with `58 passed`.

## Artifact paths

- Right-offset `0.18 m`: `outputs/validation_exp_on_field_data/3d_geometry_inventory/509_gssi51600s_finite_length_3d_profiles1_3_b020_c018_domainz070_adamw_prior_windows46_50_54_58_62_iter24`
- Right-offset `0.22 m`: `outputs/validation_exp_on_field_data/3d_geometry_inventory/510_gssi51600s_finite_length_3d_profiles1_3_b020_c022_domainz070_adamw_prior_windows46_50_54_58_62_iter24`
- Left-offset `0.22 m`, right-offset `0.14 m`: `outputs/validation_exp_on_field_data/3d_geometry_inventory/511_gssi51600s_finite_length_3d_profiles1_3_b022_c014_domainz070_adamw_prior_windows46_50_54_58_62_iter24`
- Fully uniform earlier-window reference: `outputs/validation_exp_on_field_data/3d_geometry_inventory/504_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_prior_stability_windows46_50_54_58_62_iter24`

## Next defensible task

Build a compact joint timing/geometry grid planner for profiles 1/3 that selects a few high-value combinations instead of expanding the ladder manually. The grid should report field fit, x/cover-depth branch, diameter, length, permittivity, and conductivity in one table.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
