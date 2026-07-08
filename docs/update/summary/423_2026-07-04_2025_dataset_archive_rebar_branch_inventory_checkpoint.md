# 2025 Public Dataset Archive Rebar Branch Inventory Checkpoint

## Scope

- Rechecked the local `data/2025-01-13_GPR_Dataset` archive without extracting it.
- The local folder currently contains `reference.md` and `Data Set.zip`.
- The archive has separate top-level branches for `pipe`, `rebar`, and `tunnel`.

## Archive Inventory

Top-level branch entry counts from the archive listing:

- `pipe`: `3235`
- `rebar`: `1389`
- `tunnel`: `421`

Raw IDS `.dt` file counts:

- `Data Set/pipe/.../*.dt`: `463`
- `Data Set/rebar/.../*.dt`: `144`

The visible rebar branch is under `Data Set/rebar/` and includes the `foshanJL.MIS` collection plus many `.ZON` folders.

## Interpretation

The 2025 public dataset can be useful later as an external rebar validation source, but it must be handled by branch. The recent optimizer rows that used the `pipe` branch should remain pipe-target benchmarking context and should not be described as rebar evidence.

## Next Step

If the 2025 dataset is used for rebar validation, extract only the `Data Set/rebar/` branch into a clearly named staging folder and build a separate IDS `.dt` adapter before running any predictor claims.
