# GSSI 51600S Shallow Event Detector Checkpoint

## What changed

- Added `run_gssi51600s_shallow_event_detector.py`.
- The detector scans the normalized GSSI `0-5 ns` stack, smooths the profile-mean absolute amplitude map, applies nonmax suppression, and emits candidate x/time/depth windows.
- Generated a ranked candidate artifact for the next GSSI-specific time/polarity ladder and optimizer.

## Key numbers

- Detector artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/005_gssi51600s_shallow_event_detector`
- Candidate count: `12`
- Stack shape: `4 x 510 x 274`
- dt: `0.009823 ns`
- dx: `0.003333 m`
- dielectric metadata: `2.25`
- detection time range: `0.10-4.80 ns`

Top candidate:

- rank: `1`
- x: `0.703263 m`
- time: `1.051081 ns`
- depth under epsr metadata: `0.105035 m`
- score: `0.908064`
- sample index: `107`
- trace index: `211`
- suggested sample window: `43-171`
- suggested trace window: `179-243`
- profile support count: `4 / 4`

Other high-ranking candidates are at approximately:

- x `0.109989 m`, time `1.051081 ns`
- x `0.403293 m`, time `1.070727 ns`
- repeated shallower/deeper companion events near x `0.703263 m`, `0.109989 m`, and `0.396627 m`

## Current decision

The GSSI stack now has shallow candidate windows for product-path follow-up. The top candidate is not a final rebar prediction; it is the window seed for GSSI-specific time/polarity alignment and Fast-GPR fitting.

## What remains blocked

- No GSSI-specific Fast-GPR time/polarity ladder has been run yet.
- No GSSI-specific geometry/material optimizer has been run yet.
- The detector is amplitude/event based, not hyperbola-fit or FWI based.
- The cropped stack covers only the shortest common aperture; long-profile tails are not yet scanned.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_shallow_event_detector.py tests/test_gssi51600s_shallow_event_detector.py`
- `python -m pytest tests/test_gssi51600s_shallow_event_detector.py -q` -> `5 passed`
- Detector plus stack-adapter tests -> `9 passed`
- Detector figure is nonblank, `1851 x 903`, RGBA, full channel extrema.
- `git diff --check` on detector/adapter files was clean.
- Script snapshots were frozen under `005_gssi51600s_shallow_event_detector/scripts/`.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/005_gssi51600s_shallow_event_detector/data/gssi51600s_shallow_event_detector_summary.json`
- Candidate rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/005_gssi51600s_shallow_event_detector/data/gssi51600s_shallow_event_detector_candidates.csv`
- Energy map: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/005_gssi51600s_shallow_event_detector/data/gssi51600s_shallow_event_detector_energy.npz`
- Figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/005_gssi51600s_shallow_event_detector/figures/gssi51600s_shallow_event_detector.png`

## Next defensible task

Run a GSSI-specific Fast-GPR shallow time/polarity ladder around the top candidate:

- x window centered near `0.703 m`
- use GSSI dt/dx from the predictor stack
- use a shallow Fast-GPR time window within `0-5 ns`
- use an effective trace stride near the Fast-GPR dx scale
- then pass the best shift/polarity into a shallow geometry/material optimizer

## Marathon status

The requested 20-hour local marathon is still active. Continue with the GSSI Fast-GPR shallow ladder rather than stopping at this checkpoint.
