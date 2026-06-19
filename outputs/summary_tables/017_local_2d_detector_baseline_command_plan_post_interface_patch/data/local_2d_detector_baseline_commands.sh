#!/usr/bin/env bash
set -euo pipefail

# CPU-first same-case detector-baseline commands.
# Run at most one command at a time; keep RAM <=80% and GPU utilization <=90%.
# These commands intentionally use --backend cpu and preserve existing experiment outputs.

# policy_label: local_2d_same_case_detector_baseline_command_plan_cpu_first_not_launched
# planned_case_count: 12

# target2_close14 seed 13 nominal: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1326_local2d_detector_baseline_target2_close14_seed13_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.153613 --noise-seed 13 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed13_nominal_cpu

# target2_close14 seed 13 source_mismatch: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1327_local2d_detector_baseline_target2_close14_seed13_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.153613 --noise-seed 13 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed13_source_mismatch_cpu

# target2_close14 seed 21 nominal: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1328_local2d_detector_baseline_target2_close14_seed21_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.153613 --noise-seed 21 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed21_nominal_cpu

# target2_close14 seed 21 source_mismatch: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1329_local2d_detector_baseline_target2_close14_seed21_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.153613 --noise-seed 21 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed21_source_mismatch_cpu

# target2_close14 seed 34 nominal: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1330_local2d_detector_baseline_target2_close14_seed34_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.153613 --noise-seed 34 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed34_nominal_cpu

# target2_close14 seed 34 source_mismatch: existing
# question: Does the detector/database baseline merge the close14 250/264 mm pair, or can it separate the image cues while FWI remains objective-ambiguous?
# skip existing: outputs/experiments/1331_local2d_detector_baseline_target2_close14_seed34_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 5 --tx-rx-offset-mm 45 --receiver-sampling nearest --frequency-ghz 1.5 --truth-x-values-mm 190,250,264 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.153613 --noise-seed 34 --detector-x-values-mm 180:274:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close14_seed34_source_mismatch_cpu

# target2_close50_linear29p5 seed 13 nominal: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1332_local2d_detector_baseline_target2_close50_linear29p5_seed13_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.1 --noise-seed 13 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed13_nominal_cpu

# target2_close50_linear29p5 seed 13 source_mismatch: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1333_local2d_detector_baseline_target2_close50_linear29p5_seed13_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.1 --noise-seed 13 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed13_source_mismatch_cpu

# target2_close50_linear29p5 seed 21 nominal: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1334_local2d_detector_baseline_target2_close50_linear29p5_seed21_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.1 --noise-seed 21 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed21_nominal_cpu

# target2_close50_linear29p5 seed 21 source_mismatch: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1335_local2d_detector_baseline_target2_close50_linear29p5_seed21_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.1 --noise-seed 21 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed21_source_mismatch_cpu

# target2_close50_linear29p5 seed 34 nominal: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1336_local2d_detector_baseline_target2_close50_linear29p5_seed34_nominal_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1 --time-shift-ps 0 --amplitude-scale 1 --noise-fraction 0.1 --noise-seed 34 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed34_nominal_cpu

# target2_close50_linear29p5 seed 34 source_mismatch: existing
# question: Does detector-only ambiguity track the seed13 x-ambiguity caveat, or is the 29.5 mm issue specific to the waveform objective?
# skip existing: outputs/experiments/1337_local2d_detector_baseline_target2_close50_linear29p5_seed34_source_mismatch_cpu
# conda run -n gpr-fdtd-fwi python run_rebar_detection_pipeline.py --backend cpu --grid-step-mm 1 --scan-step-mm 8 --sources 4 --tx-rx-offset-mm 29.5 --receiver-sampling linear --frequency-ghz 1.5 --truth-x-values-mm 190,250,300 --truth-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --frequency-scale 1.1 --time-shift-ps -50 --amplitude-scale 1.1 --noise-fraction 0.1 --noise-seed 34 --detector-x-values-mm 180:310:1 --detector-z-values-mm 75:110:1 --detector-time-offset-ps-values 500,550,600,650,667,700,750 --top-k 20 --x-min-separation-mm 4 --z-min-separation-mm 4 --window-half-x-mm 16 --window-half-z-mm 16 --truth-tolerance-x-mm 8 --truth-tolerance-z-mm 8 --background-mode median --geometry-mode hard --run-name local2d_detector_baseline_target2_close50_linear29p5_seed34_source_mismatch_cpu
