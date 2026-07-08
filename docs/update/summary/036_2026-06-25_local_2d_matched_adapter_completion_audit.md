# Local 2D Matched Adapter Completion Audit

Date: 2026-06-25

## Scope

Resolve whether the run `142` recommendation to start a matched 2D BEM/FDTD
adapter should trigger a new generic adapter run.

This is a planning audit only. It does not rerun BEM/FDTD or open GPU/FWI/field
gates.

## Output

```text
outputs/summary_tables/143_local_2d_matched_adapter_completion_audit
```

Tracked experiment note:

```text
docs/experiments/874_local_2d_matched_adapter_completion_audit.md
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

## Interpretation

BEM runs `014-016` already provide the generic matched-adapter ladder:
dielectric cylinder, PEC cylinder, and air/concrete half-space PEC cylinder.
The right next step is not another generic matched adapter.

## Decision

If continuing local 2D without real field data, start a CPU-only source-
amplitude/time-zero perturbation replay from a duplicated script. Keep GPU,
field transfer, field FWI, and 3D/HPC gates closed.

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

## Next Marathon Branch

The marathon remains active. The next branch should duplicate an appropriate
local 2D replay script and build a CPU-only source-amplitude/time-zero
perturbation design/replay.
