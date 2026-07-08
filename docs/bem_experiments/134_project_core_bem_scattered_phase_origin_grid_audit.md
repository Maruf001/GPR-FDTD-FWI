# BEM Experiment 134: Scattered Phase-Origin Grid Audit

Date: 2026-06-27

## Purpose

Test whether a frequency-linear phase delay can explain the project-core
BEM/FDTD scattered-field mismatch.

Run `133` showed that per-receiver circular time shifts are the strongest
simple diagnostic factor, but still do not pass the scattered-field comparison
gate. This run moves the same question into the frequency domain:

```text
Can per-receiver phase-slope correction and complex scale repair the scattered
project-core BEM/FDTD bridge?
```

This is a CPU-only audit of saved run `017` arrays. It does not rerun FDTD or
BEM solvers, compare against field data, launch GPU/HPC work, run 3D validation,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/134_project_core_bem_scattered_phase_origin_grid_audit
```

Key artifacts:

```text
data/project_core_bem_scattered_phase_candidate_metrics.csv
data/project_core_bem_scattered_phase_trace_delays.csv
data/project_core_bem_scattered_phase_origin_grid_audit_summary.json
figures/project_core_bem_scattered_phase_origin_grid_audit.png
docs/PROJECT_CORE_BEM_SCATTERED_PHASE_ORIGIN_GRID_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate count:                         3
phase trace rows:                        7
scattered acceptance gate:               0.1
baseline symmetric L2:                   1.3943651626310445
best candidate:                          per_receiver_phase_slope_complex_scale
best candidate symmetric L2:             0.1866176083623045
best candidate relative L2 vs FDTD:      0.18500684021427607
best candidate passes gate:              false
best improvement factor:                 7.471777046483127
equivalent delay min:                    1.2604589809231894 ns
equivalent delay max:                    2.3108414650258466 ns
equivalent delay span:                   1.0503824841026572 ns
per-receiver phase trace L2 mean:        0.1857080769816001
phase-origin fix ready:                  false
project-core bridge ready:               false
project-core FDTD comparison ready:      false
real 3D validation ready:                false
field FWI ready:                         false
gpu/hpc ready:                           false
```

Candidate metrics:

| Candidate | Symmetric L2 | Relative L2 vs FDTD | Passes gate |
| --- | ---: | ---: | --- |
| source_normalized_baseline | 1.3943651626310445 | 1.4641925358593955 | false |
| global_phase_slope_complex_scale | 1.4038619675676435 | 0.9404912320272313 | false |
| per_receiver_phase_slope_complex_scale | 0.1866176083623045 | 0.18500684021427607 | false |

Per-receiver phase delays:

| Trace | Receiver x (m) | Raw delay (ns) | Equivalent circular delay (ns) | Trace L2 |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.19 | -5.6920726995658315 | 2.3108414650258466 | 0.18949368530567956 |
| 1 | 0.21333333333333335 | -6.21226212026429 | 1.7906520443273881 | 0.1793023114811356 |
| 2 | 0.23666666666666666 | -6.5924005430823955 | 1.4105136215092833 | 0.19629288260249014 |
| 3 | 0.26 | -6.742455183668489 | 1.2604589809231894 | 0.20230041833465104 |
| 4 | 0.2833333333333333 | -6.5924005430823955 | 1.4105136215092833 | 0.17962219088792022 |
| 5 | 0.3066666666666667 | -6.2222657629700295 | 1.7806484016216486 | 0.16683850609646525 |
| 6 | 0.33 | -5.6920726995658315 | 2.3108414650258466 | 0.18610654416285885 |

## Interpretation

Per-receiver frequency-linear phase delays explain more of the mismatch than
direct time-domain shifting. The best symmetric relative L2 improves from
`1.3943651626310445` to `0.1866176083623045`, a `7.4718x` improvement.

The fitted equivalent delays vary across the receiver line, from about
`1.26 ns` at the scan center to about `2.31 ns` near the edges. This scan-shaped
delay pattern shows that the issue is not one global time-zero offset.

The corrected response still misses the `0.1` comparison gate. Phase/time origin
is therefore a major part of the problem, but the remaining waveform error is
too large for a project-core BEM/FDTD bridge claim.

## Decision

Keep the project-core bridge blocked. The next useful work is a causal
source-wavelet and reconstruction contract: define the exact source phase, time
zero, selected-frequency Hermitian reconstruction, and scattered-field
observable before rerunning a matched adapter.

## Validation

Focused test:

```text
tests/test_project_core_bem_scattered_phase_origin_grid_audit.py
6 passed
```

Figure validation:

```text
project_core_bem_scattered_phase_origin_grid_audit.png
2949x882, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_scattered_phase_origin_grid_audit.py
sha256=6e7b62b53d14d7fdd6f574424343231d2ed0591163fac88e3a08e76633dab7c9

tests/test_project_core_bem_scattered_phase_origin_grid_audit.py
sha256=e31bf804d46f7bc2dc2ea01078f6061fc08a75c11d37e26fe11e3eacf474e032
```
