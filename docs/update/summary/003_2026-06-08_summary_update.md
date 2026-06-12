## User

› Please explore this project thoroughly. some directories you can specifically look
  into (in addition to exploring the entire project):

  Experiment tracker directory:

  `docs/experiments`

  Experiment data directory:

  `outputs/experiments`

  The project now has roughly **868 experiments**, and I need you to understand the full
  progression.

  The main goal is to identify the project’s **major milestones**: the important “train
  stations” the project passed through as the experiments evolved.

  Please think of the experiment history like a train route. Each major milestone should
  represent a meaningful capability that was reached, for example (and I know there are
  way more than what I am listing as exmaples):

  * detecting a single rebar, and estimating the size/location of a single rebar,
  * distinguishing nearby rebars from one another, estimating size/location for multiple
  rebars,
  * testing different lateral spacings, testing different Tx/Rx offsets,
  * improving optimization reliability,
  * adding confidence intervals, uncertainty, ambiguity handling, or other later-stage
  capabilities.

  These are only examples. Please do not assume these are the only milestones. Explore
  the tracker and experiment folders and determine what the real milestones are.

  For each major milestone, please explain:

  * what capability was demonstrated,
  * which experiment number or range demonstrated it,
  * what changed compared with the previous milestone,
  * why it mattered,
  * whether it was later superseded by a stronger milestone,
  * whether the later milestones truly include the earlier capabilities or only solve a
  different branch of the problem.

  This cumulative question is important. For example, if the latest system can
  distinguish and size multiple nearby rebars, then it should presumably also handle a
  simpler single-rebar case. But please verify whether that is actually true from the
  experiments rather than assuming it.

  Please also explain the **current state of the project** after all these experiments:

  * What can the current best workflow actually do?
  * What is the strongest demonstrable result?
  * Which scripts or experiment workflows seem to represent the most mature/current
  version?
  * Which older scripts or approaches were superseded (major ones)?
  * What capabilities are confirmed, partially confirmed, or still unresolved?
  * What are the remaining limitations or ambiguities?


## Agent

• I inspected the tracker and output archive. One archive note: outputs/experiments now
  reaches 871; 870 is a complete run, while 871 currently only has empty data/ and
  figures/, so I would not count it as evidence yet.

  Milestone Route

   Station                Solver foundation
   Experiments            01-10
   Capability and Change  GPU FDTD, adjoint validation, GPU CPML, and first 3-rebar
                          geometry inversion. Exp 04 recovered 3 same-depth bars to <3 mm
                          x error and <1 mm radius error using derivative-free geometry
                          inversion.
   Cumulative Status      Superseded as workflow, but still the technical base. Pixel FWI
                          became mostly validation/background.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Single-rebar exact/noise recovery
   Experiments            11-14, outputs 001-023
   Capability and Change  One rebar x/z/r recovered with 2 mm global search, 1 mm Powell,
                          then deterministic grid polish. Worked through 10% synthetic
                          noise, but radius was grid/depth coupled.
   Cumulative Status      Later workflows include this only when a local basin is already
                          known. Raw Powell alone was superseded.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Objective triage and source profiling
   Experiments            15-31, outputs 024-058
   Capability and Change  Tested trace-shift/OT, PEBDD bandwidth, W2, material tradeoff,
                          wavelet mismatch. Key result: source amplitude/time/frequency
                          profiling fixed radius failures from source mismatch.
   Cumulative Status      This superseded fixed-source LS for radius reporting. W2/OT and
                          free material inversion were rejected for final radius
                          selection.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Robust single-rebar profiled polish
   Experiments            32-33, outputs 059-062
   Capability and Change  Source-profiled polish passed exact, noise, source-mismatch,
                          seed replication, and wider x/z/r windows.
   Cumulative Status      This is the mature local single-rebar radius estimator. It
                          still assumes a good local window.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Multi-rebar local profiling
   Experiments            34-41, outputs 063-080
   Capability and Change  Moved to 3 rebars: common radius, per-target radius, then local
                          x/z/r per target under 10% noise/source mismatch. All 24 Stage-
                          6 rows recovered truth, but 22/24 were weak confidence.
   Cumulative Status      Includes earlier radius profiling ideas, but not full joint
                          inversion. Confidence/ambiguity reporting became mandatory.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Sequential coordinate optimizer
   Experiments            42-44, outputs 081-098
   Capability and Change  First bounded all-target coordinate optimizer. Compact 4-seed
                          case recovered all three bars; 2 mm seed-offset stress exposed
                          edge high-radius branches and led to guarded revisit.
   Cumulative Status      Supersedes one-target-at-a-time reporting as the main multi-
                          rebar optimizer. Still bounded/local, not global.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Detection-to-FWI pipeline
   Experiments            47, outputs 107-134
   Capability and Change  Hyperbola detector seeded x/z windows; single-rebar detector
                          hit 48/48 nominal and 48/48 source-mismatch scenarios. Packaged
                          detector -> 2 mm screen -> 1 mm polish cut runtime while
                          preserving radius.
   Cumulative Status      This truly includes single-rebar local refinement, but the
                          detector itself estimates x/z only, not radius.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Shallow/small-radius ambiguity
   Experiments            outputs 121-134
   Capability and Change  Shallow z=70 mm, r=4 mm cases recovered point truth under
                          mismatch/noise, but with weak/broad intervals. Subcell and
                          equal multifrequency did not solve it.
   Cumulative Status      Not superseded. Current rule is interval reporting, not high-
                          confidence scalar radius.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Variable-radius close spacing
   Experiments            outputs 216-419
   Capability and Change  Same-depth variable radii [5,6,8] and close spacing. Staged
                          pipeline recovered joint radius tuple for seeds; 7-source
                          target-2 refinement removed x ambiguity. Later close-spacing
                          sweeps reached close14 under Tx/Rx=50 with clean boundary near
                          19.642333984375% RMS.
   Cumulative Status      Strong branch, but target-focused. It does not prove the later
                          variable-depth workflow handles extreme close-spacing
                          automatically.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Variable-depth/radius staged coordinate
   Experiments            54-66, outputs 451-533
   Capability and Change  Combined depth/radius: x=[150,250,350], z=[80,100,120],
                          r=[5,6,8]. Detector assignment found physical seeds; staged
                          coordinate path reached exact truth across seeds. Tx/Rx=50 gave
                          12/12 truth rows, zero x/z ambiguity, max radius ambiguity 0.25
                          mm.
   Cumulative Status      This is a stronger multi-rebar branch, but not a global all-
                          parameter solve. Base objective remains production update;
                          veryhigh is reporting diagnostic only.
  ───────────────────────────────────────────────────────────────────────────────────────
   Station                Fitted-ringdown/source-shape stress
   Experiments            outputs 740-870, trackers 273-403
   Capability and Change  Added fitted source ringdown and target-specific acquisition
                          policies. Ringdown035 8/9/9 Tx/Rx=60 passed 9/9 exact/moderate.
                          Ringdown0459375 transferred but was near cutoff. Ringdown050:
                          seeds 13/89/34 pass full policy, seed21 needs practical lower
                          threshold; run 870 shows seed55 target0 passes full ringdown050
                          with low reserve.
   Cumulative Status      Current frontier. It includes variable-depth/radius final-state
                          capability, but not single-rebar shallow r4, close14 spacing,
                          or field data claims.

  Current State

  The best current workflow is not one universal optimizer. It is a family:

  - Single rebar: run_rebar_detection_pipeline.py or
    run_detection_seeded_two_stage_refinement.py for detector-seeded coarse-to-fine
    source-profiled radius estimation.

  - Multi rebar: detector/assignment when needed, then
    run_multi_rebar_coordinate_optimizer.py with bounded windows, source amplitude/time/
    frequency/ringdown profiling, confidence rows, ambiguity intervals, and diagnostic
    objective variants.

  - Reporting: run_coordinate_confidence_aggregate.py,
    run_coordinate_objective_diagnostic_report.py, and the fitted-ringdown summary
    scripts are part of the mature workflow, not optional decoration.

  The strongest demonstrable result is the controlled synthetic variable-depth/variable-
  radius 3-rebar workflow with source mismatch, 10% noise, fitted ringdown/acquisition
  stress, exact geometry/radius rows across multiple seeds, and explicit near-cutoff
  policy limits. The strongest tight-spacing result is separate: close14 target-2 under
  Tx/Rx=50 with a noise boundary near 19.642333984375% RMS.

  Superseded

  Older broad/pixel FWI, raw Powell radius, fixed-source LS radius, W2 as final radius
  objective, PEBDD as final radius selector, and free material inversion are superseded
  or rejected. run_multi_rebar_common_radius_profile.py and
  run_multi_rebar_local_geometry_profile.py remain useful diagnostics, but the coordinate
  optimizer is the mature multi-rebar path.

  Still Unresolved

  No field/lab data. No 3D. No universal global 9-parameter or all-parameter optimizer.
  Radius confidence can still be weak, especially shallow/small bars, edge targets,
  source-shape center cases, and near-threshold ringdown policies. Receiver/grid
  quantization matters for Tx/Rx thresholds. The late multi-rebar branch does not
  automatically prove all earlier special branches; close spacing, shallow single-rebar
  sizing, and field-like source-shape calibration remain separate guarded capabilities.
