# Experiment 805: Target2 Archive Ambiguity Objective Diagnostic

Date: 2026-06-17

## Purpose

CPU-only objective-level diagnostic for the target2 exact-strong ambiguous rows
identified by experiments 803 and 804. This run reads existing
coordinate-confidence aggregate CSVs and classifies the near-best competing
geometries without launching new FDTD, FWI, GPU kernels, or optimizer runs.

## Output

```text
outputs/experiments/1283_target2_archive_ambiguity_objective_diagnostic
```

Artifacts:

```text
data/target2_archive_ambiguity_objective_diagnostic_rows.csv
data/target2_archive_ambiguity_objective_diagnostic_summary.json
data/figure_validation.csv
figures/target2_archive_ambiguity_objective_diagnostic.png
run_manifest.json
```

## Result

Policy label:

```text
target2_archive_ambiguity_near_tie_diagnostic_cpu_no_gpu
```

Summary:

```text
aggregate files audited:                 67
rows:                                    21
families:                                4
competitors within ambiguity threshold:  21
one-mm lateral near ties:                19
depth/radius coupled near ties:          2
mixed objective near ties:               0
minimum competitor objective gap:        2.210812e-05
maximum competitor objective gap:        1.159108e-03
minimum margin inside threshold:         3.491030e-07
maximum margin inside threshold:         1.544696e-03
max x ambiguity width:                   1.000 mm
max z ambiguity width:                   1.000 mm
max radius ambiguity width:              0.750 mm
gpu priority:                            none_now
```

## Interpretation

The target2 strict-clean exceptions are objective near-ties, not mixed
unclassified failures. Most are one-grid-cell lateral competitors; the two
variable-depth/radius rows are coupled z/radius competitors. All competitors
remain inside the ambiguity threshold.

This supports a stricter reporting rule: exact and strong is not sufficient for
paper-clean location claims unless the ambiguity width is also zero. Future
work should first use CPU-side objective-margin diagnostics or a revised
reporting metric. This result does not justify a broad GPU sweep.

## Validation

Focused tests:

```text
tests/test_target2_archive_ambiguity_objective_diagnostic.py: 4 passed
```

Figure validation:

```text
target2_archive_ambiguity_objective_diagnostic.png: 2263x1583,
nonwhite=0.3283, dynamic range=255
```
