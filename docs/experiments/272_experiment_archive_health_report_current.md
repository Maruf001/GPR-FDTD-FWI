# Experiment 272: Experiment Archive Health Report Current

## Purpose

Run 739 audits the numbered experiment archive after the user noticed that
runs 430-730, and especially runs after 535, finished much faster than the
earlier experimental sequence. The suspicion was that the post-crash resume
style had shifted toward short checkpoint/report documents rather than
physics-heavy experiments with `data/`, `figures/`, and figure notes.

This tracker records the corrective audit and the operating policy change it
implies.

## 739: Experiment Archive Health Report Current

Output:

```text
outputs/experiments/739_experiment_archive_health_report_current
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_experiment_archive_health_report.py --run-name experiment_archive_health_report_current
```

Code and tests:

```text
run_experiment_archive_health_report.py
tests/test_experiment_archive_health_report.py
```

Artifacts:

```text
README.md
data/experiment_archive_health_rows.csv
data/experiment_archive_health_summary.json
figures/artifact_coverage_by_range.png
figures/run_type_mix_by_range.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Method

The runner inspects every numbered directory under `outputs/experiments` and
records:

```text
run number and slug
stable range bin: 001-430, 431-534, 535-730, or 731+
probable run category: physics/diagnostic, analysis/report, checkpoint/audit, or unclear
presence of data/, figures/, image files, figures/FIGURE_NOTES.md, README.md, and run_manifest.json
issue and warning flags
```

The range bins were chosen to answer the exact concern:

```text
001-430: early and middle experiment growth
431-534: late pre-drift experiment block, ending with the last long figure-heavy run mentioned by the user
535-730: post-resume acceleration block
731+: current crash-recovery tail
```

## Results

The audit inspected 738 numbered output folders.

| Range | Runs | Category mix | Data dirs | Figure dirs | Image runs | Figure notes |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `001-430` | 430 | 281 physics/diagnostic, 61 analysis, 87 unclear, 1 checkpoint | 430 | 395 | 418 | 289 |
| `431-534` | 104 | 61 physics/diagnostic, 40 analysis, 2 unclear, 1 checkpoint | 104 | 101 | 101 | 101 |
| `535-730` | 196 | 169 reporting/audit/checkpoint, 14 analysis, 12 unclear, 1 physics/diagnostic | 132 | 8 | 7 | 7 |
| `731+` | 8 | 8 reporting/audit/checkpoint | 6 | 0 | 0 | 0 |

Archive-wide issue counts:

```text
figure_images_missing_figure_notes: 106
missing_run_manifest: 4
```

Archive-wide warning counts:

```text
unclear_run_type: 101
physics_or_diagnostic_without_figures_dir: 26
checkpoint_without_machine_readable_data: 60
```

## Interpretation

The user concern is valid. The fast completion of runs 535-730 was not because
the physical experiments suddenly became more efficient. It happened because
the run stream became dominated by small reporting, archive, queue, validation,
and resume-checkpoint outputs.

The comparison to run 534 is especially diagnostic. The 431-534 block still
has data coverage for 104/104 runs, figure folders for 101/104 runs, image
outputs for 101/104 runs, and figure notes for 101/104 runs. In contrast,
535-730 has only 8 figure folders and 7 runs with figure notes, while 169/196
runs classify as reporting/audit/checkpoint work.

That means the post-crash resume process preserved state, but it also inflated
the experiment count with many short bookkeeping records. Those records are
not wrong individually, but they should not be allowed to stand in for
substantive FDTD/FWI progress.

## Policy Change

Future numbered work should use stricter artifact expectations:

```text
Physical or diagnostic experiments:
  require data/, parameters, output metrics, and figures/FIGURE_NOTES.md when images exist.

Analysis or report runs:
  require machine-readable data summaries and figure notes for generated images.

Checkpoint, queue, archive, and commit-summary runs:
  should be rare; if numbered, include data/ unless the artifact is intentionally human-only.
```

The next marathon stage should avoid additional pointer churn. It should either
produce a new decision-grade physics/diagnostic result or deliberately repair
archive hygiene exposed by run 739.

## Validation

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_experiment_archive_health_report.py
4 passed in 0.17s

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
272 passed in 24.74s

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile run_experiment_archive_health_report.py
passed

figure validation:
artifact_coverage_by_range.png dynamic range 255
run_type_mix_by_range.png dynamic range 255

git diff --check: clean after run 739
```

## Next Decision

Use the run 739 report as the current guardrail. Continue with one of two
substantive paths:

```text
1. run a new physics/diagnostic experiment with full data and figure notes
2. perform a targeted archive hygiene repair for missing older figure notes
```
