# 2025 Public GPR Dataset Provenance Checkpoint

## What Changed

- Audited `data/2025-01-13_GPR_Dataset/Data Set.zip` after the user flagged that this source may not be the same as the trusted GSSI 51600S rebar data.
- Confirmed the archive contains three top-level local subsets: `Data Set/pipe`, `Data Set/rebar`, and `Data Set/tunnel`.
- Confirmed the recent 3D stack optimizer work that used `0701`, `0704`, and `0806` came from `Data Set/pipe`, not `Data Set/rebar`.
- Ran the existing rebar-subset inventory and thumbnail scout so the public rebar subset can be used later as a separate external validation source.

## Key Numbers

- Local archive subset entry counts:
  - `Data Set/pipe`: `3235` zip entries.
  - `Data Set/rebar`: `1389` zip entries.
  - `Data Set/tunnel`: `421` zip entries.
- Rebar-subset inventory artifact: `outputs/validation_exp_on_field_data/dataset_intake_2025_gpr/009_rebar_dataset_archive_inventory/`.
- Rebar zones: `60`.
- Rebar `.dt` files: `144`.
- Rebar thumbnail scout artifact: `outputs/validation_exp_on_field_data/dataset_intake_2025_gpr/010_rebar_ids_dt_profile_scout/`.
- Successfully parsed first-profile thumbnails: `34`.
- Compact visual candidates for later external rebar checks include `foshanJL.MIS/LS1.ZON`, `BH2.ZON`, `B3.ZON`, and `BS1.ZON`, but these are not part of the current GSSI product claim.

## Source Check

- Local bundled reference states that the public dataset includes tunnel lining data, underground pipeline data, and rebar data.
- Zenodo API record `10.5281/zenodo.14637589` describes the same public GPR dataset as including tunnel linings, underground pipelines, and reinforced concrete components.
- The local subset path is the controlling evidence for each run. A public dataset can contain rebar files while a specific optimizer run still comes from a pipe subset.

## Current Decision

The trusted rebar product path remains `data/2026-06-09_GSSI_model_51600S`. The 2025 `pipe` rows are optimizer-transfer or acceleration context only and must not be described as rebar prediction evidence. The 2025 `rebar` subset is real and usable later, but it needs its own deliberate parser, profile selection, and validation path before it enters any rebar-product comparison.

## Validation

- `python run_2025_gpr_dataset_rebar_inventory.py` completed and wrote the rebar archive inventory.
- `python run_2025_rebar_ids_dt_profile_scout.py` completed and wrote two contact-sheet figures.
- Visual inspection of the first contact sheet showed repeated rebar-like hyperbolic responses in multiple rebar-subset profiles.

## Next Defensible Task

Keep the current predictor default GSSI-first, then add or verify tests that product-facing rows label `external_2025_pipe_*` as non-rebar context and `gssi51600s` as the user-confirmed rebar target.

The local marathon request remains active.
