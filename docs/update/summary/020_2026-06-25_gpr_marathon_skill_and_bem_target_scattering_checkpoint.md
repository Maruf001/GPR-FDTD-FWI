# GPR Marathon Skill And BEM Target-Scattering Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the continuation after the user asked to keep the
autonomous marathon going and save the marathon workflow as a skill.

No field FWI, heavy GPU queue, field 3D/HPC work, neural-network training, or
historical `outputs/experiments` archive comparison was launched.

## Skill

Created and validated a reusable personal Codex skill:

```text
/home/lam002/.codex/skills/gpr-marathon
```

Validation:

```text
python /home/lam002/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /home/lam002/.codex/skills/gpr-marathon

Skill is valid.
```

The skill records the project marathon workflow, track folders, current
scientific guardrails, validation expectations, and stop conditions. It is a
workflow skill, not a background daemon; future sessions can invoke it to
resume this style of BEM/field/2D marathon.

## BEM Runs Added

```text
029_project_core_empirical_green_surface_audit
030_project_core_homogeneous_dielectric_empirical_green_replay
031_project_core_homogeneous_dielectric_inrange_bridge_adapter
032_project_core_homogeneous_dielectric_inrange_empirical_green_replay
033_project_core_homogeneous_dielectric_strength_ladder
034_project_core_target_rasterization_audit
```

Tracked notes:

```text
docs/bem_experiments/029_project_core_empirical_green_surface_audit.md
docs/bem_experiments/030_project_core_homogeneous_dielectric_empirical_green_replay.md
docs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter.md
docs/bem_experiments/032_project_core_homogeneous_dielectric_inrange_empirical_green_replay.md
docs/bem_experiments/033_project_core_homogeneous_dielectric_strength_ladder.md
docs/bem_experiments/034_project_core_target_rasterization_audit.md
```

## BEM Findings

Run `029` is a positive direct-wave result:

```text
analytic Green all-pair L2:          1.6206668574552767
offset-mean empirical L2:            0.3347857456839478
leave-one-source empirical L2:       0.3764644678142781
rank-1 empirical L2:                 0.25970063183964165
coarse-grid validation L2:           0.13204235679778975
empirical Green surface ready:       true
```

Interpretation:

```text
The project-core direct wave is not well represented by the continuous
homogeneous analytic Green function, but it is smooth and predictable as a
finite-domain empirical source/offset Green surface.
```

Run `030` showed that the older target run `019` is mostly outside the run
`029` empirical source range:

```text
target sources in Green range:       1 / 7
empirical Green coverage ready:      false
```

Run `031` reran the target bridge inside the empirical source/offset range:

```text
direct/background relative L2:       0.24273323569821098
total time symmetric L2:             0.42038566376997455
scattered time symmetric L2:         1.5431553591086644
```

Run `032` replayed that in-range target using the empirical Green surface:

```text
empirical direct/background L2:      0.01662205712366382
legacy total time L2:                0.42038566376997455
empirical total time L2:             0.35174147593288074
legacy scattered time L2:            1.5431553591086644
empirical scattered time L2:         1.552057143941903
empirical target replay ready:       false
```

Run `033` tested whether weak dielectric targets fix the scattered mismatch:

| epsr | Empirical scattered L2 | Empirical total L2 | Peak scattered |
| ---: | ---: | ---: | ---: |
| 1.25 | 1.5332658067665847 | 0.03651854818819029 | 0.0005043437377672006 |
| 2.0 | 1.6256015896432827 | 0.13899561896992846 | 0.0019199564388843707 |
| 4.0 | 1.5524351934845986 | 0.34919297169096886 | 0.005027122996891264 |

Run `034` checked whether this failure is just target geometry rasterization:

```text
best radius error:                  0.0013260133260549478 mm
worst radius error:                 0.04776287834105941 mm
best centroid error:                0.0 mm
worst centroid error:               5.551115123125783e-14 mm
rasterization geometry ready:       true
```

## BEM Decision

The direct-wave bridge is now good enough for controlled diagnostics, but the
target-scattering bridge is not.

Current BEM interpretation:

```text
Stop direct-wave-only calibration for now.
Next BEM/project-core work should audit discrete target rasterization,
subcell representation, and the analytic-to-discrete target-scattering
operator. Run `034` clears gross target area/centroid geometry, so the next
priority is the discrete scattering/operator piece rather than another
geometry-size check.
```

This still does not justify comparison against the historical synthetic 2D
archive, field data, field FWI, or 3D inversion.

## Field Track

No field-side state changed in this block.

Current field checkpoint remains run `164`:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/164_gssi51600s_controlled_collection_intake_manifest_template
```

Field next step remains measured collection using the intake manifest: 11 real
metadata values and nine real files, with paths, checksums, operator initials,
and timestamps. Field FWI/GPU/HPC remains blocked until structural and
provenance gates pass on real data.

## Synthetic 2D Track

No new synthetic 2D GPU work was launched.

Current 2D checkpoint remains:

```text
outputs/summary_tables/134_local_2d_detector_fixed_radius_locking_generalization_audit
```

The fixed-radius branch remains a single-branch mechanism result, not a broad
policy. No new fixed-radius GPU probe is justified by current evidence.

## Next Defensible Improvements

1. BEM: audit discrete target rasterization and subcell material assignment for
   the same in-range weak/medium dielectric targets.
2. BEM: compare analytic cylinder scattering against a discrete target
   surrogate on the project grid, rather than continuing direct-wave
   normalization.
3. Field: use run `164` for collection-day intake, then rerun structural and
   provenance gates when real files exist.
4. 2D: refresh the evidence/report pack to include BEM runs `029`-`033` without
   implying historical archive validation.

## Validation

```text
python -m py_compile \
  run_project_core_empirical_green_surface_audit.py \
  run_project_core_homogeneous_dielectric_empirical_green_replay.py \
  run_project_core_homogeneous_dielectric_strength_ladder.py \
  run_project_core_target_rasterization_audit.py

python run_project_core_empirical_green_surface_audit.py
python run_project_core_homogeneous_dielectric_empirical_green_replay.py
python run_project_core_homogeneous_dielectric_strength_ladder.py
python run_project_core_target_rasterization_audit.py
```

Focused figure checks and final repository validation are recorded in the
current session handoff.
