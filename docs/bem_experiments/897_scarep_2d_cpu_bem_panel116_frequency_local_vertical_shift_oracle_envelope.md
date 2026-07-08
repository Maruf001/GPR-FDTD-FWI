# BEM Experiment 897: Panel-116 Frequency-Local Vertical-Shift Oracle Envelope

Date: 2026-07-01

## Purpose

Measure the best possible per-frequency vertical-shift envelope after the fixed
`+0.15 mm` shift failed the multi-frequency holdout in run `892`.

This run reruns the 116-panel CPU BEM target case and compares the response
against analytic references with common source/receiver vertical shifts from
`0.00 mm` to `0.40 mm` in `0.05 mm` increments. Each frequency is allowed to
choose its best shift from that grid. This is an oracle envelope, not a
physical correction. It does not run project FDTD, field processing, 3D/HPC
work, or GPU kernels.

## Output

```text
outputs/bem_experiments/897_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope
```

## Result

```text
source holdout validation ready:       true
frequency count:                       25
high-band frequency count:              9
shift candidates:                       9
candidate rows:                       225
target relative L2:                    0.001
wall seconds:                          65.50717453216203
baseline per-frequency pass count:     23
oracle per-frequency pass count:       25
baseline high-band pass count:          7
oracle high-band pass count:            9
baseline worst frequency:              2.3125 GHz
baseline worst relative L2:            0.0020304660813911003
oracle worst frequency:                2.65625 GHz
oracle worst relative L2:              0.0008518855375610986
unique selected shifts:                 4
minimum selected shift:                 0.0 mm
maximum selected shift:                 0.15 mm
selected shift counts:                  {"0.00": 1, "0.05": 16, "0.10": 7, "0.15": 1}
frequency-local oracle passes:          true
oracle correction promoted:             false
smooth frequency model required:        true
project FDTD comparison ready:          false
field transfer ready:                   false
real 3D validation ready:               false
gpu priority:                           none
```

High-band selected shifts:

| Frequency (GHz) | Best shift (mm) | Baseline relative L2 | Oracle relative L2 | Oracle pass |
| ---: | ---: | ---: | ---: | --- |
| 2.083333333333333 | 0.05 | 0.0004436868487678074 | 0.00021715991754292952 | true |
| 2.1979166666666665 | 0.10 | 0.0005216069052595891 | 0.00007034002475083531 | true |
| 2.3125 | 0.15 | 0.0020304660813911003 | 0.00029663254700154477 | true |
| 2.427083333333333 | 0.05 | 0.0004092037546254354 | 0.00022394436333890793 | true |
| 2.5416666666666665 | 0.05 | 0.0005526488245481426 | 0.0001944960476559569 | true |
| 2.65625 | 0.10 | 0.001124829226316987 | 0.0008518855375610986 | true |
| 2.770833333333333 | 0.05 | 0.0006783429800694514 | 0.00025478222155756277 | true |
| 2.8854166666666665 | 0.05 | 0.0005607606328217628 | 0.0002605733403178845 | true |
| 3.0 | 0.05 | 0.0005620505398097652 | 0.0002781575781508855 | true |

## Interpretation

The per-frequency vertical-shift oracle can bring every frequency below the
target. This confirms that a vertical source/receiver representation error is a
strong diagnostic lead.

The selected shift is not constant. Most frequencies choose `0.05 mm`, several
choose `0.10 mm`, the original worst bin chooses `0.15 mm`, and the lowest
frequency chooses `0.00 mm`. This means the current evidence supports a
frequency-aware source/receiver model target, not a fixed geometry correction.

## Decision

Do not promote the oracle envelope as a correction. Use it as the target for a
constrained smooth frequency-aware source/receiver model that must pass without
per-frequency free choice.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_local_vertical_shift_oracle_envelope.py
3 passed
```

Figure check:

```text
2788x870, dynamic range=255
```

