# BEM Experiment 823: Complex FDTD Adapter Input Staged Handoff Packet

Date: 2026-07-01

## Purpose

Split the 279-row complex FDTD adapter input template into practical staged
handoff files.

Runs `808-822` guarded the complete fill-in template and the external preflight
boundary, but the template was still one full CSV. This run creates a staged
packet so a real FDTD producer can begin with one center receiver-frequency
pair before filling the full 279-pair packet.

This run does not write into the external return path, execute FDTD, accept real
FDTD values, write completed BEM/FDTD stage files, run comparison, transfer to
field evidence, or promote 3D/HPC work.

## Output

```text
outputs/bem_experiments/823_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet
```

Key artifacts:

```text
data/complex_fdtd_adapter_input_staged_handoff/
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:                 true
source claim boundary ready:                true
stages:                                     5
stage row shape:                            1;8;30;120;120
cumulative row shape:                       1;9;39;159;279
stage-only packet files:                    5
cumulative packet files:                    5
total packet files:                         10
packet files present:                       10
packet files under external return root:    0
stage-only rows:                            279
final cumulative rows:                      279
first-stage rows:                           1
final cumulative FDTD value blank cells:    558
final cumulative provenance blank cells:    1395
external input file present:                false
accepted as real external input:            false
real BEM/FDTD comparison ready:             false
field transfer ready:                       false
3D/HPC ready:                               false
```

Stage packet:

| Stage | Stage rows | Cumulative rows | Cumulative value blanks | Cumulative provenance blanks |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 2 | 5 |
| 2 | 8 | 9 | 18 | 45 |
| 3 | 30 | 39 | 78 | 195 |
| 4 | 120 | 159 | 318 | 795 |
| 5 | 120 | 279 | 558 | 1395 |

## Interpretation

The complex-field handoff can now be executed incrementally. Stage `1` is a
one-pair smoke packet. Stage `5` cumulative is the full 279-pair packet that
must eventually be filled with real FDTD real/imaginary values and provenance.

All staged files are output-local templates. None of them is accepted as real
external input.

## Decision

Use the staged packet for incremental real FDTD production. Keep completed
BEM/FDTD stage files, real comparison, field transfer, and 3D/HPC blocked until
the guarded external input file is filled with real values and passes preflight.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet.py
```

Figure check:

```text
3544x918, dynamic range=255
```
