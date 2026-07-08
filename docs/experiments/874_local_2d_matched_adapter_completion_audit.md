# Experiment 874: Local 2D Matched Adapter Completion Audit

Date: 2026-06-25

## Purpose

Check whether the generic matched 2D BEM/FDTD adapter branch recommended by run
`142` is actually unfinished.

This is a CPU-only planning audit. It does not rerun BEM, FDTD, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/143_local_2d_matched_adapter_completion_audit
```

Key artifacts:

```text
data/local_2d_matched_adapter_completion_audit.csv
data/local_2d_matched_adapter_completion_audit_summary.json
figures/local_2d_matched_adapter_completion_audit.png
docs/LOCAL_2D_MATCHED_ADAPTER_COMPLETION_AUDIT.md
scripts/run_local_2d_matched_adapter_completion_audit.py
scripts/test_local_2d_matched_adapter_completion_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
adapters audited:                         3
completed adapters:                       3
generic matched-adapter rerun needed:     false
worst FDTD/reference relative L2:         0.03432024436144074
run142 recommendation already covered:    true
next local 2D branch:                     source_amplitude_time_zero_perturbation_replay
ready for GPU work:                       false
ready for field transfer:                 false
ready for field FWI:                      false
```

The completed adapter ladder is:

| Source run | Adapter | Best FDTD/reference L2 | Current use |
| --- | --- | ---: | --- |
| 014 | free-space dielectric cylinder | 0.02330746966791303 | baseline dielectric validation ladder |
| 015 | free-space PEC cylinder | 0.03432024436144074 | homogeneous rebar-style validation ladder |
| 016 | air/concrete half-space PEC cylinder | 0.030998297443390457 | closest current 2D BEM-side rebar adapter |

## Interpretation

The generic matched 2D BEM/FDTD adapter task is already covered by BEM runs
`014-016`. Repeating that generic branch would duplicate completed work.

The next useful local 2D branch, if no real field data arrive, should be a
CPU-only source-amplitude/time-zero perturbation replay because field run `176`
makes those references acceptance-critical.

## Decision

Use runs `014-016` as the matched-adapter validation ladder. Do not rerun a
generic matched adapter as the next local 2D task. Start a source-amplitude/
time-zero perturbation replay from a duplicated script if continuing local 2D
without real field data.

## Validation

Focused tests:

```text
tests/test_local_2d_matched_adapter_completion_audit.py
2 passed
```

Figure check:

```text
2104x769, dynamic range=255
```

Script snapshots:

```text
run_local_2d_matched_adapter_completion_audit.py
sha256=fbdb0b4949e2a6fc250724bf2185bcbf03633d1c52af4aa266a31a3f6dba8de9

test_local_2d_matched_adapter_completion_audit.py
sha256=a6dc41f2d0475ec52d3f71d4784e6878114dbdb3c242cf8a9222d08e6ba958a5
```
