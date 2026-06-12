# Experiment 67: Close50 Acquisition Metadata Repair

## Purpose

Close the handoff-matrix warning that Tx/Rx offset metadata must not be hidden
in close50 acquisition comparisons. The legacy run 273 aggregate compared a
default Tx/Rx case with Tx/Rx=40 mm, but the default input summary predated
the `tx_rx_offset_mm` field and appeared as "not recorded."

## Code Change

`run_coordinate_confidence_aggregate.py` now accepts:

```text
--default-missing-tx-rx-offset-mm VALUE
```

This option fills missing `tx_rx_offset_mm` only when explicitly requested.
Rows are marked with:

```text
tx_rx_offset_inferred=True
tx_rx_offset_source=default_missing
```

Without the option, missing offsets still remain visible as "not recorded."

Focused validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_coordinate_confidence_aggregate.py -q
6 passed in 0.18s
```

Full validation after the code change:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
255 passed in 24.14s
```

## 534: Close50 Tx/Rx20-vs-Tx/Rx40 Metadata Repair Aggregate

Output:

```text
outputs/experiments/534_coordinate_confidence_aggregate_close50_txrx20_vs_txrx40_sources5_metadata_repair
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_confidence_aggregate.py \
  --default-missing-tx-rx-offset-mm 20 \
  --run-name coordinate_confidence_aggregate_close50_txrx20_vs_txrx40_sources5_metadata_repair \
  --outdir outputs/experiments/534_coordinate_confidence_aggregate_close50_txrx20_vs_txrx40_sources5_metadata_repair \
  outputs/experiments/265_coordinate_optimizer_close50_seed34_sources5_topcandidate_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/267_coordinate_optimizer_close50_seed34_sources5_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/269_coordinate_optimizer_close50_seed13_sources5_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Aggregate result:

```text
rows: 8
truth-geometry rows: 7
confidence labels: strong=8
max x/z/r ambiguity widths: 1.0 / 0.0 / 0.0 mm
```

Acquisition summary:

| Acquisition | Rows | Truth rows | X-ambiguity rows | Margin min/mean/max |
| --- | ---: | ---: | ---: | --- |
| 5 sources, Tx/Rx offset 20 mm (filled default) | 2 | 1 | 1 | 5.924e-03 / 6.980e-03 / 8.035e-03 |
| 5 sources, Tx/Rx offset 40 mm | 6 | 6 | 0 | 2.356e-03 / 2.880e-03 / 3.376e-03 |

Plot validation:

```text
coordinate_confidence_aggregate.png:
1719x971 px, dynamic range 255, grayscale std 61.9003

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 36.9753
```

## Interpretation

The metadata repair does not change the close50 result. It makes the old
default-offset rows explicit as Tx/Rx=20 mm and marks them as inferred. Those
rows still show the original limitation: one of two rows is not exact in x and
has a 1 mm x ambiguity interval. The Tx/Rx=40 mm rows remain 6/6 exact with no
x ambiguity.

This closes the metadata packaging gap. Future acquisition aggregates should
continue to record `tx_rx_offset_mm` directly in source summaries; the default
fill option is only for legacy summaries where the default offset is known.

Archive check:

```text
The only remaining "Tx/Rx offset not recorded" acquisition entry is the
historical run 273 aggregate. Run 534 supersedes it for reporting and keeps
the filled-default rows explicitly marked.
```

## Next Decision

Return to the handoff matrix and avoid GPU work unless a new concrete physics
gap is identified.
