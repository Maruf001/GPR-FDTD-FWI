# Field Experiment Index

## Dataset Families

| Dataset family | Trackers | Output root | Status |
| --- | --- | --- | --- |
| `local_gssi_51600s_2026_06_09` | `001-004` | `outputs/field_experiments/local_gssi_51600s_2026_06_09/` | CPU-only DZT import/QC, preprocessing, reflector-cue screening, zero/common-offset hyperbola overlays; not ready for FWI |

## Policy

Field trackers are dataset-local and should not consume IDs from
`docs/experiments/`, which remains the synthetic simulation and infrastructure
tracker stream.
