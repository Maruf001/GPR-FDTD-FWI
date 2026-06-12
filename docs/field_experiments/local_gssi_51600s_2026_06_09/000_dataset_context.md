# Field Dataset Context: Local GSSI 51600S 2026-06-09

This note is dataset context only. It records where the raw files live, which
files are present, what metadata can be read from them, and which acquisition
facts are still missing. Processing results, interpretation, and next
experiments belong in the numbered field trackers.

Dataset tracker directory:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/
```

Raw data directory:

```text
data/2026-06-09_GSSI_model_51600S
```

Field-processing output directory:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09
```

This measured field dataset is deliberately separated from the synthetic
simulation archive under `outputs/experiments/`. The synthetic archive has
known truth geometry; this local field dataset does not.

## Dataset Summary

This is a small local reinforced-concrete GPR field dataset collected on
2026-06-09 with a GSSI 51600S antenna. The repository currently contains four
GSSI `.DZT` radar profile files and four `.DZX` XML metadata sidecars.

The present file family is:

```text
PROJECT001C__013
PROJECT001C__014
PROJECT001C__015
PROJECT001C__016
```

No `.DZG` GPS/position sidecar is present.

## File Types

- `.DZT`: GSSI binary radar data file containing the measured traces.
- `.DZX`: GSSI XML sidecar metadata, when present. These sidecars can contain
  scan ranges, scan spacing, depth range, dielectric, system/software fields,
  and waypoints.
- `.DZG`: optional GSSI GPS/position sidecar. None is available in this
  dataset.

The current importer path uses `readgssi` version 0.0.22 inside the `FNO`
conda environment.

## Raw File Inventory

| Stem | DZT bytes | DZX bytes | Sidecar status |
| --- | ---: | ---: | --- |
| `PROJECT001C__013` | 1,783,808 | 2,279 | `PROJECT001C__013.DZX` present |
| `PROJECT001C__014` | 692,224 | 2,279 | `PROJECT001C__014.DZX` present |
| `PROJECT001C__015` | 1,798,144 | 2,279 | `PROJECT001C__015.DZX` present |
| `PROJECT001C__016` | 692,224 | 2,279 | `PROJECT001C__016.DZX` present |

## Raw File Checksums

| File | SHA-256 |
| --- | --- |
| `PROJECT001C__013.DZT` | `aac26555e8048b00bba9f445b3c02865694fe9c1d903f82641e4fb46a06b102f` |
| `PROJECT001C__013.DZX` | `61e992a094d2fabbf6c92c79287a1f248672a8981aa74a04eaf02c2f735d7a88` |
| `PROJECT001C__014.DZT` | `54b1f1fbfe68636e1c0899a1404763d1bb183b03eb3b7aa1137f104c8fe88b13` |
| `PROJECT001C__014.DZX` | `36bd4370aa92e2de9f497ec12e08eeeaf6899a1810870a14f0f87b29eb651fec` |
| `PROJECT001C__015.DZT` | `2bfcfcdd1768c3455305cc540181a6aa14176d5fa08b7b6c26d8f43bcf99ce93` |
| `PROJECT001C__015.DZX` | `3dc3d0975e0cf34b45b3eb77a9c73e6c9d516e2f8b64291f03ce2b90a75abf69` |
| `PROJECT001C__016.DZT` | `945951709d7d05615b03e2ced342b878e1f76d09f0d1ecd203ef55f1f237144e` |
| `PROJECT001C__016.DZX` | `36bd4370aa92e2de9f497ec12e08eeeaf6899a1810870a14f0f87b29eb651fec` |

`PROJECT001C__014.DZX` and `PROJECT001C__016.DZX` currently have identical
SHA-256 hashes. That is an observed file fact from the repository contents; if
the original acquisition source expected distinct sidecar contents, confirm the
export provenance before using those sidecars as independent evidence.

## Extracted Metadata

All four DZT files import as one channel each.

| File | Samples | Traces | Profile length | DZX present | Import warning |
| --- | ---: | ---: | ---: | --- | --- |
| `PROJECT001C__013.DZT` | 510 | 807 | 2.686398 m | yes | none |
| `PROJECT001C__014.DZT` | 510 | 274 | 0.909909 m | yes | none |
| `PROJECT001C__015.DZT` | 510 | 814 | 2.709729 m | yes | none |
| `PROJECT001C__016.DZT` | 510 | 274 | 0.909909 m | yes | none |

Common metadata read from the DZT headers and available DZX sidecars:

| Field | Value |
| --- | --- |
| Antenna name | `51600S` |
| Antenna frequency | 1600 MHz |
| Time range | 5.0 ns |
| Header dielectric | 2.25 |
| Scan spacing | about 0.003333 m |
| Scans per meter | 300 |
| Approximate display depth from 5 ns and epsr=2.25 | 0.499654 m |
| DZX system | `SIR4K` for files 013-016 |
| DZX software version | `1.4.35` for files 013-016 |
| DZX depth range | 0.45 m for files 013-016 |

The 5 ns time range and dielectric 2.25 imply an approximate two-way-travel
display depth of 0.499654 m. The DZX sidecars list a 0.45 m depth range. Treat
these as display/header metadata, not calibrated cover-depth truth.

## Geometry And Positioning Metadata

The DZX sidecars for profiles 013-016 contain scan ranges that match the DZT
trace counts:

| DZX | Scan range | Trace count |
| --- | --- | ---: |
| `PROJECT001C__013.DZX` | `0,806` | 807 |
| `PROJECT001C__014.DZX` | `0,273` | 274 |
| `PROJECT001C__015.DZX` | `0,813` | 814 |
| `PROJECT001C__016.DZX` | `0,273` | 274 |

The available DZX waypoints are not enough to reconstruct a 3D survey grid.
They only show start/end-style local coordinates such as:

```text
scan 0:   [0.0, 0.0, 0.0]
last scan: [-0.003332, 0.0, 0.0]
```

From the files currently in the repository, we know profile distance along each
line, but not a complete crossline geometry, acquisition layout, survey sketch,
or GPS/total-station trajectory.

## Known Dataset Gaps

- No `.DZG` GPS/position file is present.
- No complete 2D/3D survey layout is present.
- No as-built or independently measured rebar geometry is present.
- No confirmed cover depth, bar diameter, bar spacing, material dielectric, or
  antenna time-zero reference is present.
- No acquisition notes are present that define scan direction, line ordering,
  surface condition, or exact start/end positions beyond the limited DZX
  metadata.

These gaps mean the raw profiles can support import checks, profile-level
visualization, and measured-data QC. They do not by themselves support claims of
3D survey reconstruction, confirmed rebar identity, calibrated cover depth, or
field FWI recovery of rebar geometry.

## Relation To Synthetic Data

The synthetic experiments use a known truth scene. In that setting, the
reference data are generated by running FDTD on a known model, and recovery can
be measured against hidden truth.

This field dataset is different:

- The DZT waveforms are measured observations.
- The true subsurface geometry is not encoded in the file metadata.
- The file metadata do not provide a complete acquisition geometry.
- "Exact geometry recovered" claims require external ground truth that is not
  currently present in this dataset.

## Associated Processing Records

Numbered files in this directory are processing records for this dataset, not
part of the dataset definition. The field experiment index is:

```text
docs/field_experiments/field_experiment_index.md
```

This `000_dataset_context.md` file intentionally does not summarize "the first
four" or "the first ten" experiments. There is nothing special about the first
four beyond them being the processing records that existed when this note was
first drafted. Add or revise numbered trackers as needed; update this dataset
context only when raw files, metadata, provenance, or known data gaps change.
