# Experiment 845: Branch-Preservation Archive Audit

Date: 2026-06-18

## Purpose

Scan saved coordinate optimizer candidate surfaces to test whether the run
`1343` branch-preserving effect is isolated or appears elsewhere in the archive.

This is a CPU-only archive audit. It reads existing
`multi_rebar_coordinate_optimizer_summary.json` files and their saved candidate
CSVs. It does not run FDTD, FWI, GPU kernels, field work, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/summary_tables/094_local_2d_branch_preservation_archive_audit
```

Key artifacts:

```text
data/local_2d_branch_preservation_archive_audit_summary.json
data/local_2d_branch_preservation_archive_audit_rows.csv
data/local_2d_branch_preservation_archive_audit_target_rows.csv
data/local_2d_branch_preservation_archive_audit_gates.csv
data/figure_validation.csv
figures/local_2d_branch_preservation_archive_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_branch_preservation_archive_audit_near_tie_missed_truth_lateral
audited candidate steps:              747
truth-lateral available steps:        734
truth-lateral retained steps:         730
selected truth-lateral steps:         717
retained but not selected:             13
retained but not selected fraction:     0.0174
target retained-but-not-selected:       target0=3; target1=1; target2=9
branch-preservation claim ready:       true
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Target summary:

```text
target0: 3 / 196 retained-but-not-selected
target1: 1 / 178 retained-but-not-selected
target2: 9 / 373 retained-but-not-selected
```

Representative missed-but-retained rows:

```text
1341 target1: best x=252,z=89; truth-lateral x=250,z=89; rel gap=0.0922
336 target2: best x=265,z=90; truth-lateral x=264,z=90; rel gap=0.0017
274 target2: best x=299,z=90; truth-lateral x=300,z=90; rel gap=0.0624
```

## Interpretation

Run `094` shows that the branch-preservation issue is uncommon but not unique
to the repaired close14 seed. Most saved candidate surfaces already select the
truth lateral branch, but 13 audited surfaces retain a truth-lateral branch
inside the 0.01 absolute / 10% relative preservation window while the greedy
best row selects a nearby lateral branch instead.

This supports branch preservation as a real archive-backed policy idea,
especially for target2. It does not authorize a broad GPU queue or
detector-seeded FWI. The archive scan only identifies where preserving near-tie
candidate branches may matter; coupled re-evaluation like run `1343` is still
case-specific and should stay narrow.

## Validation

Focused test for the new archive-audit script:

```text
tests/test_local_2d_branch_preservation_archive_audit.py
2 passed
```

Focused detector/field regression:

```text
64 passed
```

Full suite:

```text
879 passed
```

Figure validation:

```text
local_2d_branch_preservation_archive_audit.png: 2331x835,
nonwhite=0.2243, dynamic range=255
```
