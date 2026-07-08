# BEM Experiment Index

## Current Runs

| Run | Tracker | Output | Status |
| ---: | --- | --- | --- |
| 001 | `001_bem_repository_landscape.md` | `outputs/bem_experiments/001_bem_repository_landscape` | Created separate BEM track; shallow-cloned and assessed SCUFF-EM, bempp-cl, and OpenBEM; OpenBEM C++ examples build and run; bempp-cl is the preferred first prototype target but current project environment lacks `numba` and `meshio`. |
| 002 | `002_bempp_environment_probe.md` | `outputs/bem_experiments/002_bempp_environment_probe` | Created an isolated bempp-cl Python environment under ignored outputs; imports are ready; a Gmsh-free Maxwell sphere solve succeeds; custom screen/cylinder geometry is still blocked because Gmsh is unavailable on this ARM/aarch64 setup. |
| 003 | `003_bempp_direct_rebar_mesh_probe.md` | `outputs/bem_experiments/003_bempp_direct_rebar_mesh_probe` | Constructed a finite rebar-like cylinder mesh directly in Python and solved a Bempp Maxwell RWG smoke test without Gmsh; homogeneous PEC rebar prototype path is open, but layered GPR modeling and FDTD validation are still absent. |
| 004 | `004_bempp_rebar_receiver_response_probe.md` | `outputs/bem_experiments/004_bempp_rebar_receiver_response_probe` | Evaluated a 41-point receiver-line scattered-field response above the direct finite rebar mesh; response contract is ready for a small homogeneous BEM/FDTD comparison design, but not for layered GPR or inversion. |
| 005 | `005_bem_fdtd_comparison_design_audit.md` | `outputs/bem_experiments/005_bem_fdtd_comparison_design_audit` | Audited comparison validity; current FDTD is 2D TMz, so direct validation of the 3D finite-cylinder Bempp result is not ready. The next valid step is a 2D sanity check plus separate 3D FDTD reference design. |
| 006 | `006_bempp_rebar_frequency_sweep_probe.md` | `outputs/bem_experiments/006_bempp_rebar_frequency_sweep_probe` | Swept the direct finite-rebar Bempp receiver response over `k=4,6,8,10,12 rad/m`; all responses are finite, supporting continued BEM-only prototype development but not FDTD validation. |
| 007 | `007_bem_fdtd_2d_tmz_sanity_probe.md` | `outputs/bem_experiments/007_bem_fdtd_2d_tmz_sanity_probe` | Ran a clearly labeled 2D TMz FDTD single-rebar response-extraction sanity check; finite scattered response produced, but direct validation of the 3D Bempp finite-cylinder result remains false. |
| 008 | `008_bem_research_track_checkpoint_pack.md` | `outputs/bem_experiments/008_bem_research_track_checkpoint_pack` | Aggregated runs `001`-`007` into a BEM research checkpoint and presentation seed; BEM track is viable, `bempp-cl` remains the first prototype backend, and validation/field/FWI claims remain blocked. |
| 009 | `009_scuff_em_feasibility_probe.md` | `outputs/bem_experiments/009_scuff_em_feasibility_probe` | Probed SCUFF-EM build feasibility; relevant scattering/RF applications and examples are present, but local build/toolchain readiness is false, so SCUFF-EM remains an external reference. |
| 010 | `010_bem_research_track_checkpoint_pack_post_scuff.md` | `outputs/bem_experiments/010_bem_research_track_checkpoint_pack_post_scuff` | Refreshed the aggregate BEM checkpoint after run `009`; current evidence supports BEM prototype development and presentation, not validated 3D GPR-BEM, field readiness, or BEM-FWI. |
| 011 | `011_colleague_scarep_2d_code_audit.md` | `outputs/bem_experiments/011_colleague_scarep_2d_code_audit` | Audited the colleague-provided `scarep_gpr_forward_pkg`; CPU 2D Galerkin BEM imports, compiles, and converges against an analytic cylinder reference, but GPU MFS demos fail due missing cuBLAS and the package is not a direct 3D backend. |
| 012 | `012_bem_track_figure_pack.md` | `outputs/bem_experiments/012_bem_track_figure_pack` | Added figure folders and visual artifacts for the BEM mesh, receiver response, frequency sweep, 2D FDTD sanity response, scarep convergence, and aggregate visual checkpoint. |
| 013 | `013_scarep_2d_cpu_bem_scan_validation.md` | `outputs/bem_experiments/013_scarep_2d_cpu_bem_scan_validation` | Validated the colleague scarep CPU 2D TMz BEM path on an 11-position, 25-frequency analytic-cylinder scan; 32 panels reach 0.0028625612719971973 complex relative L2 without GPU/cuBLAS. |
| 014 | `014_2d_bem_fdtd_matched_adapter.md` | `outputs/bem_experiments/014_2d_bem_fdtd_matched_adapter` | Built the first matched 2D BEM/FDTD adapter on an analytic dielectric-cylinder scan; 32-panel CPU BEM reaches 0.003190629524250936 relative L2 and 5 mm Yee FDTD reaches 0.024754323796019783 relative L2 vs analytic. |
| 015 | `015_2d_pec_bem_fdtd_matched_adapter.md` | `outputs/bem_experiments/015_2d_pec_bem_fdtd_matched_adapter` | Extended the matched adapter to a homogeneous PEC-cylinder rebar-style case; 64-panel CPU PEC BEM reaches 4.762231342258939e-05 relative L2 and 3 mm Yee FDTD reaches 0.0343267003276678 relative L2 vs analytic. |
| 016 | `016_2d_halfspace_pec_bem_fdtd_matched_adapter.md` | `outputs/bem_experiments/016_2d_halfspace_pec_bem_fdtd_matched_adapter` | Moved the matched PEC adapter into an air/concrete half-space; 16-panel layered BEM is within 0.0004746867074423852 of the 32-panel reference and 3 mm Yee FDTD is within 0.030998297443390457 relative L2 of that reference. |
| 017 | `017_project_core_fdtd_source_normalization_adapter.md` | `outputs/bem_experiments/017_project_core_fdtd_source_normalization_adapter` | Tested a project-core FDTD bridge gate; direct/background source calibration reaches 0.03170696405248453 relative L2, but the calibrated rebar-scattered transfer fails with 1.3943651626310445 symmetric time-domain L2, so project-core FDTD/BEM comparison is not ready. |
| 018 | `018_bem_project_core_bridge_checkpoint_pack.md` | `outputs/bem_experiments/018_bem_project_core_bridge_checkpoint_pack` | Condensed runs 013-017 into a presentation checkpoint; BEM-owned ladder through run 016 is ready, but the project-core bridge gate from run 017 remains blocked. |
| 019 | `019_project_core_homogeneous_dielectric_bridge_adapter.md` | `outputs/bem_experiments/019_project_core_homogeneous_dielectric_bridge_adapter` | Removed half-space and PEC complexity; the homogeneous dielectric cylinder bridge still fails with 1.5121594456531522 scattered symmetric time-domain L2 after direct-wave calibration. |
| 020 | `020_project_core_direct_wave_green_transfer_audit.md` | `outputs/bem_experiments/020_project_core_direct_wave_green_transfer_audit` | Removed the target entirely; one per-frequency line-source scale does not transfer across Tx/Rx offsets, with 1.1999907091021738 reference-offset transfer symmetric L2, while per-offset calibration stays at or below 0.360543033595403. |
| 021 | `021_project_core_long_offset_direct_wave_green_transfer_audit.md` | `outputs/bem_experiments/021_project_core_long_offset_direct_wave_green_transfer_audit` | Extended the no-target direct-wave audit to offsets up to 0.26 m; one source scale still fails with 1.2581670693015625 reference-offset transfer symmetric L2, while per-offset calibration stays at or below 0.4026620237905695. |
| 022 | `022_project_core_distance_aware_direct_wave_calibration_probe.md` | `outputs/bem_experiments/022_project_core_distance_aware_direct_wave_calibration_probe` | Tested a distance-aware calibration table from run 021; measured per-offset scaling improves direct-wave symmetric L2 to 0.30880226614764117, but leave-one-offset interpolation remains 0.9672799928720243, so sparse distance interpolation is not ready for target scattering. |
| 023 | `023_project_core_dense_direct_wave_green_transfer_audit.md` | `outputs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit` | Sampled a denser no-target direct-wave grid from 0.02 to 0.28 m in 0.01 m steps; one source factor still fails, but measured per-offset calibration stays below 0.4418908733177504 symmetric L2. |
| 024 | `024_project_core_dense_distance_interpolation_validation.md` | `outputs/bem_experiments/024_project_core_dense_distance_interpolation_validation` | Validated dense distance interpolation from run 023; even/odd held-out offsets reach 0.34190295352453876 symmetric L2, so interpolation inside the sampled range is usable for diagnostics. |
| 025 | `025_project_core_homogeneous_dielectric_distance_calibrated_replay.md` | `outputs/bem_experiments/025_project_core_homogeneous_dielectric_distance_calibrated_replay` | Applied dense broken-path calibration to the run 019 homogeneous dielectric target; scattered symmetric L2 improves only from 1.520128574804845 to 1.4544669770583798, so direct-wave path calibration does not fix the target bridge. |
| 026 | `026_project_core_arrival_window_direct_wave_audit.md` | `outputs/bem_experiments/026_project_core_arrival_window_direct_wave_audit` | Tested whether arrival-windowing fixes the dense direct-wave transfer gate; best all-pair symmetric L2 remains 1.6206668574552758, so late-time finite-domain content is not the main bridge blocker. |
| 027 | `027_project_core_direct_wave_effective_wavenumber_audit.md` | `outputs/bem_experiments/027_project_core_direct_wave_effective_wavenumber_audit` | Tested whether a fitted real effective wavenumber explains project-core direct-wave transfer; mean symmetric L2 improves only from 1.6246350401682335 to 1.5074140243698353, so simple numerical-dispersion correction is not enough. |
| 028 | `028_project_core_source_injection_mode_direct_wave_audit.md` | `outputs/bem_experiments/028_project_core_source_injection_mode_direct_wave_audit` | Compared soft, hard, pre-update, and current-density source injection variants; the best mode still has 1.3021562348784914 reference-offset transfer L2, so simple injection-mode switching does not fix the bridge. |
| 029 | `029_project_core_empirical_green_surface_audit.md` | `outputs/bem_experiments/029_project_core_empirical_green_surface_audit` | Reused the dense no-target direct-wave sweep from run 023 as an empirical project-core Green surface; coarse held-out source/offset interpolation reaches 0.13204235679778975 symmetric L2, so the finite-domain empirical baseline is ready for controlled scattered-field ladder tests. |
| 030 | `030_project_core_homogeneous_dielectric_empirical_green_replay.md` | `outputs/bem_experiments/030_project_core_homogeneous_dielectric_empirical_green_replay` | Replayed the earlier run 019 homogeneous target with the empirical Green surface and found only 1 of 7 source positions covered, so this is a coverage warning rather than a clean target-scattering verdict. |
| 031 | `031_project_core_homogeneous_dielectric_inrange_bridge_adapter.md` | `outputs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter` | Reran the homogeneous dielectric target bridge inside the empirical Green source/offset range; the direct/background relative L2 is 0.24273323569821098 but scattered time symmetric L2 remains 1.5431553591086644. |
| 032 | `032_project_core_homogeneous_dielectric_inrange_empirical_green_replay.md` | `outputs/bem_experiments/032_project_core_homogeneous_dielectric_inrange_empirical_green_replay` | Replayed the in-range target from run 031 with the empirical Green baseline; direct/background L2 drops to 0.01662205712366382 and total time L2 improves to 0.35174147593288074, but scattered L2 remains 1.552057143941903. |
| 033 | `033_project_core_homogeneous_dielectric_strength_ladder.md` | `outputs/bem_experiments/033_project_core_homogeneous_dielectric_strength_ladder` | Ran an in-range dielectric-strength ladder at epsr 1.25, 2.0, and 4.0; empirical scattered L2 stays between 1.5332658067665847 and 1.6256015896432827, so target-scattering representation is now the bridge blocker. |
| 034 | `034_project_core_target_rasterization_audit.md` | `outputs/bem_experiments/034_project_core_target_rasterization_audit` | Audited the in-range circular target rasterization; radius error is at most 0.04776287834105941 mm and centroid error is effectively zero, so gross material-grid target geometry is not the scattering blocker. |
| 035 | `035_project_core_discrete_born_scattering_audit.md` | `outputs/bem_experiments/035_project_core_discrete_born_scattering_audit` | Built a grid-aware first-order Born surrogate from project-core background fields at the actual target cells; weak dielectric target scattered L2 drops from 1.5472037658996989 for the analytic cylinder bridge to 0.0989465314024021. |
| 036 | `036_project_core_discrete_born_strength_ladder.md` | `outputs/bem_experiments/036_project_core_discrete_born_strength_ladder` | Extended the grid-aware Born surrogate to epsr 1.25, 2.0, and 4.0; all three pass with best Born scattered L2 from 0.0989465314024021 to 0.44601690298659386, so the discrete target-scattering operator is now the positive bridge path. |
| 037 | `037_project_core_bem_scattering_adapter_contract.md` | `outputs/bem_experiments/037_project_core_bem_scattering_adapter_contract` | Converted the passing discrete Born ladder into a BEM/project-core adapter contract with seven required interface items and five gates; this is the implementation target before archive, field, or 3D claims. |
| 038 | `038_project_core_bem_scattering_adapter_smoke.md` | `outputs/bem_experiments/038_project_core_bem_scattering_adapter_smoke` | Replayed the run 037 adapter contract as an executable schema over the run 036 cases; all seven interface items are present and the worst selected adapter L2 remains 0.44601690298659386. |
| 039 | `039_project_core_bem_compatible_field_adapter_probe.md` | `outputs/bem_experiments/039_project_core_bem_compatible_field_adapter_probe` | Replaced project-core target-cell fields with BEM-compatible analytic Green fields sampled at the same cells; best analytic variant improves over the analytic-cylinder bridge but misses the adapter gate with worst L2 0.8309901396143111. |
| 040 | `040_project_core_bem_field_map_calibration_probe.md` | `outputs/bem_experiments/040_project_core_bem_field_map_calibration_probe` | Tested a two-term analytic-field mixture under leave-one-scan validation; all-scan fitting reaches worst L2 0.6280658438481003 but held-out validation fails at worst L2 0.9869554402632811. |
| 041 | `041_project_core_bem_project_domain_green_surface_probe.md` | `outputs/bem_experiments/041_project_core_bem_project_domain_green_surface_probe` | Recorded a project-domain target-cell Green surface and predicted held-out source/receiver scan positions; all three contrast cases pass with worst interpolated-surface L2 0.5573625471027422. |
| 042 | `042_project_core_bem_project_domain_green_surface_stress.md` | `outputs/bem_experiments/042_project_core_bem_project_domain_green_surface_stress` | Stress-tested the project-domain target-cell Green surface on fresh high-contrast denser and shifted target cases; all pass with worst interpolated-surface L2 0.5974979747759482. |
| 043 | `043_project_core_bem_green_surface_contract_pack.md` | `outputs/bem_experiments/043_project_core_bem_green_surface_contract_pack` | Packaged runs 037-042 into the current adapter contract: the usable bridge is the project-domain target-cell Green surface, while raw analytic/free-space Green fields remain failed and field/3D/archive claims remain blocked. |
| 044 | `044_project_core_bem_green_surface_geometry_stress.md` | `outputs/bem_experiments/044_project_core_bem_green_surface_geometry_stress` | Stress-tested the contract on target depth and radius changes at epsr 4.0; all four fresh cases pass with worst interpolated-surface L2 0.6390901970749561. |
| 045 | `045_project_core_bem_green_surface_offset_stress.md` | `outputs/bem_experiments/045_project_core_bem_green_surface_offset_stress` | Stress-tested the contract on 10, 30, and 40 mm Tx/Rx offsets at epsr 4.0; all three fresh cases pass with worst interpolated-surface L2 0.6858047703122613. |
| 046 | `046_project_core_bem_green_surface_layered_dielectric_probe.md` | `outputs/bem_experiments/046_project_core_bem_green_surface_layered_dielectric_probe` | Probed an air/concrete layered dielectric case; all-scan and exact-surface gates pass, but sparse interpolated-surface prediction fails at L2 1.1770012780031571, so layered media are not promoted yet. |
| 047 | `047_project_core_bem_green_surface_layered_dense_probe.md` | `outputs/bem_experiments/047_project_core_bem_green_surface_layered_dense_probe` | Diagnosed run 046 with a denser layered target-cell surface; increasing surface samples from 10 to 19 repairs the interpolation gate with L2 0.697021169360853 and zero edge extrapolation. |
| 048 | `048_project_core_bem_green_surface_contract_refresh.md` | `outputs/bem_experiments/048_project_core_bem_green_surface_contract_refresh` | Refreshed the contract after geometry, offset, and layered probes: homogeneous extension is ready in the tested envelope, layered media are conditionally ready with dense zero-edge-extrapolation surface sampling, and field/3D claims remain blocked. |
| 049 | `049_project_core_bem_field_table_replacement_gap_audit.md` | `outputs/bem_experiments/049_project_core_bem_field_table_replacement_gap_audit` | Audited whether raw `scarep` analytic Green fields can replace the project-domain target-cell field table; leave-one-source field L2 is 1.0723419515425194, so raw analytic replacement is not ready. |
| 050 | `050_project_core_bem_finite_domain_field_map_probe.md` | `outputs/bem_experiments/050_project_core_bem_finite_domain_field_map_probe` | Tested per-target-cell finite-domain calibration from raw analytic Green fields to project-domain fields; all-source L2 reaches 0.7242401633347877, but leave-one-source L2 is 0.8005360330027802, so replacement remains a near miss. |
| 051 | `051_project_core_bem_finite_domain_field_map_dense_probe.md` | `outputs/bem_experiments/051_project_core_bem_finite_domain_field_map_dense_probe` | Retested finite-domain calibration with a denser homogeneous field surface; dense leave-one-source L2 worsens to 0.9392735973185401, so dense calibration does not repair BEM-derived field replacement. |
| 052 | `052_project_core_bem_green_surface_adapter_module_audit.md` | `outputs/bem_experiments/052_project_core_bem_green_surface_adapter_module_audit` | Added and audited reusable helper module `bem_green_surface_adapter.py`; focused tests cover dense x-grid construction, per-cell scaling recovery, and validation errors with 4 passed. |
| 053 | `053_project_core_bem_replacement_model_requirements.md` | `outputs/bem_experiments/053_project_core_bem_replacement_model_requirements` | Defined requirements for replacing the project-domain target-cell field table with BEM-derived fields; project source and finite-domain boundary conventions are missing, and BEM field-table replacement, field claims, and 3D claims remain blocked. |
| 054 | `054_project_core_bem_source_convention_ladder.md` | `outputs/bem_experiments/054_project_core_bem_source_convention_ladder` | Tested 48 simple analytic source-convention variants; the best per-cell leave-one-source field-table L2 is 0.7871631960439586, so scalar source tweaks do not close the BEM field replacement gate. |
| 055 | `055_project_core_bem_boundary_image_ladder.md` | `outputs/bem_experiments/055_project_core_bem_boundary_image_ladder` | Tested low-order finite-domain image-source boundary corrections; cardinal image models pass the held-out field-table gate with best global LOO L2 0.3301113956330722 and best per-cell LOO L2 0.1228536659883146. |
| 056 | `056_project_core_bem_boundary_image_scattering_replay.md` | `outputs/bem_experiments/056_project_core_bem_boundary_image_scattering_replay` | Replayed the discrete scattering adapter with the run 055 boundary-image field-table candidate; all three contrast cases pass under leave-one-scan validation with worst L2 0.5620892946687726. |
| 089 | `089_project_core_homogeneous_dielectric_cylinder_bridge.md` | `outputs/bem_experiments/089_project_core_homogeneous_dielectric_cylinder_bridge` | Reran the first factorized project-core bridge rung with a homogeneous dielectric cylinder and frozen scripts; direct/background L2 is 0.21186906609266937, but scattered symmetric time L2 is 1.5075838091082052, so the half-space/project-core promotion gate remains closed. |
| 090 | `090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.md` | `outputs/bem_experiments/090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic` | Replayed run 089 with simple scale, sign, time-shift, tracewise, and per-frequency alignments; the best candidate is per-frequency complex scaling at 1.0629842444792676 symmetric L2, so the failure is not a trivial alignment issue. |
| 091 | `091_project_core_run089_geometry_discrete_born_replay.md` | `outputs/bem_experiments/091_project_core_run089_geometry_discrete_born_replay` | Replayed the run 089 geometry with a project-grid-aware discrete Born surrogate; the best variant reaches 0.5800814918790829 symmetric L2 versus 1.5075838091082052 for the continuous analytic cylinder, so the grid-aware scattering path is positive. |
| 092 | `092_project_core_run089_grid_aware_adapter_contract.md` | `outputs/bem_experiments/092_project_core_run089_grid_aware_adapter_contract` | Converted the run 091 positive path into an eight-item adapter contract with six gates; adapter smoke is ready, while half-space promotion, outputs/experiments promotion, field transfer, 3D validation, and GPU work remain blocked. |
| 093 | `093_project_core_run089_grid_aware_adapter_smoke.md` | `outputs/bem_experiments/093_project_core_run089_grid_aware_adapter_smoke` | Instantiated the run 092 contract as a saved adapter payload; all eight interface items are present, Tx/Rx target-cell fields are 7 x 753 x 17, and the smoke reproduces the run 091 gate at 0.5800814918790826 symmetric L2. |
| 094 | `094_project_core_run089_grid_aware_adapter_fresh_case_stress.md` | `outputs/bem_experiments/094_project_core_run089_grid_aware_adapter_fresh_case_stress` | Stress-tested the reusable adapter on three fresh homogeneous cases; all pass with best-case L2 values 0.1885181142668548, 0.6662947067388982, and 0.5507342875625141, so a layered or half-space smoke design is now the next bounded branch. |
| 095 | `095_project_core_grid_aware_layered_smoke_design_contract.md` | `outputs/bem_experiments/095_project_core_grid_aware_layered_smoke_design_contract` | Connected the run 093/094 grid-aware adapter path to the run 066/067 layered Sommerfeld evidence; the 12-item layered smoke design is ready and the next branch should emit executable layered payload arrays. |
| 096 | `096_project_core_grid_aware_layered_payload_smoke.md` | `outputs/bem_experiments/096_project_core_grid_aware_layered_payload_smoke` | Emitted the executable layered adapter payload for the base epsr-9 case; all 12 interface items are present, scan-level Tx/Rx fields are 5 x 533 x 17, and the leave-one-scan gate passes at 0.6497571611891657. |
| 097 | `097_project_core_grid_aware_layered_payload_stress_replay.md` | `outputs/bem_experiments/097_project_core_grid_aware_layered_payload_stress_replay` | Replayed the executable layered payload interface across four fresh layered stress cases; all pass, with worst leave-one-scan L2 0.6497571611891657, so the BEM replacement contract can be refreshed around the payload artifacts. |
| 098 | `098_project_core_grid_aware_payload_replacement_contract_refresh.md` | `outputs/bem_experiments/098_project_core_grid_aware_payload_replacement_contract_refresh` | Refreshed the BEM replacement contract around runs 093-097; homogeneous and layered payload paths are ready for scoped local 2D/project-core use, while field, historical outputs/experiments, 3D, GPU, and FWI claims remain blocked. |
| 099 | `099_project_core_bem_3d_external_decision_brief.md` | `outputs/bem_experiments/099_project_core_bem_3d_external_decision_brief` | Condensed the 3D external-FDTD decision: the request path is ready for two paired runs and 248 expected frequency rows, the synthetic return pipeline passes, real data are absent, and 3D validation, local 3D launch, GPU/HPC, and FWI remain blocked. |
| 100 | `100_project_core_bem_3d_external_fdtd_team_request_packet.md` | `outputs/bem_experiments/100_project_core_bem_3d_external_fdtd_team_request_packet` | Packaged the run 099 decision into a team-facing external FDTD request: two paired full-Maxwell target/background runs, seven request artifacts, seven acceptance gates, 31 receivers, four frequencies, and 248 expected rows; 3D validation remains blocked until real returns pass. |
| 101 | `101_project_core_bem_3d_external_fdtd_request_attachment_manifest.md` | `outputs/bem_experiments/101_project_core_bem_3d_external_fdtd_request_attachment_manifest` | Added sizes and SHA-256 hashes for all seven run-100 request attachments, making the external FDTD handoff hash-stable; real returned data and 3D validation remain absent. |
| 102 | `102_project_core_bem_3d_external_fdtd_request_bundle_pack.md` | `outputs/bem_experiments/102_project_core_bem_3d_external_fdtd_request_bundle_pack` | Packaged the seven request attachments, checksums, acceptance gates, and return instructions into a portable external-FDTD request bundle; real returned data and 3D validation remain absent. |
| 103 | `103_project_core_bem_3d_external_fdtd_return_inbox_layout.md` | `outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout` | Created the external-return inbox layout with target/background frequency-bin file locations, metadata requirements, and intake directories; no placeholder external data were installed. |
| 104 | `104_project_core_bem_3d_external_fdtd_return_inbox_preflight.md` | `outputs/bem_experiments/104_project_core_bem_3d_external_fdtd_return_inbox_preflight` | Made the return inbox executable as a preflight gate; the real inbox currently fails because returned target/background files and the completed metadata ledger are absent. |
| 105 | `105_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.md` | `outputs/bem_experiments/105_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke` | Proved the preflight can pass on an isolated complete synthetic inbox; real BEM/FDTD comparison and 3D validation remain blocked until real external returns pass the same gate. |
| 106 | `106_project_core_bem_bempp_dipole_mesh_refinement_audit.md` | `outputs/bem_experiments/106_project_core_bem_bempp_dipole_mesh_refinement_audit` | Audited the 3D Bempp dipole prototype under mesh refinement; the baseline 6x16 mesh is within 0.010296810068779048 relative L2 of the 8x20 mesh and passes the BEM-side mesh-stability gate, while 3D FDTD validation and layered 3D GPR remain blocked. |
| 107 | `107_project_core_bem_bempp_dipole_source_convention_sensitivity.md` | `outputs/bem_experiments/107_project_core_bem_bempp_dipole_source_convention_sensitivity` | Audited source-convention sensitivity on the stable 3D Bempp dipole baseline; orientation changes reach 6.800743917312345 relative L2 and 15 mm height shifts reach 0.14058934457504094, so source orientation, position, and height must be locked as required metadata before paired FDTD comparison. |
| 108 | `108_project_core_bem_bempp_receiver_height_sensitivity.md` | `outputs/bem_experiments/108_project_core_bem_bempp_receiver_height_sensitivity` | Audited receiver-height sensitivity with the stable BEM mesh and locked source convention; 15 mm receiver-height shifts change the response by about 0.10-0.13 relative L2 and a 30 mm shift reaches 0.19131367619758774, so receiver coordinates, height, span, and count must be required metadata. |
| 109 | `109_project_core_bem_3d_comparison_metadata_contract_addendum.md` | `outputs/bem_experiments/109_project_core_bem_3d_comparison_metadata_contract_addendum` | Converted runs 106-108 into a strict 13-field metadata addendum for future paired 3D FDTD returns; all 13 strict fields are absent as explicit keys from the current return metadata template, so the return gate needs this addendum before real BEM/FDTD comparison. |
| 110 | `110_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.md` | `outputs/bem_experiments/110_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum` | Made the run 109 addendum executable as a return metadata preflight; the missing real return fails, an old 12-field synthetic ledger fails, and a complete 25-field synthetic ledger passes, so real BEM/FDTD comparison remains blocked until returned data pass the upgraded gate. |
| 111 | `111_project_core_bem_bempp_dipole_frequency_grid_stability_audit.md` | `outputs/bem_experiments/111_project_core_bem_bempp_dipole_frequency_grid_stability_audit` | Audited the locked 3D Bempp dipole prototype across nine frequencies from 0.4 to 3.0 GHz; all responses are finite, max adjacent shape L2 is 0.06658931539243934, and amplitude varies strongly, so this informs frequency-bin and normalization choices but does not validate against 3D FDTD. |
| 112 | `112_project_core_bem_bempp_high_frequency_mesh_stability_audit.md` | `outputs/bem_experiments/112_project_core_bem_bempp_high_frequency_mesh_stability_audit` | Checked 2.5 and 3.0 GHz mesh stability with 6x16, 8x20, and 10x24 meshes; 3.0 GHz baseline-to-fine relative L2 reaches 0.055639649360411644, but fine-to-extra-fine drops to 0.009408458305433572, so high-frequency BEM comparisons should use 8x20 or finer as the reference. |
| 113 | `113_project_core_bem_bempp_fine_mesh_frequency_grid_audit.md` | `outputs/bem_experiments/113_project_core_bem_bempp_fine_mesh_frequency_grid_audit` | Repeated the full 0.4-3.0 GHz Bempp grid on the 8x20 fine mesh; all nine responses are finite, the max adjacent shape L2 is 0.06786245488660995, and the largest 6x16-to-8x20 gap remains at 3.0 GHz with relative L2 0.055639649360411644, so 8x20 becomes the safer high-frequency BEM reference mesh. |
| 114 | `114_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh.md` | `outputs/bem_experiments/114_project_core_bem_3d_fdtd_fine_mesh_return_contract_refresh` | Refreshed the external 3D FDTD return contract after run 113: the original four-bin return remains acceptable if real files pass gates, the preferred full fine-mesh return has nine frequencies and 558 paired rows, the 8x20 mesh is the BEM reference, and validation remains blocked until real target/background files pass the 25-field metadata and frequency-bin gates. |
| 115 | `115_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.md` | `outputs/bem_experiments/115_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates` | Wrote strict target/background import templates for the preferred nine-bin return: 9 frequencies, 31 receivers, 279 rows per file, 558 paired rows, and 3348 blank complex-field cells to be filled by real external FDTD; comparison and validation remain blocked until real values pass all gates. |
| 116 | `116_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.md` | `outputs/bem_experiments/116_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke` | Added a synthetic-fill smoke for the nine-bin templates: blank target/background templates are correctly blocked, synthetic filled target/background files pass with zero filled-check failures, and the result remains schema evidence only until real external FDTD values arrive. |
| 380 | `380_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.md` | `outputs/bem_experiments/380_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit` | Audited finite receiver-aperture averaging on the run 113 fine-mesh Bempp receiver rows; a 10.67 mm aperture already reaches 0.08009547612144642 relative L2 at 3 GHz, and a 42.67 mm aperture reaches 0.44166920910128993, so future paired BEM/FDTD returns need explicit aperture/operator metadata. |
| 381 | `381_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validator.md` | `outputs/bem_experiments/381_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validator` | Validated run 380 from artifacts with 8 of 8 checks passing, including source identity, point-receiver identity, threshold crossing, high-frequency worst case, aperture-growth progression, blocked downstream states, figure validation, and script snapshots. |
| 382 | `382_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validation_sensitivity.md` | `outputs/bem_experiments/382_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_validation_sensitivity` | Stress-tested the run 381 validator; the exact run 380 audit passes and 13 damaged variants fail as expected, closing the guarded receiver-aperture sensitivity block while real comparison and 3D validation remain blocked. |
| 383 | `383_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum.md` | `outputs/bem_experiments/383_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum` | Folded the guarded receiver-aperture sensitivity result into the preferred fine-mesh BEM/FDTD return metadata contract: the prior 30-field template becomes 35 fields, with five new blocking aperture/operator fields. |
| 384 | `384_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validator.md` | `outputs/bem_experiments/384_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validator` | Validated run 383 from artifacts with 7 of 7 checks passing, confirming field counts, aperture requirement rows, aperture template values, sensitivity evidence, downstream blocked states, figure validation, and script snapshots. |
| 385 | `385_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validation_sensitivity.md` | `outputs/bem_experiments/385_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum_validation_sensitivity` | Stress-tested the run 384 validator; the exact 35-field addendum passes and 13 damaged variants fail as expected, closing the guarded aperture metadata-addendum block before any refreshed real-return preflight. |
| 386 | `386_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh.md` | `outputs/bem_experiments/386_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh` | Refreshed the preferred nine-bin real-return preflight with the 35-field aperture-aware metadata template; all 10 blocking checks fail because returned target, background, and metadata files remain absent, so real comparison and 3D validation remain blocked. |

## Current Decision

Use BEM in parallel with FDTD, not as an immediate replacement.

```text
BEM:  fast frequency-domain 3D forward-model and candidate-screening track.
FDTD: high-fidelity time-domain validation and existing evidence anchor.
```

Current backend stance:

| Backend | Role | Current status |
| --- | --- | --- |
| `bempp-cl` | Primary first Python prototype candidate | Applicable; isolated environment, direct finite-rebar mesh, Maxwell solve, and receiver-line response are working. |
| `OpenBEM` | Low-level RWG/TEFIE/NMFIE formulation reference | Applicable as an external research reference; C++ examples build and run locally; GPL-3+ and not turnkey. |
| `SCUFF-EM` | Mature external EM-BEM reference/tool | Applicable as a benchmark/reference suite; local build readiness is false due missing `libtoolize`, `gfortran`, BLAS/LAPACK/HDF5 discovery, Gmsh absence, and licensing review. |

## Current Capability

The BEM track can now run a minimal bempp-cl Maxwell solve in an isolated venv
and a direct finite-cylinder Maxwell smoke:

```text
mesh:             bempp_cl.api.shapes.regular_sphere(1)
elements:         32
RWG DOFs:         48
solution norm:    7.7408573921293

mesh:             direct finite cylinder, length=0.5 m, radius=0.025 m
elements:         120
RWG DOFs:         180
solution norm:    10.787448040121925
Gmsh required:    false

response:         41 receiver points, y span=0.3 m, z=0.15 m
max |E_s|:        0.027575913303849516
mean |E_s|:       0.0265692019903684
symmetry error:   8.994780900757268e-05

FDTD status:      current in-repo solver is 2D TMz
direct 3D valid:  false

sweep k:          4, 6, 8, 10, 12 rad/m
sweep finite:     true
max |E_s| range:  0.01916740428427016 to 0.05802136168763753

FDTD sanity:      2D TMz single rebar, finite response
max |Ez_s|:       0.00454917485993519
3D validation:    false

checkpoint:       run 010 aggregates 8 BEM evidence runs and 3 backends
presentation:     run 010 is ready as seed outline, not final slides

SCUFF status:     external reference applicable; internal dependency ready false
SCUFF blockers:   libtoolize, gfortran, BLAS/LAPACK/HDF5 discovery, Gmsh, licensing

scarep status:    useful 2D TMz BEM/MFS reference; not direct 3D backend
scarep CPU BEM:   analytic-cylinder error drops to 0.00405772229133273 at 32 panels
scarep scan:      11 scan positions x 25 frequencies, 32-panel CPU BEM
                  complex relative L2=0.0028625612719971973 vs analytic
matched adapter:  run 014 compares CPU BEM and Yee FDTD on the same 2D
                  dielectric-cylinder setup; best BEM L2=0.003190629524250936,
                  best FDTD L2=0.024754323796019783 vs analytic
PEC adapter:      run 015 compares CPU PEC BEM and Yee FDTD on the same 2D
                  PEC-cylinder setup; best BEM L2=4.762231342258939e-05,
                  best FDTD L2=0.0343267003276678 vs analytic
half-space PEC:   run 016 compares CPU layered PEC BEM and Yee FDTD in an
                  air/concrete half-space; 16-panel BEM differs from 32-panel
                  reference by 0.0004746867074423852 and 3 mm FDTD differs
                  from that reference by 0.030998297443390457
project-core gate:
                  run 017 calibrates layered PEC BEM from the project-core
                  FDTD background/direct response; direct L2 is
                  0.03170696405248453, but scattered symmetric time L2 is
                  1.3943651626310445, so project-core comparison is not ready
checkpoint pack:  run 018 summarizes runs 013-017 for presentation planning;
                  the BEM-owned ladder is ready through run 016, while the
                  project-core bridge remains a blocker
homogeneous gate:
                  run 019 removes half-space and PEC complexity; direct L2 is
                  0.2109902555403409, total symmetric time L2 is
                  0.3506392905143433, but scattered symmetric time L2 is
                  1.5121594456531522
direct-wave audit:
                  run 020 removes the target entirely; one source factor from
                  the 20 mm Tx/Rx offset does not transfer to longer offsets,
                  while per-offset fitting is much better
long-offset audit:
                  run 021 extends the no-target direct-wave audit to 260 mm;
                  the same distance-dependent source/Green mismatch persists
distance-aware probe:
                  run 022 shows that a measured per-offset source table helps,
                  but sparse leave-one-offset interpolation is not reliable
                  enough to apply to target scattering
dense direct wave:
                  run 023 samples direct waves every 10 mm from 20 mm to
                  280 mm; one source factor still fails, but per-offset fits
                  remain much better
dense interpolation:
                  run 024 validates interpolation inside that dense sampled
                  range with 0.34190295352453876 symmetric L2 on held-out
                  offsets
target replay:
                  run 025 applies dense broken-path calibration to the
                  homogeneous dielectric target; the target scattered mismatch
                  remains too large, so direct-wave distance calibration alone
                  is not the bridge correction
arrival window:
                  run 026 shows that Gaussian direct-arrival windowing does
                  not repair the dense direct-wave transfer gate
effective k:      run 027 fits a real effective wavenumber per frequency; this
                  only slightly improves direct-wave offset agreement
source modes:     run 028 compares several project-core source-injection
                  variants; none passes the direct-wave transfer gate
empirical Green:  run 029 shows the saved project-core direct-wave responses
                  form a smooth empirical source/offset surface; coarse
                  held-out interpolation reaches 0.13204235679778975
                  symmetric L2, unlike the analytic Green baseline at
                  1.6206668574552767
target replay:    run 032 is the clean in-range empirical replay; empirical
                  direct/background L2 is 0.01662205712366382 and total time
                  L2 improves, but scattered time L2 remains 1.552057143941903
strength ladder:  run 033 tests epsr 1.25, 2.0, and 4.0 inside the empirical
                  Green range; all scattered comparisons fail above 1.53
                  symmetric L2, so direct-wave calibration is no longer the
                  active blocker
rasterization:    run 034 shows the circular target grid geometry is accurate
                  to better than 0.05 mm radius error with effectively zero
                  centroid error, so the next blocker is the discrete
                  target-scattering operator rather than gross geometry
discrete Born:    run 035 builds a project-grid-aware Born surrogate from
                  background fields at the rasterized target cells; weak target
                  scattered L2 improves from 1.5472037658996989 to
                  0.0989465314024021
Born ladder:      run 036 keeps that grid-aware surrogate below 0.45 scattered
                  L2 for epsr 1.25, 2.0, and 4.0, establishing the current
                  positive scattering-operator bridge
adapter contract: run 037 defines the seven interface items and five gates
                  needed before continuous BEM target fields can be compared
                  to project-core traces through the discrete operator
adapter smoke:    run 038 validates the run 037 contract as an executable
                  schema over the run 036 cases; missing interface items are
                  zero and the worst selected adapter L2 is 0.44601690298659386
BEM field probe:  run 039 replaces project-core target-cell fields with
                  BEM-compatible continuous analytic Green fields sampled at
                  the same cells; best analytic L2 is 0.8309901396143111, so
                  the next branch is field-map calibration rather than
                  adapter promotion
field-map probe:  run 040 shows a two-term analytic-field mixture can fit the
                  saved scan positions, but leave-one-scan validation fails
                  with worst L2 0.9869554402632811, so the next branch is a
                  project-domain Green surface at target cells
project surface:  run 041 records project-core background fields at the target
                  cells and uses them as a finite-domain Green surface; held-out
                  source/receiver predictions pass the adapter gate with worst
                  L2 0.5573625471027422 across epsr 1.25, 2.0, and 4.0
surface stress:   run 042 creates fresh high-contrast denser/shifted target
                  cases and keeps the project-domain target-cell surface inside
                  the adapter gate with worst interpolated L2 0.5974979747759482
contract pack:    run 043 packages runs 037-042 into the current reusable
                  adapter contract: project-domain target-cell Green surface
                  is usable for tested 2D cases; raw analytic/free-space Green
                  fields, archive claims, field claims, and 3D claims are not
geometry stress:  run 044 extends the contract through depth and radius changes
                  at epsr 4.0; all four cases pass with worst interpolated L2
                  0.6390901970749561
offset stress:    run 045 extends the contract through 10, 30, and 40 mm Tx/Rx
                  offsets at epsr 4.0; all three cases pass with worst
                  interpolated L2 0.6858047703122613
layered probe:    run 046 shows the layered dielectric operator can fit
                  all-scan and exact leave-one gates, but sparse target-cell
                  surface interpolation fails at L2 1.1770012780031571
layered dense:    run 047 repairs the run 046 layered interpolation failure by
                  increasing surface samples from 10 to 19; interpolated L2 is
                  0.697021169360853 with zero edge extrapolated points
contract refresh: run 048 refreshes the active contract: homogeneous tested
                  envelope ready, layered media conditionally ready with dense
                  target-cell surface sampling, field/3D claims blocked
field-table gap:  run 049 compares raw `scarep` analytic Green fields against
                  the project-domain target-cell field table; leave-one-source
                  field L2 is 1.0723419515425194, so raw analytic replacement
                  remains blocked
field-map probe:  run 050 adds per-target-cell finite-domain calibration; the
                  all-source field L2 reaches 0.7242401633347877 but held-out
                  L2 remains 0.8005360330027802, so it is a near miss only
dense field map:  run 051 retests with a denser homogeneous field surface; the
                  held-out L2 worsens to 0.9392735973185401, so dense
                  calibration is not the replacement fix
adapter module:   run 052 adds `bem_green_surface_adapter.py` with focused
                  tests for reusable dense-grid and per-cell leave-one-source
                  scaling utilities; 4 tests pass
replacement reqs: run 053 defines the next BEM replacement requirements:
                  source convention, finite-domain boundary convention, and
                  material/layer convention must pass field-table plus
                  scattering replay gates before replacement
source ladder:    run 054 tests source height, effective speed, scalar source
                  spectrum, and distance regularization variants; the best
                  held-out field-table L2 is 0.7871631960439586, still above
                  the 0.75 gate
boundary images:  run 055 adds low-order top/bottom/left/right image-source
                  components; cardinal image models pass the field-table gate
                  with best global LOO L2 0.3301113956330722
boundary replay:  run 056 replays target scattering with the run 055 field-table
                  candidate; all three contrast cases pass under leave-one-scan
                  validation with worst L2 0.5620892946687726
stress replay:    run 057 stress-tests the run 056 boundary-image replacement
                  on saved lateral, depth/radius, and Tx/Rx-offset cases; all
                  ten stress cases pass under leave-one-scan replay with worst
                  L2 0.667995713341894
layered replay:   run 058 tests the homogeneous boundary-image replacement on
                  the saved air/concrete layered case; it fails the layered
                  gate with best leave-one-scan scattering L2 0.9920836859251249,
                  so layered media remain on the dense project-domain surface
                  path
layer basis:      run 059 tests simple optical-path and interface-image
                  layer-aware basis terms; the best leave-one-scan scattering
                  L2 is 1.0946737347877629, so low-order layer-aware images do
                  not repair the run 058 failure
contract refresh: run 060 consolidates runs 047 and 055-059 into the current
                  boundary-image contract: homogeneous 2D replacement is ready
                  inside the tested project-core envelope, layered replacement
                  is not ready, dense layered project-domain surfaces remain
                  required, and field/3D/FWI/GPU claims remain blocked
layered cache:    run 061 exports the dense layered project-domain surface as
                  a reusable cache; the 19x533x17 complex surface is 2710904
                  bytes and replays the run 047 layered gate with interpolated
                  L2 0.697021169360853
cache consumer:   run 062 validates the run 061 cache consumer path; the cache
                  loads in about 0.0124 seconds, has zero validation findings,
                  and replays the layered gate with interpolated L2
                  0.697021169360853 without rerunning FDTD field recording
decimation:       run 063 uses the layered cache to test x-sampling policies;
                  three of six policies pass, the full 10 mm cache is best
                  at L2 0.697021169360853, and a 7-sample 30 mm grid passes
                  at L2 0.704323503677739 but needs fresh stress validation
30mm stress:      run 064 performs that fresh layered stress test; the 30 mm
                  grid passes three of four cases but fails the epsr-12 case
                  with L2 0.8468025283677086, so it is not promoted and the
                  full 10 mm layered cache remains the conservative default
Sommerfeld proxy: run 065 tests a scalar two-layer transmitted Sommerfeld-style
                  Green proxy against the cached layered case; it passes with
                  field-table LOO L2 0.3928483810786592 and scattering LOO L2
                  0.6497571611891658, so it is promoted to fresh layered stress
                  validation
Sommerfeld stress:
                  run 066 stress-tests that proxy on four fresh layered cases;
                  all four pass with worst scattering LOO L2
                  0.6497571611891657, promoting the scalar Sommerfeld proxy to
                  the active layered 2D replacement candidate inside the tested
                  project-core envelope
contract refresh: run 067 records the updated BEM replacement contract:
                  homogeneous 2D uses boundary images, layered 2D uses the
                  scalar Sommerfeld proxy, the full 10 mm tabulated layered
                  surface remains a fallback, compact 30 mm sampling and
                  low-order layered images are blocked, and field/3D/FWI/GPU
                  claims remain blocked
3D transition:    run 068 defines the 3D lift contract; 10 requirements are
                  listed, with 4 partial and 6 blocked. 3D transition, field
                  transfer, field FWI, and GPU/HPC remain not ready because
                  finite-rebar geometry, 3D Maxwell unknowns, source/receiver
                  modeling, and a matched 3D FDTD reference are still missing
3D reference:     run 069 defines a minimal 3D reference design: 0.30 x 0.20 x
                  0.18 m, 5 mm grid, 80 x 60 x 56 cells including PML, 630
                  time steps for 6 ns, and a padded memory estimate of 0.160
                  GiB. It is ready for design review, not for launch.
Bempp 3D backend:
                  run 070 adapts the Gmsh-free Bempp finite-cylinder backend
                  to the run 069 geometry. A 0.12 m by 0.01 m PEC cylinder
                  with 224 elements and 336 RWG DOFs solves at 0.5, 1.0, 1.5,
                  and 3.0 GHz concrete-effective wavenumbers with finite
                  receiver-line responses. This is backend readiness for a
                  future matched 3D FDTD comparison, not 3D validation.
3D FDTD contract:
                  run 071 converts the run 070 Bempp receiver table into a
                  matched 3D FDTD comparison contract. Seven items are ready,
                  one is partial, and two are blocked. The key blocker is that
                  run 070 uses a homogeneous y-polarized plane-wave convention,
                  so a fair FDTD comparison must either match that plane wave
                  or first create a Bempp point/small-dipole source run.
BEM dipole source:
                  run 072 creates that point/small-dipole source candidate in
                  Bempp. The same finite-rebar mesh solves at 0.5, 1.0, 1.5,
                  and 3.0 GHz with finite 31-receiver complex response tables.
                  This removes the immediate BEM-side source mismatch for a
                  GPR-like 3D comparison design, but paired FDTD target and
                  background manifests are still missing.
FDTD manifests:   run 073 writes those paired target/background FDTD manifest
                  templates for the run 072 dipole-source reference. The
                  manifests preserve the same homogeneous epsr-6 background,
                  source, receivers, and frequency bins, and differ only by
                  finite PEC target presence. Data are still missing, so no 3D
                  validation claim is ready.
manifest validator:
                  run 074 validates the run 073 target/background templates:
                  9 of 9 checks pass, including manifest type, receiver,
                  frequency, source, domain, and target-presence pairing. This
                  is a preflight gate for accepting future FDTD data, not a 3D
                  validation result.
FDTD comparator:
                  run 075 defines the exact target/background FDTD
                  frequency-bin schema for future comparison against the run
                  072 Bempp dipole-source reference. Each side must provide
                  124 complex-field rows: 31 receivers times four frequencies.
                  The manifest gate passes, but the comparator remains blocked
                  because zero target and zero background FDTD rows exist.
comparator smoke:
                  run 076 creates synthetic target/background frequency-bin
                  rows from the run 072 Bempp table and proves the run 075
                  comparator can pass when 124 target and 124 background rows
                  are complete and correctly keyed. This is a schema smoke
                  test only; real FDTD data are still absent.
FDTD import:
                  run 077 writes strict target/background frequency-bin import
                  templates with all 31 receiver by four frequency keys
                  prefilled and the exact 12 run 075 comparator columns. Future
                  FDTD extraction only needs to fill the six complex field
                  columns for both sides. This is import scaffolding, not real
                  FDTD data or 3D validation.
import smoke:
                  run 078 fills those run 077 templates with deterministic
                  synthetic finite field values and passes all 22 run 075
                  comparator checks. This proves the import templates are
                  mechanically usable, but remains synthetic schema evidence:
                  real paired FDTD target/background data are still absent.
execution audit:
                  run 079 audits whether the local repository can produce the
                  real paired 3D FDTD data today. Six checks pass and one is
                  partial, but three blocking gaps remain: no local 3D FDTD
                  engine, no real receiver-to-frequency-bin extractor, and no
                  paired target/background real FDTD outputs. Do not launch or
                  claim 3D validation from the current local repo state.
extractor contract:
                  run 080 defines the real 3D FDTD frequency-bin extractor
                  contract. Future 3D FDTD/exporter output must provide
                  target/background receiver time traces with nine required
                  columns, then an extractor must fill the 12-column run 077
                  frequency-bin templates. The contract is ready, but extractor
                  implementation and real 3D traces are still missing.
extractor smoke:
                  run 081 implements a direct-DFT receiver-trace extractor and
                  proves it on synthetic target/background traces shaped by run
                  080. It extracts 124 target and 124 background frequency-bin
                  rows and passes all 22 run 075 comparator checks. This is a
                  synthetic extractor smoke, not real 3D FDTD validation.
engine candidates:
                  run 082 audits candidate paths for producing the real paired
                  3D FDTD target/background data. External full-Maxwell 3D
                  FDTD import is the preferred next validation-data route. A
                  tiny local 3D engine is only supporting plumbing, while
                  direct ports of the current 2D CPU/GPU TMz solvers are
                  blocked as longer-term research work.
external request:
                  run 083 packages the external full-Maxwell 3D FDTD data
                  request. It asks for two paired runs, includes seven request
                  artifacts, fixes 31 receivers and four frequencies, and
                  expects 248 complex frequency rows before the run 075
                  comparator can be rerun on real data.
return preflight:
                  run 084 defines the return preflight for future external
                  FDTD frequency-bin files. The current pending return folder
                  fails with 10 blocking findings because no returned target or
                  background files exist yet. This is a gate, not validation.
return handoff:   run 085 packages the external-return acceptance checklist:
                  two required frequency-bin CSV files, 12 metadata fields,
                  eight acceptance steps, and eight gate crosswalk rows. The
                  project is ready to receive returned files, but the current
                  pending return still has zero real target/background files.
metadata gate:    run 086 makes the run 085 metadata ledger machine-checkable.
                  It has seven checks and currently fails all seven because no
                  metadata ledger or hash-verifiable target/background files
                  exist in the pending return.
metadata smoke:   run 087 creates a synthetic returned-file bundle and metadata
                  ledger that pass all seven run 086 checks. This proves the
                  metadata gate is satisfiable, but it is synthetic only and
                  does not provide real external FDTD data.
full return smoke:
                  run 088 creates a complete synthetic external return bundle
                  with target/background frequency-bin files and metadata. Both
                  the metadata preflight and frequency-bin return preflight
                  pass with zero blocking findings. This proves the full return
                  acceptance pipeline is satisfiable, but remains synthetic
                  only.
project-core rung:
                  run 089 revisits the first factorized project-core bridge
                  rung after the local 2D candidate-pack decision. Even in a
                  homogeneous dielectric-cylinder setup, direct/background
                  calibration reaches 0.21186906609266937 L2 while scattered
                  transfer fails with 1.5075838091082052 symmetric time-domain
                  L2. The half-space rung and project-core promotion remain
                  blocked.
alignment replay:
                  run 090 replays run 089 and tests sign, scalar amplitude,
                  global time shift, tracewise alignment, and per-frequency
                  complex scaling. The best candidate is still 1.0629842444792676
                  symmetric L2, so the homogeneous bridge failure is not a
                  trivial alignment problem.
grid replay:      run 091 replays the same run 089 geometry with project-core
                  background fields at the actual rasterized target cells. The
                  best discrete Born variant reaches 0.5800814918790829
                  symmetric L2, so grid-aware target scattering is the positive
                  bridge direction.
adapter contract:
                  run 092 converts the run 091 positive path into an
                  eight-item BEM/project-core adapter contract. The contract is
                  ready for a smoke implementation, but half-space, field,
                  outputs/experiments, GPU, and 3D claims remain blocked.
adapter smoke:    run 093 instantiates the run 092 contract and saves the full
                  adapter payload, including target cells, weights, Tx/Rx
                  target-cell fields, source spectrum, adapter frequency bins,
                  and time-band comparison. All eight interface items are
                  present and the run 091 gate is reproduced at
                  0.5800814918790826 symmetric L2.
fresh-case stress:
                  run 094 applies the reusable adapter to three fresh
                  homogeneous cases spanning contrast, radius, and target
                  position. All three pass below the 0.75 gate; the worst case
                  is shifted_deeper_epsr4 at 0.6662947067388982 symmetric L2.
layered smoke design:
                  run 095 bridges the run 093/094 grid-aware payload path with
                  the run 066/067 layered Sommerfeld evidence. The design has
                  12 interface items and five gates; prerequisites pass, but
                  the executable layered payload smoke is still the next
                  required artifact.
layered payload:
                  run 096 emits that executable layered payload for the base
                  epsr-9 case. It saves reference, proxy, fitted, and
                  leave-one layered surfaces, scan-level Tx/Rx fields, adapter
                  frequency bins, and band-limited comparisons. The best
                  leave-one-scan gate is 0.6497571611891657.
layered payload stress:
                  run 097 replays the executable layered payload interface
                  across base, shifted, deeper, and high-contrast layered
                  cases. All four pass; worst leave-one-scan L2 remains
                  0.6497571611891657.
payload contract:
                  run 098 refreshes the replacement contract around runs
                  093-097. Homogeneous project-core cases now use the
                  grid-aware target-cell payload; layered project-core cases
                  use the grid-aware payload with scalar Sommerfeld field
                  provider. Field, historical archive, 3D, GPU, and FWI claims
                  remain blocked.
scarep GPU MFS:   blocked by missing libcublas.so.12

figures:          run 012 generated 7 PNG figures across BEM runs 003, 004,
                  006, 007, 011, and 012; run 013 added 2 validation figures;
                  run 014 added 3 matched BEM/FDTD figures; run 015 added
                  3 PEC matched BEM/FDTD figures; run 016 added 3 half-space
                  matched BEM/FDTD figures; run 017 added 4 project-core
                  bridge-gate figures; run 018 added 1 checkpoint figure;
                  run 019 added 4 homogeneous dielectric bridge figures; run
                  020 added 3 direct-wave transfer figures; run 021 added
                  3 long-offset direct-wave transfer figures; run 022 added
                  2 distance-aware calibration figures; run 023 added 3 dense
                  direct-wave figures; run 024 added 2 interpolation figures;
                  run 025 added 3 target replay figures; run 026 added 1
                  arrival-window audit figure; run 027 added 1 effective
                  wavenumber figure; run 028 added 1 source-mode figure;
                  run 029 added 1 empirical Green-surface figure; run 030
                  added 1 replay figure; run 031 added 4 in-range target
                  bridge figures; run 032 added 1 in-range replay figure;
                  run 033 added 1 strength-ladder figure; run 034 added 1
                  target-rasterization figure; run 035 added 1 discrete Born
                  audit figure; run 036 added 1 discrete Born ladder figure;
                  run 037 added 1 adapter-contract figure; run 038 added
                  1 adapter-smoke figure; run 039 added 1 BEM-compatible
                  field-adapter figure; run 040 added 1 field-map calibration
                  figure; run 041 added 1 project-domain Green-surface figure;
                  run 042 added 1 project-domain Green-surface stress figure;
                  run 043 added 1 contract-pack gate figure; run 044 added
                  1 geometry-stress figure; run 045 added 1 offset-stress
                  figure; run 046 added 1 layered-dielectric probe figure;
                  run 047 added 1 layered dense-surface diagnostic figure;
                  run 048 added 1 contract-refresh figure; run 049 added
                  1 field-table replacement gap figure; run 050 added
                  1 finite-domain field-map figure; run 051 added
                  1 dense finite-domain field-map figure; run 052 added
                  1 adapter-module audit figure; run 053 added
                  1 replacement-requirements figure; run 054 added
                  1 source-convention ladder figure; run 055 added
                  1 boundary-image ladder figure; run 056 added
                  1 boundary-image scattering replay figure; run 057 added
                  1 boundary-image stress replay figure; run 058 added
                  1 boundary-image layered replay figure; run 059 added
                  1 layered interface basis ladder figure; run 060 added
                  1 boundary-image contract-refresh figure; run 061 added
                  1 layered dense-surface cache figure; run 062 added
                  1 layered cache-consumer figure; run 063 added
                  1 layered surface-decimation figure; run 064 added
                  1 layered 30 mm stress figure; run 065 added
                  1 layered Sommerfeld proxy figure; run 066 added
                  1 layered Sommerfeld stress figure; run 067 added
                  1 BEM replacement contract-refresh figure; run 068 added
                  1 BEM 3D-transition contract figure; run 069 added
                  1 minimal 3D reference-design figure; run 070 added
                  1 Bempp minimal 3D reference probe figure; run 071 added
                  1 matched 3D FDTD comparison-contract figure; run 072 added
                  1 Bempp dipole-source probe figure; run 073 added
                  1 FDTD manifest-contract figure; run 074 added
                  1 FDTD manifest-validator figure; run 075 added
                  1 FDTD pair-comparator preflight figure; run 076 added
                  1 FDTD pair-comparator synthetic-smoke figure; run 077 added
                  1 FDTD frequency-bin import-template figure; run 078 added
                  1 FDTD import-template smoke figure; run 079 added
                  1 FDTD execution-readiness audit figure; run 080 added
                  1 FDTD frequency-bin extractor-contract figure; run 081 added
                  1 FDTD frequency-bin extractor-smoke figure; run 082 added
                  1 FDTD engine-candidate audit figure; run 083 added
                  1 external 3D FDTD data-request figure; run 084 added
                  1 external 3D FDTD return-preflight figure; run 085 added
                  1 external 3D FDTD return-acceptance figure; run 086 added
                  1 external 3D FDTD return-metadata-preflight figure; run 087
                  added 1 external 3D FDTD return-metadata smoke figure; run
                  088 added 1 external 3D FDTD full-return-bundle smoke figure;
                  run 089 added 4 homogeneous dielectric bridge figures; run
                  090 added 2 homogeneous bridge alignment figures; run 091
                  added 1 run-089-geometry discrete Born replay figure; run 092
                  added 1 run-089 grid-aware adapter-contract figure; run 093
                  added 1 run-089 grid-aware adapter-smoke figure; run 094
                  added 1 run-089 grid-aware fresh-case stress figure; run 095
                  added 1 grid-aware layered-smoke design-contract figure; run
                  096 added 1 grid-aware layered-payload smoke figure; run 097
                  added 1 grid-aware layered-payload stress-replay figure; run
                  098 added 1 grid-aware payload replacement-contract figure;
                  run 099 added 1 external 3D decision-brief figure; run 100
                  added 1 external 3D FDTD request-packet figure; run 101
                  added 1 request attachment-manifest figure; run 102 added
                  1 request bundle-pack figure; run 103 added 1 external
                  return-inbox layout figure; run 104 added 1 return-inbox
                  preflight figure; run 105 added 1 synthetic preflight-smoke
                  figure; run 106 added 1 Bempp dipole mesh-refinement figure;
                  run 107 added 1 Bempp source-convention sensitivity figure;
                  run 108 added 1 Bempp receiver-height sensitivity figure; run
                  109 added 1 strict comparison-metadata addendum figure; run
                  110 added 1 metadata-preflight addendum figure; run 111
                  added 1 Bempp dipole frequency-grid stability figure; run
                  112 added 1 high-frequency mesh-stability figure
scarep/FDTD cmp:  apples-to-apples inside the BEM-owned ladder through run 016;
                  the project-core FDTD stream remains gated because the
                  factorized homogeneous bridge in run 089 still fails and run
                  090 shows simple alignment does not repair it; run 091 shows
                  the grid-aware scattering path is positive, and run 092
                  captures the reusable adapter contract; run 093 proves the
                  contract can emit a saved adapter payload on the run 089
                  geometry; run 094 passes three fresh homogeneous cases, but
                  this is still not a half-space, field, 3D, full
                  continuous-BEM, or outputs/experiments promotion. Run 095
                  defines the layered payload-smoke contract, and run 096
                  emits the layered payload arrays. Run 097 shows the payload
                  interface survives four fresh layered stress cases, but this
                  is still not a field, 3D, GPU, FWI, or outputs/experiments
                  promotion. Run 098 records that boundary as the current BEM
                  replacement contract.
```

This is environment and geometry-prototype evidence only. It is not yet a
layered GPR forward model, BEM/FDTD validation, measured-field result, or
inversion result.

## Near-Term Queue

1. Use runs `014`-`016` as the BEM/FDTD validation ladder for presentation material.
2. Treat runs `017`-`071` as the project-core bridge sequence. Dense direct-wave
   interpolation is now viable inside the sampled offset range, but it does not
   fix target scattering, and arrival-windowing does not fix direct-wave
   transfer. Effective-wavenumber fitting and simple source-injection variants
   also fail. Run `029` gives a positive finite-domain direct-wave baseline, and
   runs `032`-`033` show that this baseline closes direct/total behavior but
   not target scattering. Run `034` clears gross target geometry. Runs `055`-`057`
   establish a homogeneous boundary-image replacement candidate, but run `058`
   shows that it does not transfer to the layered case. Run `059` shows that
   simple optical/interface image terms do not repair the layered failure. Run
   `060` records the current contract. Run `061` exports the dense layered
   tabulated surface for reuse, and run `062` validates the consumer path. The
   run `063` decimation ladder shows the full 10 mm cache remains the best
   conservative default, while a 7-sample 30 mm grid is a candidate for fresh
   layered stress validation. Run `064` performs that stress test and blocks
   30 mm promotion because the epsr-12 case fails. The immediate next work is a
   run `066` stress test promotes the scalar Sommerfeld proxy to the active
   layered 2D replacement candidate inside the tested project-core envelope.
   Run `067` records the updated replacement contract. Runs `068`-`081` move
   the 3D branch from transition requirements through minimal design, Bempp
   backend proof, matched FDTD comparison contract, and a Bempp point-dipole
   source convention, then paired FDTD target/background manifest templates and
   a template validator, then a frequency-bin comparator preflight and
   synthetic smoke, then strict frequency-bin import templates and an import
   template smoke, then an execution-readiness audit and extractor contract.
   Run `081` adds a synthetic direct-DFT extractor smoke. Run `082` audits the
   candidate execution paths and selects external full-Maxwell 3D FDTD import
   as the preferred next validation-data route; direct ports of the current
   2D CPU/GPU TMz solvers are blocked as longer-term research work. The
   immediate next work is requesting or generating external target/background
   FDTD data that satisfies the run `073` manifest contract, passes run `074`
   validation, fills the run `077` templates via the run `080` extractor
   contract, and satisfies the run `075` comparator schema. Run `083` packages
   that request as two paired runs, seven request artifacts, and seven
   acceptance gates. Run `084` defines the return preflight and currently fails
   because no returned external target/background frequency-bin files exist.
   Run `085` packages the return handoff into two required files, 12 metadata
   fields, eight acceptance steps, and eight gate crosswalk rows so returned
   files can be accepted without ambiguity when they arrive. Run `086` makes
   that metadata handoff executable and currently fails because no metadata
   ledger or hash-verifiable target/background files exist. Run `087` proves the
   metadata gate can pass on a complete synthetic ledger with matching hashes,
   but no real external return has arrived. Run `088` adds the full synthetic
   return-bundle smoke: metadata and frequency-bin return gates both pass, but
   the bundle is synthetic only. Run `089` confirms that the project-core
   homogeneous dielectric bridge is still blocked before the half-space rung,
   and run `090` shows that simple alignment and per-frequency scaling do not
   repair it. Run `091` then replays the same geometry with a project-grid-aware
   discrete Born surrogate and passes at 0.5800814918790829 symmetric L2. Run
   `092` turns that positive path into an eight-item adapter contract. Run
   `093` instantiates the contract and emits the full adapter payload while
   reproducing the run `091` gate. Run `094` stress-tests that reusable adapter
   on three fresh homogeneous cases and all pass below the 0.75 line, with
   worst L2 0.6662947067388982. Run `095` connects that path to the existing
   run `066`/`067` layered Sommerfeld evidence and defines a 12-item layered
   smoke interface. Run `096` emits the actual layered payload arrays and
   passes the base leave-one-scan gate at 0.6497571611891657. Run `097` replays
   that payload interface across four fresh layered stress cases and all pass,
   with worst L2 0.6497571611891657. Run `098` refreshes the BEM replacement
   contract around those payload artifacts: homogeneous and layered local
   2D/project-core payload paths are ready, while field, historical archive,
   3D, GPU, and FWI remain blocked. Run `099` condenses the 3D branch into the
   current external-FDTD decision brief: request artifacts are ready for two
   paired target/background full-Maxwell runs with 248 expected frequency rows,
   and the synthetic return pipeline passes, but no real external FDTD return
   exists. Run `100` converts that decision into a team-facing request packet:
   two paired runs, seven request artifacts, seven acceptance gates, 31
   receivers, four frequencies, 248 expected rows, and a message that preserves
   the no-validation-before-real-return boundary. Run `101` adds sizes and
   SHA-256 hashes for those seven request attachments so the handoff is
   hash-stable. Run `102` packages the seven request attachments, checksums,
   acceptance gates, and return instructions into a portable bundle archive
   with 14 unique members and SHA-256
   `3216f129b340a14502d20ecff6b9785e790afece485e88b80ffdbc58f9ffe86a`.
   Run `103` creates the corresponding external-return inbox layout: two
   required target/background frequency-bin files, 12 metadata fields, four
   intake directories, and no placeholder data. The return layout is ready, but
   real BEM/FDTD comparison, 3D validation, local 3D launch, and GPU/HPC remain
   blocked until real returned files pass the metadata and frequency-bin gates.
   Run `104` makes that return inbox executable as a preflight gate. The gate
   currently has 18 checks, with 1 pass and 17 blocking failures: both required
   real frequency-bin files are absent and the completed 12-field metadata
   ledger is absent. Use run `104` before installing any returned files into
   the pending return root. Run `105` proves the gate can pass on an isolated
   complete synthetic inbox: 18 of 18 preflight checks pass with two synthetic
   frequency-bin files and a matching 12-field metadata ledger. The smoke does
   not change the real blocker; real BEM/FDTD comparison and 3D validation
   remain blocked until run `104` passes on real external returns in the run
   `103` inbox. Run `106` returns to the BEM-side 3D prototype and audits the
   run `072` dipole source under mesh refinement. The baseline `6x16` mesh is
   within 0.010296810068779048 relative L2 of the finer `8x20` mesh and passes
   the bounded mesh-stability gate, so it remains the local 3D Bempp prototype
   baseline. This is still not 3D FDTD validation, layered 3D GPR readiness,
   field FWI readiness, or GPU/HPC readiness. Run `107` then shows that source
   convention is a hard comparison requirement: orientation changes reach
   6.800743917312345 relative L2 and a 15 mm source-height shift reaches
   0.14058934457504094. Future paired 3D FDTD returns must therefore lock or
   report source orientation, source position, and source height explicitly.
   Run `108` shows the receiver side has the same problem: a 15 mm
   receiver-height shift changes the response by roughly 0.10-0.13 relative L2
   and a 30 mm shift reaches 0.19131367619758774. Receiver coordinates, height,
   span, and sample count are now required comparison metadata. Run `109`
   converts those sensitivity results into a strict 13-field return-metadata
   addendum. All 13 strict fields are absent as explicit keys from the current
   return metadata template, so the external-return gate should be updated
   before accepting real FDTD files for BEM comparison. Run `110` makes that
   update executable: the missing real return fails, a synthetic ledger with
   only the old 12 metadata fields fails, and a complete 25-field synthetic
   ledger passes. Real BEM/FDTD comparison and 3D validation remain blocked
   until real returned files pass this upgraded metadata gate and the
   frequency-bin gates. Run `111` audits the locked 3D Bempp dipole prototype
   across nine frequencies from 0.4 to 3.0 GHz. All responses are finite and
   adjacent receiver-line shape changes remain small relative to amplitude
   changes, with max adjacent shape L2 0.06658931539243934. Use this as
   BEM-side frequency-grid and normalization evidence, not as 3D FDTD
   validation. Run `112` then checks high-frequency mesh stability at 2.5 and
   3.0 GHz. The 3.0 GHz 6x16-to-8x20 change reaches
   0.055639649360411644 relative L2, but the 8x20-to-10x24 change drops to
   0.009408458305433572, so high-frequency comparison should use 8x20 or finer
   as the BEM-side reference. Run `113` repeats the full 0.4-3.0 GHz grid on
   the 8x20 fine mesh. All nine responses are finite, the max adjacent shape L2
   is 0.06786245488660995, and the largest 6x16-to-8x20 gap remains at 3.0 GHz,
   so future high-frequency BEM/FDTD comparison should use 8x20 as the BEM-side
   reference mesh. Run `114` refreshes the external FDTD return contract around
   that decision: the original four-bin handoff remains acceptable if real files
   pass all gates, while the preferred full-grid return has nine frequencies and
   558 paired target/background rows. Validation remains blocked until real
   files pass the 25-field metadata ledger and frequency-bin gates. Run `115`
   writes strict target/background CSV templates for that preferred nine-bin
   return: 279 rows per file, 558 paired rows, and 3348 blank complex-field
   cells awaiting real external FDTD values. Run `116` proves the nine-bin
   templates are executable: blank templates are blocked, while deterministic
   synthetic filled target/background files pass schema, key, receiver-position,
   finite-component, and paired-key checks with zero filled-check failures. Run
   `117` exports the fine-mesh BEM side into the same frequency-bin schema:
   279 total-field target rows, 279 incident-field background rows, and 279
   scattered-reference rows. Keys match the run `115` import template, all
   component cells are finite, and total minus background reproduces the
   scattered reference to about `2.3e-12`; real BEM/FDTD comparison remains
   blocked until real external FDTD returns pass the metadata and frequency-bin
   gates. Run `118` uses that fine-mesh reference to run a synthetic
   target/background comparator sensitivity check over all nine frequencies and
   31 receivers: exact reconstruction gives max relative L2
   `8.942279382796571e-15`, a five percent scattered-field scale error passes
   the provisional `0.1` line, and a thirty percent error fails. This verifies
   comparator behavior but remains synthetic only. Run `119` makes the
   preferred nine-bin real-return gate explicit: 279 target rows, 279
   background rows, and a combined 25-field metadata ledger are expected under
   the fine-mesh pending return root. The BEM reference export and synthetic
   sensitivity smoke are ready, but the real target file, background file, and
   metadata ledger are absent, so all real BEM/FDTD comparison and 3D
   validation claims remain blocked. Run `120` updates the preferred return
   metadata template for the fine-mesh branch: the older 25-field ledger is
   extended with five explicit fields for the `8x20` BEM reference mesh, nine
   frequencies, 31 receivers, the scattered-reference SHA-256, and the
   comparator threshold, producing a 30-field fillable ledger for future
   preferred nine-bin returns. Run `121` refreshes the current real-return
   preflight around that 30-field ledger: 29 metadata fields are now
   blocking-required, and the current pending return still fails because the
   real target frequency-bin file, background frequency-bin file, and metadata
   ledger are absent. Run `122` packages the preferred fine-mesh return path
   into a handoff bundle: 14 attachments, three helper files, nine frequencies,
   31 receivers, 279 rows per target/background file, 30 metadata fields, and
   SHA-256
   `a041256e8182db8b5d25e3ad09ffc31a60c59c947ce7a7509f530754f4e942d7`.
   The handoff bundle is ready, but real BEM/FDTD comparison, 3D validation,
   local 3D FDTD launch, GPU/HPC, layered 3D GPR claims, and field FWI remain
   blocked until real returned files pass the run `121` preflight. Run `123`
   verifies that bundle from the consumer side: 17 archive members are
   path-safe, 16 checksum entries pass, 14 attachments and three helper files
   extract correctly, and the archive SHA-256 matches run `122`. The bundle is
   transport-readable, but it still contains templates and BEM references only;
   real BEM/FDTD comparison remains blocked on real returned target,
   background, and metadata files. Run `124` then proves the preferred
   30-field preflight can pass when a complete return is present: a synthetic
   target/background/metadata return passes all 25 blocking checks with nine
   frequencies, 31 receivers, 279 target rows, 279 background rows, and 30
   metadata rows. This validates the gate mechanics only; real BEM/FDTD
   comparison and 3D validation remain blocked until real external FDTD files
   pass the same run `121` gate. Run `125` rechecks the optional scarep GPU MFS
   dependency path: CuPy imports (`14.0.1`) and reports CUDA runtime `12090`,
   but `cupy.linalg.solve` still fails because `libcublas.so.12` is missing.
   This keeps only the optional scarep GPU MFS demo blocked; the validated
   scarep CPU 2D BEM path and the Bempp 3D prototype path remain the active BEM
   routes. Run `126` strengthens the preferred fine-mesh BEM/FDTD comparator by
   auditing 10 schema-valid synthetic mismatch modes. Three scenarios pass as
   expected: exact reconstruction, a five percent scattered-field amplitude
   perturbation, and common-mode target/background bias that cancels under
   subtraction. Seven scenarios fail as expected: large amplitude error,
   high-frequency-localized amplitude error, phase rotation, Ey component sign
   error, receiver-key assignment error, frequency-key assignment error, and
   background-only bias. The audit has zero unexpected outcomes and zero schema
   validation failures, but it remains synthetic; real BEM/FDTD comparison and
   3D validation are still blocked until real returned target, background, and
   metadata files pass the fine-mesh preflight. Run `127` then interprets the
   provisional `0.1` comparator threshold with synthetic sweeps. For the
   fine-mesh reference, global scattered-field amplitude error is bracketed by
   9.5% pass and 10.5% fail, phase rotation is bracketed by 5.7 degrees pass
   and 6.0 degrees fail, and background-only incident-field bias is bracketed
   by `0.0005` pass and `0.001` fail as a fraction of the incident/background
   field. This makes the threshold easier to interpret for future returned
   files, but it remains synthetic and does not unlock real comparison or 3D
   validation. Run `128` audits the fine-mesh scattered-reference norm floor:
   all 279 reference rows are safely above `1e-8`, with minimum scattered norm
   `8.80585591190322` and zero low-norm rows. The per-row relative-L2 metric is
   therefore numerically stable for this reference. The maximum
   background/scatter ratio is `107.16891488389032`, which explains why
   background-only incident-field bias near `0.001` can trip the strict
   threshold. Real returned FDTD files are still required before real
   comparison or 3D validation. Run `129` returns to the colleague-provided
   `scarep` 2D CPU BEM validation and extends the analytic dielectric-cylinder
   scan from 32 to 64 panels. The 64-panel solve reduces complex-spectrum
   relative L2 from `0.0028625612719971973` to `0.0007053747139208214` and
   time-B-scan relative L2 from `0.0021161825095859987` to
   `0.0005202399688500149`, about a `4x` error reduction at `3.48x` wall-time
   cost. This strengthens 2D scarep CPU BEM method-validation evidence, but it
   remains an analytic dielectric-cylinder validation rather than a direct
   comparison to the project FDTD archive. Run `130` fits the run `129`
   8/16/32/64-panel panel sweep: complex-spectrum error order is
   `1.9956212230756902`, time-B-scan error order is `1.9882322328508204`, and
   the wall-time cost exponent is `1.620278753154497`. The 2D scarep CPU BEM
   path therefore has near-second-order convergence on its analytic
   dielectric-cylinder validation case, while project FDTD comparison, 3D
   validation, GPU/HPC, and field FWI remain blocked on matched setups. Run
   `131` synthesizes the 2D BEM validation ladder: scarep analytic convergence,
   matched dielectric BEM/FDTD, matched PEC BEM/FDTD, and matched air/concrete
   half-space PEC BEM/FDTD. All four stages are ready, the best matched
   FDTD/BEM relative L2 is `0.02330746966791303`, and the half-space FDTD/BEM
   relative L2 is `0.030998297443390457`. This is a BEM-side 2D validation
   checkpoint only; project FDTD archive comparison, 3D validation, GPU/HPC,
   and field FWI remain blocked on matched setups or real returned data. Run
   `132` refreshes the bridge decision after that ladder: the BEM-side ladder
   is ready and the project-core direct/background source-normalization check
   passes with relative L2 `0.03170696405248453`, but the project-core
   rebar-scattered transfer remains at symmetric relative L2
   `1.3943651626310445`, about `59.82481936040623x` larger than the best
   matched ladder error. The bridge to project-core FDTD therefore remains
   blocked specifically at the scattered-field adapter, not at BEM method
   validation or direct/background normalization. Run `133` factorizes that
   scattered-field adapter mismatch across sign, global scale, receiver order,
   global time shift, per-receiver time shift, derivative, and integral
   candidates. Simple sign, scale, receiver-order, derivative, and integral
   changes do not repair the mismatch. The best diagnostic candidate is
   per-receiver circular time shift plus scale, which reduces symmetric
   relative L2 from `1.3943651626310445` to `0.24094406788990988`, a
   `5.787090650715443x` improvement, but still misses the `0.1` gate. The
   project-core bridge remains blocked, with the next useful adapter work
   focused on phase convention, source time-origin alignment, and causal
   reconstruction. Run `134` moves that timing clue into the frequency domain:
   per-receiver frequency-linear phase delay plus complex scale improves the
   scattered-field symmetric relative L2 to `0.1866176083623045`, a
   `7.471777046483127x` improvement over baseline, but still misses the `0.1`
   gate. The equivalent delays vary from `1.2604589809231894 ns` near the scan
   center to `2.3108414650258466 ns` near the scan edges, so the issue is not
   one global time-zero offset. The next BEM adapter task is a causal
   source-wavelet and reconstruction contract before rerunning the matched
   project-core bridge. Run `135` packages that contract: direct FDTD
   source-wavelet phase hypotheses do not repair the mismatch, and the best
   evidence remains run `134` with symmetric relative L2 `0.1866176083623045`.
   Four blocking contract items remain open before any interpretable rerun:
   source-wavelet phase convention, per-receiver delay model, causal Hermitian
   reconstruction, and scattered-observable definition. The `0.1` acceptance
   gate is defined, but the project-core BEM/FDTD bridge remains blocked. Run
   `136` adds a synthetic causal-reconstruction smoke guard for that contract:
   the exact per-receiver delay/complex-scale reconstruction passes with
   symmetric relative L2 `0.0`, while missing delay, one global delay, opposite
   phase sign, and receiver reversal all fail the `0.1` scattered-field gate
   with best wrong-contract L2 `0.26554256916978447`. This validates the
   contract mechanics only; real project-core FDTD/BEM comparison, 3D
   validation, GPU/HPC, and field FWI remain blocked. Run `137` audits the
   residual spectrum after the best run `134` per-receiver phase correction:
   the overall spectral relative L2 is `0.18500684021427602`, only one of 17
   frequency bins passes the `0.1` gate, the worst residual is the low-frequency
   edge at `0.6247724137942329 GHz` with relative L2 `0.45939283372879625`, and
   the best bin is `1.3744993103473124 GHz` with relative L2
   `0.0953354196293874`. The next adapter focus is band-edge handling, source
   spectrum conditioning, and observable scaling, not another global phase
   shift. Run `138` checks whether a contiguous frequency window can rescue the
   bridge after phase correction. Only one isolated bin passes the `0.1` gate;
   the best two-bin window is `0.10447496219871069` and the best three-bin
   window is `0.11287493942418508`, so no defensible multi-bin band is ready
   for promotion. Run `139` validates that no-go from the consumer side: seven
   of seven checks pass, the 153-window table has exactly one passing window,
   zero passing multi-bin windows, and the project-core bridge remains blocked.
   Run `140` checks whether that no-go is only a weak-source edge effect by
   filtering contiguous windows across 10 source-amplitude thresholds. It
   evaluates 860 conditioned windows; every threshold still has zero passing
   multi-bin windows, and the best two-bin result remains
   `0.10447496219871069` from `1.3744993103473124` to
   `1.499453793106159 GHz`. Source-amplitude conditioning therefore does not
   change the no-go decision. The next adapter target is observable scaling and
   residual structure rather than simple source-spectrum edge removal. Run
   `141` tests that observable-scaling path directly. Global and per-receiver
   complex scaling do not improve the phase-corrected mismatch, while
   per-frequency scaling lowers the spectral relative L2 to
   `0.1171692949091954` and separable receiver/frequency scaling lowers it to
   `0.117062890994582`. Both remain above the `0.1` gate, so simple observable
   scaling is not enough to promote the project-core bridge. The residual is
   now localized as frequency-structured rather than weak-source or
   receiver-only scaling. Run `142` localizes that residual after the best
   separable scaling: eight of 17 frequency bins pass and three of seven
   receiver rows pass, but the top three frequency bins carry
   `0.3631456510078532` of residual energy and the top three receivers carry
   `0.6414922156373815`. The dominant receiver residuals are receivers `6`,
   `0`, and `3`, and the dominant frequency residuals include
   `1.9992717241415452`, `2.374135172418085`, and
   `0.8746813793119261 GHz`. The next adapter target is frequency-local and
   receiver-local residual structure, not another global scale, global phase,
   or weak-source filter. Run `143` tests receiver-subset sensitivity: the
   full aperture still fails at `0.117062890994582`, dropping only receiver
   `6` still fails at `0.10899321819765909`, but dropping both edge receivers
   `0` and `6` passes narrowly at `0.09909330221470856`. More aggressive
   post-hoc subsets also pass. This confirms receiver-local structure but does
   not promote the bridge because the full aperture fails and the passing
   subsets are chosen after seeing the residual. Run `144` ties that pattern
   to aperture position rather than Tx/Rx offset: all receiver rows have a
   fixed `0.02 m` Tx/Rx offset to numerical precision, while the edge receiver
   pair `0-6` carries `0.4414221920328564` of residual energy and the edge
   pair plus center receiver carries `0.6414922156373816`. The next adapter
   target is aperture-position effects and receiver-edge modeling. Run `145`
   turns that diagnosis into a promotion contract: two items pass
   (post-hoc receiver exclusion remains unpromoted, and aperture localization
   evidence exists), but four blocking items remain. The full aperture still
   fails, no pre-registered edge correction exists, holdout validation is
   missing, and frequency/receiver joint residual closure has not been
   achieved. Receiver-edge correction, receiver exclusion, project-core
   comparison, 3D validation, GPU/HPC, and field FWI remain blocked. Run `146`
   tests one concrete correction family under leave-one-receiver-out
   validation: polynomial complex correction by aperture midpoint. The best
   result is degree `2`, improving the scaled residual from
   `0.117062890994582` to `0.1082856299479433`, with five receiver holdouts
   passing, but the full leave-one-receiver-out metric still misses the `0.1`
   gate and edge holdouts remain problematic. Receiver-position correction
   remains an open adapter problem. Run `147` validates that no-go from the
   consumer side: seven of seven checks pass, degree `2` is confirmed as best,
   no tested degree passes the gate, edge holdouts remain failing, and
   receiver-position correction, project-core comparison, 3D validation,
   GPU/HPC, and field FWI remain blocked.
   Run `148` tests a stricter, symmetry-constrained aperture correction. The
   even-in-aperture-position degree `2` model passes the easier
   leave-one-receiver-out check with spectral relative L2
   `0.06977055235365863` and seven of seven receiver rows passing the `0.1`
   gate. The result does not survive leave-one-symmetry-pair-out validation:
   the best pair-holdout model has spectral relative L2 `0.12895136750102182`,
   only two of four symmetry groups pass, and the edge pair remains too large.
   The correction is useful diagnostically, but project-core comparison, 3D
   validation, GPU/HPC, and field FWI remain blocked until the edge-pair
   holdout closes or a fresh matched case validates the correction.
   Run `149` validates the run `148` decision from saved tables: eight of
   eight checks pass, the best leave-one-receiver-out degree is confirmed as
   `2` with L2 `0.06977055235365863`, the best symmetry-pair holdout degree is
   confirmed as `1` with L2 `0.12895136750102182`, and the edge pair still
   fails. The symmetry correction remains diagnostic only; project-core
   comparison, 3D validation, GPU/HPC, and field FWI remain blocked.
   Run `150` turns that no-go into a calibration-design result. Nine
   pre-registered receiver subsets and 28 model rows are tested. Exactly one
   holdout design passes: `edge_pair_plus_inner_pair`, degree `1`, training on
   receivers `0;2;4;6` and predicting `1;3;5`, with overall relative L2
   `0.06410622276417251` and holdout relative L2 `0.08334442794624965`. No
   design without both edge receivers passes. This identifies the next BEM
   adapter candidate, but it does not promote the project-core bridge; fresh
   matched-case validation is still required before 3D validation, GPU/HPC, or
   field FWI escalation.
   Run `151` validates that candidate from saved tables: eight of eight checks
   pass, exactly one design passes, the passing design is confirmed as
   `edge_pair_plus_inner_pair`, degree `1`, with train receivers `0;2;4;6`,
   holdout receivers `1;3;5`, and holdout relative L2
   `0.08334442794624965`. The candidate is ready for fresh-case validation,
   but project-core bridge promotion, 3D validation, GPU/HPC, and field FWI
   remain blocked.
   Run `152` stress-tests that candidate across frequency. The candidate still
   passes when fit independently at each frequency, but it does not pass
   alternating frequency holdouts: even-train/odd-hold and odd-train/even-hold
   both fail, and only one narrow edge-frequency holdout passes. The candidate
   is therefore a per-frequency adapter candidate, not a frequency-generalized
   bridge. Project-core comparison, 3D validation, GPU/HPC, and field FWI
   remain blocked until frequency generalization or fresh matched-case
   validation closes this gap.
   Run `153` validates that frequency-holdout no-go from saved tables: eight
   of eight checks pass, the direct per-frequency candidate passes, only one
   edge-frequency holdout passes, zero alternating frequency holdouts pass, and
   frequency generalization remains unready. Project-core comparison, 3D
   validation, GPU/HPC, and field FWI remain blocked.
   Run `154` checks whether local coefficient interpolation closes that gap.
   It tests nearest-neighbor and linear interpolation across six frequency
   holdout schemes. Zero of 12 interpolation rows pass; the best
   held-frequency result is still `0.1116397436685101`, above the `0.1` gate,
   and no alternating split passes. The BEM symmetry calibration design remains
   a per-frequency candidate only.
   Run `155` tests smoother coefficient interpolation families: cubic, PCHIP,
   and Akima. Zero of 16 smooth-interpolation rows pass; the best
   held-frequency result is PCHIP on the even-train/odd-hold split at
   `0.1169203875467621`, still above the `0.1` gate. Simple smooth
   interpolation is therefore not enough to make the candidate
   frequency-generalized.
   Run `156` tests whether that no-go is caused by direct real/imaginary
   interpolation or simple phase wrapping. It interpolates correction
   coefficient log-magnitude and unwrapped phase, with and without linear phase
   detrending. Zero of 44 phase/magnitude rows pass; no alternating frequency
   split passes; the best held-frequency result is `0.11704123813863182`, and
   the best alternating split is `0.1225366210060622`. The BEM symmetry
   calibration remains a per-frequency candidate only. The next defensible BEM
   branch is a fresh matched-case validation or a more structural frequency
   model, not another simple coefficient interpolation variant.
   Run `157` applies the original frozen symmetry calibration coefficients to
   the three independent fresh project-core cases saved by run `094`, without
   refitting on those cases. The transfer does not hold: one of three cases is
   a non-regression, zero cases reach the strict `0.1` scattered-field gate,
   and the best frozen transfer L2 is `0.21310977787624946`. Same-case refits
   also fail to improve the fresh cases. This makes the symmetry calibration a
   local diagnostic for the original saved case, not a transferable
   project-core bridge. The next BEM branch should return to a physically
   grounded project-core adapter family rather than extending this
   receiver-position correction line.
   Run `158` tests the simplest physically grounded alternative on the same
   fresh cases: global and per-frequency complex scalar factors fitted only on
   training receivers. No deployable scalar row passes, no deployable scalar
   row improves held-out receivers, and the best deployable holdout result is
   `0.18135484838602173`, slightly worse than baseline. This rules out a
   simple source-amplitude, global phase, or per-frequency scalar explanation
   for the fresh-case mismatch. The next adapter work should focus on
   structural field/operator mismatch.
   Run `159` localizes that structural mismatch on the same three fresh cases.
   Receiver `6` is the largest residual-energy receiver in all three cases,
   the worst case is `shifted_deeper_epsr4` with L2 `0.5997321402926066`, and
   the top five frequency bins carry at least `0.6363043457279565` of residual
   energy in every case. This points the next BEM adapter branch toward
   receiver-edge and frequency-local operator mismatch on fresh cases, while
   the project-core bridge, 3D validation, GPU/HPC, and field FWI remain
   blocked.
   Run `160` checks whether that receiver-edge finding can be handled by
   excluding receiver `6` or both edge receivers. Exclusion lowers some errors
   but does not close the gate: zero deployable subsets pass, and the worst
   best subset remains `0.5439481056909283` on `shifted_deeper_epsr4`.
   Receiver exclusion is therefore diagnostic only. The next branch should
   model receiver-edge/frequency-local operator mismatch rather than dropping
   receivers, and project-core bridge promotion remains blocked.
   Run `161` performs the matching frequency-exclusion sensitivity. Dropping
   the largest residual-frequency bins reduces errors, but still produces zero
   strict-gate passes. Even after dropping the top eight residual bins, the
   worst best fresh case remains `0.518283007674826`. Frequency exclusion is
   therefore also diagnostic only; the next branch should model frequency-local
   operator mismatch rather than trim bands.
   Run `162` tests the matching empirical cross-case correction idea. It fits
   receiver-frequency, receiver-only, and frequency-only complex scale factors
   on two fresh cases and evaluates the third held-out case. Zero of nine
   leave-one-case-out rows pass the strict gate. Receiver-frequency scaling
   overfits, frequency-only scaling is neutral, and the best worst-case result
   remains `0.5984793935748264` on `shifted_deeper_epsr4`. The project-core
   bridge remains blocked; the next BEM branch needs a physics/geometry
   operator change, not an empirical scale table.
   Run `163` tests a more constrained physical timing hypothesis: global,
   receiver-specific, and linear receiver-delay phase ramps fitted on two fresh
   cases and evaluated on the held-out third case. Zero of nine rows pass the
   strict gate. Global delay is neutral, receiver-specific delays slightly
   improve only `shifted_deeper_epsr4`, and the best worst-case result remains
   `0.5924545602816863`. This rules out a pure timing-delay phase ramp as the
   project-core bridge fix; the next operator change should target
   geometry/material Green-function structure or source/receiver aperture
   modeling.
   Run `164` recomputes the fresh-case project-core adapter with five
   target-cell weight discretizations. Binary or uniform target-cell weighting
   gives small improvements in all three cases, but no improvement reaches
   `0.01` relative L2 and zero rows pass the strict gate. The worst best case
   remains `0.5987298321189344` on `shifted_deeper_epsr4`. Target-cell
   discretization alone is not the missing operator change; Green-function
   structure, material/interface modeling, or source/receiver aperture effects
   remain the next BEM priorities.
   Run `165` tests one of those aperture candidates directly by recomputing
   the fresh-case adapter with binary target weights and a three-point 5 mm
   lateral source/receiver aperture average. The aperture average slightly
   improves two cases, slightly regresses one case, and still produces zero
   strict-gate passes. The best worst-case result is `0.598056418177049`.
   A simple lateral aperture average is not enough; a more faithful antenna
   model or Green-function/interface update is required before project-core
   bridge promotion.
   Run `166` synthesizes the fresh-case operator branch from runs `159`-`165`.
   Seven branch labels across three fresh cases produce zero strict-gate
   passes. Even the best diagnostic branch, frequency exclusion, leaves the
   worst case at `0.518283007674826`; the best physical operator branch leaves
   the worst case at `0.5924545602816863`. Treat the current local operator
   tweaks as exhausted for bridge promotion. The next BEM priority is
   Green-function/interface physics, material modeling, or a more faithful
   antenna model, not another local scale, delay, weight, aperture, or trimming
   variant.
   Run `167` turns that no-go into a transition contract. The BEM path now
   splits into a primary Green-function/interface physics branch, a scoped
   layered 2D payload branch that remains ready only inside its tested gates,
   and a parallel external 3D FDTD return-acquisition branch. Three tracks are
   scoped-ready, but real external 3D FDTD data are still absent and project-
   core bridge promotion, 3D validation, GPU/HPC, and field FWI remain blocked.
   Run `168` defines the next extended layered payload stress ladder with four
   cases: shallower target, larger target radius, lower target contrast, and
   stronger lower-halfspace contrast. The design is ready for execution, but it
   does not promote any broader layered, field, 3D, GPU/HPC, or field-FWI
   claim.
   Run `169` executes that extended layered stress ladder. Three of four rows
   pass, but the larger-radius case fails the `0.75` leave-one-scan gate at
   `0.7745663063852277`. The low-contrast case is also degenerate because the
   target permittivity equals the lower-halfspace permittivity, producing zero
   target cells. Do not promote the layered payload beyond the previous scoped
   stress boundary; repair the extended design before drawing a broader layered
   conclusion.
   Run `170` repairs that degenerate low-contrast design by changing the target
   permittivity to `epsr=7.5` while keeping the lower-halfspace at `epsr=6.0`.
   The repaired case has 533 target cells and a nonzero permittivity contrast of
   `1.5`, so it is ready for execution. This does not repair the larger-radius
   failure from run `169`, and it does not promote the layered payload,
   project-core bridge, 3D validation, GPU/HPC, field transfer, or field FWI.
   Run `171` executes the repaired low-contrast case. The corrected row has 533
   target cells and passes the `0.75` leave-one-scan gate with L2
   `0.6672239886633535`. This replaces the degenerate low-contrast evidence row
   from run `169`, but it still does not promote the extended layered ladder
   because the larger-radius case from run `169` remains failed at
   `0.7745663063852277`.
   Run `172` synthesizes the corrected extended ladder by combining run `169`
   rows with the repaired low-contrast row from run `171`. The corrected ladder
   has no zero-target-cell cases, but still passes only three of four rows. The
   remaining blocker is now localized to the larger-radius case at L2
   `0.7745663063852277`, so the next BEM branch should target larger-radius
   support/modeling rather than low contrast.
   Run `173` sweeps the target radius from 25 mm to 35 mm using the same
   grid-aware layered payload adapter. The adapter passes through 32.5 mm
   radius, with leave-one L2 `0.7137722378850567`, and fails only at 35 mm with
   leave-one L2 `0.7745663063852277`. The larger-radius issue is therefore a
   near-boundary larger-footprint generalization problem. Do not promote the
   extended ladder; target a 35 mm support/modeling repair next.
   Run `174` tests that repair direction by replacing full-volume target support
   with outer-shell target support on the 35 mm case. The best shell, 10 mm
   thick, improves leave-one L2 from `0.7745663063852277` to
   `0.7503674453090535`, but still misses the `0.75` gate by
   `0.0003674453090535`. Shell support is the right direction, but the coarse
   shell ladder is not enough for promotion; refine the 8-12 mm shell region.
   Run `175` refines that shell-support branch at 1 mm resolution from 8 mm to
   14 mm. The 11 mm and 12 mm shells pass; the best row is `outer_shell_11mm`,
   with 574 active target cells and leave-one L2 `0.7443538860706249`. This
   closes the 35 mm larger-radius gate for the tested case, but the repair must
   still be synthesized into the corrected extended ladder before any layered
   payload claim is refreshed.
   Run `176` performs that synthesis. Replacing the failed 35 mm full-volume
   row with the run `175` 11 mm shell-support row makes the corrected extended
   ladder pass four of four cases. The worst row remains the 35 mm
   larger-radius case, now at L2 `0.7443538860706249` below the `0.75` gate.
   This is a scoped layered-payload success and is ready for a tracked layered
   contract refresh, while field transfer, 3D validation, GPU/HPC, field FWI,
   and synthetic `outputs/experiments` promotion remain blocked.
   Run `177` records that tracked contract refresh. The accepted scope is local
   2D project-core air/concrete layered dielectric payload cases with
   leave-one-scan relative L2 `<= 0.75`, full-volume target support for standard
   25 mm targets, and 11 mm outer-shell support for the 35 mm larger-radius
   target. The refreshed contract passes four of four cases; field transfer,
   3D validation, GPU/HPC escalation, field FWI, and synthetic
   `outputs/experiments` promotion remain explicitly blocked.
   Run `178` independently checks the 11 mm shell-support rule on four
   neighboring 35 mm holdout cases: left shift, right shift, shallower, and
   deeper targets. All four shell rows pass, with worst shell L2
   `0.7200480775878574`. Full-volume support also passes all four holdouts,
   so the original centered 35 mm failure is a specific near-boundary case, not
   a broad collapse of all nearby 35 mm geometries. The shell repair is
   independently supported for this small holdout set, but field transfer, 3D
   validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `179` refreshes the scoped contract with the run `178` holdout evidence.
   The holdout-augmented contract now has eight passing rows: the original four
   accepted contract cases plus four neighboring 35 mm shell-support holdouts.
   The worst row is still the original larger-radius case at L2
   `0.7443538860706249`, below the `0.75` gate. This strengthens the local 2D
   BEM/FDTD layered-payload evidence, while field transfer, 3D validation,
   GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion remain
   blocked.
   Run `180` adds material/interface holdouts for the 35 mm shell-support rule:
   low target contrast, high target contrast, and stronger lower-halfspace
   contrast. All three 11 mm shell rows pass, with worst shell L2
   `0.7109170307749919`, and all three improve relative to full-volume support.
   This strengthens the shell-support evidence beyond geometric shifts, while
   field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
   `outputs/experiments` promotion remain blocked.
   Run `181` synthesizes the current validated shell-support contract. The
   evidence set now contains 11 passing local 2D BEM/FDTD rows: four original
   contract rows, four geometric holdouts, and three material/interface
   holdouts. The worst row remains `larger_radius_epsr9` at L2
   `0.7443538860706249`. This is the current validated local 2D BEM layered-
   payload contract, while field transfer, 3D validation, GPU/HPC, field FWI,
   and synthetic `outputs/experiments` promotion remain blocked.
   Run `182` validates that contract from a downstream consumer perspective.
   It performs nine consistency checks against the run `181` case table and
   summary: total rows, all-ready status, contract/geometry/material holdout
   counts, worst L2 gate, source contract readiness, and blocked field/3D/GPU
   promotion flags. All nine checks pass with zero blocking failures, so run
   `181` is consumer-ready as a
   local 2D BEM/FDTD layered-payload contract. This does not add new physics
   evidence and does not unblock field transfer, 3D validation, GPU/HPC, field
   FWI, or synthetic `outputs/experiments` promotion.
   Run `183` adds negative-control sensitivity around the run `182` validator.
   It accepts the exact run `181` contract and rejects nine intentionally
   damaged variants: missing rows, not-ready rows, count mismatch, above-gate
   L2, false source readiness, and incorrect field/3D/GPU/FWI promotion flags.
   There are zero unexpected outcomes. Runs `181`-`183` are therefore the
   current validated local 2D BEM shell-support contract package, while field
   transfer, 3D validation, GPU/HPC, field FWI, and synthetic
   `outputs/experiments` promotion remain blocked.
   Run `184` audits the acceptance margins across the 11 accepted contract
   rows. The contract is valid but narrow: one case is within the tight-margin
   band. The limiting row is `larger_radius_epsr9` with 11 mm outer-shell
   support, leave-one L2 `0.7443538860706249`, and only
   `0.005646113929375085` L2 margin below the `0.75` gate. The next BEM branch
   should stress this larger-radius shell case before any claim widening, field
   transfer, 3D validation, GPU/HPC, field FWI, or synthetic
   `outputs/experiments` promotion.
   Run `185` performs that targeted stress with shell thicknesses from
   10.00 mm to 12.00 mm in 0.25 mm steps. The best row remains the 11.00 mm
   outer shell at leave-one L2 `0.7443538860706249`, so sub-millimeter shell
   tuning does not improve the contract boundary. Six of nine shell supports
   pass, and repeated active-cell counts show grid quantization in the support
   masks. Keep the run `181` 11 mm shell row as the boundary case; the next BEM
   stress should target model/grid behavior rather than sub-grid shell tuning.
   Run `186` performs that model/grid stress by applying +/-2.5 mm target-center
   offsets around the 35 mm larger-radius case. The 11 mm shell passes four of
   five offset cases but fails the deeper `z_plus_2p5mm` case at leave-one L2
   `0.7549628470028724`, above the `0.75` gate. The shallower `z_minus_2p5mm`
   case improves to `0.734539466050683`. This localizes the next BEM blocker to
   depth-sensitive model/grid behavior. Do not widen the shell-support contract;
   target the deeper 35 mm offset next while keeping field transfer, 3D
   validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion blocked.
   Run `187` tests whether thicker shells repair that deeper `z_plus_2p5mm`
   failure. They do not: zero of nine support modes pass, the best row remains
   the original 11 mm shell at leave-one L2 `0.7549628470028724`, and thicker
   shells worsen the fit. The deeper +2.5 mm case is therefore a known local 2D
   BEM shell-support failure. The next BEM repair must change model/grid
   treatment rather than shell thickness alone, and field transfer, 3D
   validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `188` synthesizes that boundary. The accepted shell-support contract
   remains the 11-case run `181` local 2D result, while the deeper
   `z_plus_2p5mm` case is recorded as an explicit known depth-offset failure:
   L2 `0.7549628470028724`, margin `-0.004962847002872417`, and zero ready
   repair supports from run `187`. The shell-support rule is not depth-robust
   for 35 mm larger-radius targets. Do not widen the claim, transfer to field,
   launch 3D/GPU work, or promote to synthetic `outputs/experiments` evidence
   from this BEM branch.
   Run `189` validates that boundary from a consumer perspective. Eight of
   eight checks pass: 11 scoped accepted contract cases, five sub-cell shell
   cases, the `z_plus_2p5mm` known failure, its negative margin, zero ready
   repair supports, blocked depth-robust rule, ready boundary synthesis, and
   blocked field/3D/GPU states. Use run `188` as the depth-boundary synthesis
   and run `189` as its validator.
   Run `190` stress-tests that validator. The exact boundary passes, while
   eight damaged variants fail as expected: missing known failure, positive
   failure margin, repair support marked ready, depth-robust rule marked ready,
   boundary synthesis not ready, field transfer marked ready, accepted-contract
   count drift, and sub-cell count drift. There are zero unexpected outcomes.
   Use runs `188`-`190` as the current BEM shell-support depth-boundary guard
   package.
   Run `191` tests radial target-weight profiles for the same known deeper
   failure. Weighting improves the failure but does not close it: the best row
   is `outer_shell_18mm_linear_radial` at leave-one L2
   `0.7525645647728268`, an improvement of `0.0023982822300455675` over the
   binary 11 mm shell but still above the `0.75` gate. Do not refresh the
   shell-support contract from radial weighting alone; the next repair must
   change model/grid treatment more substantially.
   Run `192` tests that model/grid hypothesis by changing subcell
   rasterization density for the same deeper `z_plus_2p5mm` failure. It checks
   five subcell sample counts and three support modes, including the best radial
   shell from run `191`. Zero of fifteen rows pass. The best row remains the
   default five-sample `outer_shell_18mm_linear_radial` case at leave-one L2
   `0.7525645647728268`, with margin `-0.0025645647728268495`. This narrows the
   blocker away from target rasterization alone; the next repair should target
   the operator/source model or Green-surface representation. Field transfer,
   3D validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `193` tests that operator/source-model hypothesis on the same fixed
   support. It evaluates 108 layer-aware basis variants using optical path,
   direct air/concrete, interface-reflected, and cardinal image terms. Zero
   variants pass, and the best leave-one L2 is `0.9606924830049194`, worse than
   the run `192` Sommerfeld transmitted-surface baseline
   `0.7525645647728268`. This rules out the low-order image/optical-path basis
   as the deeper-offset repair. The next credible BEM branch should target a
   true layered Green function or a denser tabulated FDTD field-surface model.
   Field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
   `outputs/experiments` promotion remain blocked.
   Run `194` tests the denser tabulated FDTD field-surface branch on the same
   fixed deeper-offset support. This is the first branch that closes the gate:
   the 10 mm plus exact policy reaches leave-one L2 `0.6131125861743153`, and
   the 5 mm plus exact policy reaches `0.5654888528068279`. The minimum ready
   sample count is 19, and the best row improves over the run `192` Sommerfeld
   transmitted-surface baseline by `0.18707571196599893` L2. The exact
   source/receiver-only policy fails because held-out source/receiver points
   require extrapolation. Treat run `194` as a practical tabulated-surface
   repair candidate and upper-bound diagnostic, not as an analytic BEM contract
   refresh. It needs validator and sensitivity guards before any claim refresh;
   field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
   `outputs/experiments` promotion remain blocked.
   Run `195` validates the run `194` candidate from a consumer perspective.
   Eleven of eleven checks pass with zero blocking failures: policy counts,
   ready counts, exact-only failure with extrapolation, 10 mm dense readiness
   without extrapolation, 5 mm dense best-and-ready status, best L2 consistency,
   below-gate L2, improvement over the Sommerfeld baseline, minimum ready sample
   count 19, blocked contract refresh, and blocked field/3D/GPU/FWI states.
   Use run `195` as the validator for the tabulated-surface repair candidate;
   negative-control sensitivity is still required before any claim refresh.
   Run `196` stress-tests that validator. The exact run `194` result passes,
   while nine damaged variants fail as expected: missing dense 5 mm policy,
   exact-only policy marked ready, exact-only extrapolation removed, dense
   10 mm policy marked not ready, dense 10 mm policy marked extrapolated,
   above-gate summary L2, no Sommerfeld improvement, contract refresh marked
   ready, and field transfer marked ready. There are zero unexpected outcomes.
   Use runs `194-196` as the current guarded tabulated-surface repair package.
   Analytic contract refresh, field transfer, 3D validation, GPU/HPC, field FWI,
   and synthetic `outputs/experiments` promotion remain blocked until
   generalization is tested.
   Run `197` performs that generalization test across the five 35 mm
   subcell-offset cases from run `186`, using the 10 mm plus exact tabulated
   surface policy and testing full-volume, 11 mm binary shell, and 18 mm radial
   shell supports. All five cases have at least one ready support, with 11 of
   15 rows ready. The worst best-case row is `z_minus_2p5mm` with 11 mm binary
   shell support at leave-one L2 `0.650662226077945`, giving a margin of
   `0.099337773922055` below the `0.75` gate. Treat this as a candidate
   generalized tabulated-surface repair across the 35 mm offset family, not as
   an analytic BEM contract refresh. Validator and sensitivity guards are still
   required before any claim refresh; field transfer, 3D validation, GPU/HPC,
   field FWI, and synthetic `outputs/experiments` promotion remain blocked.
   Run `198` validates the run `197` generalized repair from a consumer
   perspective. Eleven of eleven checks pass with zero blocking failures:
   offset case count, support mode count, support row count, ready row count,
   every case having a ready best support, zero held-out extrapolation, worst
   best-case identity, worst best-case L2 below gate, positive worst-case margin,
   blocked contract refresh, and blocked field/3D/GPU/FWI states. Use run `198`
   as the validator for the generalized tabulated-surface repair; negative-
   control sensitivity is still required before any claim refresh.
   Run `199` stress-tests that validator. The exact run `197` result passes,
   while nine damaged variants fail as expected: missing offset case, case
   without ready support, held-out extrapolation present, wrong worst best case,
   worst best L2 above gate, negative worst best margin, generalization marked
   not ready, contract refresh marked ready, and field transfer marked ready.
   There are zero unexpected outcomes. Use runs `197-199` as the guarded
   generalized tabulated-surface repair package for the 35 mm offset family.
   Analytic contract refresh, field transfer, 3D validation, GPU/HPC, field FWI,
   and synthetic `outputs/experiments` promotion remain blocked until scope and
   claim language are refreshed deliberately.
   Run `200` synthesizes the current claim boundary. Three claims are ready:
   the scoped analytic shell-support contract, the guarded single-case
   tabulated-surface repair, and the guarded offset-family tabulated-surface
   repair. Two claims remain blocked: a depth-robust analytic shell rule and an
   analytic BEM replacement for the tabulated surface. The offset-family
   tabulated repair covers five local 2D 35 mm offset cases with worst best-case
   L2 `0.650662226077945` and margin `0.099337773922055`, but it is not field
   transfer, 3D validation, GPU/HPC, field FWI, or synthetic
   `outputs/experiments` promotion. Use run `200` as the current BEM
   claim-boundary synthesis and validate it before presentation/report use.
   Run `201` validates that claim-boundary synthesis from a consumer
   perspective. Eight of eight checks pass with zero blocking failures: claim
   count, ready/blocked counts, offset-family tabulated repair ready with
   positive margin, depth-robust analytic shell rule blocked with negative
   margin, analytic replacement claim blocked, synthesis-ready flag, analytic
   contract refresh blocked, and field/3D/GPU/FWI states blocked. Use run `201`
   as the validator for BEM claim-boundary language; negative-control
   sensitivity remains the next guard before using the synthesis in a report or
   presentation source.
   Run `202` stress-tests that validator. The exact claim-boundary synthesis
   passes, while nine damaged variants fail as expected: missing offset-family
   claim, offset-family claim marked blocked, offset-family negative margin,
   depth-robust analytic shell rule marked ready, depth-robust positive margin,
   analytic replacement marked ready, synthesis marked not ready, analytic
   contract refresh marked ready, and field transfer marked ready. There are
   zero unexpected outcomes. Use runs `200`-`202` as the guarded BEM
   claim-boundary package. The supported claim remains a scoped analytic
   shell-support contract plus guarded tabulated-surface repair for the tested
   35 mm offset family; analytic replacement, field transfer, 3D validation,
   GPU/HPC readiness, field FWI readiness, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `203` measures the surface-sample density boundary for that guarded
   tabulated-surface repair. Exact source/receiver-only and 20 mm plus exact
   policies fail across the five 35 mm offset cases. The 15 mm, 10 mm, and
   5 mm plus exact policies all pass every offset case. The cheapest all-case
   ready policy by actual sample count is 10 mm plus exact with 19 samples and
   worst best-case leave-one L2 `0.650662226077945`, margin
   `0.099337773922055`. The 15 mm grid is coarser but uses 23 samples after
   exact point insertion, while 5 mm gives the best observed L2 at 37 samples.
   Use 10 mm plus exact as the current practical tabulated-surface spacing;
   validator and sensitivity guards remain the next step before promoting this
   density boundary into downstream contract language.
   Run `204` validates that density boundary from a consumer perspective.
   Eleven of eleven checks pass with zero blocking failures: support/policy row
   count, case/support/policy counts, exact-only failure with held-out
   extrapolation, 20 mm boundary failure, 15 mm readiness without lower sample
   count than 10 mm, 10 mm as the minimum all-case-ready policy, 5 mm as the
   best observed accuracy reference, no lower-sample all-case-ready policy
   beating 10 mm, density-boundary readiness, blocked analytic refresh, and
   blocked field/3D/GPU/FWI states. Use run `204` as the validator for run
   `203`; negative-control sensitivity remains the next guard.
   Run `205` stress-tests that validator. The exact density-boundary result
   passes, while ten damaged variants fail as expected: missing 10 mm policy
   summary, support/policy row-count drift, exact policy marked ready, 20 mm
   policy promoted, 15 mm sample relation broken, minimum policy changed away
   from 10 mm, lower-sample policy marked ready, density boundary marked not
   ready, analytic contract refresh marked ready, and field transfer marked
   ready. There are zero unexpected outcomes. Use runs `203`-`205` as the
   guarded BEM tabulated-surface density-boundary package; the practical policy
   remains 10 mm plus exact, and analytic replacement, field transfer, 3D
   validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `206` performs the follow-on grid-only ablation. It shows that exact
   source/receiver point insertion is not required for the tested five-case
   35 mm offset family. The cheapest all-case-ready policy is now
   `grid_15mm_only`: 13 samples, worst best-case leave-one L2
   `0.6083307089797199`, margin `0.14166929102028014`. The previous practical
   10 mm plus-exact policy also passes but uses 19 samples; 5 mm grid-only
   gives the best observed L2 at 37 samples; 20 mm grid-only and 20 mm
   plus-exact both fail. Treat 15 mm grid-only as the current practical
   tabulated-surface policy for this tested family, pending validator and
   sensitivity guards. Analytic replacement, field transfer, 3D validation,
   GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion remain
   blocked.
   Run `207` validates that grid-only ablation from a consumer perspective.
   Thirteen of thirteen checks pass with zero blocking failures: row count,
   case/support/policy counts, 20 mm grid-only failure, 20 mm plus-exact
   failure, 15 mm grid-only as the cheapest ready policy, no exact insertion
   in the 15 mm grid-only policy, 15 mm plus-exact readiness at higher sample
   count, 10 mm plus-exact as a higher-sample ready baseline, 5 mm grid-only
   as the best accuracy reference, lower-sample readiness relative to 10 mm
   plus-exact, ablation-ready state, blocked analytic refresh, and blocked
   field/3D/GPU/FWI states. Use run `207` as the validator for run `206`;
   negative-control sensitivity remains the next guard before refreshing claim
   language around 15 mm grid-only.
   Run `208` stress-tests that validator. The exact grid-only ablation passes,
   while twelve damaged variants fail as expected: missing 15 mm grid-only
   policy, support/policy row-count drift, 20 mm grid-only promotion, 20 mm
   plus-exact promotion, 15 mm grid-only marked not ready, 15 mm grid-only
   marked exact-inserted, 15 mm grid-only sample-count drift, cheapest policy
   changed away from grid 15 mm, lower-sample readiness removed, ablation marked
   not ready, analytic contract refresh marked ready, and field transfer marked
   ready. There are zero unexpected outcomes. Use runs `206`-`208` as the
   guarded BEM grid-only tabulated-surface package. The practical policy for
   the tested family is 15 mm grid-only; analytic replacement, field transfer,
   3D validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
   promotion remain blocked.
   Run `209` refreshes the BEM claim boundary around that guarded result. It
   records six claims: two ready and four blocked. The recommended practical
   claim is `grid15_tabulated_surface_offset_repair`, using `grid_15mm_only`
   with 13 samples, worst best-case leave-one L2 `0.6083307089797199`, and
   margin `0.14166929102028014`. This supersedes the previous 10 mm plus-exact
   practical policy. The scoped analytic shell-support claim remains ready only
   in its validated scope; 20 mm grid-only, depth-robust analytic shell,
   analytic replacement, field transfer, 3D validation, GPU/HPC, field FWI, and
   synthetic `outputs/experiments` promotion remain blocked. Validate and
   stress-test this refreshed boundary before using it downstream.
   Run `210` validates that refreshed boundary from a consumer perspective.
   Thirteen of thirteen checks pass with zero blocking failures: claim count,
   ready/blocked counts, single recommended practical policy, 15 mm grid-only
   ready with positive margin, 20 mm grid-only blocked with negative margin,
   scoped analytic shell support still ready, depth-robust analytic shell rule
   blocked, analytic replacement blocked, field transfer blocked, previous
   10 mm plus-exact policy superseded, claim-boundary refresh ready, analytic
   refresh blocked, and field/3D/GPU/FWI states blocked. Use run `210` as the
   validator for run `209`; negative-control sensitivity remains the next guard.
   Run `211` stress-tests that validator. The exact refreshed claim boundary
   passes, while thirteen damaged variants fail as expected: missing 15 mm
   grid claim, multiple recommended claims, grid15 marked blocked, grid15
   negative margin, grid20 marked ready, analytic shell marked not ready,
   depth-robust marked ready, analytic replacement marked ready, field transfer
   claim marked ready, previous 10 mm policy not superseded, claim boundary
   marked not ready, analytic contract refresh marked ready, and field transfer
   marked ready. There are zero unexpected outcomes. Use runs `209`-`211` as
   the guarded refreshed BEM claim-boundary package. The practical claim is
   15 mm grid-only for the tested 35 mm offset family; analytic replacement,
   field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
   `outputs/experiments` promotion remain blocked.
   Run `212` makes the support-mode choice explicit for that 15 mm grid-only
   policy. Both shell support modes pass all five tested cases, but
   `outer_shell_11mm_binary` has the lower worst-case leave-one L2
   (`0.6083307089797199`) than `outer_shell_18mm_linear_radial`
   (`0.6160940767643346`). Volume support passes only one of five cases. Use
   `grid_15mm_only` with `outer_shell_11mm_binary` as the current fixed
   support-mode contract for the tested 35 mm offset family. Analytic
   replacement, field transfer, 3D validation, GPU/HPC, field FWI, and
   synthetic `outputs/experiments` promotion remain blocked.
   Run `213` validates that support-mode contract from a consumer perspective.
   Nine of nine checks pass with zero blocking failures: grid-15 policy,
   five cases and 13 samples, two ready shell modes, `outer_shell_11mm_binary`
   recommendation, positive margin, volume support rejected, no per-case router,
   support-contract readiness, and blocked field/3D/GPU/FWI states. Negative-
   control sensitivity remains required before folding this into refreshed BEM
   claim language.
   Run `214` stress-tests that validator. The exact support contract passes,
   while fourteen damaged variants fail as expected: wrong surface policy,
   wrong case count, wrong sample count, only one ready shell mode, shell-18 not
   ready, wrong recommended support, negative margin, L2 above gate, volume
   support promoted, volume ready count drift, per-case router required,
   contract not ready, field transfer ready, and GPU ready. There are zero
   unexpected outcomes. Use runs `212`-`214` as the guarded BEM grid-15
   support-mode contract: `grid_15mm_only` with
   `outer_shell_11mm_binary`, 13 samples, scoped to the tested local 2D 35 mm
   offset family. Analytic replacement, field transfer, 3D validation, GPU/HPC,
   field FWI, and synthetic `outputs/experiments` promotion remain blocked.
   Run `215` refreshes the BEM claim boundary with that support-specific
   contract. The recommended practical claim is now
   `grid15_shell11_tabulated_surface_offset_repair`: `grid_15mm_only` with
   `outer_shell_11mm_binary`, 13 samples, worst leave-one L2
   `0.6083307089797199`, and margin `0.14166929102028014`. Shell-18 remains a
   guarded alternative but is not recommended; volume support and a per-case
   support router are blocked. Field transfer, 3D validation, GPU/HPC, field
   FWI, analytic replacement, and synthetic `outputs/experiments` promotion
   remain blocked. Validate and stress-test this refreshed boundary before
   using it downstream.
   Run `216` validates the run `215` support-specific claim boundary. Nine of
   nine checks pass with zero blocking failures: claim counts, single
   shell-11 recommendation, recommended metrics, shell-18 alternative not
   recommended, volume support blocked, per-case router blocked, field transfer
   blocked, boundary refresh ready, and blocked field/3D/GPU/FWI states.
   Negative-control sensitivity remains required before treating the refreshed
   boundary as fully guarded.
   Run `217` stress-tests that validator. The exact support-specific boundary
   passes, while thirteen damaged variants fail as expected: claim-count drift,
   missing recommended policy, multiple recommended policies, wrong support
   mode, negative recommended margin, shell-18 not ready, volume marked ready,
   volume positive margin, router marked ready, field claim marked ready,
   boundary not ready, field-transfer summary ready, and GPU summary ready.
   There are zero unexpected outcomes. Use runs `215`-`217` as the guarded
   support-specific BEM claim-boundary package. The supported practical claim is
   `grid_15mm_only` plus `outer_shell_11mm_binary`, 13 samples, worst
   leave-one L2 `0.6083307089797199`, and margin
   `0.14166929102028014`, scoped to the tested local 2D 35 mm offset family.
   Run `218` audits whether that guarded 2D support-specific claim can change
   the 3D FDTD validation path. It finds four ready or handoff-ready items and
   six direct-promotion blockers. The 2D support claim is guarded, and the 3D
   external-return pipeline remains handoff-ready, but dimensionality/unknowns,
   source convention, medium model, observable contract, absent real 3D FDTD
   data, and field transfer block direct 2D-to-3D promotion. Keep the 2D
   support claim and the 3D external-return gate separate.
   Run `219` validates that alignment audit from a consumer perspective. Eight
   of eight checks pass with zero blocking failures, confirming the 10-item
   alignment table, the guarded but bounded 2D support claim, the six named
   direct-promotion blockers, the handoff-ready external-return route, absent
   real 3D FDTD data, and blocked downstream states. Negative-control
   sensitivity remains required before treating the alignment boundary as fully
   guarded.
   Run `220` stress-tests that validator. The exact alignment boundary passes,
   while 18 damaged variants fail as expected for count drift, 2D-support
   policy drift, removed direct-promotion blockers, external request readiness
   drift, synthetic-return smoke drift, real-data status drift, direct
   promotion, real comparison readiness, 3D validation readiness, field
   transfer, GPU readiness, field FWI readiness, and a next-action contract
   change. There are zero unexpected outcomes. Use runs `218`-`220` as the
   guarded BEM 2D-support to 3D-FDTD alignment package.
   Run `221` quantifies the surface-sample budget for the guarded
   tabulated-surface policy. The recommended policy remains `grid_15mm_only`
   with `outer_shell_11mm_binary`: 13 samples, worst leave-one L2
   `0.6083307089797199`, and 31.579% fewer samples than the previous
   `dense_10mm_plus_exact` baseline. The 5 mm grid-only policy costs 37
   samples for a modest worst-case L2 gain of about `0.016591770790743476`.
   Use this as the bounded tabulation scaling policy for the tested local 2D
   35 mm offset family; do not promote inversion-scale half-space BEM, field
   transfer, 3D validation, GPU work, or field FWI from this audit.
   Run `222` validates that scaling audit from a consumer perspective. Eight of
   eight checks pass with zero blocking failures, confirming the policy and
   budget row counts, the recommended 13-sample `grid_15mm_only` policy with
   `outer_shell_11mm_binary`, positive savings against the 19-sample baseline,
   positive acceptance margin, 5 mm fine-grid cost/gain tradeoff,
   candidate-count scaling, and blocked downstream states. Sensitivity remains
   required before treating this scaling boundary as fully guarded.
   Run `223` stress-tests that validator. The exact scaling boundary passes,
   while 20 damaged variants fail as expected for policy-count drift,
   budget-count drift, recommendation policy/support drift, grid15 sample count
   or readiness drift, baseline sample/savings drift, recommended L2 or margin
   drift, 5 mm fine-grid cost/gain drift, candidate-budget scaling drift,
   scaling-policy readiness drift, half-space promotion, field transfer, 3D
   validation, GPU readiness, and field-FWI readiness. There are zero
   unexpected outcomes. Use runs `221`-`223` as the guarded BEM
   tabulated-surface scaling budget package.
   Run `224` rechecks and prioritizes the optional `scarep` GPU MFS CUDA/cuBLAS
   dependency. CuPy import and CUDA runtime pass, but `cupy.linalg.solve` still
   fails with `ImportError: libcublas.so.12`. This blocks only the optional GPU
   MFS demo path. The validated `scarep` CPU BEM path, Bempp 3D reference path,
   and guarded tabulated-surface work remain unblocked. Do not prioritize
   CUDA/cuBLAS repair unless a specific GPU-MFS objective appears.
   Run `225` turns the open half-space Green-function gap into a concrete BEM
   objective contract. It joins the guarded 13-sample `grid_15mm_only` plus
   `outer_shell_11mm_binary` surface policy with the 9-frequency, 31-receiver
   3D BEM reference shape. For 1000 candidate geometries, that already implies
   13,000 surface samples and a floor of 3,627,000 frequency-receiver-sample
   kernel evaluations before dense-solve overhead. The next BEM objective is a
   CPU half-space Green-kernel smoke with homogeneous-limit recovery and
   single-interface sanity checks. Inversion-scale half-space BEM, real
   BEM/FDTD comparison, 3D validation, field transfer, GPU/HPC, and field FWI
   remain blocked until that kernel objective passes.
   Run `226` validates the run `225` objective contract from a consumer
   perspective. Eight of eight checks pass with zero blocking failures,
   confirming the 11-item objective table, five half-space blockers, five
   objective stages, five candidate-budget rows, guarded 2D/3D inputs, explicit
   kernel blockers, the homogeneous-limit kernel smoke as the first executable
   stage, the 3,627,000 kernel-evaluation floor proxy for 1000 candidates, low
   optional GPU-MFS priority, and blocked downstream states.
   Run `227` stress-tests that validator. The exact objective contract passes,
   while 27 damaged variants fail as expected for count drift, missing or
   weakened blockers, wrong first stage, cost-proxy drift, false
   kernel/inversion promotion, guarded-input drift, GPU-priority drift, and
   downstream promotion. There are zero unexpected outcomes. Use runs `225-227`
   as the guarded BEM half-space Green-function objective package.
   Run `228` executes the first CPU scalar half-space Green-kernel smoke from
   that package. The 13-sample, 31-target, nine-frequency shape gives a
   3,627-entry kernel-evaluation floor for one candidate. The two-layer helper
   recovers the homogeneous limit with relative L2
   `1.3693101062433268e-16`, the normal-incidence transmission magnitude
   decreases from 1.0 at lower `epsr=1` to 0.5 at lower `epsr=9`, and the
   concrete half-space field is finite and nonzero. This promotes only a scalar
   kernel smoke and readiness for a finite-rebar half-space smoke. It does not
   promote inversion-scale half-space BEM, real BEM/FDTD comparison, 3D
   validation, field transfer, GPU/HPC, or field FWI.
   Run `229` validates the scalar kernel smoke from a consumer perspective.
   Seven of seven checks pass with zero blocking failures, confirming the
   13-by-31-by-9 shape, homogeneous-limit relative L2 below `1e-10`,
   monotonic interface transmission, finite nonzero concrete half-space field,
   smoke readiness separated from inversion readiness, source-objective guard
   readiness, and blocked comparison/3D/field/GPU/FWI states.
   Run `230` stress-tests that validator. The exact smoke result passes, while
   19 damaged variants fail as expected for shape drift, homogeneous-limit
   failure, interface-trend breakage, concrete-field invalidity, smoke-readiness
   drift, false inversion promotion, source-objective guard failure, and
   downstream promotion. There are zero unexpected outcomes. Use runs `228-230`
   as the guarded scalar half-space Green-kernel smoke package.
   Run `231` couples that scalar half-space incident field to a simple
   finite-rebar scattering proxy. The scattered response is finite and nonzero,
   peaks at the target center (`x=0.13 m`), has maximum symmetry-pair imbalance
   `7.108390876697042e-16`, and satisfies
   total-background-scattered residual accounting with maximum residual
   `1.4210854715202004e-14`. This promotes only a scalar finite-rebar coupling
   smoke. It remains a proxy, not full 3D Maxwell BEM and not a FDTD-validated
   result.
   Run `232` validates that coupling smoke from a consumer perspective. Seven
   of seven checks pass with zero blocking failures, confirming the
   13-surface-sample, 31-target, nine-frequency shape, normalized centered
   target weights, centered scattered-response peak, finite nonzero fields,
   symmetry and residual tolerances, and blocked inversion/real-comparison/3D/
   field/GPU/FWI states. This guards the scalar finite-rebar coupling smoke but
   still does not promote full 3D Maxwell BEM or FDTD-validated claims.
   Run `233` stress-tests that validator. The exact coupling smoke passes,
   while 24 damaged scenarios fail as expected for surface/target/frequency
   shape drift, target-weight normalization or centering drift, missing or
   duplicated peak markers, off-center peak response, invalid field state,
   excessive symmetry imbalance, excessive residual error, source/coupling
   readiness drift, and false promotion to inversion, real BEM/FDTD comparison,
   3D validation, field transfer, GPU, or field FWI. There are zero unexpected
   outcomes. Use runs `231-233` as the guarded scalar finite-rebar half-space
   coupling package, scoped as a proxy rather than a full 3D Maxwell BEM result.
   Run `234` converts that guarded scalar package into an explicit claim
   boundary. It records six supported claims and seven blocked claims with zero
   unexpected claim failures. Supported: bounded scalar surface sampling,
   scalar half-space kernel shape, homogeneous-limit recovery, single-interface
   sanity trend, centered finite-rebar proxy response, and negative-control
   sensitivity. Blocked: full 3D Maxwell BEM, real BEM/FDTD comparison,
   inversion-scale half-space BEM, field transfer, GPU/HPC escalation, field
   FWI, and broadband antenna/time-domain reconstruction. The one-candidate
   kernel-evaluation floor remains 3,627 and the 1000-candidate floor remains
   3,627,000 before dense-solve overhead.
   Run `235` defines the matched scalar BEM/FDTD comparison contract from that
   boundary. It writes 31 schema columns, 14 requirements, and six acceptance
   metrics. Nine requirements are contract-ready, three need implementation,
   and two remain blocked. The contract is ready as an implementation target,
   but actual comparison remains blocked by missing BEM exporter alignment,
   missing FDTD frequency extraction, uncalibrated thresholds, and absent real
   paired BEM/FDTD files. Real BEM/FDTD agreement, 3D validation, inversion,
   field transfer, GPU/HPC readiness, and field FWI remain false.
   Run `236` validates that comparison contract from a consumer perspective.
   Seven of seven checks pass with zero blocking failures, confirming the 14
   requirements, 31 schema columns, six acceptance metrics, guarded requirement
   status counts, complete required schemas, explicit metric readiness, the
   13-by-31-by-9 source shape, the 3,627 one-candidate kernel-evaluation floor,
   and blocked exporter/extractor/real-comparison/3D/inversion/field/GPU/FWI
   states.
   Run `237` stress-tests that validator. The exact comparison contract passes,
   while 21 damaged scenarios fail as expected for requirement-count drift,
   requirement-status drift, blocking-flag drift, schema-count/schema-required/
   schema-name drift, metric-count or metric-readiness drift, source-shape or
   cost-floor drift, contract-readiness drift, and false exporter, extractor,
   real-comparison, 3D, inversion, field, GPU, or field-FWI promotion. There
   are zero unexpected outcomes. Use runs `235-237` as the guarded scalar
   BEM/FDTD comparison-contract package.
   Run `238` implements the BEM side of that comparison contract. It exports
   the run `231` scalar background, scattered, and total complex frequency
   fields into the run `235` BEM schema: 10 columns, three model roles, 13
   receiver samples, nine frequencies, and 351 rows. Four of four exporter
   checks pass, the scattered-norm relative error is zero against run `231`,
   and the total-background-scattered residual remains
   `1.4210854715202004e-14`. FDTD frequency extraction, real BEM/FDTD
   comparison, 3D validation, inversion, field transfer, GPU/HPC readiness, and
   field FWI remain blocked.
   Run `239` validates that BEM-side export from a consumer perspective. Eight
   of eight checks pass with zero blocking failures, confirming the 351-row
   export, 10-column contract schema, complete background/scattered/total key
   sets, finite field values, residual accounting, source scattered norm,
   locked geometry/observable/normalization metadata, passing source exporter
   checks, and blocked FDTD extraction/real-comparison/3D/inversion/field/GPU/
   FWI states.
   Run `240` stress-tests that exporter validator. The exact BEM export passes,
   while 21 damaged scenarios fail as expected for row-count or role-key drift,
   extra schema columns, residual-accounting drift, nonfinite field values,
   scattered-norm drift, geometry/observable/normalization metadata drift,
   failed source exporter checks, summary-count drift, and false exporter, FDTD
   extraction, real-comparison, 3D, inversion, field, GPU, or field-FWI
   promotion. There are zero unexpected outcomes. Use runs `238-240` as the
   guarded BEM-side export package for the scalar comparison contract.
   Run `241` defines the FDTD-side time-trace input contract for that scalar
   comparison. It writes a 13-column target/background time-trace schema, 13
   required receiver keys, nine required frequency keys, and 10 requirements.
   Six requirements are contract-ready, two need implementation, and two remain
   blocked. The input contract is ready, but FDTD frequency extraction remains
   blocked by the scalar projection convention, complex frequency extractor,
   and missing paired target/background FDTD trace files.
   Run `242` validates that FDTD-side input contract from a consumer
   perspective. Six of six checks pass with zero blocking failures, confirming
   the 13-column schema, 13 receiver keys, nine frequency keys, guarded
   requirement status counts, source BEM export shape, and blocked projection/
   extractor/trace-file/FDTD-extraction/real-comparison/3D/inversion/field/GPU/
   FWI states.
   Run `243` stress-tests that validator. The exact input contract passes,
   while 24 damaged scenarios fail as expected for schema count/required/name
   drift, receiver or frequency key count/required drift, requirement
   count/status drift, extraction-blocker accounting drift, source BEM export
   shape drift, and false input-contract, projection, extractor, trace-file,
   FDTD-extraction, real-comparison, 3D, inversion, field, GPU, or field-FWI
   promotion. There are zero unexpected outcomes. Use runs `241-243` as the
   guarded FDTD input-contract package for the scalar comparison path.
   Run `244` executes a synthetic scalar frequency-extractor smoke. It
   generates target/background scalar time traces from the BEM total/background
   spectra, recovers nine selected complex frequency bins at 13 receivers by
   least-squares sine/cosine extraction, and compares the recovered scattered
   spectrum with the BEM scattered spectrum. The design matrix condition number
   is `1.050778890483821`, maximum absolute error is
   `7.105427357601002e-13`, and maximum relative error is
   `2.1699084408491636e-13`. This validates extraction mechanics only; real
   FDTD extraction, real BEM/FDTD comparison, 3D validation, inversion, field
   transfer, GPU/HPC readiness, and field FWI remain blocked.
   Run `245` validates that synthetic extractor smoke from a consumer
   perspective. Five of five checks pass with zero blocking failures, confirming
   the 117-row extracted shape, receiver/global error summaries, well
   conditioned design matrix, synthetic-smoke readiness, and blocked real
   FDTD-extraction/real-comparison/3D/inversion/field/GPU/FWI states.
   Run `246` stress-tests that validator. The exact synthetic extractor smoke
   passes, while 17 damaged scenarios fail as expected for extracted-shape
   drift, receiver-error summary drift, global error-summary drift, excessive
   extraction error, poor design-matrix conditioning, source guard or synthetic
   readiness drift, and false real FDTD-extraction, real-comparison, 3D,
   inversion, field, GPU, or field-FWI promotion. There are zero unexpected
   outcomes. Use runs `244-246` as the guarded synthetic frequency-extractor
   package.
   Run `247` connects the guarded BEM export and guarded synthetic frequency
   extractor into the first end-to-end synthetic pairwise comparison smoke. It
   pairs all 117 receiver-frequency keys with zero missing keys and zero
   duplicate keys, reports maximum scattered absolute error
   `7.105427357601002e-13`, maximum scattered relative error
   `2.1699084408491636e-13`, normalized L2 error
   `2.459587752743292e-15`, and zero scan peak-location error across the nine
   frequencies. This validates comparison plumbing only; real FDTD extraction,
   real BEM/FDTD comparison, 3D validation, inversion-scale use, field
   transfer, GPU/HPC readiness, and field FWI remain blocked until real paired
   FDTD traces are available and pass the same key, residual, and peak-location
   checks.
   Run `248` validates that synthetic pairwise comparison from a consumer
   perspective. Six of six checks pass with zero blocking failures, confirming
   source guard readiness, complete 117-key pairing, finite and small residual
   metrics, nine scan peak-location rows with 13 receivers each, explicit
   metric boundaries with phase-reference residual still blocked, and blocked
   real-FDTD/real-comparison/3D/inversion/field/GPU/FWI states. Sensitivity
   remains required before treating the pairwise comparison guard as robust.
   Run `249` stress-tests that validator. The exact synthetic pairwise
   comparison passes, while 30 damaged variants fail as expected for source
   readiness drift, paired-key drift, missing or duplicate keys, nonfinite or
   excessive residuals, normalized-L2 readiness drift, scan peak-location
   drift, phase-reference readiness drift, synthetic readiness drift, and false
   real-FDTD/real-comparison/3D/inversion/field/GPU/FWI promotion. There are
   zero unexpected outcomes. Use runs `247-249` as the guarded synthetic
   BEM/FDTD pairwise comparison package; real comparison remains blocked until
   real paired FDTD traces are available.
   Run `250` converts the FDTD-side trace schema into a real-FDTD trace intake
   manifest contract. It requires 26 projected scalar trace files: 13
   background traces and 13 target traces, one per receiver, plus 182 planned
   checks across file presence, schema columns, receiver-key match, constant
   time step, reference fields, projection metadata, and SHA-256 checksum. The
   manifest is ready for real trace generation planning, but real trace files,
   real projection convention, real time-zero/amplitude references, real
   frequency extraction, real BEM/FDTD comparison, 3D validation, inversion,
   field transfer, GPU/HPC readiness, and field FWI remain blocked.
   Run `251` validates that manifest from a consumer perspective. Six of six
   checks pass with zero blocking failures, confirming source readiness, 26
   trace rows across two roles and 13 receivers, 13 schema columns, nine
   frequency keys, CSV trace-table format, required reference/projection
   fields, 182 unexecuted planned checks, trace-generation readiness, and
   blocked real trace intake, real frequency extraction, real comparison, 3D,
   inversion, field transfer, GPU/HPC readiness, and field FWI. Sensitivity
   remains required before treating the manifest guard as robust.
   Run `252` stress-tests that validator. The exact manifest passes, while 34
   damaged variants fail as expected for source-readiness drift, trace-count
   drift, missing trace rows, role/receiver-key drift, schema/format/reference/
   projection drift, planned-check drift, check-execution drift, trace-
   generation drift, real-intake drift, and false real-FDTD/real-comparison/3D/
   inversion/field/GPU/FWI promotion. There are zero unexpected outcomes. Use
   runs `250-252` as the guarded real-FDTD trace intake manifest package.
   Run `253` evaluates that guarded manifest against an empty trace root as a
   fail-closed dry run. All 182 planned checks fail with zero passes: 26
   file-present failures and 156 dependent checks blocked by missing trace
   files. No shell commands are executed, no real trace files are inferred, and
   real FDTD extraction, real BEM/FDTD comparison, 3D validation, inversion,
   field transfer, GPU/HPC readiness, and field FWI remain blocked.
   Run `254` validates that empty-root dry run from a consumer perspective. Six
   of six checks pass with zero blocking failures, confirming source readiness,
   the 182-check fail-closed shape, 26 missing trace-file failures, 156
   dependent blocked checks, all seven check groups, no shell execution, no real
   trace promotion, and blocked real-extraction/real-comparison/3D/inversion/
   field/GPU/FWI states. Sensitivity remains required before treating the
   fail-closed precheck as fully guarded.
   Run `255` stress-tests that validator. The exact empty-root dry run passes,
   while 21 damaged variants fail as expected for source-readiness drift,
   dry-run count drift, unexpected row pass, failure-reason drift, missing-file
   count drift, check-group drift, shell-execution drift, real-trace promotion,
   and false real-FDTD/real-comparison/3D/inversion/field/GPU/FWI promotion.
   There are zero unexpected outcomes. Use runs `253-255` as the guarded
   fail-closed precheck package for future real-FDTD trace staging.
   Run `256` adds the positive populated-root synthetic smoke. It stages 26
   synthetic projected trace files with 416 total samples into the manifest
   layout, passes all 182 checks across all seven check groups, executes no
   shell commands, and keeps real trace intake, real FDTD extraction, real
   BEM/FDTD comparison, 3D validation, inversion, field transfer, GPU/HPC
   readiness, and field FWI false. Use it as the acceptance-mechanics smoke;
   validator and sensitivity coverage remain the next guarded step.
   Run `257` validates that populated-root synthetic smoke from a consumer
   perspective. Six of six checks pass with zero blocking failures, confirming
   source guard readiness, 26 synthetic trace files, 416 samples, 182 passing
   checks across seven groups, recorded checksums, no shell execution, and
   blocked real trace intake, real FDTD extraction, real BEM/FDTD comparison,
   3D validation, inversion, field transfer, GPU/HPC readiness, and field FWI.
   Sensitivity remains required before treating this acceptance path as fully
   guarded.
   Run `258` stress-tests that validator. The exact populated-root synthetic
   smoke passes, while 29 damaged variants fail as expected for source-
   readiness drift, trace-inventory drift, sample-count drift, manifest-check
   drift, check-group drift, checksum drift, shell-execution drift, synthetic/
   real trace-boundary drift, and false real-FDTD/real-comparison/3D/inversion/
   field/GPU/FWI promotion. There are zero unexpected outcomes. Use runs
   `256-258` as the guarded positive acceptance-mechanics package for future
   real-FDTD trace staging.
   Run `259` consumes that accepted synthetic trace root with a frequency-bin
   extractor. The 26 staged synthetic traces produce 117 finite receiver-
   frequency bins across 13 receivers and nine required frequencies. The
   reference/error columns are self-reference schema-compatibility fields, not
   BEM/FDTD agreement evidence. Real trace files, real FDTD extraction, real
   BEM/FDTD comparison, 3D validation, inversion, field transfer, GPU/HPC
   readiness, and field FWI remain blocked.
   Run `260` validates that trace-root synthetic frequency-extraction smoke
   from a consumer perspective. Six of six checks pass with zero blocking
   failures, confirming source readiness, 26 traces, 117 finite bins, 13
   receiver summaries, explicit self-reference schema fields, and blocked real
   trace intake, real FDTD extraction, real BEM/FDTD comparison, 3D validation,
   inversion, field transfer, GPU/HPC readiness, and field FWI. Sensitivity
   remains required before treating this extraction path as fully guarded.
   Run `261` stress-tests that validator. The exact trace-root frequency-
   extraction smoke passes, while 30 damaged variants fail as expected for
   source-readiness drift, trace-count drift, role-count drift, sample-count
   drift, receiver/frequency coverage drift, finite-bin drift, receiver-summary
   drift, self-reference drift, and false real-trace/real-FDTD/real-comparison/
   3D/inversion/field/GPU/FWI promotion. There are zero unexpected outcomes.
   Use runs `259-261` as the guarded trace-root-to-frequency-bin mechanics
   package.
   Run `262` compares those trace-root synthetic bins against the BEM scattered
   spectra as a negative control. All 117 receiver-frequency keys pair cleanly,
   with zero missing or duplicate keys, but the normalized L2 mismatch is
   `1.0000000672667073` and the maximum scattered relative error is
   `1.000208702121816`. This is the expected no-go: the self-referenced
   trace-root frequency table is plumbing evidence only, not BEM/FDTD agreement
   evidence. Real trace files, real FDTD extraction, real BEM/FDTD comparison,
   3D validation, inversion, field transfer, GPU/HPC readiness, and field FWI
   remain blocked.
   Run `263` validates that negative-control comparison from a consumer
   perspective. Five of five checks pass with zero blocking failures: source
   readiness flags are valid, all 117 receiver-frequency pairs are complete,
   unique, and finite, the nine frequency summaries reproduce the pairwise rows,
   the normalized L2 mismatch recomputes to `1.0000000672667073`, and agreement
   plus downstream claims remain blocked. Sensitivity remains required before
   treating this negative-control boundary as fully guarded.
   Run `264` stress-tests that validator. The exact run `262` audit passes,
   while 28 damaged variants fail as expected for source-readiness drift,
   pairwise key-coverage drift, nonfinite pairwise values, frequency-summary
   drift, mismatch-metric drift, false synthetic-agreement promotion, and false
   real-comparison/3D/inversion/field/GPU/FWI promotion. There are zero
   unexpected outcomes. Use runs `262-264` as the guarded negative-control
   package for synthetic trace-root bins. Real FDTD traces and a real paired
   BEM/FDTD comparison remain required.
   Run `265` joins the guarded comparison contract, BEM exporter, synthetic
   trace-intake mechanics, synthetic trace-frequency extraction mechanics, and
   synthetic negative-control boundary into one real-comparison readiness
   table. Five support items are ready or guarded, but four blockers remain:
   real FDTD trace files, real frequency extraction, real paired BEM/FDTD
   comparison, and threshold calibration after the first real pair. Do not claim
   BEM/FDTD agreement, 3D validation, inversion scale, field transfer, GPU/HPC
   readiness, or field FWI from the synthetic plumbing.
   Run `266` validates that real-comparison readiness boundary from a consumer
   perspective. Five of five checks pass with zero blocking failures, confirming
   the expected 10 boundary items, five support items, four blockers,
   synthetic-only support that cannot count as real agreement, and blocked real
   comparison plus downstream 3D/inversion/field/GPU/FWI states. Sensitivity
   remains required before treating the boundary as fully guarded.
   Run `267` stress-tests that validator. The exact run `265` boundary passes,
   while 22 damaged variants fail as expected for item-count drift, status-count
   drift, synthetic-support promotion, missing real blockers, missing
   next-action fields, and false real/downstream readiness. There are zero
   unexpected outcomes. Use runs `265-267` as the guarded real-comparison
   readiness boundary.
   Run `268` defines the threshold-calibration protocol for the first real
   matched BEM/FDTD pair. Three structural gates are ready before data:
   receiver-frequency key completeness, duplicate/missing key guards, and
   finite complex bins. Numerical agreement thresholds remain uncalibrated:
   normalized L2, maximum relative error, scan-peak location tolerance, and
   phase residual tolerance require the first real paired return and explicit
   time-zero convention. The run `262` synthetic negative-control mismatch
   remains a false-promotion guard, not a threshold source. Real traces, real
   extraction, real comparison, 3D validation, inversion scale, field transfer,
   GPU/HPC work, and field FWI remain blocked.
   Run `269` validates that threshold-calibration protocol from a consumer
   perspective. Five of five checks pass with zero blocking failures,
   confirming the 10 protocol items, six metric rows, structural gate versus
   agreement-threshold split, synthetic negative-control exclusion, and blocked
   thresholds/real-comparison/3D/inversion/field/GPU/FWI states. Sensitivity
   remains required before treating this protocol as fully guarded.
   Run `270` stress-tests that validator. The exact run `268` protocol passes,
   while 30 damaged variants fail as expected for protocol-count drift,
   metric-count drift, status-count drift, missing rows, item-name drift,
   premature threshold readiness, synthetic negative-control promotion, metric
   boundary drift, and false real/downstream readiness. There are zero
   unexpected outcomes. Use runs `268-270` as the guarded threshold-
   calibration protocol; real traces and the first real paired BEM/FDTD return
   remain required before numerical agreement thresholds can be set.
   Run `271` turns that guarded threshold-calibration protocol into an empty
   template pack for the first real matched BEM/FDTD pair. It defines four
   threshold rows, eight required metadata fields, zero calibrated thresholds,
   and zero ready metadata rows. The synthetic negative control remains
   unusable for calibration. Real traces, real FDTD extraction, real BEM/FDTD
   comparison, 3D validation, inversion scale, field transfer, GPU/HPC work,
   and field FWI remain blocked.
   Run `272` validates that template pack from a consumer perspective. Five of
   five checks pass with zero blocking failures, confirming four threshold
   rows, eight metadata rows, blank values, zero calibrated thresholds, required
   metadata, synthetic negative-control exclusion, and blocked real-comparison/
   downstream states.
   Run `273` stress-tests that template-pack validator. The exact run `271`
   template passes, while 26 damaged variants fail as expected for threshold
   row drift, metadata drift, synthetic negative-control promotion, and false
   real/downstream readiness. There are zero unexpected outcomes. Use runs
   `271-273` as the guarded first-real-pair threshold-calibration template
   pack; real traces and the first real paired BEM/FDTD return remain required
   before numerical agreement thresholds can be set.
   Run `274` fills that threshold-calibration template with deterministic
   synthetic threshold and metadata values as a positive-control smoke. All 13
   synthetic checks pass, including threshold value shape, shared pair ID,
   SHA-256-shaped metadata fields, frequency-grid parsing, synthetic negative-
   control exclusion, and no real-threshold or real-metadata promotion. The
   filled template remains synthetic only; real threshold calibration and real
   BEM/FDTD agreement remain blocked until real paired data arrive.
   Run `275` validates that synthetic fill smoke from saved artifacts. Five of
   five checks pass with zero blocking failures, confirming filled synthetic
   threshold rows, filled synthetic metadata rows, 13 passing synthetic checks,
   consistent summary counts, and blocked real-comparison/downstream states.
   Sensitivity remains required before treating the synthetic fill smoke as
   fully guarded.
   Run `276` stress-tests that validator. The exact run `274` synthetic fill
   smoke passes, while 24 damaged variants fail as expected for threshold row
   drift, metadata drift, saved-check drift, summary-count drift, synthetic
   negative-control promotion, real-threshold/metadata promotion, malformed
   frequency-grid metadata, and false real/downstream readiness. There are zero
   unexpected outcomes. Use runs `274-276` as the guarded positive-control
   threshold-fill smoke; real paired BEM/FDTD data remain required before
   calibration.
   Run `277` synthesizes the current threshold-calibration intake boundary.
   Two support items are ready: the guarded blank template and the guarded
   synthetic fill positive control. Five real-data blockers remain: real FDTD
   trace files, real frequency extraction, real paired BEM/FDTD comparison,
   real threshold calibration, and downstream 3D/inversion/field/GPU/FWI
   claims. Do not set thresholds or promote BEM/FDTD agreement until real
   paired data pass the guarded intake path.
   Run `278` converts that guarded threshold-calibration boundary into a
   non-executed command plan. Three current guard-validation commands can run
   now, while four future real-pair commands require a real FDTD trace root,
   real frequency extraction, a real paired BEM/FDTD comparison, and real
   threshold values. No commands are executed in this run. Use it as the
   first-real-pair calibration checklist; threshold calibration, BEM/FDTD
   agreement, 3D validation, inversion scale, field transfer, GPU/HPC work, and
   field FWI remain blocked.
   Run `279` validates that command plan from saved artifacts. Six of six
   checks pass with zero blocking failures, confirming source readiness,
   command partition counts, executable current guard commands, blocked future
   real-pair gates, summary/table count consistency, and blocked real
   comparison/downstream states. Sensitivity remains required before treating
   the command checklist as fully guarded.
   Run `280` stress-tests that validator. The exact run `278` command plan
   passes, while 31 damaged variants fail as expected for command-row drift,
   command-order drift, command-group drift, current guard executability drift,
   future gate blocking drift, summary-count drift, command-execution
   promotion, real-trace promotion, real-comparison promotion, threshold
   promotion, and false 3D/field/GPU/FWI readiness. There are zero unexpected
   outcomes. Use runs `278-280` as the guarded first-real-pair threshold-
   calibration command checklist.
   Run `281` executes only the three current guard-validation commands from
   that checklist. All three pass: the template-pack guard, synthetic threshold
   fill guard, and threshold-intake boundary guard. The four future real-pair
   commands remain unexecuted because real paired BEM/FDTD data are still
   missing. Use run `281` as the current-guard execution smoke; threshold
   calibration, BEM/FDTD agreement, 3D validation, inversion scale, field
   transfer, GPU/HPC work, and field FWI remain blocked.
   Run `282` validates the run `281` current-guard execution smoke from saved
   artifacts. Six of six checks pass with zero blocking failures, confirming
   that the saved execution rows match the runnable current-guard subset of the
   run `278` command plan, all three commands passed, summary counts match the
   execution table, and future real-pair plus downstream states remain blocked.
   Sensitivity remains required before treating the execution smoke as fully
   guarded.
   Run `283` stress-tests that execution-smoke validator. The exact run `281`
   smoke passes, while 30 damaged variants fail as expected for execution-row
   drift, command-template drift, real-data requirement drift, command failure,
   elapsed-time corruption, source command-plan mismatch, summary-count drift,
   future real-pair execution promotion, real-trace promotion, real-comparison
   promotion, threshold promotion, and false 3D/inversion/field/GPU/FWI
   readiness. There are zero unexpected outcomes. Use runs `281-283` as the
   guarded current-guard execution smoke for the first-real-pair threshold-
   calibration checklist.
   Run `284` synthesizes the current post-execution boundary. Two support
   items are ready: the guarded first-real-pair command checklist and the
   guarded current-guard execution smoke. Five real-data blockers remain:
   future real-pair command execution, real FDTD trace files, real paired
   BEM/FDTD comparison, real threshold calibration, and downstream
   3D/inversion/field/GPU/FWI escalation. Use run `284` as the current BEM
   threshold-calibration boundary; do not execute future real-pair commands or
   set thresholds until real paired data are staged.
   Run `285` validates that post-execution boundary from saved artifacts. Six
   of six checks pass with zero blocking failures, confirming the two-support/
   five-blocker row partition, guarded support rows, real-data blocker rows,
   summary/table count consistency, and blocked real comparison, threshold,
   3D, inversion, field, GPU, and FWI states. Sensitivity remains required
   before treating the boundary as fully guarded.
   Run `286` stress-tests that post-execution boundary validator. The exact
   run `284` boundary passes, while 25 damaged variants fail as expected for
   boundary-row drift, support/blocker status drift, missing real-data blocker
   flags, summary-count drift, unguarded command/execution support, future
   real-pair execution promotion, real-trace promotion, real-comparison
   promotion, threshold promotion, and false 3D/inversion/field/GPU/FWI
   readiness. There are zero unexpected outcomes. Use runs `284-286` as the
   guarded current BEM threshold-calibration post-execution boundary.
   Run `287` combines the first-real-pair threshold template with the guarded
   post-execution boundary. The resulting handoff table has 19 rows: four
   threshold metrics, eight required metadata fields, two guarded return
   supports, and five real-data/downstream blockers. The pack is ready as a
   checklist, but real traces, a real paired BEM/FDTD comparison, and accepted
   threshold values are still absent. Do not set thresholds, promote BEM/FDTD
   agreement, start 3D validation, start inversion-scale studies, transfer to
   field evidence, use GPU/HPC, or run field FWI from the current guarded-only
   state.
   Run `288` validates the run `287` return-readiness pack from saved
   artifacts. Seven of seven checks pass with zero blocking failures,
   confirming the four threshold metrics, eight required metadata fields, two
   guarded return supports, five real-data blockers, guard summary readiness,
   and false real-comparison/threshold/3D/inversion/field/GPU/FWI states.
   Sensitivity remains required before treating the pack validator as guarded.
   Run `289` stress-tests that validator. The exact run `287` pack passes,
   while 41 damaged variants fail as expected for threshold-row drift,
   metadata-row drift, support/blocker drift, summary-count drift, guard-
   readiness drift, premature calibrated-threshold or metadata readiness, real-
   trace promotion, real-comparison promotion, threshold promotion, 3D/
   inversion promotion, field-transfer promotion, GPU promotion, and field-FWI
   promotion. There are zero unexpected outcomes. Use runs `287-289` as the
   guarded BEM first-real-pair return-readiness pack.
   Run `290` returns to the Bempp 3D prototype evidence and converts runs
   `107`, `108`, and `113` into a fine-mesh reference adoption checklist. The
   8x20 finite-cylinder mesh, the run `113` frequency grid, and the locked
   source/receiver metadata are ready as the future BEM-side reference
   convention. The 6x16 mesh is demoted to smoke-test use only. Real BEM/FDTD
   agreement, 3D validation, layered GPR readiness, field transfer, GPU/HPC
   readiness, and field FWI remain blocked until a matched FDTD comparison
   exists.
   Run `291` validates the run `290` checklist from saved artifacts. Seven of
   seven checks pass with zero failures, confirming the expected seven-row
   partition, the 8x20 reference adoption, the 6x16 smoke-only demotion, source
   and receiver metadata locks, valid figure output, script snapshots, and
   false real-comparison/3D/layered/field/GPU/FWI readiness. Sensitivity
   remains required before treating the validator itself as guarded.
   Run `292` stress-tests that validator. The exact run `290` checklist
   passes, while 30 damaged variants fail as expected for checklist-row drift,
   summary-count drift, 8x20 demotion, 6x16 promotion, source/receiver lock
   drift, downstream promotion, figure-validation drift, and script-snapshot
   drift. There are zero unexpected outcomes. Use runs `290-292` as the
   guarded Bempp fine-mesh reference adoption checkpoint, and consume that
   reference contract only in a future matched FDTD export/comparison path.
   Run `293` consumes that guarded reference contract and defines the future
   matched FDTD export/comparison contract. The contract has four ready BEM/
   metadata rows, two required FDTD export rows, one paired-residual row, one
   threshold-metadata row, and one downstream-blocked row. It is ready as a
   schema and handoff contract, but real target/background FDTD exports, real
   BEM/FDTD residuals, threshold calibration, 3D validation, inversion scale,
   field transfer, GPU/HPC work, and field FWI remain blocked.
   Run `294` validates the run `293` matched FDTD export contract from saved
   artifacts. Seven of seven checks pass with zero failures, confirming the
   ready BEM reference rows, required target/background FDTD export rows,
   paired-export schema, source guard readiness, figure output, script
   snapshots, and blocked real-comparison/threshold/3D/inversion/field/GPU/FWI
   states. Sensitivity remains required before treating the validator itself as
   guarded.
   Run `295` stress-tests that validator. The exact run `293` contract passes,
   while 33 damaged variants fail as expected for BEM reference drift, FDTD
   export promotion, comparison-blocker drift, schema drift, source-guard
   drift, downstream promotion, figure-validation drift, and script-snapshot
   drift. There are zero unexpected outcomes. Use runs `293-295` as the
   guarded BEM/FDTD matched-export contract.
   Run `296` converts that guarded contract into a non-executed command plan.
   Three current guard commands are executable now. Four future commands remain
   blocked until real target/background FDTD frequency exports, paired residual
   rows, and threshold-calibration inputs are staged. No commands are executed
   in this run, and real comparison, threshold calibration, 3D validation,
   inversion scale, field transfer, GPU/HPC work, and field FWI remain blocked.
   Run `297` validates the run `296` command plan from saved artifacts. Seven
   of seven checks pass with zero failures, confirming the command counts,
   current guard command executability, future real-export gating, no-execution
   state, valid figure output, script snapshots, and blocked real-comparison/
   threshold/3D/field/GPU/FWI states. Sensitivity remains required before
   treating the command-plan validator as guarded.
   Run `298` stress-tests that validator. The exact run `296` command plan
   passes, while 37 damaged variants fail as expected for missing command rows,
   current-guard executability drift, future real-export gate drift, accidental
   command execution, summary drift, downstream promotion, figure-validation
   drift, and script-snapshot drift. There are zero unexpected outcomes. Use
   runs `296-298` as the guarded non-executed command plan for the first
   matched BEM/FDTD export path.
   Run `299` audits the existing `outputs/experiments` 2D FDTD archive against
   that guarded export path. It scans 4513 CSV/NPZ/HDF files and finds 80
   convertible time-domain B-scan files across 76 experiments, but zero strict
   fine-mesh target/background frequency exports in the run `293` schema and
   zero legacy 3D frequency-bin exports. The comparator remains blocked. The
   next useful BEM/FDTD task is a dedicated FDTD frequency-export adapter for a
   selected 2D B-scan case, not direct comparator execution from the archive.
   Run `300` performs the first guarded target-side adapter smoke from that
   audit. It selects the run `107` clean B-scan, interpolates it onto the
   locked 31-point receiver line, extracts the run `113` nine-frequency grid,
   and writes 279 finite rows shaped like the run `293` schema. This is a
   proxy target export only: source lock, receiver lock, background export,
   accepted target/background pairing, real comparison, thresholds, 3D
   validation, field transfer, GPU/HPC, and field FWI remain blocked.
   Run `301` validates the run `300` proxy export from saved artifacts. Ten of
   ten checks pass with zero failures, confirming the row count, strict schema
   shape, finite values, locked frequency grid, locked receiver grid, source
   archive provenance, closed acceptance gate, blocked downstream states,
   figure output, and script snapshots. Sensitivity remains required before
   treating the proxy validator as guarded.
   Run `302` stress-tests that validator. The exact run `300` proxy export
   passes, while 42 damaged variants fail as expected for row-count drift,
   schema drift, non-finite values, receiver/frequency drift, provenance drift,
   proxy acceptance promotion, downstream promotion, figure-validation drift,
   and script-snapshot drift. There are zero unexpected outcomes. Use runs
   `300-302` as a guarded target-side proxy export branch only; accepted
   target/background export and real BEM/FDTD comparison remain blocked.
   Run `303` generates the missing background side for a local adapter smoke by
   simulating a no-rebar FDTD background with the same grid, scan line, source
   wavelet, and Tx/Rx convention as the run `107` target archive. It writes
   279 target rows, 279 background rows, and 279 scattered rows in the run
   `293` schema shape. This creates a paired 2D scalar proxy export, not an
   accepted run `293` 3D FDTD pair: source lock, receiver lock, real BEM/FDTD
   comparison, 3D validation, field transfer, GPU/HPC readiness, and field FWI
   remain blocked.
   Run `304` validates the run `303` paired scalar proxy export from saved
   artifacts. Ten of ten checks pass, confirming strict schema rows, matching
   target/background/scattered frequency-receiver keys, finite values,
   scattered equals target minus background, generated-background provenance,
   run `107` target provenance, valid figure output, script snapshots, and
   closed accepted-pair/real-comparison/3D/field/GPU/FWI gates. Sensitivity
   remains required before using the paired proxy in a proxy comparator.
   Run `305` stress-tests the run `304` validator. The exact run `303` paired
   proxy passes, while 43 damaged variants fail as expected for row-count
   drift, schema drift, solver and pair-id drift, frequency/receiver drift,
   non-finite values, scattered-residual drift, metadata/provenance drift,
   summary drift, downstream promotion, figure-validation drift, and
   script-snapshot drift. Zero unexpected outcomes. Use runs `303-305` as the
   guarded paired scalar proxy export; accepted run `293` evidence and real
   BEM/FDTD comparison remain blocked.
   Run `306` compares the guarded 2D scalar proxy scattered amplitudes with
   the run `117` 3D Bempp scattered-reference vector norms as a plumbing-only
   diagnostic. It writes 279 receiver comparison rows and nine frequency
   summary rows. After per-frequency scale fitting, seven of nine frequencies
   are under the 0.15 shape marker, but raw amplitudes require enormous,
   frequency-dependent scale factors spanning about 136x. Treat this as a
   proxy-comparator smoke only; calibrated amplitude agreement, accepted run
   `293` evidence, real BEM/FDTD comparison, 3D validation, field transfer,
   GPU/HPC readiness, and field FWI remain blocked.
   Run `307` validates the run `306` proxy-comparator smoke from saved
   artifacts. Eight of eight checks pass, confirming row counts, source
   readiness, per-frequency receiver counts, scale diagnostics, shape-marker
   counts, finite receiver rows, valid figure output, script snapshots, and
   closed raw-amplitude/scale-calibration/accepted-pair/real-comparison/3D/
   field/GPU/FWI gates. Sensitivity remains required before treating the
   diagnostic validator as guarded.
   Run `308` stress-tests that validator. The exact run `306` proxy-comparator
   artifact set passes, while 34 damaged variants fail as expected for row-count
   drift, source-readiness drift, frequency receiver-count drift, scale-
   diagnostic drift, shape-marker drift, non-finite receiver rows, downstream
   promotion, figure-validation drift, and script-snapshot drift. There are
   zero unexpected outcomes. Use runs `306-308` as the guarded proxy-comparator
   diagnostic path only; calibrated amplitude agreement, real BEM/FDTD
   comparison, 3D validation, field transfer, GPU/HPC readiness, and field FWI
   remain blocked.
   Run `309` audits where that guarded proxy-comparator mismatch lives. The
   branch has seven shape-marker passes and two frequency-local shape failures
   at `0.4 GHz` and `3.0 GHz`. The scale factor still spans about `136x`,
   the minimum shape correlation is about `0.399`, and the worst edge/center
   residual ratio is about `6.95`. The 3D Bempp scattered field is mostly `Ey`
   but not purely scalar. This rejects a scale-only explanation and motivates a
   component-aware source/operator diagnostic before any calibrated agreement,
   real comparison, 3D validation, field transfer, GPU/HPC readiness, or field
   FWI claim.
   Run `310` tests whether a simple component projection repairs that
   mismatch. It evaluates seven projections over the same nine frequencies:
   vector-norm amplitude, component magnitudes, and complex component fits.
   The original vector-norm amplitude comparison remains best with seven of
   nine frequencies passing. The closest component-only model is `Ey` magnitude
   with five of nine passing, and complex component fits pass zero frequencies.
   Component projection therefore does not repair the proxy comparator; the
   next useful branch is a source/operator diagnostic.
   Run `311` tests low-order receiver-line operator bases for that source/
   operator diagnostic. The scale-only baseline passes seven of nine
   frequencies. An edge-plus-gradient operator is the simplest model that
   passes all nine frequencies, and an edge-gradient-curvature operator is the
   lowest-error model with mean fit L2 about `0.0437` and max fit L2 about
   `0.0974`. This is a diagnostic signal for a receiver-aperture/source-
   operator mismatch, not a physical BEM/FDTD agreement claim, because the
   operator is fitted on the same receiver grid and still needs holdout
   validation.
   Run `312` validates the saved run `311` receiver-operator basis probe. Eight
   of eight checks pass, confirming policy/counts/source readiness, the expected
   model-feature contract, frequency-row consistency, baseline/best/minimum
   pass-all summary metrics, the diagnostic-only gate state, blocked downstream
   states, figure output, and script snapshots. Sensitivity remains required
   before treating the receiver-operator validator as guarded.
   Run `313` stress-tests that validator. The exact run `311` receiver-operator
   artifact set passes, while 42 damaged variants fail as expected for operator
   rows, model-summary rows, baseline/best/minimum-pass-all metrics, diagnostic
   and physical-claim gate drift, downstream promotion, figure-validation drift,
   and script-snapshot drift. There are zero unexpected outcomes. Use runs
   `311-313` as a guarded receiver-operator diagnostic branch only; physical
   operator claims and calibrated BEM/FDTD agreement remain blocked until
   holdout validation exists.
   Run `314` audits whether such holdout validation data already exist. Seven
   candidate sources are checked, including the fine-mesh Bempp reference,
   paired scalar proxy, BEM-derived synthetic sensitivity/preflight rows,
   half-space synthetic pairwise rows, trace-root negative-control rows, and
   2D archive B-scans. None are independent schema-compatible holdouts for the
   run `311` operator. The next required artifact is an independent fine-mesh
   target/background frequency-export pair on the `31 receiver x 9 frequency`
   grid with a matching BEM reference.
   Run `315` converts that blocker into a concrete holdout design packet. It
   specifies nine required future artifacts, seven acceptance checks, and 27
   frozen run `311` operator coefficient rows across identity-scale,
   edge-and-gradient, and edge-gradient-curvature models. The future holdout
   must apply the frozen operators without refitting on the holdout data. No
   holdout data are present yet, so the receiver-operator diagnostic, physical
   BEM/FDTD agreement, 3D validation, field transfer, GPU/HPC, and field FWI
   remain blocked.
   Run `316` validates that design packet from saved artifacts. Eight of eight
   checks pass, confirming the packet counts, exact nine-file unfilled
   worklist, seven acceptance checks, 27 apply-only frozen-operator rows,
   blocked holdout/downstream states, source lineage, nonblank figure output,
   and script snapshots. The design packet is now a guarded worklist only; no
   independent holdout data are present yet.
   Run `317` stress-tests that validator. The exact run `315` packet passes,
   while 40 damaged variants fail as expected for required-file worklist drift,
   acceptance-check drift, frozen-operator drift, source-summary drift,
   downstream promotion, source-lineage loss, figure-validation drift, and
   script-snapshot drift. There are zero unexpected outcomes. Use runs
   `315-317` as the guarded receiver-operator holdout design-packet block.
   Run `318` turns the guarded holdout design packet into an ordered
   non-executed command plan with seven phases: independent pair definition,
   BEM holdout export, FDTD target export, FDTD background export, scattered
   derivation, no-refit operator application, and holdout validation. No
   commands execute now, no GPU/HPC work is requested, no holdout data are
   present, and physical BEM/FDTD, 3D, field-transfer, GPU/HPC, and field-FWI
   claims remain blocked.
   Run `319` validates that command plan from saved artifacts. Seven of seven
   checks pass, confirming source counts, phase order, no-refit contract,
   non-executed/non-GPU command state, comment-only command script, blocked
   downstream states, nonblank figure output, and script snapshots. The holdout
   command plan is guarded but remains non-executed until independent holdout
   geometry and data exist.
   Run `320` stress-tests that command-plan validator. The exact run `318`
   no-refit plan passes, while 15 damaged variants fail as expected for
   source-count drift, phase drift, no-refit contract drift, accidental
   execution, GPU/HPC requirement drift, command-script drift, downstream
   promotion, figure-validation drift, and script-snapshot drift. There are
   zero unexpected outcomes. Use runs `318-320` as the guarded non-executed
   receiver-operator holdout command-plan block.
   Run `321` audits the frozen receiver-operator coefficients from the run
   `315` holdout design packet. The same-data fits still pass for
   `edge_and_gradient` and `edge_gradient_curvature`, but the coefficients are
   not stable physical transfer functions: all eight coefficient series span at
   least `100x` in absolute magnitude and five series change sign across
   frequency. This keeps the receiver-operator branch diagnostic-only until
   independent no-refit holdout data exist.
   Run `322` validates that coefficient-stability audit from saved artifacts.
   Six of six checks pass, confirming the source counts, exact stability-risk
   metrics, diagnostic-only status of the pass-all models, blocked downstream
   states, figure output, and script snapshots. Use run `322` as the validator
   for the BEM coefficient-stability no-promotion audit.
   Run `323` stress-tests that validator. The exact run `321` audit passes,
   while 12 damaged variants fail as expected for coefficient-row drift,
   frequency-row drift, summary-count drift, sign-flip drift, dynamic-range
   drift, stability-concern drift, pass-all model drift, false downstream
   promotion, figure-validation drift, and script-snapshot drift. There are
   zero unexpected outcomes. Use runs `321-323` as the guarded BEM
   coefficient-stability no-promotion block.
   Run `324` audits whether that coefficient instability can be explained by
   ill-conditioned same-data operator fits from run `311`. It checks 90
   operator-frequency rows across 10 operator models. No row exceeds the
   condition-number threshold of 100, and the maximum condition number is about
   `14.4`, while both pass-all models still have coefficient L2 dynamic range
   above `100x`. This means condition-number repair alone is not the next useful
   BEM fix; the branch still needs an independent no-refit holdout or a
   physically constrained smooth operator design before any physical BEM/FDTD,
   3D validation, field-transfer, GPU/HPC, or field-FWI claim.
   Run `325` validates run `324` from saved artifacts. Six of six checks pass,
   confirming source counts, the low condition-number attribution, the pass-all
   model identity, blocked downstream states, figure output, and script
   snapshots. Use runs `324-325` as the guarded no-conditioner-repair block.
   Run `326` tests whether the pass-all same-data receiver operators can be
   replaced by low-degree smooth coefficient curves across frequency. Twelve
   smooth candidates are tested across the two pass-all models and polynomial
   degrees zero through five. Ten candidates reduce coefficient L2 dynamic
   range below `100x`, but none preserves all nine frequency passes. The best
   smooth candidate still passes only seven of nine frequencies, with maximum
   relative L2 fit error about `1.17` compared with the original pass-all
   maximum of about `0.141`. Simple coefficient smoothing is therefore not a
   sufficient BEM repair; the branch still needs an independent no-refit
   holdout or a new physically constrained operator family.
   Run `327` validates the run `326` smooth-coefficient no-repair result from
   saved artifacts. Seven of seven checks pass, confirming the candidate count,
   zero pass-all smooth candidates, best smooth candidate identity, smoothing
   tradeoff, blocked downstream states, figure output, and script snapshots.
   Use runs `326-327` as the guarded smooth-coefficient no-repair block.
   Run `328` audits the BEM/project-grid adapter lineage that begins at run
   `037`. Ten of eleven lineage rows are accepted. The only blocked row is the
   known raw continuous analytic-field replacement path from run `039`. The
   accepted branch is the project-grid target-cell adapter path: run `038`
   implements the run `037` contract, runs `041-048` validate the
   project-domain target-cell Green-surface path, and runs `092-098` establish
   the reusable grid-aware homogeneous/layered payload contract. Guard checks
   confirm that historical `outputs/experiments`, field, 3D, GPU, and field-FWI
   claims remain blocked.
   Run `329` validates the run `328` lineage audit from saved artifacts. Seven
   of seven checks pass, confirming lineage counts, the ready contract-to-
   payload implementation branch, the still-blocked raw analytic-field path,
   downstream guardrails, figure output, and script snapshots. Use runs
   `328-329` as the guarded project-grid adapter lineage block.
   Run `330` stress-tests the run `329` validator. The exact run `328` audit
   passes, while nine damaged variants fail as expected for lineage-count
   drift, implementation-readiness drift, raw-analytic false promotion,
   guardrail drift, downstream promotion, figure-validation drift, and
   script-snapshot drift. There are zero unexpected outcomes. Use runs
   `328-330` as the guarded project-grid adapter lineage block.
   Run `331` audits the interface evolution from the run `037` seven-item
   adapter contract to the later run `092` and run `093` eight-item grid-aware
   payload interface. Five physical payload items are retained, two items are
   tightened into explicit grid-aware formula and controlled calibration-policy
   entries, and one new payload output item requires comparator-ready complex
   frequency-bin predictions. All eight later items are emitted by run `093`.
   Field, historical-archive, 3D, GPU, and field-FWI claims remain blocked.
   Run `332` validates the saved run `331` interface-evolution audit from
   artifacts. Eight of eight checks pass, confirming the 7-to-8 item evolution,
   the seven old-item successors, the explicit new adapter-output frequency-bin
   product, all emitted run `093` payload items, blocked downstream states,
   figure output, and script snapshots. Use runs `331-332` as the guarded
   interface-evolution block.
   Run `333` stress-tests the run `332` validator. The exact run `331` audit
   passes, while ten damaged variants fail as expected for count drift,
   old-item successor loss, output-product semantics drift, payload emission
   loss, source-validation failure, downstream promotion, figure-validation
   drift, and script-snapshot drift. There are zero unexpected outcomes. Use
   runs `331-333` as the guarded interface-evolution block.
   Run `334` replays the saved run `093` grid-aware adapter payload from its
   interface items. Recomputing the three formula variants recovers the same
   best variant, `receiver_conjugate_div_source`, and reproduces the saved
   adapter frequency bins and time-band output exactly to numerical precision:
   maximum frequency-bin delta `0.0` and maximum time-band delta `0.0`. Use run
   `334` as the executable replay checkpoint for the eight-item payload.
   Run `335` validates the saved run `334` replay audit from artifacts. Seven
   of seven checks pass, confirming stable payload shapes, recovered best
   variant and metric, zero replay deltas, passed source checks, blocked
   downstream states, figure output, and script snapshots. Use runs `334-335`
   as the guarded executable payload replay block.
   Run `336` stress-tests the run `335` replay validator. The exact run `334`
   audit passes, while nine damaged variants fail as expected for count drift,
   payload-shape drift, best-variant drift, nonzero replay deltas, source-check
   failure, downstream promotion, figure-validation drift, and script-snapshot
   drift. There are zero unexpected outcomes. Use runs `334-336` as the guarded
   executable payload replay block.
   Run `337` audits whether the older run `094` fresh-case stress outputs can
   meet the stricter executable replay standard demonstrated by run `334`.
   All three run `094` fresh cases passed their numerical adapter comparison,
   but each saved case lacks three formula inputs needed for independent replay:
   Tx background fields, Rx background fields, and the source spectrum. Use run
   `337` as the fresh-case replay boundary and require future fresh-case stress
   scripts to save the full replay payload per case.
   Run `338` validates the saved run `337` boundary from artifacts. Seven of
   seven checks pass, confirming the fresh-case counts, replay-payload item
   counts, stable per-case missing inputs, the ready single-payload replay
   source, blocked downstream states, figure output, and script snapshots. Use
   runs `337-338` as the guarded fresh-case replay-boundary block.
   Run `339` stress-tests the run `338` validator. The exact run `337`
   boundary passes, while 11 damaged variants fail as expected for count drift,
   pass-count drift, metric drift, replay-item drift, missing-input identity
   drift, comparator-output drift, downstream promotion, figure-validation
   drift, and script-snapshot drift. There are zero unexpected outcomes. Use
   runs `337-339` as the guarded fresh-case replay-boundary block.
   Run `340` duplicates the run `094` fresh homogeneous stress path and saves
   the full formula-replay payload for each of the three fresh cases. This is
   the concrete repair for the run `337` artifact-completeness boundary: the
   numerical fresh-case pass is retained, and each case now saves Tx background
   fields, Rx background fields, and source spectrum in addition to the adapter
   and FDTD comparison arrays. Use run `340` as the full-payload fresh-case
   stress checkpoint before independent saved-payload replay.
   Run `341` independently replays the saved run `340` full-payload arrays.
   All three fresh cases recover the saved best variant and reproduce the
   adapter frequency bins and time-band outputs to numerical precision. Use run
   `341` as the executable replay checkpoint for the full-payload fresh-case
   branch before validator and sensitivity hardening.
   Run `342` validates the saved run `341` replay audit from artifacts. Six of
   six checks pass, confirming source readiness, recovered best variants, zero
   replay deltas, blocked downstream states, figure output, and script
   snapshots. Use runs `340-342` as the guarded full-payload replay checkpoint.
   Run `343` stress-tests the run `342` validator. The exact run `341` audit
   passes, while 11 damaged variants fail as expected for count drift,
   replay-ready count drift, best-variant drift, metric drift, replay-delta
   drift, downstream promotion, figure-validation drift, and script-snapshot
   drift. There are zero unexpected outcomes. Use runs `340-343` as the guarded
   full-payload fresh-case replay block.
   Run `344` synthesizes the BEM claim boundary after that replay repair. Four
   claims are guarded: the old replay gap was identified, the full-payload
   stress was created, all three saved payloads replay exactly, and the tested
   homogeneous project-grid adapter branch is now replayable from saved formula
   payloads. Three broader claims remain blocked: broad BEM replacement, field
   transfer/measured evidence, and GPU/3D/HPC/field-FWI escalation.
   Run `345` validates the saved run `344` claim boundary from artifacts. Six
   of six checks pass, confirming claim counts, full-payload replay counts,
   blocked broader claims, downstream guardrails, figure output, and script
   snapshots. Run `346` stress-tests that validator: the exact run `344`
   claim boundary passes, while 11 damaged variants fail as expected for claim
   count drift, replay-count drift, replay-delta drift, false blocked-claim
   promotion, downstream promotion, figure-validation drift, and
   script-snapshot drift. There are zero unexpected outcomes. Use runs
   `344-346` as the guarded full-payload replay claim-boundary block.
   Run `347` audits whether that guarded full-payload replay repair makes a
   real matched BEM/FDTD comparison executable. Three support gates are ready:
   the homogeneous full-payload replay block, the real-trace intake manifest,
   and the return-readiness pack. Eight gates remain blocked, including seven
   real-data blockers: 26 missing target/background projected scalar FDTD
   traces, scalar projection convention, time-zero reference, amplitude
   reference, frequency extraction, paired residual table, and calibrated
   thresholds. The next BEM/FDTD step is staging those real traces and
   references, not more replay repair.
   Run `348` validates the saved run `347` real-pair execution readiness audit
   from artifacts. Eight of eight checks pass, confirming gate counts, support
   gate readiness, required real-artifact counts, blocked real-pair states,
   blocked downstream states, blocker reasons, figure output, and script
   snapshots. Use run `348` as the validator for the post-replay BEM real-pair
   execution gate.
   Run `349` stress-tests that validator. The exact run `347` audit passes,
   while 16 damaged variants fail as expected for gate-count drift, support
   readiness drift, required real-artifact count drift, false real-pair
   promotion, downstream promotion, missing blocker reasons, figure-validation
   drift, and script-snapshot drift. There are zero unexpected outcomes. Use
   runs `347-349` as the guarded post-replay BEM real-pair execution gate.
   Run `350` converts that gate into a file-level FDTD export packet contract:
   26 projected scalar FDTD traces, eight metadata/control files, 217
   acceptance checks, 234 expected FDTD frequency-bin rows, and 117 expected
   paired residual rows. This is a handoff contract only; real packet files,
   real BEM/FDTD comparison, threshold calibration, broad replacement, 3D
   validation, GPU/HPC work, field transfer, and field FWI remain blocked until
   the packet is staged and validated.
   Run `351` validates the saved run `350` packet contract from artifacts.
   Seven of seven checks pass, confirming packet counts, trace-role coverage,
   receiver keys, metadata/control items, expected frequency and residual row
   counts, blocked execution states, figure output, and script snapshots.
   Run `352` stress-tests that validator. The exact run `350` packet contract
   passes, while 12 damaged variants fail as expected for packet count drift,
   trace row loss, receiver-key drift, metadata drift, acceptance-count drift,
   frequency/residual row drift, false execution promotion, downstream
   promotion, figure-validation drift, and script-snapshot drift. Use runs
   `350-352` as the guarded real-pair export packet contract.
   Run `353` converts that guarded contract into an ordered non-executed staging
   command plan with eight phases: packet directories, projected trace export,
   metadata/reference controls, checksums, FDTD frequency extraction,
   BEM/FDTD paired residuals, threshold calibration, and acceptance validators.
   All commands are intentionally commented out. Use run `353` as the handoff
   command plan, not as evidence that real packet files have been staged.
   Run `354` validates the saved run `353` command plan from artifacts. Eight
   of eight checks pass, confirming plan counts, phase order and dependencies,
   expected output counts, non-executed command semantics, source-contract
   linkage, blocked real-execution states, figure output, and script snapshots.
   Run `355` stress-tests that validator. The exact run `353` plan passes,
   while 13 damaged variants fail as expected for plan-count drift, phase-order
   drift, dependency drift, output-count drift, command execution promotion,
   uncommented command text, source-link drift, false real-packet promotion,
   downstream promotion, figure-validation drift, and script-snapshot drift.
   Use runs `353-355` as the guarded real-pair packet staging command-plan block.
   Run `356` audits the current expected filesystem packet root against the
   guarded run `350` packet contract and run `353-355` command-plan block. No
   required packet files are present: all 34 packet items are missing, including
   26 projected FDTD traces and eight metadata/control artifacts. The open
   staging work reduces to four action groups: stage projected traces, stage
   primary metadata/references, derive frequency export artifacts, and derive
   paired residuals/thresholds. Real BEM/FDTD comparison, threshold
   calibration, GPU work, field transfer, field FWI, and 3D validation remain
   blocked until the packet is actually staged and revalidated.
   Run `357` validates the saved run `356` filesystem gap audit from artifacts.
   Eight of eight checks pass, confirming the guarded packet contract, 34
   missing packet files, 26 missing projected traces, eight missing
   metadata/control artifacts, four open action groups, expected frequency and
   residual row counts, blocked downstream states, figure output, and script
   snapshots.
   Run `358` stress-tests that validator. The exact run `356` gap audit passes,
   while 14 damaged variants fail as expected for source identity drift,
   contract-guard drift, packet-count drift, false file presence, missing-file
   group drift, action-row drift, derived row-count drift, downstream
   promotion, figure-validation drift, and script-snapshot drift. Use runs
   `356-358` as the guarded BEM real-pair packet filesystem gap-audit block.
   Run `359` refreshes the BEM claim boundary after that filesystem gap audit.
   The current boundary contains 11 claims: eight guarded and three blocked.
   The real-pair gate, packet contract, staging plan, and filesystem gap audit
   are guarded, but all 34 expected packet files remain missing, including 26
   projected FDTD traces and eight metadata/control artifacts. Real BEM/FDTD
   comparison, broad BEM replacement, field transfer, 3D validation, GPU work,
   and field FWI remain blocked until the packet is staged and revalidated.
   Run `360` validates that saved run `359` claim boundary from artifacts. Nine
   of nine checks pass, confirming the claim counts, guarded support blocks,
   claim-row order, blocked claim rows, packet gap counts, downstream blocked
   states, figure output, and script snapshots.
   Run `361` stress-tests that validator. The exact run `359` claim boundary
   passes, while 21 damaged variants fail as expected for claim-count drift,
   guarded support drift, claim-row drift, packet-gap drift, false downstream
   promotion, figure-validation drift, and script-snapshot drift. There are zero
   unexpected outcomes. Use runs `359-361` as the guarded BEM real-pair packet
   gap claim-boundary block.
   Run `362` converts that guarded packet gap boundary into a rerunnable
   return-packet acceptance gate. Two source/inventory gates are ready: guarded
   source contracts are available, and the expected 34-file packet inventory is
   known. Six data/execution gates remain blocked because no required packet
   files are present: all 34 items are missing, including 26 projected FDTD
   traces and eight metadata/control artifacts. Use run `362` as the acceptance
   gate for future returned BEM/FDTD packet files; do not run real comparison,
   threshold calibration, GPU work, field transfer, field FWI, or 3D validation
   until it passes.
   Run `363` validates the saved run `362` acceptance gate from artifacts.
   Seven of seven checks pass, confirming acceptance-gate counts, gate order,
   packet file rows, action-group rows, downstream blocked states, figure
   validation, and script snapshots. Sensitivity hardening remains required
   before treating the acceptance gate as fully guarded.
   Run `364` stress-tests that validator. The exact run `362` gate passes,
   while 14 damaged variants fail as expected for gate-count drift,
   packet-presence promotion, gate-order drift, blocked-reason removal,
   packet-row drift, action-count drift, downstream promotion, figure-validation
   drift, and script-snapshot drift. Use runs `362-364` as the guarded BEM
   real-pair return-packet acceptance gate. Real comparison and threshold
   calibration remain blocked until a complete packet is present and passes
   this gate.
   Run `365` folds that guarded acceptance gate into the BEM claim boundary.
   The boundary now has 12 claims: nine guarded and three blocked. The new
   guarded claim states that the return-packet acceptance gate is available;
   real packet files, real comparison, threshold calibration, broad BEM
   replacement, field transfer, GPU work, and 3D validation remain blocked
   until the packet is present and passes the gate.
   Run `366` validates the saved run `365` BEM post-acceptance claim boundary
   from artifacts. Seven of seven checks pass, confirming claim counts, the
   acceptance-gate claim row, acceptance-gate metrics, blocked claim rows,
   downstream blocked states, figure validation, and script snapshots.
   Run `367` stress-tests that validator. The exact run `365` boundary passes,
   while nine damaged variants fail as expected for source identity drift,
   claim-count drift, acceptance-gate claim drift, acceptance metric drift,
   blocked-row drift, downstream promotion, figure-validation drift, and
   script-snapshot drift. Use runs `365-367` as the guarded BEM
   post-acceptance claim-boundary block.
   Run `368` creates a non-evidence intake worksheet for the future returned
   BEM/FDTD packet. It writes 34 packet-item templates plus a README inside the
   run folder only: 26 projected trace templates and eight metadata/control
   templates. The expected real packet root remains absent, no packet files are
   staged, and real comparison, threshold calibration, GPU work, field transfer,
   field FWI, and 3D validation remain blocked until real files are staged and
   the return-packet acceptance gate passes.
   Run `369` validates that saved run `368` worksheet from artifacts. Eight of
   eight checks pass, confirming worksheet counts, directory coverage,
   action-group coverage, template non-evidence status, the blocked real-packet
   state, derived row expectations, figure validation, and script snapshots.
   Sensitivity hardening remains required before treating the worksheet as a
   guarded handoff artifact.
   Run `370` stress-tests that validator. The exact run `368` worksheet passes,
   while 14 damaged variants fail as expected for count drift, action drift,
   template evidence promotion, false packet presence, downstream promotion,
   figure drift, and script-snapshot drift. Use runs `368-370` as the guarded
   BEM return-packet intake worksheet block; real comparison remains blocked
   until real packet files pass the acceptance gate.
   Run `371` folds that guarded intake worksheet into the BEM claim boundary.
   The boundary now has 13 claims: ten guarded and three blocked. The new
   guarded claim states that the 34-item BEM/FDTD return-packet worksheet is
   generated, validated, and sensitivity-hardened as a non-evidence handoff
   artifact. Real packet files, real comparison, threshold calibration, broad
   BEM replacement, field transfer, GPU work, and 3D validation remain blocked
   until the real packet passes the acceptance gate.
   Run `372` validates the saved run `371` BEM post-intake claim boundary from
   artifacts. Seven of seven checks pass, confirming claim counts, the
   intake-worksheet claim row, worksheet metrics, blocked claim rows,
   downstream blocked states, figure validation, and script snapshots.
   Run `373` stress-tests that validator. The exact run `371` boundary passes,
   while nine damaged variants fail as expected for source identity drift,
   claim-count drift, intake-worksheet claim drift, worksheet-metric drift,
   blocked-row drift, downstream promotion, figure-validation drift, and
   script-snapshot drift. Use runs `371-373` as the guarded BEM post-intake
   claim-boundary block.
   Run `374` converts the guarded return-packet worksheet into a four-stage
   dependency plan: 26 projected FDTD trace exports, four primary
   metadata/reference files, two derived frequency-export files, and two
   derived residual/threshold files. The plan is ready as a staging sequence,
   but the current archive still has zero real packet files; the acceptance
   gate, real comparison, threshold calibration, GPU work, field transfer, and
   3D validation remain blocked.
   Run `375` validates the saved run `374` staging dependency plan from
   artifacts. Seven of seven checks pass, confirming source identity, stage
   order, dependency chain, missing-file classes, blocked downstream states,
   figure validation, and script snapshots. Sensitivity hardening remains
   required before closing this staging-plan block.
   Run `376` stress-tests that validator. The exact run `374` plan passes,
   while 14 damaged variants fail as expected for stage-count drift,
   stage-order drift, missing-count drift, dependency-chain drift, readiness
   promotion, downstream promotion, figure-validation drift, and
   script-snapshot drift. Use runs `374-376` as the guarded BEM
   return-packet staging dependency block.
   Run `377` folds that guarded staging dependency block into the BEM claim
   boundary. The boundary now has 14 claims: 11 guarded and three blocked. The
   new guarded claim states that the 34 required return-packet items are
   organized into a four-stage dependency plan: 26 projected FDTD trace
   exports, four primary metadata/reference files, two frequency derivatives,
   and two residual/threshold derivatives. Real packet files, real comparison,
   threshold calibration, broad BEM replacement, field transfer, GPU work, and
   3D validation remain blocked until the real packet passes the acceptance
   gate.
   Run `378` validates the saved run `377` BEM post-staging claim boundary
   from artifacts. Seven of seven checks pass, confirming claim counts, the
   staging dependency claim row, four stages, three dependency edges, 34
   missing packet items, blocked downstream states, figure validation, and
   script snapshots. Sensitivity hardening remains required before closing this
   claim-boundary block.
   Run `379` stress-tests that validator. The exact run `377` claim boundary
   passes, while 12 damaged variants fail as expected for claim drift, staging
   row drift, staging metric drift, blocked-row drift, downstream promotion,
   figure-validation drift, and script-snapshot drift. Use runs `377-379` as
   the guarded BEM post-staging claim-boundary block. Real comparison remains
   blocked until the 34-item return packet is present and passes the acceptance
   gate.
   Run `380` returns to the 8x20 fine-mesh Bempp reference and audits finite
   receiver-aperture averaging over the saved run `113` complex receiver rows.
   Point receivers reproduce exactly, but the smallest non-point aperture
   tested, 3 receiver samples or 10.67 mm, reaches `0.08009547612144642`
   relative L2 at 3 GHz. Wider apertures are much stronger: 5 samples reach
   `0.189423069968709`, 7 samples reach `0.3151872365924616`, and 9 samples
   reach `0.44166920910128993`. This makes receiver-aperture metadata and an
   aperture/operator convention mandatory for future calibrated 3D BEM/FDTD
   returns. Runs `381-382` validate and sensitivity-harden that result: eight
   validator checks pass, the exact audit passes, and 13 damaged variants fail
   as expected. Use runs `380-382` as the guarded BEM receiver-aperture
   sensitivity block. Real comparison and 3D validation remain blocked until
   returned FDTD data specify or match the receiver-aperture convention.
   Run `383` folds that aperture result into the preferred fine-mesh BEM/FDTD
   return metadata contract. The previous run `120` template had 30 fields and
   did not specify the receiver-aperture convention. Run `383` adds five
   blocking fields for aperture model, sample count, span, operator convention,
   and the run `380` sensitivity guard, bringing the preferred return template
   to 35 fields with 34 blocking fields. Runs `384-385` validate and
   sensitivity-harden the addendum: seven validator checks pass, the exact
   addendum passes, and 13 damaged variants fail as expected. Use runs
   `383-385` as the guarded aperture metadata-addendum block before refreshing
   the real-return preflight.
   Run `386` performs that refresh. The preferred nine-bin return gate now
   requires 35 metadata fields, 34 of them blocking, including the five
   aperture/operator fields. The gate fails closed with 10 blocking failures
   because target frequency bins, background frequency bins, and the metadata
   ledger are absent from the pending return folder. Use run `386` as the
   current preferred BEM/FDTD real-return preflight. Runs `387-388` validate
   and sensitivity-harden that refreshed gate: seven validator checks pass, the
   exact run `386` artifacts pass, and 13 damaged variants fail as expected for
   source identity drift, metadata-count drift, expected-file drift,
   preflight-row drift, aperture-guard drift, downstream promotion, figure
   drift, and script-snapshot drift. Use runs `386-388` as the guarded
   aperture-aware real-return preflight block. Real comparison and 3D validation
   remain blocked until the target, background, and metadata return files exist
   and pass the gate.
   Run `389` folds the guarded aperture branch into the BEM claim boundary.
   The boundary now has 17 claims: 14 guarded and three blocked. The three new
   guarded claims cover receiver-aperture sensitivity (`380-382`), the
   aperture metadata addendum (`383-385`), and the aperture-aware real-return
   preflight (`386-388`). Runs `390-391` validate and sensitivity-harden that
   boundary: seven validator checks pass, the exact run `389` artifacts pass,
   and 12 damaged variants fail as expected for claim drift, aperture-row
   drift, preflight-metric drift, downstream promotion, figure drift, and
   script-snapshot drift. Use runs `389-391` as the current guarded BEM
   post-aperture-preflight claim-boundary block.
   Run `392` collapses the 35-field aperture-aware preflight failures from run
   `386` into four closure actions: stage target frequency bins, stage
   background frequency bins, complete the aperture-aware metadata ledger, and
   rerun the 35-field preflight. The closure requires three external return
   files and 34 blocking metadata fields, including five receiver-aperture
   addendum fields. Runs `393-394` validate and sensitivity-harden that closure
   plan: six validator checks pass, the exact run `392` artifacts pass, and
   10 damaged variants fail as expected for count drift, action-row drift,
   source-file promotion, downstream promotion, figure-validation drift, and
   script-snapshot drift. Use runs `392-394` as the guarded 35-field BEM/FDTD
   preflight closure block.
   Run `395` folds that guarded closure plan into the BEM claim boundary. The
   boundary now has 18 claims: 15 guarded and three blocked. The new guarded
   claim states that the 10 blocking preflight failures collapse into four
   closure actions requiring three external files and 34 blocking metadata
   fields. Runs `396-397` validate and sensitivity-harden the boundary: seven
   validator checks pass, exact run `395` artifacts pass, and 10 damaged
   variants fail as expected for claim drift, closure-row drift,
   source-readiness drift, downstream promotion, figure-validation drift, and
   script-snapshot drift. Use runs `395-397` as the current guarded BEM
   post-closure claim-boundary block.
   Run `398` converts the guarded 35-field closure plan into a concrete
   non-evidence return-template pack: two 279-row frequency-bin CSV templates
   and one 35-field metadata-ledger template. The pack exposes the remaining
   fill-in burden directly: 3348 blank frequency-component cells and 12 blank
   metadata values. Runs `399-400` validate and sensitivity-harden that pack:
   eight validator checks pass, exact run `398` artifacts pass, and 11 damaged
   variants fail as expected for source-label drift, template-count drift,
   false evidence promotion, frequency-row drift, blank-component count drift,
   metadata-field drift, aperture-key removal, downstream promotion,
   figure-validation drift, script-snapshot drift, and written-template hash
   drift. Use runs `398-400` as the guarded non-evidence 35-field BEM/FDTD
   return-template block.
   Run `401` folds that guarded template pack into the BEM claim boundary. The
   boundary now has 19 claims: 16 guarded and three blocked. The new guarded
   claim states that the future return handoff contains three packet templates:
   two 279-row frequency files and one 35-field metadata ledger. Runs `402-403`
   validate and sensitivity-harden that boundary: seven validator checks pass,
   the exact run `401` artifacts pass, and 13 damaged variants fail as expected
   for claim drift, template-metric drift, downstream promotion, figure drift,
   and script-snapshot drift. Use runs `401-403` as the current guarded BEM
   post-template-pack claim-boundary block.
   Run `404` tests the 35-field return-template pack as a consumer artifact by
   copying it into an isolated synthetic packet and filling all required
   frequency and metadata values. The synthetic packet passes all 25 preflight
   checks, filling 558 frequency rows, 3348 frequency-component cells, and 35
   metadata fields with zero blank or nonfinite values. Runs `405-406` validate
   and sensitivity-harden that smoke: seven validator checks pass, the exact
   run `404` artifacts pass, and 12 damaged variants fail as expected for count
   drift, packet-root drift, metadata-hash drift, false evidence promotion,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `404-406` as the guarded synthetic consumer-smoke block only; real
   comparison remains blocked until real returned FDTD files replace the
   synthetic packet.
   Run `407` folds the guarded synthetic consumer-smoke result into the BEM
   claim boundary. The boundary now has 20 claims: 17 guarded and three
   blocked. The new guarded claim says the 35-field return templates are
   fillable and preflight-compatible in an isolated synthetic packet; it does
   not promote synthetic values to real evidence. Runs `408-409` validate and
   sensitivity-harden that boundary: seven validator checks pass, the exact
   run `407` artifacts pass, and 13 damaged variants fail as expected for
   claim drift, smoke-metric drift, false evidence promotion, downstream
   promotion, figure drift, and script-snapshot drift. Use runs `407-409` as
   the current guarded BEM post-synthetic-fill-smoke claim-boundary block.
   Run `410` consumes that filled 35-field synthetic packet downstream by
   pairing target/background rows and computing target-minus-background
   scattered rows. It produces 279 paired scattered rows across 31 receivers
   and nine frequencies, with all 10 consumer checks passing. Runs `411-412`
   validate and sensitivity-harden that smoke: eight validator checks pass, the
   exact run `410` artifacts pass, and 14 damaged variants fail as expected for
   count drift, source-preflight demotion, consumer-check failure, row removal,
   norm drift, coordinate drift, false evidence promotion, downstream
   promotion, figure drift, and script-snapshot drift. Use runs `410-412` as a
   guarded synthetic downstream-consumer block only; real comparison remains
   blocked until real returned FDTD files replace the synthetic packet.
   Run `413` folds that guarded synthetic downstream-consumer block into the
   BEM claim boundary. The boundary now has 21 claims: 18 guarded and three
   blocked. The new guarded claim says the filled 35-field synthetic packet can
   be paired and subtracted by the downstream consumer, producing 279 scattered
   rows and 1674 scattered component cells, but the packet remains synthetic
   non-evidence. Runs `414-415` validate and sensitivity-harden that boundary:
   seven validator checks pass, exact run `413` artifacts pass, and 14 damaged
   variants fail as expected for claim drift, consumer-metric drift, coordinate
   drift, false evidence promotion, downstream promotion, figure drift, and
   script-snapshot drift. Use runs `413-415` as the current guarded BEM
   post-synthetic-comparator-smoke claim-boundary block.
   Run `416` audits the anatomy of the guarded run `410` synthetic scattered
   table. The synthetic scattered norm increases monotonically with frequency
   and receiver index in this fill, peaks at receiver `30` and `3 GHz`, and is
   dominated by the `ez` component with energy fraction `0.6703296703296703`.
   Runs `417-418` validate and sensitivity-harden that anatomy audit: six
   validator checks pass, exact run `416` artifacts pass, and 19 damaged
   variants fail as expected for source-readiness drift, table-shape drift,
   monotonicity damage, dominant-component drift, peak-location drift, evidence
   promotion, figure drift, and script-snapshot drift. Use runs `416-418` as
   the guarded synthetic scattered-anatomy block only; real comparison remains
   blocked until real returned FDTD files replace the synthetic packet.
   Run `419` folds the guarded synthetic scattered-anatomy result into the BEM
   claim boundary. The boundary now has 22 claims: 19 guarded and three
   blocked. The new guarded claim says the synthetic scattered table has
   structured consumer anatomy: 31 receivers, nine frequencies, dominant `ez`
   component, peak receiver `30`, peak frequency `3 GHz`, and peak scattered
   norm `1.7743269146355192`. Runs `420-421` validate and sensitivity-harden
   that boundary: six validator checks pass, exact run `419` artifacts pass,
   and 15 damaged variants fail as expected for count drift, anatomy-readiness
   drift, evidence-text drift, metric drift, blocked-row drift, downstream
   promotion, figure drift, and script-snapshot drift. Use runs `419-421` as
   the current guarded BEM post-synthetic-scattered-anatomy claim-boundary
   block.
   Run `422` derives a comparison-normalization policy from the guarded
   35-field synthetic scattered table. The raw synthetic scattered norm spans
   `232.5x` and is monotonic with frequency and receiver index, while dividing
   by frequency in GHz and receiver index plus one collapses the synthetic
   scale to a nearly constant coefficient: mean `0.01907878402833891`,
   coefficient of variation `2.0884850334665626e-16`, and range
   `1.0408340855860843e-17`. Runs `423-424` validate and sensitivity-harden
   that policy: six validator checks pass, exact run `422` artifacts pass, and
   17 damaged variants fail as expected for readiness drift, count drift,
   coefficient-spread drift, raw-metric promotion, normalized-metric demotion,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `422-424` as the guarded synthetic scattered normalization-policy block for
   future real BEM/FDTD packet comparison. Raw synthetic magnitude remains
   diagnostic only; real comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until real returned FDTD files
   replace the synthetic packet.
   Run `425` folds that guarded normalization-policy result into the BEM claim
   boundary. The boundary now has 23 claims: 20 guarded and three blocked. The
   new guarded claim preserves raw synthetic magnitude as diagnostic only and
   requires the frequency-receiver normalized metric before any future real
   comparison claim. Runs `426-427` validate and sensitivity-harden that
   boundary: five validator checks pass, exact run `425` artifacts pass, and
   18 damaged variants fail as expected for claim-count drift,
   normalization-readiness drift, metric-spread drift, evidence-text drift,
   blocked-row drift, downstream promotion, figure drift, and script-snapshot
   drift. Use runs `425-427` as the current guarded BEM
   post-normalization-policy claim-boundary block. Real comparison, 3D
   validation, GPU/HPC work, field transfer, and field FWI remain blocked until
   real returned FDTD files replace the synthetic packet.
   Run `428` applies the guarded frequency-receiver normalization as a concrete
   normalized-comparator score smoke. All 279 synthetic rows pass the `1e-12`
   residual tolerance, with maximum normalized residual
   `3.6369686315440523e-16` and maximum raw-reconstruction error
   `4.4336379508346526e-16`. Runs `429-430` validate and sensitivity-harden
   that score artifact: five validator checks pass, exact run `428` artifacts
   pass, and 27 damaged variants fail as expected for readiness drift, count
   drift, residual drift, decision-item drift, downstream promotion, figure
   drift, and script-snapshot drift. Use runs `428-430` as the guarded BEM
   synthetic normalized-comparator score-smoke block for future real returned
   packet scoring. Real comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until real returned files exist.
   Run `431` folds the guarded normalized-comparator score smoke into the BEM
   claim boundary. The boundary now has 24 claims: 21 guarded and three
   blocked. The new guarded claim records the executable synthetic score
   contract: 279 score rows, 40 axis rows, 279 passes, zero failures, maximum
   normalized residual `3.6369686315440523e-16`, and maximum
   raw-reconstruction error `4.4336379508346526e-16`. Runs `432-433` validate
   and sensitivity-harden that boundary: five validator checks pass, exact run
   `431` artifacts pass, and 20 damaged variants fail as expected for count
   drift, score-readiness drift, score-metric drift, evidence-text drift,
   blocked-row drift, downstream promotion, figure drift, and script-snapshot
   drift. Use runs `431-433` as the current guarded BEM post-score-smoke
   claim-boundary block. Real comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until real returned files exist.
   Run `434` stress-tests the guarded synthetic normalized-comparator score
   around the configured `1e-12` residual tolerance. It writes nine
   perturbation scenarios and 2511 perturbed score rows: five scenarios pass,
   four fail, 1395 rows pass, and 1116 rows fail. The nearest passing maximum
   residual is `9.50339903422461e-13`; the nearest failing residual is
   `1.0501746923583452e-12`, with first failing perturbations at `+/-1.05e-12`.
   Runs `435-436` validate and sensitivity-harden that threshold ladder: five
   validator checks pass, the exact run `434` artifacts pass, and 22 damaged
   variants fail as expected for source-readiness drift, ladder-shape drift,
   pass/fail split drift, threshold-margin drift, row-count drift, downstream
   promotion, figure drift, and script-snapshot drift. Use runs `434-436` as
   the guarded synthetic normalized-comparator threshold-ladder block. Real
   comparison, 3D validation, GPU/HPC work, field transfer, and field FWI
   remain blocked until real returned files exist.
   Run `437` folds the guarded threshold ladder into the BEM claim boundary.
   The boundary now has 25 claims: 22 guarded and three blocked. The new
   guarded claim records the nine-scenario threshold behavior and marks the
   synthetic comparator threshold calibration ready, while keeping real
   comparison, 3D validation, GPU/HPC work, field transfer, and field FWI
   blocked. Runs `438-439` validate and sensitivity-harden that boundary: five
   validator checks pass, exact run `437` artifacts pass, and 26 damaged
   variants fail as expected for claim-count drift, threshold-claim support
   drift, threshold-metric drift, blocked-row drift, downstream promotion,
   figure drift, and script-snapshot drift. Use runs `437-439` as the current
   guarded BEM post-threshold-ladder claim-boundary block.
   Run `440` converts the guarded synthetic normalized-comparator score and
   threshold contracts into a non-evidence real-return scorecard template. The
   template preserves the 31-by-9 receiver/frequency grid with 279 rows,
   carries the `1e-12` residual tolerance and reference coefficient
   `0.01907878402833891`, and leaves 1116 required real input cells blank:
   returned FDTD norm, returned BEM norm, FDTD source hash, and BEM source hash
   for each row. It also writes five acceptance rules. The template is not
   comparison evidence; real BEM/FDTD comparison, 3D validation, GPU/HPC work,
   field transfer, and field FWI remain blocked until returned real values and
   hashes exist.
   Run `441` validates that non-evidence scorecard template: five checks pass,
   the 279 template rows and 1116 blank real-return input cells are preserved,
   all template rows remain non-evidence, and the required snapshots and figure
   are present. Use runs `440-441` as the guarded real-return scorecard
   template block. Real comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until returned real BEM/FDTD values
   and source hashes exist.
   Run `442` sensitivity-hardens that validator: the exact run `440` template
   passes, and 23 damaged variants fail as expected for readiness drift,
   row-count drift, receiver/frequency count drift, filled real-return cells,
   filled generated-score cells, evidence promotion, acceptance-rule drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `440-442` as the guarded non-evidence real-return scorecard-template block.
   Run `443` folds that guarded non-evidence scorecard-template block into the
   BEM claim boundary. The boundary now has 26 claims: 23 guarded and three
   blocked. The new guarded claim records the 279-row, 31-receiver,
   nine-frequency scorecard template with 1116 required real input cells and
   five acceptance rules while keeping all rows non-evidence. Runs `444-445`
   validate and sensitivity-harden that boundary: five validator checks pass,
   exact run `443` artifacts pass, and 28 damaged variants fail as expected
   for claim-count drift, template-claim drift, metric drift, evidence
   promotion, downstream promotion, figure drift, and script-snapshot drift.
   Use runs `443-445` as the current guarded BEM post-scorecard-template
   claim-boundary block.
   Run `446` audits the precision budget for the reference coefficient used by
   that real-return scorecard template. The coefficient
   `0.01907878402833891` is guarded by a `1e-12` relative residual tolerance:
   12 significant digits fail the tolerance, while 13 significant digits pass.
   Runs `447-448` validate and sensitivity-harden that precision-budget
   result: five validator checks pass, exact run `446` artifacts pass, and 21
   damaged variants fail as expected for readiness drift, precision-count
   drift, threshold split drift, tolerance drift, zero-reference drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `446-448` as the guarded BEM reference-coefficient precision-budget block.
   Future real-return scorecards must preserve at least 13 significant digits
   for the reference coefficient.
   Run `449` folds that precision-budget block into the BEM claim boundary.
   The boundary now has 27 claims: 24 guarded and three blocked. The new
   guarded claim records the reference coefficient, the `1e-12` tolerance, the
   12-significant-digit fail point, and the 13-significant-digit pass and
   recommendation. Runs `450-451` validate and sensitivity-harden that
   boundary: five validator checks pass, exact run `449` artifacts pass, and
   29 damaged variants fail as expected for claim-count drift,
   precision-readiness drift, reference/tolerance drift, significant-digit
   drift, precision-claim drift, blocked-row drift, downstream promotion,
   figure drift, and script-snapshot drift. Use runs `449-451` as the current
   guarded BEM post-precision-budget claim-boundary block.
   Run `452` turns the 13-significant-digit rule into a concrete JSON/CSV/text
   serialization round-trip guard for future real-return scorecards. Twelve
   serialization scenarios are checked: nine pass and three fail. JSON and CSV
   text at 13 significant digits pass the `1e-12` comparator tolerance, while
   JSON and CSV text at 12 significant digits fail. The preferred production
   storage rule is full Python/JSON numeric representation or
   17-significant-digit text, with 13 significant digits as the minimum
   tolerance-preserving floor. Runs `453-454` validate and sensitivity-harden
   that guard: six validator checks pass, exact run `452` artifacts pass, and
   33 damaged variants fail as expected for readiness drift, count drift,
   reference/tolerance drift, threshold split drift, preferred-format drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `452-454` as the guarded BEM serialization round-trip block. This remains a
   scorecard-storage guard, not real BEM/FDTD comparison evidence.
   Run `455` folds that serialization round-trip block into the BEM claim
   boundary. The boundary now has 28 claims: 25 guarded and three blocked. The
   new guarded claim records the 12-scenario JSON/CSV/text storage check, the
   13-significant-digit minimum safe scorecard floor, and the
   17-significant-digit preferred storage rule. Runs `456-457` validate and
   sensitivity-harden that boundary: five validator checks pass, exact run
   `455` artifacts pass, and 31 damaged variants fail as expected for
   claim-count drift, serialization-readiness drift, reference/tolerance drift,
   serialization-metric drift, serialization-claim drift, downstream
   promotion, figure drift, and script-snapshot drift. Use runs `455-457` as
   the current guarded BEM post-serialization claim-boundary block.
   Run `458` applies the serialization rule to the non-evidence real-return
   scorecard template: all 279 rows now carry the preferred
   17-significant-digit coefficient text `0.019078784028338909`, while 1116
   real-return cells and 1116 generated-score cells remain blank. Runs
   `459-460` validate and sensitivity-harden that storage refresh: six
   validator checks pass, exact run `458` artifacts pass, and 29 damaged
   variants fail as expected for storage-rule drift, blank-cell drift,
   evidence promotion, downstream promotion, figure drift, and script-snapshot
   drift. Use runs `458-460` as the guarded storage-refreshed real-return
   scorecard-template block.
   Run `461` folds that storage-refreshed template into the BEM claim
   boundary. The boundary now has 29 claims: 26 guarded and three blocked. The
   new guarded claim records the 279-row storage-refreshed scorecard template,
   279 preferred-storage rows, 1116 blank real-return cells, 1116 blank
   generated-score cells, zero evidence rows, and the serialized reference
   coefficient `0.019078784028338909`. Runs `462-463` validate and
   sensitivity-harden that boundary: five validator checks pass, exact run
   `461` artifacts pass, and 36 damaged variants fail as expected for
   claim-count drift, storage-refresh metric drift, storage text/digit drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `461-463` as the current guarded BEM post-storage-refresh claim-boundary
   block.
   Run `464` converts that storage-refreshed 35-field scorecard into a
   non-evidence intake worksheet with 279 receiver-frequency rows and 1116
   explicit real-return requirements: two scattered-norm values and two source
   hashes per row. The worksheet keeps all 1116 cells blank, records zero
   evidence rows, and preserves the 17-significant-digit reference coefficient
   text. Runs `465-466` validate and sensitivity-harden that worksheet: six
   validator checks pass, exact run `464` artifacts pass, and 39 damaged
   variants fail as expected for count drift, row-completion drift,
   requirement-schema drift, storage-precision drift, downstream promotion,
   figure drift, and script-snapshot drift. Use runs `464-466` as the guarded
   non-evidence 35-field normalized-comparator scorecard intake worksheet
   block.
   Run `467` folds that guarded intake worksheet into the BEM claim boundary.
   The boundary now has 30 claims: 27 guarded and three blocked. The new
   guarded claim records 279 worksheet rows, 1116 required real-return cells,
   zero filled cells, zero evidence rows, 558 hash requirements, 558 norm
   requirements, and the preserved 17-significant-digit reference coefficient
   text. Runs `468-469` validate and sensitivity-harden that boundary: five
   validator checks pass, exact run `467` artifacts pass, and 37 damaged
   variants fail as expected for claim-count drift, worksheet-readiness drift,
   worksheet-metric drift, claim-support drift, downstream promotion, figure
   drift, and script-snapshot drift. Use runs `467-469` as the current guarded
   BEM post-intake-worksheet claim-boundary block.
   Run `470` converts the 1116-cell scorecard worksheet into an ordered return
   staging plan with six actions and seven dependency edges. The staged cells
   split into 558 source-hash requirements and 558 scattered-norm
   requirements, followed by 279 computed comparator rows and 279 evidence
   review rows. Runs `471-472` validate and sensitivity-harden that plan: five
   validator checks pass, exact run `470` artifacts pass, and 21 damaged
   variants fail as expected for count drift, stage-group drift, action-order
   drift, dependency-edge drift, downstream promotion, figure drift, and
   script-snapshot drift. Use runs `470-472` as the guarded BEM scorecard
   return staging-plan block.
   Run `473` folds that guarded staging plan into the BEM claim boundary. The
   boundary now has 31 claims: 28 guarded and three blocked. The new guarded
   claim records 1116 staged real-return cells, six actions, seven dependency
   edges, 558 source-hash cells, 558 scattered-norm cells, 279 computed
   comparator rows, and 279 evidence-review rows, while preserving zero filled
   real-return values. Runs `474-475` validate and sensitivity-harden that
   boundary: five validator checks pass, exact run `473` artifacts pass, and
   31 damaged variants fail as expected for claim-count drift,
   staging-readiness drift, staging-metric drift, claim-support drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `473-475` as the current guarded BEM post-return-staging-plan
   claim-boundary block.
   Run `476` converts the 1116 staged real-return cells into four concrete
   blank return-file templates: FDTD source hashes, BEM source hashes, FDTD
   scattered norms, and BEM scattered norms. Each file template has 279 entries
   over the 31-receiver by nine-frequency grid, for 1116 total blank entries.
   Runs `477-478` validate and sensitivity-harden that manifest: six validator
   checks pass, exact run `476` artifacts pass, and 32 damaged variants fail
   as expected for file-count drift, file-key drift, row-count drift,
   receiver/frequency drift, template-fill drift, template-hash drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `476-478` as the guarded BEM return-file manifest block. Real comparison,
   3D validation, GPU/HPC work, field transfer, and field FWI remain blocked
   until the four real returned files are filled with measured/computed values
   and source hashes.
   Run `479` folds that guarded return-file manifest into the BEM claim
   boundary. The boundary now has 32 claims: 29 guarded and three blocked. The
   new guarded claim records four return-file templates, 1116 blank template
   entries, 558 source-hash entries, 558 scattered-norm entries, 31 receivers,
   and nine frequencies. Runs `480-481` validate and sensitivity-harden that
   boundary: five validator checks pass, exact run `479` artifacts pass, and
   32 damaged variants fail as expected for claim-count drift,
   manifest-claim drift, manifest-metric drift, blocked-row drift,
   downstream promotion, figure drift, and script-snapshot drift. Use runs
   `479-481` as the current guarded BEM post-return-file-manifest
   claim-boundary block.
   Run `482` fills the four return-file templates with deterministic synthetic
   source hashes and synthetic scattered-norm values, then merges them into a
   279-row normalized-comparator scorecard over 31 receivers and nine
   frequencies. The run fills all 1116 entries, produces 558 valid source-hash
   entries and 558 finite scattered-norm entries, and records a mean synthetic
   normalized norm difference of 0.011899240440684099 with a maximum of
   0.017999697624207837. Runs `483-484` validate and sensitivity-harden that
   consumer smoke: six validator checks pass, exact run `482` artifacts pass,
   and 36 damaged variants fail as expected for source-readiness drift,
   fill-count drift, scorecard-count drift, hash drift, norm drift, evidence
   promotion, downstream promotion, figure drift, and script-snapshot drift.
   Use runs `482-484` as the guarded synthetic return-file consumer-smoke
   block. This proves the four-file handoff can be parsed and merged; it does
   not create real BEM/FDTD comparison evidence, 3D validation, GPU/HPC
   readiness, field transfer, or field FWI readiness.
   Run `485` folds that synthetic consumer smoke into the BEM claim boundary.
   The boundary now has 33 claims: 30 guarded and three blocked. The new
   guarded claim records four synthetic return files, 1116 filled synthetic
   entries, 279 scorecard rows, 558 valid source-hash entries, 558 finite
   scattered-norm entries, 31 receivers, nine frequencies, and zero synthetic
   values promoted as evidence. Runs `486-487` validate and sensitivity-harden
   that boundary: five validator checks pass, exact run `485` artifacts pass,
   and 30 damaged variants fail as expected for claim-count drift,
   synthetic-fill readiness drift, synthetic-fill metric drift, synthetic
   evidence promotion, downstream promotion, figure drift, and script-snapshot
   drift. Use runs `485-487` as the current guarded BEM
   post-synthetic-return-file-fill claim-boundary block. Real BEM/FDTD
   comparison evidence, 3D validation, GPU/HPC readiness, field transfer, and
   field FWI remain blocked.
   Run `488` defines the real return-file acceptance gate for replacing the
   synthetic return-file smoke with real returned BEM/FDTD files. The gate
   requires four real return files, 1116 real entries, 279 accepted real
   scorecard rows, 558 real source-hash entries, and 558 real scattered-norm
   entries before any real comparison can be promoted. The current state has
   zero accepted real files, zero accepted real entries, zero accepted real
   scorecard rows, and no accepted real return packet. Runs `489-490` validate
   and sensitivity-harden that gate: five validator checks pass, exact run
   `488` artifacts pass, and 34 damaged variants fail as expected for
   gate-count drift, premature real-file acceptance, premature real-entry
   acceptance, scorecard acceptance, packet acceptance, downstream promotion,
   figure drift, and script-snapshot drift. Use runs `488-490` as the guarded
   real return-file acceptance-gate block.
   Run `491` folds that guarded real return-file acceptance gate into the BEM
   claim boundary. The boundary now has 34 claims: 31 guarded and three
   blocked. The new guarded claim records four required real return files,
   1116 required real entries, 279 required real scorecard rows, 558 source
   hash requirements, 558 scattered-norm requirements, zero accepted real
   files, zero accepted real entries, zero accepted real scorecard rows, and
   no accepted real packet. Runs `492-493` validate and sensitivity-harden that
   boundary: five validator checks pass, exact run `491` artifacts pass, and
   33 damaged variants fail as expected for claim-count drift,
   acceptance-gate readiness drift, acceptance-gate metric drift, premature
   packet acceptance, downstream promotion, figure drift, and script-snapshot
   drift. Use runs `491-493` as the current guarded BEM
   post-real-return-file-acceptance claim-boundary block.
   Run `494` audits the filesystem against the four real return-file names
   required by the acceptance gate. The scan finds zero real-return candidates
   and four open required-path gaps. The eight matching filenames currently on
   disk are non-evidence copies: four blank templates and four synthetic
   reference files. Runs `495-496` validate and sensitivity-harden that audit:
   five validator checks pass, exact run `494` artifacts pass, and 21 damaged
   variants fail as expected for scan-count drift, real-file promotion,
   template/synthetic misclassification, non-evidence promotion, downstream
   promotion, figure damage, and script-snapshot damage. Use runs `494-496` as
   the guarded real-return filesystem gap-audit block.
   Run `497` folds that filesystem gap audit into the BEM claim boundary. The
   boundary now has 35 claims: 32 guarded and three blocked. The new guarded
   claim records four open real-return gaps, zero real-return candidates, four
   blank-template matches, and four synthetic-reference matches. Runs
   `498-499` validate and sensitivity-harden that boundary: five validator
   checks pass, exact run `497` artifacts pass, and 26 damaged variants fail as
   expected for claim-count drift, claim-support drift, filesystem metric
   drift, accepted-real-count promotion, downstream promotion, figure damage,
   and script-snapshot damage. Use runs `497-499` as the current guarded BEM
   post-real-return-filesystem-gap claim-boundary block.
   Run `500` audits the producer side of that gap. The four required real
   return files require 1116 accepted real entries across 279 scorecard rows.
   The audit finds zero exact producer scripts that write the accepted
   `real_return_files` CSV contract, while recording 176 partial local
   implementation references to FDTD/BEM/scattered-norm machinery. The current
   state is therefore not a consumer/template problem: the next BEM progress is
   to build or receive the exact FDTD and BEM producer outputs, then rerun the
   real return-file acceptance gate and normalized-comparator scorecard. Runs
   `501-502` validate and sensitivity-harden that producer-route audit: five
   validator checks pass, exact run `500` artifacts pass, and 30 damaged
   variants fail as expected for count drift, route-row drift, exact-producer
   promotion, producer-gap metric drift, action-row drift, template/synthetic
   completion leakage, downstream promotion, figure damage, and script-snapshot
   damage. Use runs `500-502` as the guarded BEM producer-route audit block.
   Real BEM/FDTD comparison, 3D validation, GPU/HPC work, field transfer, and
   field FWI remain blocked.
   Run `503` audits historical Bempp-side coverage against the exact 35-field
   producer grid: 31 receivers by nine frequencies, or 279 rows. It scans 145
   candidate summaries, including 106 with grid metadata and 54 Bempp runtime
   candidates. The audit finds 41 total 31x9 metadata matches and one
   Bempp-tagged 31x9 metadata match, but zero exact 35-field Bempp producer
   candidates. Run `504` validates that audit with four passing checks. Run
   `505` sensitivity-hardens the validator: the exact artifacts pass, while 10
   damaged variants fail as expected for count drift, exact-producer
   promotion, downstream comparison promotion, figure damage, and
   script-snapshot damage. The BEM-side next step is therefore still an
   explicit 9-frequency Bempp export plus a `real_return_files` writer, not
   promotion of existing metadata as real comparison evidence.
   Run `506` converts that conclusion into an implementation contract. The
   accepted real-return producer must write four 279-row CSV files: FDTD source
   hashes, BEM source hashes, FDTD scattered-field norms, and BEM
   scattered-field norms. The schema is ready over the 31-receiver by
   nine-frequency grid, but three implementation blockers remain: the FDTD
   exporter, the BEM exporter, and the accepted return-file writer are all
   absent. Run `507` validates that contract with five passing checks,
   confirming the four required return files, the 31-by-9 schema, the three
   open implementation blockers, and the blocked downstream state. Run `508`
   sensitivity-hardens that validator: the exact run `506` artifacts pass, and
   eight damaged variants fail as expected for missing return-file rows,
   entry-count drift, schema frequency drift, premature exporter availability,
   exact-producer promotion, real-return promotion, figure damage, and
   script-snapshot damage. Real return production and real BEM/FDTD comparison
   remain blocked.
   Run `509` adds and audits a guarded return-file writer interface. The
   interface validates all four accepted return-file keys, rejects an unknown
   key, and refuses real-write requests. No accepted file is written and no
   evidence state is promoted. Run `510` validates that interface with five
   passing checks, confirming all four keys, unknown-key rejection, real-write
   refusal, no evidence writes, and blocked downstream states. Run `511`
   sensitivity-hardens the validator: exact artifacts pass, while eight
   damaged variants fail as expected for audit count drift, missing key rows,
   evidence promotion, blocker-count drift, downstream comparison promotion,
   figure damage, and script-snapshot damage. The remaining real-return
   blockers are now the BEM exporter, the FDTD exporter, and a later real-write
   implementation path with real values and provenance.
   Run `512` adds and audits the guarded Bempp-side exporter interface. The
   interface verifies the two Bempp return-file keys, rejects an FDTD-side key,
   rejects an unknown key, and refuses real Bempp export requests. Five of five
   audit cases pass. No real values are exported, no accepted return file is
   written, and real return production, real BEM/FDTD comparison, 3D validation,
   GPU/HPC work, field transfer, and field FWI remain blocked. Run `513`
   validates that interface audit with five passing checks, confirming both
   Bempp keys, wrong-key rejection, real-export refusal, no evidence writes,
   three remaining real-return blockers, and the blocked downstream state. Run
   `514` sensitivity-hardens that validator: exact artifacts pass, while nine
   damaged variants fail as expected for audit-count drift, a missing Bempp
   key row, fake real export, accepted-file promotion, hidden evidence
   readiness, blocker drift, downstream comparison promotion, figure damage,
   and script-snapshot damage.
   Run `515` adds and audits the matching guarded FDTD-side exporter
   interface. The interface verifies the two FDTD return-file keys, rejects a
   Bempp-side key, rejects an unknown key, and refuses real FDTD export
   requests. Five of five audit cases pass. No real values are exported, no
   accepted return file is written, and real return production remains blocked.
   Run `516` validates that interface audit with five passing checks,
   confirming both FDTD keys, wrong-key rejection, real-export refusal, no
   evidence writes, three remaining real-return blockers, and the blocked
   downstream state. Run `517` sensitivity-hardens that validator: exact
   artifacts pass, while nine damaged variants fail as expected for
   audit-count drift, a missing FDTD key row, fake real export, accepted-file
   promotion, hidden evidence readiness, blocker drift, downstream comparison
   promotion, figure damage, and script-snapshot damage. Run `518` synthesizes
   the 35-field real-return interface completion boundary. The producer
   contract, writer guard, Bempp exporter guard, and FDTD exporter guard are
   all ready for contract checks, but real-value readiness remains zero and
   accepted-evidence readiness remains zero. The three open implementation
   actions are real Bempp value export, real FDTD value export, and then an
   evidence-producing writer path after real values and provenance exist. Run
   `519` validates that boundary with five passing checks, confirming the four
   guarded interfaces, required four return files, 1116 entries, 279 scorecard
   rows, three ordered implementation actions, zero real values, zero accepted
   evidence files, and blocked downstream states. Run `520`
   sensitivity-hardens that validator: exact artifacts pass, while ten damaged
   variants fail as expected for guarded-interface count drift, fake real-value
   readiness, fake accepted-evidence readiness, required-count drift,
   action-order damage, early evidence permission, blocker-count drift,
   downstream comparison promotion, figure damage, and script-snapshot damage.
   Run `521` makes the first BEM-side candidate-value export for the 35-field
   return schema. It computes 279 Bempp scattered-norm values and 279 BEM
   source-lineage hashes over the required 31-receiver by nine-frequency grid.
   The candidate export is complete and finite, but it is not accepted
   comparison evidence because it uses a 4x12 homogeneous PEC cylinder rather
   than the fine 8x20 reference mesh, the matched FDTD return files are absent,
   and the accepted evidence writer remains blocked.
   Run `522` validates that candidate export with five passing checks:
   complete candidate counts, preserved return-file schema, nine ready
   frequency rows on the 31-receiver grid, blocked acceptance/downstream
   states, and nonblank figure/script snapshots.
   Run `523` sensitivity-hardens that validator. The exact run `521` artifacts
   pass, while ten damaged variants fail as expected for count drift, missing
   BEM norm rows, bad source hashes, nonpositive norms, failed frequency rows,
   false fine-mesh promotion, accepted-evidence promotion, downstream
   comparison promotion, figure damage, and script-snapshot damage. Use runs
   `521-523` as the guarded BEM-side candidate-value export block.
   Run `524` tests the required 8x20 fine mesh at the 400 MHz and 3 GHz
   endpoints. Both endpoint solves complete with a closed 360-element mesh and
   540 RWG degrees of freedom. The 4x12-to-8x20 relative L2 change is 0.0389 at
   400 MHz and 0.2535 at 3 GHz, with an estimated full nine-frequency runtime
   of about 193 seconds. This justifies a full 8x20 Bempp-side candidate export
   while keeping matched FDTD returns and accepted comparison evidence blocked.
   Run `525` performs that full 8x20 nine-frequency candidate export. All nine
   Bempp solves complete, producing 279 BEM source-lineage hashes and 279 BEM
   scattered-norm values in the 35-field return-file schema. The BEM-side
   fine-mesh candidate export is ready, but accepted BEM/FDTD comparison
   remains blocked because the matched FDTD return files and accepted writer
   are still absent.
   Run `526` validates the run `525` fine-mesh candidate export with five
   passing checks: complete candidate values, preserved return-file schema,
   nine 8x20 frequency rows, blocked acceptance/downstream states, and nonblank
   figure/script snapshots.
   Run `527` sensitivity-hardens that validator. The exact run `525` artifacts
   pass, while ten damaged variants fail as expected for candidate-count drift,
   missing norm rows, bad source hashes, nonpositive norms, failed frequency
   rows, mesh-element drift away from 8x20, accepted-evidence promotion,
   downstream comparison promotion, figure damage, and script-snapshot damage.
   Use runs `525-527` as the guarded 8x20 BEM-side candidate-value export
   block. The remaining comparison blockers are matched FDTD returns and the
   accepted evidence writer.
   Run `528` turns the completed 8x20 BEM rows into an explicit matched-FDTD
   handoff design. It writes two required FDTD return tables with 279 rows each
   and a 279-row comparison pairing table aligned to the same 31-receiver by
   nine-frequency grid. BEM values are ready, FDTD values are absent, comparison
   rows are not ready, and the two remaining blockers are real FDTD return
   values and the accepted evidence writer. Run `529` validates the handoff
   with five passing checks: guarded source readiness, FDTD row counts and key
   alignment, absent FDTD values, blocked downstream states, and figure/script
   snapshots. Run `530` sensitivity-hardens that validator. The exact run `528`
   artifacts pass, while 11 damaged variants fail as expected for source
   readiness damage, row-count drift, key-alignment damage, premature FDTD
   value promotion, premature comparison promotion, accepted-writer promotion,
   action-order damage, figure damage, and script-snapshot damage. Use runs
   `528-530` as the guarded matched-FDTD handoff block after the fine-mesh BEM
   export. Run `531` turns that handoff into two concrete guarded FDTD
   contract-check commands, one for the source-hash manifest and one for the
   scattered-norm values. Both commands pass contract-check probes over 279
   required rows each, while real FDTD export commands, FDTD values, accepted
   evidence, comparison readiness, 3D validation, GPU/HPC work, field transfer,
   and field FWI remain blocked. Run `532` validates that command inventory
   with four passing checks: guarded source chain, two hashed contract-check
   outputs, blocked real FDTD export, and figure/script snapshots. Run `533`
   sensitivity-hardens that validator: the exact run `531` artifacts pass,
   while ten damaged variants fail as expected for source-chain damage,
   command-count drift, missing command rows, hash drift, payload/row real
   export promotion, real-command promotion, downstream promotion, figure
   damage, and script-snapshot damage. Use runs `531-533` as the guarded
   matched-FDTD contract-check command block before implementing real FDTD
   return-value export. Run `534` probes the real-export path for the two FDTD
   return-file keys. Both probes are refused with exit code 2, no FDTD return
   values are exported, no accepted return files are written, and comparison,
   3D validation, GPU/HPC work, field transfer, and field FWI remain blocked.
   The next BEM-side implementation step is real FDTD value export and
   validation, followed by the accepted evidence writer only after both BEM and
   FDTD real values exist. Run `535` validates that gap audit with five passing
   checks: source readiness, two real-export refusals, four implementation
   blockers, blocked comparison/downstream states, and figure/script
   snapshots. Run `536` sensitivity-hardens that validator: exact run `534`
   artifacts pass, while ten damaged variants fail as expected for source
   damage, probe-count/refusal drift, value export promotion, accepted-file
   promotion, evidence promotion, action promotion, downstream promotion,
   figure damage, and script-snapshot damage. Use runs `534-536` as the
   guarded real-export preflight gap block. Run `537` defines the required
   schema for the future real matched-FDTD return exports: two files, 558
   receiver-frequency row keys, and 22 required columns. No real FDTD values,
   accepted return files, comparison evidence, GPU/HPC work, field transfer, or
   field FWI are promoted. Use run `537` as the schema contract before accepting
   matched FDTD return files or writing BEM/FDTD comparison evidence. Run `538`
   validates that contract with five passing checks: source readiness, exact
   two-file/558-key/22-column schema, contract-only zero-value state, blocked
   actions/downstream states, and figure/script snapshots. Run `539`
   sensitivity-hardens that validator: exact run `537` artifacts pass, while
   13 damaged variants fail as expected for source-chain damage,
   file/key/column count drift, required-value-field damage, real file/value
   promotion, schema acceptance, template substitution, action/downstream
   promotion, figure damage, and script-snapshot damage. Use runs `537-539` as
   the guarded matched-FDTD real-export schema block before implementing a
   bounded real FDTD return exporter. Run `540` probes the current FDTD export
   and accepted-file writer interfaces in real mode after that schema block.
   Both FDTD exporter probes and all four accepted-writer probes refuse real
   evidence production. The remaining blockers are real FDTD return-value
   export, schema validation of those real returns, accepted writer enablement
   after values exist, and then the real BEM/FDTD comparison. Run `541`
   validates that implementation-gap audit with five passing checks: schema
   source readiness, two FDTD exporter refusals, four accepted-writer refusals,
   preserved implementation blockers, blocked downstream states, and
   figure/script snapshots. Run `542` sensitivity-hardens that validator:
   exact run `540` artifacts pass, while 15 damaged variants fail as expected
   for source-chain damage, exporter probe/refusal drift, exporter enablement
   or value promotion, writer probe/refusal drift, writer enablement, accepted
   file/evidence promotion, blocker damage, downstream promotion, figure
   damage, and script-snapshot damage. Use runs `540-542` as the guarded
   matched-FDTD real-export implementation-gap block. Run `543` turns the
   matched-FDTD return schema into a concrete two-file acceptance gate: two
   real return files, 558 receiver-frequency entries, and 22 required columns.
   No real return files, entries, columns, comparison evidence, GPU/HPC work,
   field transfer, or field FWI are accepted. Run `544` validates that
   acceptance gate with five passing checks: source chain, file gate shape,
   entry/column gate shape, blocked actions/downstream states, and
   figure/script snapshots. Run `545` sensitivity-hardens that validator: the
   exact run `543` artifacts pass, while 15 damaged variants fail as expected
   for source-chain damage, file count/presence/nonempty/acceptance promotion,
   entry or column drift, action drift, downstream promotion, figure damage,
   and script-snapshot damage. Use runs `543-545` as the real matched-FDTD
   return-file acceptance gate before any BEM/FDTD comparison evidence. Run
   `546` creates the empty staging directory for those two future matched-FDTD
   return CSV files under
   `outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_return_pending`.
   It creates no return files, accepts no evidence, and keeps comparison,
   GPU/HPC, field-transfer, and field-FWI readiness blocked. Run `547`
   validates that scaffold with five passing checks: source readiness, staging
   directory presence, two required files still missing, blocked
   actions/downstream states, and figure/script snapshots. Run `548`
   sensitivity-hardens that validator: exact run `546` artifacts pass, while
   13 damaged variants fail as expected for source damage, directory damage,
   unexpected-file promotion, file presence/nonempty/acceptance promotion,
   action damage, downstream promotion, figure damage, and script-snapshot
   damage. Run `549` locks the expected row identities for the two future
   matched-FDTD return CSV files: 558 unique row identities, two file sequence
   hashes, and 22 required columns, while accepting zero staged files or
   values. Run `550` validates that row-identity contract with five passing
   checks. Run `551` sensitivity-hardens the validator: the exact run `549`
   artifacts pass, while ten damaged variants fail as expected for source
   damage, missing or duplicate rows, sequence-hash drift, staged-file
   promotion, row-acceptance promotion, downstream promotion, figure damage,
   and script-snapshot damage. Use runs `546-551` as the current
   matched-FDTD return-file staging and row-identity lock before copying real
   FDTD return CSVs. Run `552` adds the value-domain contract after that row
   lock: 558 expected return values split into 279 lowercase SHA-256 source
   hashes and 279 positive finite scattered-norm values, with zero real values
   accepted. Run `553` validates that contract with four passing checks.
   Run `554` sensitivity-hardens the validator: exact run `552` artifacts
   pass, while nine damaged variants fail as expected for source damage,
   value-row damage, value-domain misclassification, premature value presence
   or acceptance, action promotion, comparison promotion, figure damage, and
   script-snapshot damage. Use runs `546-554` as the current guarded
   matched-FDTD return staging, row-identity, and value-domain block before
   real BEM/FDTD comparison evidence. Run `555` converts that guarded return
   requirement into a two-file producer checklist: one 279-row source-hash
   manifest CSV and one 279-row scattered-norm values CSV, both still pending.
   Use run `555` as the practical return-file production checklist before
   rerunning row-identity, value-domain, and BEM/FDTD comparison acceptance.
   Run `556` turns that checklist into two non-executed CSV validation
   commands: one hash-manifest row-count/SHA-256 check and one scattered-norm
   row-count/positive-float check. Use run `556` only after the two real return
   CSV files are produced. Run `557` accepts the real fine-mesh Bempp candidate
   values from run `525` as the BEM-side half of the 35-field return packet:
   two schema-conforming BEM return files, 558 accepted BEM rows, 279 source
   hashes, and 279 positive scattered-field norms. This closes the BEM-side
   return-file gap only. The matched-FDTD return files are still absent, so
   BEM/FDTD comparison evidence, 3D validation claims, field transfer, field
   FWI, and GPU/HPC escalation remain blocked. Run `558` validates that
   BEM-side return-file acceptance with six passing checks: source summary,
   file shape, row identities, value domains, written-file hashes, blocked
   downstream states, figure output, and frozen script snapshots. Run `559`
   sensitivity-hardens that validator: the exact run `557` source passes,
   while nine damaged variants fail as expected for summary readiness drift,
   missing source-hash rows, duplicate scattered-norm identities, bad hash
   values, negative norms, written-file hash drift, premature comparison
   promotion, figure damage, and missing script snapshots. Use runs `557-559`
   as the guarded BEM-side return-file block; the remaining comparison blocker
   is the two matched-FDTD return CSV files defined by runs `555-556`. Run
   `560` audits existing candidate sources for those two FDTD return files.
   The expected return directory is empty, and the only 279-row FDTD-like
   source is an older 2D scalar proxy export, which is shape-compatible but
   not real matched-FDTD evidence. Synthetic pairwise rows, synthetic inbox
   files, and local 2D FDTD summaries are also rejected as substitutes. Run
   `561` converts the row-identity and value-domain contracts into two
   fillable matched-FDTD return templates: 279 source-hash rows and 279
   scattered-norm rows, all blank and non-evidence. Fill those templates only
   with real matched-FDTD output, then run the command checks from run `556`.
   Run `562` validates that fillable-template pack with five passing checks:
   source readiness, exact two-file/558-row shape, blank value columns, zero
   evidence/downstream promotion, figure output, and frozen script snapshots.
   Run `563` sensitivity-hardens that validator: the exact run `561` template
   pack passes, while nine damaged variants fail as expected for source
   readiness drift, missing or duplicate template rows, premature hash/norm
   values, ready-file promotion, downstream comparison promotion, figure
   damage, and script-snapshot damage. Use runs `561-563` as the guarded blank
   matched-FDTD return-template block before real matched-FDTD values are
   produced. Run `564` audits the interface boundary after that block: the
   BEM-side return files are accepted and validated with 2 files and 558 rows,
   while the matched-FDTD side still has 0 accepted files, 0 accepted rows, 558
   blank template values, and 2 unexecuted command checks. This confirms that
   the next comparison-enabling task is producing the two real matched-FDTD CSV
   return files, not running a comparison from templates or proxy values. Run
   `565` sensitivity-hardens that boundary audit: the exact run `564` source
   state passes, while seven damaged states fail as expected for BEM validation
   damage, BEM row-count drift, FDTD template readiness damage, FDTD blank-value
   drift, FDTD file promotion, command-execution promotion, and downstream
   comparison promotion. Run `566` combines the accepted BEM-side return state
   with the matched-FDTD real-export implementation gap: one of six bindings is
   ready, while five remain blocking because exporter real mode, writer real
   mode, matched-FDTD return CSV files, matched-FDTD return values, and command
   execution are still absent. Use run `566` as the current blocker map before
   implementing the controlled real matched-FDTD return exporter/writer. Run
   `567` adds that next guarded exporter shell: both required FDTD file-key
   contract checks pass and the exporter now has an input-bound validation/write
   path, but no real FDTD input CSVs are supplied and no accepted FDTD return
   CSVs are written. Use run `567` as the current exporter checkpoint before
   producing the two real matched-FDTD input CSV files. Run `568` creates that
   practical handoff packet: two fillable matched-FDTD input templates with 558
   row identities prefilled, 3348 real solver/provenance/value cells left
   blank, and two non-executed exporter commands. Use run `568` as the current
   fillable input packet before any accepted FDTD return-file production. Run
   `569` validates that packet with eight passing checks: source readiness,
   exact two-template shape, prefilled identities, blank real solver/provenance
   values, future-input command routing, zero command execution, blocked
   downstream states, and figure/script presence. Run `570`
   sensitivity-hardens the validator: the exact run `568` packet passes, while
   seven damaged cases fail as expected for source readiness damage, template
   shape damage, command routing to blank templates, command execution
   promotion, downstream comparison promotion, figure damage, and missing
   script snapshots. Run `571` defines the real-input acceptance gate for that
   input-bound exporter: two future real matched-FDTD input CSVs, 558 total
   rows, 22 file-column checks, and zero currently present or accepted real
   input files. BEM/FDTD comparison, 3D validation, GPU/HPC escalation, field
   transfer, and field FWI remain blocked until both real input CSVs pass this
   gate and the exporter writes accepted return files. Run `572` validates
   that acceptance gate with seven passing checks: source readiness,
   two-file/558-row shape, 22-column gate shape, zero accepted current input,
   zero executed commands or return files, blocked downstream states, and
   figure/script artifacts. Run `573` sensitivity-hardens the validator: the
   exact run `571` gate passes, while ten damaged states fail as expected for
   source readiness removal, missing file gates, row-count drift, missing
   column gates, premature input acceptance, premature command execution,
   premature return-file promotion, premature BEM/FDTD comparison promotion,
   figure damage, and missing script snapshots.
   Run `574` audits the locked filesystem handoff paths from the real-input
   gate. The two expected real input CSV paths and two expected accepted-return
   CSV paths are all absent; their parent directories are also absent. Exporter
   execution, BEM/FDTD comparison, 3D validation, GPU/HPC escalation, field
   transfer, and field FWI remain blocked. Run `575` validates that filesystem
   gap audit with five passing checks: source readiness, four-path shape, absent
   parent directories/files, blocked actions/downstream states, and
   figure/script artifacts.
   Run `576` sensitivity-hardens that validator: the exact run `574` gap audit
   passes, while nine damaged states fail as expected for source readiness
   removal, path-shape damage, parent-directory promotion, file-presence
   promotion, blocking-count drift, BEM/FDTD comparison promotion,
   action-readiness promotion, figure damage, and missing script snapshots.
   Run `577` creates a fresh external staging scaffold for the input-bound
   matched-FDTD handoff without editing historical run `568`: two empty staging
   directories are present, four required staged files are still missing, zero
   files are accepted, and exporter execution, BEM/FDTD comparison, 3D
   validation, GPU/HPC, field transfer, and field FWI remain blocked.
   Run `578` validates that scaffold with five passing checks: source-chain
   readiness, two staging directories present, four required files still
   missing, actions/downstream states blocked, and figure/script artifacts
   present.
   Run `579` sensitivity-hardens the validator: the exact run `577` scaffold
   passes, while fifteen damaged states fail as expected for source-chain
   readiness removal, directory drift/absence, unexpected-file promotion, file
   obligation drift, staged/accepted file promotion, action promotion/count
   drift, BEM/FDTD comparison promotion, figure damage, and missing script
   snapshots.
   Run `580` converts the guarded staging scaffold into a practical four-file
   intake manifest: two real input CSV files from the external matched-FDTD
   producer and two future accepted return CSV files from the input-bound
   exporter. No staged files are present or accepted, and exporter execution,
   BEM/FDTD comparison, 3D validation, GPU/HPC, field transfer, and field FWI
   remain blocked.
   Run `581` validates that intake manifest with five passing checks: source
   readiness, four-row manifest shape, zero file acceptance/promotion,
   blocked actions/downstream states, and figure/script artifacts.
   Run `582` sensitivity-hardens the validator: the exact run `580` manifest
   passes, while twelve damaged states fail as expected for source readiness
   removal, manifest identity damage, staged/accepted file promotion,
   exporter/comparison readiness promotion, action readiness promotion,
   downstream comparison promotion, figure damage, and missing script
   snapshots. Run `583` applies the real receipt acceptance gate to the fresh
   external staging paths: four required staged files are checked with
   row/content validation rules, but zero files are currently present or
   accepted. Exporter execution, BEM/FDTD comparison, 3D validation, GPU/HPC,
   field transfer, and field FWI remain blocked. Run `584` validates that
   receipt gate with five passing checks: source readiness, four-row receipt
   shape, zero file promotion, blocked actions/downstream states, and
   figure/script artifacts. Run `585` sensitivity-hardens the validator: the
   exact run `583` receipt gate passes, while fourteen damaged states fail as
   expected for receipt identity drift, file-presence/acceptance promotion,
   validation-error drift, readiness promotion, downstream promotion, figure
   damage, and missing script snapshots. Run `586` exercises that receipt gate
   with output-local synthetic files: two valid synthetic files are accepted
   with 558 accepted rows total, two malformed synthetic files are rejected,
   and the external real staging area remains empty. This is a gate smoke, not
   BEM/FDTD comparison evidence. Run `587` validates that synthetic smoke with
   five passing checks: source readiness, two accepted and two rejected
   synthetic cases, 558 synthetic accepted rows, zero real evidence, zero
   external staged/accepted files, blocked downstream states, and figure/script
   artifacts. Run `588` sensitivity-hardens the validator: the exact run `586`
   smoke passes, while twelve damaged states fail as expected for case-count
   drift, accept/reject drift, accepted-row drift, real-evidence promotion,
   external-file promotion, BEM/FDTD comparison promotion, figure damage, and
   missing script snapshots. Run `589` uses the valid synthetic receipt files
   from run `586` to exercise the input-bound exporter write path: two
   full-schema synthetic return CSVs are written with 558 accepted rows total,
   the invalid synthetic references remain rejected, and the result remains
   non-evidence with real BEM/FDTD comparison blocked. Run `590` validates that
   roundtrip with five passing checks: source readiness, four-case shape, two
   synthetic return files, 558 accepted synthetic rows, zero real evidence,
   blocked downstream states, and figure/script artifacts. Run `591`
   sensitivity-hardens the validator: the exact run `589` roundtrip passes,
   while twelve damaged states fail as expected for case-shape damage,
   return-file/success/row-count damage, real-evidence promotion,
   BEM/FDTD comparison promotion, figure damage, and missing script snapshots.
   Run `592` audits the locked external staging paths after the synthetic
   roundtrip and confirms that the two synthetic return files stayed inside
   run `589`: all four external real staging paths remain absent, unaccepted,
   and unpolluted. Run `593` validates that guard with five passing checks:
   source-chain readiness, four empty external paths, zero synthetic pollution,
   blocked downstream states, and figure/script artifacts. Run `594`
   sensitivity-hardens the validator: the exact run `592` guard passes, while
   thirteen damaged states fail as expected for source-chain damage, synthetic
   return-count damage, accepted-row damage, external file promotion, synthetic
   pollution promotion, downstream promotion, figure damage, and missing script
   snapshots. Run `595` converts that guarded external staging gap into a
   four-step closure plan: supply two real matched-FDTD input CSVs, rerun the
   receipt gate on those inputs, run the input-bound exporter to create two
   accepted return CSVs, then rerun the receipt/exporter/BEM-FDTD comparison
   gates. No staged files are present or accepted, so real comparison, 3D
   validation claims, GPU/HPC work, field transfer, and field FWI remain
   blocked. Run `596` validates that closure plan with five passing checks:
   four closure groups, four missing staged files, two real inputs, two
   accepted returns, zero present/accepted files, blocked downstream states,
   and figure/script artifacts. Run `597` sensitivity-hardens the validator:
   the exact run `595` plan passes, while twelve damaged states fail as
   expected for closure-group damage, file-role damage, file presence or
   acceptance promotion, real-comparison promotion, GPU/HPC promotion, figure
   damage, and missing script snapshots. Run `598` converts the closure block
   into a producer route specification: two external matched-FDTD producer
   input files first, two input-bound exporter return files second, then
   comparison-gate reruns after all four files pass. Each input/return phase
   requires 558 rows across two files and the two value fields
   `returned_fdtd_source_hash` and `returned_fdtd_scattered_norm`; no files are
   present or accepted yet. Run `599` validates the producer route with five
   passing checks: four routes, three phases, two producer input routes, two
   exporter return routes, 558 input rows, 558 return rows, two required value
   fields, zero current files, blocked downstream states, and figure/script
   artifacts. Run `600` sensitivity-hardens the validator: the exact run `598`
   route passes, while fifteen damaged states fail as expected for route/phase
   damage, route-count damage, row-count damage, value-field damage, file
   presence or acceptance promotion, real-comparison promotion, GPU/HPC
   promotion, figure damage, and missing script snapshots. Run `601` exercises
   the run `598` route with a complete output-local synthetic packet: two
   synthetic matched-FDTD producer input CSVs and two synthetic exporter return
   CSVs are accepted with 1116 rows total, while all real external staging
   paths remain empty and real BEM/FDTD comparison, 3D-validation claims,
   GPU/HPC, field transfer, and field FWI remain blocked. Run `602` validates
   that packet smoke with five passing checks: four route files, two input
   files, two return files, 1116 accepted rows, zero real external files, zero
   real evidence files, blocked downstream states, and figure/script artifacts.
   Run `603` sensitivity-hardens the validator: the exact run `601` packet
   passes, while fifteen damaged states fail as expected for packet-shape
   damage, row-count damage, file-acceptance damage, real-file/evidence
   promotion, downstream promotion, figure damage, and missing script
   snapshots. Run `604` audits the locked real external staging paths after
   that synthetic packet and confirms that all four packet files stayed
   output-local: zero external files exist, zero packet files overlap the
   external paths, zero packet files are under the external root, and real
   BEM/FDTD comparison, 3D-validation claims, GPU/HPC, field transfer, and
   field FWI remain blocked. Run `605` validates that guard with five passing
   checks: exact four-row shape, four packet files, zero external files, zero
   packet/external path overlap, zero packet files under the external root,
   zero real evidence files, blocked downstream states, and figure/script
   artifacts. Run `606` sensitivity-hardens the validator: the exact run `604`
   guard passes, while fourteen damaged states fail as expected for external
   file promotion, packet/external path overlap, packet-under-external-root
   promotion, packet evidence promotion, downstream promotion, figure damage,
   and missing script snapshots. Run `607` returns to the numerical 2D
   colleague-code validation branch and extends the scarep CPU Galerkin BEM
   panel sweep to 128 boundary panels. The endpoint is the best current
   analytic-cylinder result: complex relative L2 improves from
   0.0007053747139208214 at 64 panels to 0.00017926490798156493 at 128 panels,
   and time-B-scan relative L2 improves from 0.0005202399688500149 to
   0.00013202484159666165. The 64-to-128 error order is about 1.98 while wall
   time rises by about 3.84x, so the CPU BEM method-validation evidence is
   stronger but project-FDTD comparison, 3D validation, GPU/HPC, field
   transfer, and field FWI remain blocked until a matched setup is used. Run
   `608` recomputes the convergence-rate audit over all five panel levels
   `[8, 16, 32, 64, 128]`: complex-spectrum error order is
   1.9961624062950216, time-B-scan error order is 1.9918880456546393, and
   wall-time cost exponent is 1.6952684551080672. The 128-panel endpoint is
   therefore the current high-accuracy validation endpoint, while repeated
   sweeps should still prefer lower panel counts unless that accuracy is
   required. Run `609` converts that ladder into an accuracy/cost policy:
   32 panels satisfy loose `1e-2` and `5e-3` targets, 64 panels are the
   repeat-sweep default for a `1e-3` target, 128 panels are the high-accuracy
   endpoint for `5e-4` and `2e-4` targets, and the current ladder does not
   satisfy a `1e-4` target. Run `610` validates that policy with five passing
   checks: source readiness, exact 8-128 threshold ladder shape, 64-panel
   repeat default, 128-panel high-accuracy endpoint, near-second-order
   convergence, blocked project-FDTD/3D/GPU/HPC/field-FWI claims, and
   figure/script artifacts. Run `611` sensitivity-hardens that validator: the
   exact run `609` policy passes, while sixteen damaged states fail as
   expected for threshold-row damage, threshold-count damage, panel-policy
   damage, convergence damage, project-FDTD/3D/GPU/HPC/field-FWI promotion,
   figure damage, and missing script snapshots. Run `612` performs three real
   64-panel CPU BEM repeats on the scarep analytic-cylinder validation problem.
   All three repeats produce identical frequency-response hashes, identical
   reconstructed time-B-scan hashes, identical complex relative L2
   `0.0007053747139208214`, and identical time-B-scan relative L2
   `0.0005202399688500149`; mean wall time is about `20.59` seconds. This
   supports 64 panels as the repeat-sweep default while project-FDTD, 3D,
   GPU/HPC, field-transfer, and field-FWI claims remain blocked. Run `613`
   validates that audit with five passing checks: source readiness, exact
   three-repeat/64-panel shape, identical response/time-B-scan hashes,
   sub-`1e-3` errors, analytic-only claim boundary, and figure/script
   artifacts. Run `614` sensitivity-hardens that validator: the exact run
   `612` audit passes, while thirteen damaged states fail as expected for
   repeat-row damage, panel damage, error-threshold damage, hash damage,
   project-FDTD/3D/GPU/HPC/field-FWI promotion, figure damage, and missing
   script snapshots. Run `615` performs three real 128-panel CPU BEM repeats
   on the same scarep analytic-cylinder validation problem. All three repeats
   produce identical frequency-response hashes, identical reconstructed
   time-B-scan hashes, identical complex relative L2
   `0.00017926490798156493`, and identical time-B-scan relative L2
   `0.00013202484159666165`; mean wall time is about `79.58` seconds. This
   confirms 128 panels as a repeatable high-accuracy endpoint while 64 panels
   remains the cheaper repeat-sweep default. Run `616` validates that audit
   with five passing checks: source readiness, exact three-repeat/128-panel
   shape, identical response/time-B-scan hashes, sub-`2e-4` errors,
   analytic-only claim boundary, and figure/script artifacts. Run `617`
   sensitivity-hardens that validator: the exact run `615` audit passes, while
   thirteen damaged states fail as expected for repeat-row damage, panel
   damage, high-accuracy error-threshold damage, hash damage,
   project-FDTD/3D/GPU/HPC/field-FWI promotion, figure damage, and missing
   script snapshots. Run `618` converts the validated 64-panel and 128-panel
   repeatability audits into a tradeoff scorecard: 128 panels reduce complex
   relative L2 by about `3.93x` and time-B-scan relative L2 by about `3.94x`,
   while costing about `3.86x` more wall time. The resulting policy is to keep
   64 panels as the repeat-sweep default and reserve 128 panels for
   high-accuracy endpoint confirmation. Run `619` validates that scorecard
   with five passing checks: source readiness, 64/128 policy roles, tradeoff
   ratios above `3x`, analytic-only claim boundary, and figure/script
   artifacts. Run `620` sensitivity-hardens that validator: the exact run
   `618` scorecard passes, while fifteen damaged states fail as expected for
   score-row shape, policy-role damage, threshold damage, ratio damage,
   project-FDTD/3D/GPU/HPC/field-FWI promotion, figure damage, and missing
   script snapshots. Run `621` performs one real 64-panel CPU BEM solve and
   audits ten receiver/scan-line subsets against the scarep analytic-cylinder
   reference. All full, cropped, one-sided, alternating, and sparse subsets
   remain below the `1e-3` target; the worst complex relative L2 is
   `0.0007704118971318319` and the worst time-B-scan relative L2 is
   `0.0005678637768138664`. This supports 64 panels for receiver-line
   sensitivity studies while project-FDTD comparison, 3D validation, GPU/HPC,
   field transfer, and field FWI remain blocked. Run `622` validates that
   subset audit from saved artifacts with five passing checks: source
   readiness, receiver-line subset design, all subset errors below target,
   saved NPZ array hashes, analytic-only claim boundary, figure output, and
   script snapshots. Run `623` sensitivity-hardens that validator: the exact
   run `621` audit passes, while eighteen damaged states fail as expected for
   source readiness, subset design, error thresholds, pass counts, array hashes
   and shape, project-FDTD/3D/GPU/HPC/field promotion, figure damage, and
   missing script snapshots. Run `624` reuses the saved run `621` arrays to
   audit frequency-subset stability for the 64-panel default. Eight of nine
   subsets remain below the `1e-3` target, including the full band, low band,
   mid band, even/odd decimation, every-third decimation, center band, and
   edge-band subset. The high-frequency-only 2.08-3.00 GHz subset fails at
   `0.001736291511432671`, so high-frequency-only claims need the 128-panel
   endpoint or a dedicated high-frequency confirmation. Run `625` validates
   that frequency-subset audit with five passing checks: source readiness,
   exact nine-subset frequency design, preserved 8-pass/1-fail
   high-frequency boundary, analytic-only claim boundary, figure output, and
   script snapshots. Run `626` sensitivity-hardens that validator: the exact
   run `624` source passes, while twenty-four damaged states fail as expected
   for source readiness, frequency design, erased high-band failure, pass/fail
   count damage, summary-flag damage, project-FDTD/3D/GPU/HPC/field
   promotion, figure damage, and missing script snapshots. Run `627` performs
   one fresh 128-panel CPU BEM endpoint solve on the same analytic-cylinder
   problem and reruns the nine frequency-subset checks. All nine subsets pass
   below the `1e-3` target. The high-frequency-only 2.08-3.00 GHz error drops
   from the 64-panel value `0.001736291511432671` to
   `0.0004276569548253307`, a `4.06x` improvement, confirming 128 panels as
   the high-frequency endpoint while project-FDTD, 3D, GPU/HPC, field-transfer,
   and field-FWI claims remain blocked. Run `628` validates that endpoint with
   six passing checks: source readiness, all nine frequency subsets below the
   target, preserved high-frequency closure, saved NPZ array hashes and errors,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `629` sensitivity-hardens that validator: the exact run `627` endpoint
   passes, while twenty-six damaged states fail as expected for source
   readiness, frequency design, endpoint-boundary damage, saved-array
   consistency damage, panel-count damage, project-FDTD/3D/GPU/HPC/field
   promotion, figure damage, and missing script snapshots. Run `630` converts
   the guarded frequency-subset results into a frequency-aware panel policy:
   use 64 panels for receiver-line sensitivity and broad/low/mid-band sweeps,
   use 128 panels for high-frequency-only 2.08-3.00 GHz claims, and make no
   project-FDTD, field-transfer, 3D, GPU/HPC, or field-FWI promotion from the
   scarep analytic-cylinder BEM evidence alone. Run `631` validates that
   policy with five passing checks: source readiness, preserved four-row
   frequency split, preserved 64-fail/128-pass high-frequency boundary,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `632` sensitivity-hardens that policy validator: the exact run `631`
   validator passes, while nineteen damaged states fail as expected for source
   readiness, missing/damaged policy rows, high-frequency boundary damage,
   improvement-factor damage, project-FDTD/3D/GPU/HPC/field promotion, figure
   damage, and missing script snapshots. Run `633` then tests an intermediate
   96-panel solve on the same scarep analytic-cylinder scan. All nine
   frequency subsets pass below the `1e-3` target; the high-frequency-only
   error drops from the 64-panel value `0.001736291511432671` to
   `0.0007600368161379071`, while taking about `0.57x` of the 128-panel wall
   time. This makes 96 panels a lower-cost high-frequency candidate pending
   validator hardening, while 128 panels remains the stricter endpoint and
   project-FDTD/3D/GPU/HPC/field claims remain blocked. Run `634` validates
   the 96-panel bridge with six passing checks: source readiness, nine
   passing frequency subsets, preserved 64/96/128 high-band relationship,
   saved-array hash consistency, analytic-only claim boundary, figure output,
   and script snapshots. Run `635` sensitivity-hardens that validator: the
   exact run `633` artifact passes, while twenty-one damaged states fail as
   expected for source readiness, subset shape, high-frequency boundary,
   64/96/128 cost relation, saved arrays and hashes, project-FDTD/3D/GPU/HPC/
   field promotion, figure damage, and missing script snapshots. Run `636`
   refreshes the frequency-cost panel policy: use 64 panels for receiver-line
   and broad/low/mid-frequency sweeps, use 96 panels as the lower-cost
   high-frequency candidate, keep 128 panels as the strict high-frequency
   endpoint, and make no project-FDTD, field-transfer, 3D, GPU/HPC, or field
   FWI promotion from this analytic-cylinder BEM evidence. Run `637` validates
   that refreshed policy with five passing checks: source readiness, preserved
   64/96/128 split, high-frequency cost and strict-endpoint roles,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `638` sensitivity-hardens that validator: the exact run `636` policy
   passes, while twenty-four damaged states fail as expected for source
   readiness, row shape, 64/96/128 role drift, high-frequency threshold and
   cost drift, downstream promotion, figure damage, and missing script
   snapshots. Run `639` tests whether the lower-cost high-frequency threshold
   can move below 96 panels. The 80-panel solve improves on 64 panels but still
   fails the high-frequency-only 2.08-3.00 GHz subset at
   `0.0010993149385036519`, with eight of nine subsets passing. The current
   bracket is therefore: 64 fails high band, 80 fails high band, 96 passes high
   band, and 128 remains the strict endpoint.
   Run `640` validates the 80-panel no-go result with six passing checks:
   source readiness, preserved eight-pass/one-fail frequency-subset outcome,
   preserved 80-to-96 threshold bracket, saved-array hash consistency,
   analytic-only claim boundary, figure output, and script snapshots. This
   confirms that 80 panels should not be promoted for high-frequency work and
   keeps the run `636` policy unchanged. Run `641` sensitivity-hardens that
   no-go validator: the exact run `640` source passes, while twenty-five
   damaged states fail as expected for source-readiness drift, no-go
   promotion, panel and row damage, threshold-bracket damage, saved-array
   damage, project-FDTD/3D/GPU/HPC/field promotion, figure damage, and missing
   script snapshots. Run `642` tests the midpoint between the validated
   80-panel no-go and the guarded 96-panel pass. The 88-panel solve passes all
   nine frequency subsets, including the high-frequency-only 2.08-3.00 GHz
   subset at `0.0009060002386797175`. The current high-frequency bracket is
   therefore: 64 fails, 80 fails, 88 passes, 96 passes, and 128 remains the
   strict endpoint. This promotes 88 panels only as a pending-validator
   lower-cost high-frequency candidate; project-FDTD, 3D, GPU/HPC,
   field-transfer, and field-FWI claims remain blocked. Run `643` validates
   the 88-panel result with six passing checks: source readiness, preserved
   nine-pass/zero-fail frequency-subset outcome, preserved 80-to-88-to-96
   threshold bracket, saved-array hash consistency, analytic-only claim
   boundary, figure output, and script snapshots. This promotes 88 panels as
   the guarded lower-cost high-frequency candidate within the analytic-cylinder
   BEM policy only. Run `644` sensitivity-hardens that validator: the exact
   run `643` source passes, while twenty-six damaged states fail as expected
   for source-readiness drift, bridge readiness drift, panel and row damage,
   threshold-bracket damage, saved-array damage, project-FDTD/3D/GPU/HPC/field
   promotion, figure damage, and missing script snapshots. Run `645` refreshes
   the frequency-cost policy: 64 panels remain the default for receiver-line
   and broad/low/mid-band sweeps, 80 panels are a validated no-go lower bound,
   88 panels become the guarded lower-cost high-frequency candidate, 96 panels
   remain a valid but superseded high-frequency reference, and 128 panels
   remain the strict endpoint. Project-FDTD, field-transfer, 3D, GPU/HPC, and
   field-FWI claims remain blocked from this analytic-cylinder BEM evidence.
   Run `646` validates that refreshed policy with five passing checks: source
   readiness, preserved seven-row 64/80/88/96/128 split, preserved
   high-frequency candidate/reference/endpoint roles, analytic-only claim
   boundary, figure output, and script snapshots. Run `647`
   sensitivity-hardens that validator: the exact run `646` source passes,
   while thirty-two damaged states fail as expected for source readiness, row
   shape, policy-role drift, high-frequency threshold and cost drift,
   downstream promotion, figure damage, and missing script snapshots. Run
   `648` tests the midpoint between the validated 80-panel no-go and the
   guarded 88-panel pass. The 84-panel solve passes all nine frequency subsets,
   including the high-frequency-only 2.08-3.00 GHz subset at
   `0.000995562585853498`. This is only `4.437414146502028e-6` below the
   `1e-3` target, so 84 panels are a narrow-margin candidate pending validator
   and sensitivity hardening, not yet the active policy replacement. Run `649`
   validates that narrow-margin 84-panel result with six passing checks:
   source readiness, preserved nine-pass/zero-fail frequency-subset outcome,
   preserved 80-to-84-to-96 threshold bracket, saved-array hash consistency,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `650` sensitivity-hardens that validator: the exact run `649` source
   passes, while twenty-six damaged states fail as expected for source
   readiness, bridge readiness, panel and row damage, threshold-bracket damage,
   saved-array damage, downstream promotion, figure damage, and missing script
   snapshots. Run `651` tests 82 panels, the midpoint below the narrow
   84-panel pass. The 82-panel solve improves on 80 panels but still fails the
   high-frequency-only subset at `0.001045485149014675`, leaving eight of nine
   subsets passing. The current lowest tested passing high-frequency panel
   count is therefore 84 panels, with 82 panels as the nearest tested no-go
   lower side. Run `652` validates the 82-panel no-go with six passing checks:
   source readiness, preserved eight-pass/one-fail frequency-subset outcome,
   preserved 82-to-96 threshold bracket, saved-array hash consistency,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `653` sensitivity-hardens that no-go validator: the exact run `652` source
   passes, while twenty-five damaged states fail as expected for source
   readiness, no-go promotion, panel and row damage, threshold-bracket damage,
   saved-array damage, downstream promotion, figure damage, and missing script
   snapshots. Run `654` refreshes the active analytic-cylinder BEM panel
   policy: 64 panels remain default for receiver-line and broad/low/mid-band
   sweeps, 82 panels become the nearest tested no-go lower bound, 84 panels
   become the minimum guarded high-frequency candidate, 88 panels become the
   wider-margin low-cost reference, 96 panels remain a validated superseded
   reference, and 128 panels remain the strict endpoint. Project-FDTD,
   field-transfer, 3D, GPU/HPC, and field-FWI claims remain blocked from this
   evidence. Run `655` validates that refreshed policy with five passing
   checks: source readiness, preserved eight-row 64/82/84/88/96/128 split,
   preserved 82-to-84 threshold role, analytic-only claim boundary, figure
   output, and script snapshots. Run `656` sensitivity-hardens that validator:
   the exact run `655` source passes, while thirty-four damaged states fail as
   expected for source readiness, row-shape damage, 82-panel no-go promotion,
   84-panel role damage, 88/96/128 role drift, high-frequency threshold drift,
   84-panel margin loss, 84-panel cost drift, project-FDTD promotion, 3D
   promotion, GPU/HPC promotion, field-transfer promotion, field-FWI
   promotion, figure damage, and missing script snapshots. Run `657` tests
   whether the 84-panel high-frequency policy transfers across controlled
   material and geometry variants. It solves four analytic-cylinder variants
   at 84 and 128 panels: smaller radius, larger radius, lower dielectric
   contrast, and higher dielectric contrast. The 84-panel candidate passes the
   smaller-radius and lower-contrast cases but fails the larger-radius case
   (`0.0018449395379997787`) and higher-contrast case
   (`0.001188193969563737`) against the `1e-3` high-band target. The
   128-panel endpoint passes all four variants, with maximum high-band error
   `0.0007789581648464677`. Run `658` validates this as a no-go for broad
   84-panel transfer with five passing checks: source readiness, exact
   four-case/eight-solve shape, preserved 84-panel 2-pass/2-fail boundary,
   preserved 128-panel all-pass endpoint, analytic-only claim boundary, figure
   output, and script snapshots. Run `659` sensitivity-hardens that validator:
   the exact run `657` source passes, while twenty damaged states fail as
   expected for source readiness, case/solve shape damage, false 84-panel
   promotion, false 128-panel demotion, threshold-boundary damage, wall-ratio
   damage, project-FDTD promotion, 3D promotion, GPU/HPC promotion,
   field-transfer promotion, field-FWI promotion, figure damage, and missing
   script snapshots. Run `660` tests 96 panels on the same four
   material/geometry transfer variants. It improves on 84 panels and passes
   three of four cases, including the higher-contrast case, but the
   larger-radius case still fails at `0.0013995629205128856` against the
   `1e-3` high-band target. The 128-panel endpoint again passes all four
   variants, so 96 panels are a partial-transfer result rather than a general
   transfer policy. Run `661` validates that partial-transfer boundary with
   five passing checks: source readiness, exact four-case/four-solve shape,
   preserved 96-panel 3-pass/1-fail boundary, preserved 128-panel all-pass
   endpoint, analytic-only claim boundary, figure output, and script
   snapshots. Run `662` sensitivity-hardens that validator: the exact run
   `660` source passes, while twenty damaged states fail as expected for
   source readiness, case/solve shape damage, false 96-panel promotion, false
   128-panel demotion, threshold-boundary damage, wall-ratio damage,
   project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
   promotion, field-FWI promotion, figure damage, and missing script
   snapshots. Run `663` tests 112 panels as the next intermediate candidate
   between the 96-panel partial-transfer result and the 128-panel endpoint.
   The 112-panel result is a near miss: it still passes three of four variants,
   but the larger-radius case remains just above the target at
   `0.0010208970808398296`. The 128-panel endpoint again passes all four
   variants. Run `664` validates this near-miss boundary with five passing
   checks: source readiness, exact four-case/four-solve shape, preserved
   112-panel 3-pass/1-fail boundary, preserved 128-panel all-pass endpoint,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `665` sensitivity-hardens that validator: the exact run `663` source
   passes, while twenty damaged states fail as expected for source readiness,
   case/solve shape damage, false 112-panel promotion, false 128-panel
   demotion, near-miss erasure, threshold-boundary damage, wall-ratio damage,
   project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
   promotion, field-FWI promotion, figure damage, and missing script
   snapshots. Run `666` tests 120 panels as the next intermediate candidate.
   This closes the transfer gap: all four material/geometry variants pass,
   including the larger-radius case at `0.0008874668710960488`, while the mean
   wall-time ratio is `0.8813044366721805` relative to 128 panels. Run `667`
   validates 120 panels as the current analytic material/geometry transfer
   endpoint with five passing checks: source readiness, exact
   four-case/four-solve shape, preserved 112-panel 3-pass/1-fail lower-side
   boundary, preserved 120-panel 4-pass/0-fail promotion, preserved
   128-panel all-pass endpoint, analytic-only claim boundary, figure output,
   and script snapshots. Run `668` sensitivity-hardens that validator: the
   exact run `666` source passes, while twenty damaged states fail as expected
   for source readiness, case/solve shape damage, transfer demotion,
   128-panel endpoint demotion, target failure, wall-ratio damage,
   project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
   promotion, field-FWI promotion, figure damage, and missing script
   snapshots. Run `669` tests 116 panels as the midpoint between the
   112-panel near miss and the validated 120-panel endpoint. It passes all
   four variants, including the larger-radius case at
   `0.0009506170756247567`, with mean wall-time ratio
   `0.934122476353184` relative to 120 panels. Run `670` validates 116 panels
   as the current lowest tested passing analytic transfer endpoint with five
   passing checks: source readiness, exact four-case/four-solve shape,
   preserved 112-panel 3-pass/1-fail lower-side boundary, preserved
   116-panel 4-pass/0-fail promotion, preserved 120-panel all-pass endpoint,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `671` sensitivity-hardens that validator: the exact run `669` source
   passes, while twenty damaged states fail as expected for source readiness,
   case/solve shape damage, transfer demotion, 120-panel endpoint demotion,
   target failure, wall-ratio damage, project-FDTD promotion, 3D promotion,
   GPU/HPC promotion, field-transfer promotion, field-FWI promotion, figure
   damage, and missing script snapshots. Run `672` tests 114 panels as the
   midpoint between the 112-panel near miss and the validated 116-panel
   endpoint. It passes all four variants, including the larger-radius case at
   `0.0009848005761020824`, leaving only a tight margin below the `1e-3`
   target. Run `673` validates 114 panels as the current lowest tested passing
   analytic transfer endpoint with five passing checks: source readiness,
   exact four-case/four-solve shape, preserved 112-panel 3-pass/1-fail
   lower-side boundary, preserved 114-panel 4-pass/0-fail promotion,
   preserved 116-panel all-pass endpoint, analytic-only claim boundary,
   figure output, and script snapshots. Run `674` sensitivity-hardens that
   validator: the exact run `672` source passes, while twenty damaged states
   fail as expected for source readiness, case/solve shape damage, transfer
   demotion, 116-panel endpoint demotion, target failure, wall-ratio damage,
   project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
   promotion, field-FWI promotion, figure damage, and missing script
   snapshots. Run `675` tests 113 panels as the one-panel lower candidate
   below the validated 114-panel endpoint. It fails only the larger-radius
   case, and only narrowly, at `0.0010026008820656063`. This establishes the
   current bracket as 113 panels no-go and 114 panels pass for the tested
   material/geometry variants. Run `676` validates that lower-side no-go with
   five passing checks: source readiness, exact four-case/four-solve shape,
   preserved 113-panel 3-pass/1-fail boundary, preserved 114-panel all-pass
   endpoint, analytic-only claim boundary, figure output, and script
   snapshots. Run `677` sensitivity-hardens that validator: the exact run
   `675` source passes, while twenty damaged states fail as expected for
   source readiness, case/solve shape damage, false 113-panel promotion,
   114-panel endpoint demotion, no-go erasure, endpoint failure, wall-ratio
   damage, project-FDTD promotion, 3D promotion, GPU/HPC promotion,
   field-transfer promotion, field-FWI promotion, figure damage, and missing
   script snapshots. Run `678` converts this threshold into a margin-aware
   analytic transfer policy: 113 panels are the nearest tested no-go, 114
   panels are the minimum validated pass with margin
   `1.5199423897917664e-05`, and 116 panels are the guarded recommended
   endpoint under a `2.5e-05` guard margin. Run `679` validates that policy
   split with five passing checks: source readiness, exact five-panel policy
   row set, preserved 113/114/116 roles, preserved source validators,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `680` sensitivity-hardens that validator: the exact run `678` source
   passes, while seventeen damaged states fail as expected for source
   readiness, row-shape damage, no-go/minimum/guarded role drift, margin
   damage, source-validation damage, project-FDTD promotion, 3D promotion,
   GPU/HPC promotion, field-transfer promotion, field-FWI promotion, figure
   damage, and missing script snapshots.
   Run `681` tests the current 114/116-panel margin policy on a denser
   49-frequency grid for the same four material/geometry variants and the
   114, 116, and 128 panel counts. All three panel counts pass all four cases
   on this denser grid. The maximum high-band errors are
   `0.0007904252030039112` for 114 panels,
   `0.0007631424594234813` for 116 panels, and
   `0.0006260191501451638` for 128 panels. The minimum dense-grid margins are
   `0.00020957479699608883` for 114 panels and
   `0.0002368575405765187` for 116 panels. This supports the guarded 116-panel
   analytic transfer policy but does not erase the original tight-margin
   reason for keeping 116 panels conservative after run `678`. Run `682`
   validates the dense-frequency audit with five passing checks: source
   readiness, exact four-case/twelve-solve/49-frequency shape, preserved
   114/116/128 panel set, dense-grid transfer boundary, analytic-only claim
   boundary, figure output, and script snapshots. Run `683`
   sensitivity-hardens that validator: the exact run `681` source passes,
   while twenty damaged states fail as expected for source readiness, case or
   solve shape damage, frequency-count damage, panel-set damage, pass-count or
   guard-count damage, minimum/guarded panel drift, 116-panel error or margin
   damage, FDTD comparison promotion, real-3D promotion, GPU/HPC promotion,
   field-transfer promotion, field-FWI promotion, figure damage, and missing
   script snapshots.
   Run `684` audits why the dense 49-frequency block lowered the aggregate
   high-band errors. It focuses on the larger-radius case that controlled the
   113/114/116 decision and compares 25-frequency and 49-frequency sampling
   for 114 and 116 panels. The aggregate high-band errors drop from
   `0.0009848005761020824` to `0.0007904252030039112` for 114 panels and from
   `0.0009506170756247567` to `0.0007631424594234813` for 116 panels, but the
   worst high-band per-frequency errors are unchanged:
   `0.002107396735185063` for 114 panels and `0.002033505195979887` for 116
   panels. This shows that the aggregate metric is frequency-grid sensitive;
   the dense-grid pass supports the guarded 116-panel policy but should not
   lower the policy to 114 panels. Run `685` validates that anatomy result with
   five passing checks: source readiness, exact four-row grid/two-panel/two-grid
   shape, 148 per-frequency rows, preserved aggregate-grid sensitivity,
   unchanged worst per-frequency maxima, no policy lowering, analytic-only
   claim boundary, figure output, and script snapshots. Run `686`
   sensitivity-hardens that validator: the exact run `684` source passes,
   while twenty-two damaged states fail as expected for source readiness,
   grid-row or frequency-row damage, target-case damage, panel or grid-count
   damage, grid-sensitivity damage, dense-lower flag damage, per-frequency max
   damage, tight-margin or guard-margin damage, lower-policy promotion, FDTD
   comparison promotion, real-3D promotion, GPU/HPC promotion, field-transfer
   promotion, field-FWI promotion, figure damage, and missing script snapshots.
   Run `687` refreshes the BEM transfer metric policy after the dense-grid and
   frequency-anatomy findings. The policy keeps aggregate high-band relative L2
   as the comparable acceptance metric only on a fixed frequency grid, keeps
   the `2.5e-05` guard margin before recommending a lower-cost endpoint, adds
   per-frequency anatomy as a diagnostic guard when aggregate metrics change
   across grids, and keeps 116 panels as the guarded analytic transfer
   endpoint. It explicitly does not lower the policy to 114 panels from the
   dense-grid aggregate result alone. Run `688` validates that policy with five
   passing checks: source readiness, five policy rows, preserved
   113/114/116 roles, preserved guard-margin boundary, preserved
   grid-sensitive aggregate metric and per-frequency diagnostic requirement,
   analytic-only claim boundary, figure output, and script snapshots. Run
   `689` sensitivity-hardens that validator: the exact run `687` policy
   passes, while fifteen damaged states fail as expected for source readiness,
   policy row or policy item damage, minimum-panel or guarded-panel damage,
   grid-sensitivity loss, per-frequency diagnostic removal, lower-policy
   promotion, FDTD comparison promotion, real-3D promotion, GPU/HPC promotion,
   field-transfer promotion, field-FWI promotion, figure damage, and missing
   script snapshots.
   Run `690` returns to the 35-field Bempp/FDTD comparison packet and creates
   the current live-delta monitor: the BEM side has two accepted files and 558
   accepted rows, while the matched-FDTD side still has zero of four required
   files present or accepted. The monitor separates the accepted BEM half from
   the absent matched-FDTD half, keeping real BEM/FDTD comparison, 3D
   validation claims, GPU/HPC work, field transfer, and field FWI blocked. Run
   `691` validates that monitor with seven passing checks covering source-chain
   readiness, component and phase shape, BEM acceptance, matched-FDTD absence,
   downstream blocking, figure output, and frozen script snapshots. Run `692`
   sensitivity-hardens that validator: the exact live-delta state passes,
   while fourteen damaged or prematurely promoted states fail as expected.
   Run `693` turns that live-delta state into a closure sequence: the accepted
   BEM baseline has two files and 558 rows, while the remaining comparison work
   is two matched-FDTD producer input CSV files, two input-bound exporter return
   CSV files, and then the final comparison gate. Run `694` validates that
   closure sequence with six passing checks covering source readiness, shape,
   accepted BEM baseline preservation, matched-FDTD gap preservation,
   downstream blocking, figure output, and frozen script snapshots. Run `695`
   sensitivity-hardens that validator: the exact closure sequence passes,
   while fourteen damaged or prematurely promoted states fail as expected.
   Run `696` adds a numeric receiver-grid robustness audit for the guarded
   116-panel analytic policy on the larger-radius controlling case
   `radius_75mm_baseline_eps`. It solves 116 and 128 panels at 9, 11, and 13
   scan positions. The 116-panel endpoint passes all three scan counts with
   maximum high-band relative L2 `0.0009518291083452528`, below the `0.001`
   target, while 128 panels also pass as the endpoint. The result supports
   116 panels as receiver-grid robust for this analytic worst-case check but
   does not promote project-FDTD, real 3D, GPU/HPC, field transfer, or field
   FWI claims. Run `697` validates that audit with six passing checks covering
   source readiness, scan/solve shape, target lock, transfer pass status,
   analytic-only boundary, figure output, and script snapshots. Run `698`
   sensitivity-hardens the validator: the exact receiver-grid audit passes,
   while thirteen damaged states fail as expected.
   Run `699` repeats the controlling larger-radius receiver-grid check for
   116 panels on the denser 49-frequency grid at 9, 11, and 13 scan positions.
   The 116-panel endpoint passes all three scan counts with maximum aggregate
   high-band relative L2 `0.0007643703508458867` and minimum margin
   `0.00023562964915411328` to the `0.001` target. This supports the
   receiver-grid robustness of the guarded 116-panel analytic policy under the
   49-frequency aggregate metric, while preserving the earlier per-frequency
   diagnostic caution and all project-FDTD, real-3D, GPU/HPC, field-transfer,
   and field-FWI blockers. Run `700` validates that dense-frequency audit with
   six passing checks covering source readiness, dense scan/solve shape,
   target lock, 116-panel pass status, analytic-only claim boundary, figure
   output, and frozen script snapshots. Run `701` sensitivity-hardens the
   validator: the exact run `699` audit passes, while fifteen damaged states
   fail as expected. Run `702` refreshes the receiver-grid policy from the
   validated 25-frequency and 49-frequency receiver-grid audits: 116 panels
   remain the guarded analytic endpoint, the worst aggregate high-band
   relative L2 is `0.0009518291083452528`, the minimum margin to the `0.001`
   target is `0.000048170891654747265`, fixed-frequency-grid comparison and
   per-frequency anatomy diagnostics remain required, and project-FDTD, real
   3D, GPU/HPC, field-transfer, and field-FWI claims remain blocked. Run `703`
   validates that policy refresh with six passing checks covering source
   readiness, metric/policy shape, guarded endpoint status, diagnostic policy,
   analytic-only boundary, figure output, and frozen script snapshots. Run
   `704` sensitivity-hardens the validator: the exact run `702` policy passes,
   while fifteen damaged or prematurely promoted states fail as expected.
   Run `705` returns to the 35-field BEM/FDTD bridge and turns the run `693`
   closure sequence into a dependency-level critical-path audit. The accepted
   BEM baseline is complete with two files and 558 rows. The root bridge
   blocker is now explicit: two matched-FDTD producer input CSV files are
   missing. The two input-bound exporter return files and the final six-file
   comparison gate remain downstream of those producer inputs, so real
   BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, and
   field FWI remain blocked. Run `706` validates that critical path with six
   passing checks covering source readiness, file/action/level shape, accepted
   BEM baseline preservation, matched-FDTD producer-input blocking, downstream
   blocking, figure output, and frozen script snapshots. Run `707`
   sensitivity-hardens the validator: the exact run `705` state passes, while
   seventeen damaged or prematurely promoted states fail as expected.
   Run `708` performs a current live-route rescan that reconciles the run
   `705` critical path with the earlier input-bound exporter route spec and
   the actual external staging directories. The directories exist, but zero of
   the four matched-FDTD route files are present or accepted. The first
   actionable blocker remains the two matched-FDTD producer input CSV files;
   exporter returns, the final comparison gate, 3D validation claims, GPU/HPC
   work, field transfer, and field FWI remain blocked. Run `709` validates
   that live rescan with six passing checks covering source readiness, route
   shape, empty live external paths, producer-input root blocking, downstream
   blocking, figure output, and frozen script snapshots. Run `710`
   sensitivity-hardens the validator: the exact run `708` state passes, while
   nineteen damaged or prematurely promoted states fail as expected.
   Run `711` creates a non-live matched-FDTD producer-input handoff template
   pack tied to the latest live route. It writes two template CSV files under
   the run output folder, preserving 558 locked row identities and eleven
   columns per file while leaving 2790 solver-provenance cells and 558 required
   FDTD value cells blank. The live external input files remain absent, so the
   packet is a handoff aid only and does not unlock exporter execution,
   BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, or
   field FWI. Run `712` validates the packet with seven passing checks covering
   source readiness, manifest/action shape, locked-row preservation, blank real
   fields, absent live files, downstream blocking, figure output, and frozen
   script snapshots. Run `713` sensitivity-hardens the validator: the exact
   non-live template packet passes, while fourteen damaged or prematurely
   promoted states fail as expected.
   Run `714` dry-runs the input-bound exporter acceptance checks against the
   run `711` non-live producer input templates. The two templates preserve all
   558 locked row identities, but both correctly fail acceptance because real
   solver provenance and real FDTD values are blank. The dry-run records 2790
   validation errors across six expected missing-field families, zero accepted
   files, zero accepted rows, zero live input files, and no exporter/FDTD/GPU
   readiness. Run `715` validates that dry-run with seven passing checks
   covering source readiness, file/row shape, row-identity matching, expected
   rejection, error-family accounting, downstream blocking, figure output, and
   frozen script snapshots. Run `716` sensitivity-hardens the validator: the
   exact non-evidence rejection state passes, while thirteen damaged or
   prematurely promoted states fail as expected.
   Run `717` audits the `input_contract_sha256` gate for the matched-FDTD
   producer input path. It defines two canonical per-file contract hashes for
   the 558 required producer rows and shows that the current exporter accepts
   two arbitrary-but-syntactically-valid hex64 contract hashes. The current
   gate therefore checks hash syntax but not exact contract binding. Exporter
   execution, real BEM/FDTD comparison, 3D validation claims, GPU/HPC work,
   field transfer, and field FWI remain blocked. Run `718` validates this
   audit with seven passing checks covering source readiness, canonical hash
   shape, probe counts, arbitrary-hash gap exposure, canonical strict-hash pass
   behavior, downstream blocking, figure output, and frozen script snapshots.
   Run `719` sensitivity-hardens that validator: the exact audit state passes,
   while sixteen damaged or prematurely promoted states fail as expected.
   Run `720` prototypes the strict contract-hash guard without changing the
   historical shared exporter in place. The current exporter passes four probe
   cases because it accepts canonical and arbitrary hex64 hashes; the strict
   guard passes only the two canonical-hash cases and rejects the two arbitrary
   hashes plus four blank or non-hex damaged cases. Exporter execution, real
   BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, and
   field FWI remain blocked. Run `721` validates that prototype with seven
   passing checks covering source readiness, probe/contract shape, strict pass
   counts, canonical-hash acceptance, noncanonical rejection, downstream
   blocking, figure output, and frozen script snapshots. Run `722`
   sensitivity-hardens that validator: the exact strict-guard state passes,
   while sixteen damaged or prematurely promoted states fail as expected.
   Run `723` moves the strict contract-hash behavior into the shared
   input-bound exporter as an opt-in strict mode. Synthetic probes show that
   default mode still passes four cases while strict mode passes only the two
   canonical-hash cases and rejects two arbitrary hex64 hashes plus four blank
   or non-hex damaged cases. A command-line smoke writes one synthetic accepted
   file under the run output folder and rejects the arbitrary-hash synthetic
   file; no real evidence, exporter readiness, real BEM/FDTD comparison, 3D
   validation claim, GPU/HPC work, field transfer, or field FWI is promoted.
   Run `724` validates that shared-exporter strict-mode smoke with six passing
   checks covering source readiness, strict pass counts, strict hash behavior,
   command-line smoke behavior, downstream blocking, figure output, and frozen
   script snapshots. Run `725` sensitivity-hardens that validator: the exact
   strict-mode smoke state passes, while sixteen damaged or prematurely
   promoted states fail as expected.
   Run `726` applies the strict acceptance path to the current live
   matched-FDTD producer input routes without writing to those routes. Both
   route parent directories exist, but zero of two live producer input files
   are present, zero strict-mode rows are accepted, and exporter execution,
   real BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field
   transfer, and field FWI remain blocked. Run `727` validates that rescan
   with seven passing checks covering source readiness, route shape, absent
   live files, absent strict acceptance, no completed actions, downstream
   blocking, figure output, and frozen script snapshots. Run `728`
   sensitivity-hardens that validator: the exact empty-live-route strict-mode
   state passes, while fourteen damaged or prematurely promoted states fail as
   expected.
   Run `729` refreshes the producer handoff templates for strict contract-hash
   mode. The two templates preserve 558 locked rows and eleven columns while
   pre-filling 558 exact `input_contract_sha256` values. The remaining blanks
   are real solver provenance and returned FDTD values: 2232 solver-provenance
   cells and 558 returned-value cells. The templates remain non-live handoff
   files and do not unlock exporter execution, real BEM/FDTD comparison, 3D
   validation claims, GPU/HPC work, field transfer, or field FWI. Run `730`
   validates that template pack with seven passing checks covering source
   readiness, template shape, prefilled contract hashes, blank real fields, the
   single completed hash-preservation action, downstream blocking, figure
   output, and frozen script snapshots. Run `731` sensitivity-hardens that
   validator: the exact strict-contract template state passes, while fifteen
   damaged or prematurely promoted states fail as expected.
   Run `732` dry-runs the strict shared-exporter acceptance path against those
   strict-contract templates. All 558 rows now pass exact contract-hash binding
   with zero hash errors, but both files correctly fail acceptance because real
   solver provenance and returned FDTD values remain blank. The dry run records
   2232 validation errors across five real-data error families, zero accepted
   files, zero live input files, and no exporter/FDTD/GPU readiness. Run `733`
   validates that dry run with seven passing checks covering source readiness,
   file/row shape, strict contract-hash acceptance, expected blank-template
   rejection, real-data error-family accounting, downstream blocking, figure
   output, and frozen script snapshots. Run `734` sensitivity-hardens that
   validator: the exact strict-template dry-run state passes, while eighteen
   damaged or prematurely promoted states fail as expected.
   Run `735` adds the paired positive control: it fills the same two strict
   templates with run-local synthetic solver provenance and synthetic returned
   FDTD values. The strict acceptance path accepts both synthetic files and all
   558 rows with zero validation errors and zero strict-hash errors, while
   preserving zero real evidence, zero live producer input files, and blocked
   exporter/comparison/GPU/field readiness. Run `736` validates that synthetic
   acceptance smoke with six passing checks covering source readiness, shape,
   strict synthetic acceptance, synthetic-boundary preservation, downstream
   blocking, figure output, and frozen script snapshots. Run `737`
   sensitivity-hardens that validator: the exact synthetic smoke passes, while
   fourteen damaged or prematurely promoted states fail as expected.
   Run `738` converts the strict-template dry run and synthetic positive
   control into the current real-producer acceptance frontier. The strict hash
   path is closed with 558 exact contract hashes and zero hash errors, but zero
   live producer files are present and 2232 real-data cells remain unresolved:
   1116 solver-provenance cells, 558 real FDTD export flags, and 558 returned
   FDTD values. Run `739` validates that frontier with eight passing checks.
   Run `740` sensitivity-hardens the validator: the exact frontier passes,
   while seventeen damaged or falsely promoted states fail with zero unexpected
   outcomes. Real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until both live producer files pass
   strict acceptance with real values.
   Run `741` converts that aggregate frontier into a per-file completion
   worksheet. Each of the two live producer files has 279 required rows; every
   row still needs real solver status, real solver log hash, real FDTD export
   flag, and the returned value for that file type. The worksheet records 2232
   total missing real-data cells, zero live files present, zero
   strict-acceptance-ready files, and no real comparison or downstream
   promotion.
   Run `742` converts the worksheet into an execution-priority map. The two
   strict producer files share 279 receiver-frequency pairs over 31 receivers
   and 9 frequencies. The map splits them into five batches: one center-pair
   smoke, an 8-pair center-receiver frequency sweep, a 30-pair center-frequency
   receiver sweep, a 120-pair midband receiver matrix, and a 120-pair edgeband
   receiver matrix. The first three batches cover 39 pairs and 312 real-data
   cells, while full strict acceptance still requires all 279 pairs, 558 file
   rows, and 2232 real-data cells. Real BEM/FDTD comparison, 3D validation,
   GPU/HPC work, field transfer, and field FWI remain blocked until both live
   producer files pass strict acceptance with real values.
   Run `743` turns that priority map into a staged handoff packet for the real
   matched-FDTD producer. It writes ten stage-only CSV files and ten cumulative
   CSV files under the BEM experiment output folder. Stage 1 is a two-row
   center-pair smoke return, stages 2 and 3 expand to 18 and 78 cumulative rows,
   and the final stage reaches the full 558-row strict input requirement. The
   packet makes the first real return check small and concrete while preserving
   the rule that real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
   transfer, and field FWI remain blocked until the final cumulative files are
   fully populated and strict-accepted.
   Run `744` exercises the stage-1 packet with an output-local synthetic
   partial return. The two center-pair rows can be filled and checked locally
   with zero blank required fields and two row-level schema passes, but the
   result is only 2 of the 558 strict file rows required for full acceptance.
   It is mechanics coverage for the smallest return unit, not real evidence or
   comparison readiness.
   Run `745` defines the live stage-1 return contract that replaces the
   synthetic smoke with real producer files. The contract expects two one-row
   CSV files under the existing external input route: one source-hash manifest
   row and one scattered-norm row, both for receiver index `15` at `1.0 GHz`.
   Both parent directories exist, but zero live stage-1 files are present.
   Full strict acceptance and real BEM/FDTD comparison remain blocked until
   the complete live producer files are returned and strict-accepted.
   Run `746` defines the live stage-2 return contract for the center-receiver
   frequency sweep. The contract expects two eight-row CSV files under the
   same external input route: one source-hash manifest and one scattered-norm
   table for receiver index `15` at eight non-center frequencies from `0.4` to
   `3.0 GHz`. Both parent directories exist, but zero live stage-2 files are
   present. Full strict acceptance and real BEM/FDTD comparison remain blocked
   until the complete live producer files are returned and strict-accepted.
   Run `747` defines the live stage-3 return contract for the center-frequency
   receiver sweep. The contract expects two thirty-row CSV files under the same
   external input route: one source-hash manifest and one scattered-norm table
   for receiver indices `0-14` and `16-30` at `1.0 GHz`. Both parent
   directories exist, but zero live stage-3 files are present. Full strict
   acceptance and real BEM/FDTD comparison remain blocked until the complete
   live producer files are returned and strict-accepted.
   Run `748` defines the live stage-4 return contract for the midband receiver
   matrix. The contract expects two 120-row CSV files under the same external
   input route: one source-hash manifest and one scattered-norm table for
   receiver indices `0-14` and `16-30` at `0.75`, `1.25`, `1.5`, and `2.0 GHz`.
   Both parent directories exist, but zero live stage-4 files are present.
   Full strict acceptance and real BEM/FDTD comparison remain blocked until
   the complete live producer files are returned and strict-accepted.
   Run `749` defines the live stage-5 return contract for the edgeband receiver
   matrix and closes the five-stage live-return contract sequence. The contract
   expects two 120-row CSV files under the same external input route: one
   source-hash manifest and one scattered-norm table for receiver indices
   `0-14` and `16-30` at `0.4`, `0.5`, `2.5`, and `3.0 GHz`. Both parent
   directories exist, but zero live stage-5 files are present. Completing
   stages `1-5` with real values would cover all 279 receiver-frequency pairs
   and all 558 strict file rows, but full strict acceptance and real BEM/FDTD
   comparison remain blocked until all live producer files are returned and
   strict-accepted.
   Run `750` combines the stage-1 through stage-5 live-return contracts into a
   single checklist. The ledger contains ten expected live files, five contract
   stages, all 279 receiver-frequency pairs, and all 558 strict file rows. All
   ten live parent directories exist and zero live files are present. The BEM
   live-return contract is complete as a checklist, but strict acceptance and
   real BEM/FDTD comparison remain blocked until all ten live files are
   returned and accepted.
   Run `751` adds a reusable intake gate for those ten staged live producer
   files. The gate can classify missing files, unreadable CSV files, row-count
   mismatches, missing required fields, blank required values, failed real-FDTD
   export flags, and accepted files. The current state remains pre-return: all
   ten parent directories exist, zero live files are present, and all 2790
   required real-data cells are still unfilled. Strict acceptance, real
   BEM/FDTD comparison, 3D validation, GPU/HPC work, field transfer, and field
   FWI remain blocked until all ten files pass intake.
   Run `752` validates the saved run `751` intake gate from artifacts. Seven of
   seven checks pass, confirming source readiness, ten expected live files,
   zero live files present, preserved stage row shape, blocked acceptance,
   blocked downstream states, and figure/script snapshot presence. Sensitivity
   hardening remains the next step before relying on the gate for damaged
   future returns.
   Run `753` sensitivity-hardens that validator. The exact run `751` intake
   state passes, while eight damaged states fail as expected: source readiness
   damage, missing-file count drift, file-status damage, stage-shape damage,
   false acceptance, downstream promotion, figure damage, and script-snapshot
   damage. Use runs `751-753` as the guarded BEM live-return intake block.
   Run `754` adds the paired output-local positive control for the smallest
   stage-1 return. Two run-local files, one source-hash manifest row and one
   scattered-norm row, pass intake with zero blank required cells. This proves
   the gate's positive mechanics without accepting live producer evidence.
   Real BEM/FDTD comparison remains blocked until live producer files pass the
   guarded intake path.
   Run `755` checks whether those accepted stage-1 positive-control rows can
   feed the comparison layer. They cover only two of the 558 strict rows needed
   for full BEM/FDTD comparison, so the handoff remains blocked. The run keeps
   the positive control as mechanics coverage only.
   Run `756` defines and tests the future comparison metrics on two tiny
   synthetic complex-valued rows. The formulas compute amplitude relative
   error, wrapped phase error, and complex relative error. This prepares the
   numerical comparison layer without using real BEM/FDTD values or promoting a
   real comparison claim. Real comparison remains blocked until all 558 strict
   rows contain accepted real numeric values.
   Run `757` validates that metric-definition smoke from saved outputs. Seven
   of seven checks pass: source readiness, synthetic-only row status,
   formula recomputation, metric-max preservation, strict comparison boundary,
   blocked downstream states, and figure/script snapshot presence.
   Run `758` sensitivity-hardens that validator. The exact saved state passes,
   while ten damaged states fail: source flag damage, row-count damage,
   formula damage, metric-max damage, false real-value promotion, false
   comparison promotion, strict-boundary damage, downstream promotion, figure
   damage, and script-snapshot damage. Use runs `756-758` as the synthetic-only
   metric-definition block before real numeric BEM/FDTD comparison.
   Run `759` audits the existing live-return schema against those metric
   requirements. The current contract has equivalents for five of thirteen
   required columns and is sufficient for scalar scattered-norm checks only.
   It is missing row identity, receiver/frequency coordinates, complex BEM
   components, complex FDTD components, and a normalization label. A real
   numeric return-schema addendum is required before amplitude/phase comparison
   can be enabled.
   Run `760` defines that addendum. It requires five stage-specific complex
   metric-value files covering all 279 receiver-frequency pairs, with thirteen
   fields per row and 1,116 required complex component cells across BEM and
   FDTD values. The schema is defined but unfilled; all five addendum files are
   still absent, so real amplitude/phase comparison remains blocked.
   Run `761` validates the saved addendum schema. Seven of seven checks pass:
   source addendum readiness, five represented addendum files, preserved stage
   row shape, preserved required cell counts, all required columns present in
   each addendum file, unfilled comparison-blocked state, and figure/script
   snapshot presence.
   Run `762` sensitivity-hardens that validator. The exact saved state passes,
   while nine damaged states fail: source flag damage, file-count damage,
   stage-row damage, required-column damage, cell-count damage, false filled
   state, false comparison promotion, figure damage, and script-snapshot
   damage. Use runs `759-762` as the guarded real numeric return-schema block.
   Run `763` adds the live-return intake gate for those five complex metric
   addendum files. The gate checks row counts, required columns, finite numeric
   values, finite BEM/FDTD complex components, real FDTD export flags, and
   completed solver status. The current state is pre-return: five parent
   directories exist, zero addendum files are present, zero rows are accepted,
   and real comparison remains blocked.
   Run `764` validates that intake gate from saved outputs. Seven of seven
   checks pass: source intake readiness, five represented addendum files,
   preserved required rows/cells, pre-return state, explicit missing columns,
   blocked real comparison, and figure/script snapshot presence.
   Run `765` sensitivity-hardens that intake validator. The exact saved state
   passes, while nine damaged states fail: source flag damage, file-count
   damage, required-row damage, live-file promotion, false acceptance,
   missing-column count damage, comparison promotion, figure damage, and
   script-snapshot damage. Use runs `763-765` as the guarded complex metric
   intake block.
   Run `766` adds an output-local synthetic positive-control consumer for the
   complex metric addendum shape. It writes five synthetic addendum CSV files,
   covers all 279 receiver-frequency pairs, and computes amplitude relative
   error, wrapped phase error, and complex relative error for every row. The
   run proves consumer mechanics only: no real FDTD export rows are accepted,
   no real BEM/FDTD comparison is promoted, and run `763-765` remains the guard
   for future real addendum files.
   Run `767` validates the saved run `766` artifacts. Seven of seven checks
   pass: source positive-control readiness, five files and 279 rows, preserved
   stage shape, schema-shaped synthetic files with zero real FDTD-exported
   rows, positive finite metric values, blocked real comparison, and
   figure/script snapshot presence.
   Run `768` sensitivity-hardens that validator. The exact saved run `766`
   state passes, while ten damaged states fail: source flag damage, file-count
   damage, metric-row damage, stage-shape damage, real-export damage,
   synthetic-row-count damage, metric-value damage, false real-comparison
   promotion, figure damage, and script-snapshot damage. Use runs `766-768` as
   the guarded BEM/FDTD complex metric consumer mechanics block.
   Run `769` writes five output-local real-return CSV templates for the complex
   metric addendum. The templates cover all 279 receiver-frequency rows and all
   thirteen required columns, but 3,348 required value cells are blank. No
   template is accepted as a real return, no real FDTD export row is present,
   and real BEM/FDTD comparison remains blocked until live files pass the
   guarded intake gate.
   Run `770` validates the saved run `769` templates from disk. Seven of seven
   checks pass: source template-pack readiness, five files and 279 rows,
   required columns in every template, blank solver-value fields with stable
   pair identifiers, output-local non-accepted template status, blocked real
   comparison, and figure/script snapshot presence.
   Run `771` sensitivity-hardens that validator. The exact run `769` template
   pack passes, while twelve damaged states fail as expected: source flag
   damage, file-count damage, row-count damage, required-column damage,
   blank-value damage, pair-id damage, output-location damage, false
   acceptance, real-export promotion, real-comparison promotion, figure damage,
   and script-snapshot damage. Use runs `769-771` as the guarded BEM/FDTD
   complex metric real-return template-pack block.
   Run `772` reconciles those five real-return templates against the live
   complex metric addendum intake paths. All five output-local templates are
   present and cover 279 rows, all five live parent directories are present,
   zero live addendum files are present, zero files are ready for guarded live
   intake, and zero files are accepted as real returns. Real BEM/FDTD
   comparison remains blocked.
   Run `773` validates the saved run `772` reconciliation table. Seven of
   seven checks pass: source reconciliation readiness, five files and 279 rows,
   present blank templates, absent and unaccepted live addendum files, preserved
   status split, blocked real comparison, and figure/script snapshot presence.
   Run `774` sensitivity-hardens that validator. The exact run `772`
   pre-return state passes, while fourteen damaged states fail as expected:
   source flag damage, file-count damage, row-count damage, template-missing
   damage, blank-value damage, live-parent damage, live-file promotion,
   ready-for-intake promotion, false file acceptance, real-return acceptance,
   status-split damage, real-comparison promotion, figure damage, and
   script-snapshot damage. Use runs `772-774` as the guarded BEM/FDTD complex
   metric live-intake reconciliation block.
   Run `775` creates the non-executed staging plan for those five real complex
   metric CSV files. It defines five producer-file placeholders, five exact
   live intake paths, five non-executed copy commands, and four guarded action
   groups: produce real CSVs, preflight real CSVs, stage only real CSVs, then
   rerun intake and comparison gates. Blank templates are explicitly marked as
   non-stageable, zero commands are executed, and real BEM/FDTD comparison
   remains blocked.
   Run `776` validates the saved run `775` staging plan. Seven of seven checks
   pass: source staging-plan readiness, five staging files and 279 rows,
   non-stageable blank-template status, no real producer or live files ready,
   five present but non-executed commands, blocked action groups and real
   comparison, and figure/script snapshot presence.
   Run `777` sensitivity-hardens that validator. The exact run `775`
   non-executed staging plan passes, while fifteen damaged states fail as
   expected: source flag damage, file-count damage, row-count damage,
   template-copy permission damage, missing not-template guard, real-producer
   file promotion, live-file promotion, ready-to-stage promotion,
   executed-command promotion, copy-command damage, action-count damage,
   ready-action promotion, real-comparison promotion, figure damage, and
   script-snapshot damage. Use runs `775-777` as the guarded BEM/FDTD complex
   metric real-return staging-plan block.
   Run `778` defines the preflight gate for those five real complex metric CSV
   files before staging. It checks not-template path, CSV existence, all
   thirteen required columns, row-count match, no blank required value cells,
   real FDTD export flags, completed solver status, and finite complex
   BEM/FDTD values. The current state remains pre-return: zero producer CSVs
   are present, zero files pass preflight, zero files are ready to stage, and
   real BEM/FDTD comparison remains blocked.
   Run `779` validates the saved run `778` preflight gate. Seven of seven
   checks pass: source preflight readiness, five-file and 279-row coverage,
   thirteen-column schema enforcement, absent producer CSV files, zero
   preflight-passed or stageable files, blocked real comparison, and
   figure/script snapshot presence.
   Run `780` sensitivity-hardens that validator. The exact run `778`
   absent-producer state passes, while fourteen damaged states fail as
   expected: source flag damage, file-count damage, row-count damage,
   required-column damage, required-columns promotion, producer-file promotion,
   observed-row promotion, row-match promotion, preflight-passed promotion,
   ready-to-stage promotion, executed-command promotion, real-comparison
   promotion, figure damage, and script-snapshot damage. Use runs `778-780` as
   the guarded BEM/FDTD complex metric real-return preflight block.
   Run `781` records the claim boundary after that preflight block. Two claims
   are guarded: the complex-metric return schema and the fail-closed preflight
   gate. Three claims remain blocked: real BEM/FDTD complex-metric comparison,
   detector or inversion use, and field/3D transfer. Zero producer CSV files
   are present, zero files pass preflight, and no downstream claim is promoted.
   Run `782` validates that saved claim boundary. Seven of seven checks pass,
   confirming claim counts, source preflight metrics, guarded rows, blocked
   rows, downstream blocks, figure validation, and script snapshots.
   Run `783` sensitivity-hardens the validator. The exact run `781` boundary
   passes, while thirteen damaged states fail as expected: policy-label
   damage, claim-count damage, guarded-count damage, blocked-count damage,
   guarded-ready damage, blocked-ready promotion, producer-file promotion,
   preflight-pass promotion, comparison promotion, downstream promotion,
   sensitivity damage, figure damage, and script-snapshot damage. Use runs
   `781-783` as the guarded post-preflight claim-boundary block.
   Run `784` splits the absent five-file real-return blocker into producer-side
   dependencies. Across 279 metric rows and 13 required columns, 279 pair-id
   cells are already filled, 558 BEM complex-value cells can be prepared on the
   BEM side, 558 shared sampling cells and 279 normalization-policy cells remain
   to be filled, and 558 FDTD complex-value cells plus 1395 FDTD provenance and
   status cells require matched FDTD export. Zero producer files are present,
   zero files pass preflight, and no real comparison or downstream claim is
   promoted.
   Run `785` validates the saved run `784` dependency audit. Eight of eight
   checks pass, confirming dependency-group shape, 3627 required cells, 3348
   blank cells, the 558/558/1395 BEM-value/FDTD-value/FDTD-provenance split,
   five-stage row coverage, absent producer files, blocked downstream claims,
   and figure/script snapshot presence.
   Run `786` sensitivity-hardens that validator. The exact run `784` state
   passes, while twelve damaged states fail as expected: source-ready damage,
   dependency-group damage, required-cell damage, blank-cell damage, stage-shape
   damage, BEM-count damage, FDTD-count damage, producer-file promotion,
   preflight promotion, comparison promotion, figure damage, and script-snapshot
   damage. Use runs `784-786` as the current BEM/FDTD complex-metric
   producer-side dependency split.
   Run `787` checks whether the accepted scalar BEM-side return files from run
   `557` can fill the BEM fields required by the complex-metric schema. The
   accepted source has two files and 279 scalar-norm rows, and its receiver and
   frequency sampling can be reused. It has zero compatible `bem_real` or
   `bem_imag` cells, so direct scalar-norm repackaging is rejected and a new
   BEM complex-field exporter is required before a partial complex-metric
   producer fill.
   Run `788` validates the saved run `787` compatibility audit. Seven of seven
   checks pass, confirming the two-file scalar source shape, absent complex
   component columns, reusable sampling fields, 558 required BEM complex cells,
   zero compatible BEM complex cells, required new complex-field exporter, and
   blocked real comparison.
   Run `789` sensitivity-hardens that validator. The exact run `787` state
   passes, while eleven damaged states fail as expected: source-ready damage,
   file-count damage, scalar-row-count damage, complex-source-column promotion,
   complex-compatibility promotion, sampling damage, scalar repackage
   promotion, exporter-requirement removal, comparison promotion, figure damage,
   and script-snapshot damage. Use runs `787-789` as the current BEM source
   compatibility boundary for complex-metric work.
   Run `790` closes the BEM-side complex-field gap for the five-stage
   complex-metric packet. It reruns the fine-mesh Bempp receiver solve for nine
   frequencies and exports the `scattered_ey` complex component into five
   partial stage files. All 279 receiver-frequency rows have finite `bem_real`
   and `bem_imag` values, giving 558 filled BEM complex cells. The files remain
   partial and non-stageable because 558 FDTD value cells and 1395 FDTD
   provenance/status cells are blank; zero files pass preflight and real
   BEM/FDTD comparison remains blocked.
   Run `791` validates the saved run `790` partial export. Seven of seven
   checks pass, confirming nine completed frequency solves, five stage files
   with 279 rows, 558 finite BEM complex cells, blank FDTD-dependent fields,
   zero preflight passes, blocked downstream claims, and figure/script snapshot
   presence.
   Run `792` sensitivity-hardens that validator. The exact run `790` state
   passes, while eleven damaged states fail as expected: source-ready damage,
   frequency damage, stage-file damage, row-count damage, BEM-value damage,
   FDTD-value promotion, FDTD-provenance promotion, preflight promotion,
   comparison promotion, figure damage, and script-snapshot damage. Use runs
   `790-792` as the current BEM-side complex-component export block.
   Run `793` records the claim boundary after that BEM-side export block. Two
   claims are guarded: finite BEM complex-component values are available for all
   279 receiver-frequency rows, and the five partial stage files are guarded as
   BEM-side evidence with blank FDTD fields. Three claims remain blocked: real
   BEM/FDTD complex-metric comparison, detector or inversion use, and field/3D
   transfer. The packet contains 558 BEM complex-value cells, while 558 FDTD
   value cells and 1395 FDTD provenance/status cells remain blank.
   Run `794` validates the saved run `793` boundary. Seven of seven checks pass,
   confirming claim counts, guarded partial-export rows, blocked comparison
   rows, BEM/FDTD cell counts, downstream blocked states, figure validation, and
   script snapshots.
   Run `795` sensitivity-hardens that validator. The exact run `793` boundary
   passes, while fourteen damaged states fail as expected: policy-label damage,
   claim-count damage, guarded-count damage, blocked-count damage,
   guarded-ready damage, blocked-ready promotion, BEM value-count damage, FDTD
   blank-count damage, preflight promotion, comparison promotion, downstream
   promotion, figure damage, and script-snapshot damage. Use runs `793-795` as
   the current claim boundary for the BEM-side complex-component partial export.
   Run `796` audits whether the older input-bound matched-FDTD route can
   directly complete the new complex-metric partial packet. Three dimensions
   are reusable: receiver/frequency identity, strict contract-hash guards, and
   the 558-row value-count scale. Four dimensions block direct reuse: the older
   route expects `returned_fdtd_scattered_norm` and
   `returned_fdtd_source_hash` rather than `fdtd_real`/`fdtd_imag`, it has a
   two-input/two-return topology rather than five complex stage files, it does
   not directly fill the current FDTD provenance/status columns, and it still
   produces no real complex comparison output. Build a new complex FDTD adapter
   around the reusable identity/hash guards; do not treat the scattered-norm
   route as a direct completion path for run `790`.
   Run `797` validates the saved run `796` compatibility audit. Seven of seven
   checks pass, confirming the source identity, seven compatibility dimensions,
   three directly reusable dimensions, four blocking dimensions, the 5-file/
   279-row complex packet shape, 558 required FDTD complex value cells, 558
   existing input rows in the older route, the value-field mismatch, the
   required new complex FDTD adapter, blocked direct exporter reuse, and blocked
   downstream states.
   Run `798` sensitivity-hardens that validator. The exact run `796` audit
   passes, while fifteen damaged states fail as expected: policy-label damage,
   dimension-count damage, direct-reuse-count damage, blocking-count damage,
   stage-file-count damage, FDTD-value-cell-count damage, existing-input-row
   damage, value-field promotion, topology promotion, adapter-requirement
   removal, direct-exporter promotion, comparison promotion, downstream
   promotion, figure damage, and script-snapshot damage. Use runs `796-798` as
   the guarded decision that a new complex FDTD adapter is required.
   Run `799` converts that adapter decision into a concrete complex FDTD
   adapter contract. The adapter input requires twelve columns: stage, pair id,
   receiver index, frequency, `fdtd_real`, `fdtd_imag`, returned FDTD source
   hash, solver run id, solver status, solver log hash, real-export flag, and
   input contract hash. The completed stage files would fill eleven current
   packet columns and must supply 558 FDTD complex-value cells plus 1395
   provenance/status cells before comparison can run. The contract is ready,
   but adapter implementation, completed stage files, real BEM/FDTD comparison,
   field transfer, and 3D/HPC remain blocked.
   Run `800` validates the saved run `799` adapter contract. Seven of seven
   checks pass, confirming source readiness, the twelve input columns, eleven
   completed-stage output-fill columns, four identity columns, two complex-value
   columns, six provenance/guard columns, five mapping steps, eight guards, the
   5-file/279-row packet shape, the 558 FDTD complex-value cells, the 1395
   provenance/status cells, and blocked adapter implementation/comparison
   states.
   Run `801` sensitivity-hardens that validator. The exact run `799` contract
   passes, while sixteen damaged states fail as expected: policy-label damage,
   column-count damage, output-fill-count damage, value-column damage,
   mapping-count damage, ready-mapping promotion, guard-count damage,
   ready-guard promotion, stage-file-count damage, FDTD-cell-count damage,
   adapter-implementation promotion, completed-output promotion, comparison
   promotion, downstream promotion, figure damage, and script-snapshot damage.
   Use runs `799-801` as the guarded complex FDTD adapter contract before any
   implementation work.
   Run `802` creates the guarded interface checkpoint for that contract. It
   computes the canonical input contract hash
   `8c0e4be114e3c7d8703aa8b0afaa468c6dd33968c62742fdff01bc52a736339a`
   for the 279 required receiver-frequency identities and records six interface
   components. Three are ready: the canonical contract hash, input-column
   contract, and completed-stage output-column contract. Three remain blocked:
   real FDTD complex input, completed-stage writing, and real BEM/FDTD
   comparison. The interface guard produces zero evidence and keeps completed
   outputs, field transfer, and 3D/HPC blocked.
   Run `803` validates the saved run `802` interface guard. Six of six checks
   pass, confirming source readiness, the canonical contract hash, the 279-row
   identity payload, twelve adapter input columns, eleven completed-stage output
   columns, six interface components, three ready non-evidence interface
   components, zero evidence-producing components, and blocked real-input,
   writer, completed-output, comparison, and 3D/HPC states.
   Run `804` sensitivity-hardens that validator. The exact run `802` interface
   guard passes, while thirteen damaged states fail as expected: policy-label
   damage, contract-hash damage, identity-payload damage, interface-count
   damage, ready-count damage, evidence promotion, input promotion, writer
   promotion, completed-output promotion, comparison promotion, downstream
   promotion, figure damage, and script-snapshot damage. Use runs `802-804` as
   the guarded non-evidence interface checkpoint before adding a writer path.
   Run `805` adds that writer path as a fail-closed dry run. It reads the five
   BEM partial stage files from run `790`, checks the required complex FDTD
   input contract hash, and finds no real FDTD complex input file. The dry run
   accepts zero FDTD rows, leaves all 279 receiver-frequency identities missing
   on the FDTD side, writes zero completed stage files, and keeps real BEM/FDTD
   comparison, field transfer, and 3D/HPC blocked.
   Run `806` validates the saved run `805` writer dry run. Eight of eight
   checks pass, confirming the five-stage/279-row partial packet shape, absent
   candidate FDTD complex input, zero accepted FDTD rows, 279 missing FDTD
   identities, zero completed stage files, the stable contract hash, figure
   validation, script snapshots, and blocked comparison/downstream states.
   Run `807` sensitivity-hardens that validator. The exact run `805` dry-run
   state passes, while fifteen damaged states fail as expected: policy-label
   damage, stage-count damage, partial-row-count damage, candidate-input
   promotion, adapter-input-row promotion, accepted-row promotion, missing-row
   damage, completed-file promotion, full-input promotion, completed-ready
   promotion, comparison promotion, downstream promotion, contract-hash damage,
   figure damage, and script-snapshot damage. Use runs `805-807` as the guarded
   complex FDTD adapter writer dry-run block before any non-dry-run writer is
   allowed to complete BEM/FDTD comparison files.
   Run `808` creates the producer-side complex FDTD adapter input template. It
   contains all 279 receiver-frequency identities and the canonical contract
   hash, with twelve adapter input columns. Identity and contract-hash cells are
   prefilled, while 558 FDTD real/imaginary value cells and 1395 FDTD
   provenance/status cells remain blank. The template is ready for real FDTD
   fill-in but is not accepted as evidence and does not promote completed stage
   files or BEM/FDTD comparison.
   Run `809` validates the saved run `808` template packet. Eight of eight
   checks pass, confirming the twelve-column schema, 279 template rows, five
   stage groups, 1116 prefilled identity cells, 279 prefilled contract-hash
   cells, 558 blank FDTD value cells, 1395 blank FDTD provenance/status cells,
   figure validation, script snapshots, and blocked evidence/comparison states.
   Run `810` sensitivity-hardens that validator. The exact run `808` template
   passes, while twelve damaged states fail as expected: policy-label damage,
   schema damage, row-count damage, stage-shape damage, contract-hash damage,
   filled FDTD value blanks, filled FDTD provenance blanks, evidence promotion,
   comparison promotion, downstream promotion, figure damage, and
   script-snapshot damage. Use runs `808-810` as the guarded complex FDTD
   fill-in template block.
   Run `811` guards the external handoff boundary for that template. The
   output-local template exists with 279 rows and is not under the external
   return root. The expected external filled-input file path exists only as a
   parent directory; the real input CSV is absent, zero external rows are
   accepted, and completed stage files, real BEM/FDTD comparison, field
   transfer, and 3D/HPC remain blocked.
   Run `812` validates the saved run `811` handoff guard. Seven of seven checks
   pass, confirming the two-row handoff shape, output-local template presence,
   279 template rows, separation from the external return root, absent external
   filled-input file, zero accepted external rows, blocked comparison/downstream
   states, figure validation, and script snapshots.
   Run `813` sensitivity-hardens that validator. The exact run `811` handoff
   guard passes, while eleven damaged states fail as expected: policy-label
   damage, handoff-shape damage, template disappearance, template row-count
   damage, template-under-external-root promotion, external-input presence
   promotion, external-input acceptance promotion, comparison promotion,
   downstream promotion, figure damage, and script-snapshot damage. Use runs
   `811-813` as the guarded external handoff boundary for real complex FDTD
   input.
   Run `814` records the claim boundary after that guarded handoff block. Two
   claims are guarded: the 279-row complex FDTD input template is a valid
   fill-in contract, and the external filled-input handoff is fail-closed. Three
   claims remain blocked: real external FDTD complex input, completed BEM stage
   files with FDTD real/imaginary values, and real BEM/FDTD comparison or
   downstream escalation. Zero external FDTD rows are accepted.
   Run `815` validates the saved run `814` claim boundary. Eight of eight
   checks pass, confirming the five-claim shape, two guarded claims, three
   blocked claims, 279 output-local template rows, zero external rows, zero
   accepted external rows, eleven rejected damaged handoff states, blocked
   comparison/downstream states, figure validation, and script snapshots.
   Run `816` sensitivity-hardens that validator. The exact run `814` boundary
   passes, while seventeen damaged states fail as expected: policy-label damage,
   claim-count damage, guarded/blocked-count damage, missing guarded claims,
   claim-evidence damage, external-input promotion, template-row-count damage,
   sensitivity damage, blocked-support damage, completed-stage promotion,
   comparison promotion, field/3D promotion, figure damage, and script-snapshot
   damage. Use runs `814-816` as the guarded BEM complex FDTD external handoff
   claim-boundary block.
   Run `817` defines the real external complex FDTD input preflight gate after
   that claim boundary. The expected external CSV is absent, so zero rows are
   accepted. A future real return must provide 279 matching receiver-frequency
   identities, 558 finite real/imaginary FDTD value cells, 1395 provenance and
   status cells, completed solver statuses, valid solver-log hashes, real-export
   flags, and the canonical input contract hash before completed stage files or
   real BEM/FDTD comparison can be promoted.
   Run `818` validates the saved run `817` preflight gate. Six of six checks
   pass, confirming the single expected input item, absent external CSV, zero
   accepted rows, zero finite FDTD value cells, zero provenance/status cells,
   blocked completed-stage/comparison/downstream states, figure validation, and
   script snapshots.
   Run `819` sensitivity-hardens that validator. The exact run `817` gate
   passes, while seventeen damaged states fail as expected: policy-label damage,
   gate-readiness damage, source-readiness damage, item-count damage, false file
   presence, false schema validity, false row/identity/value/provenance/status
   counts, false accepted input, completed-stage promotion, comparison
   promotion, 3D promotion, figure damage, and script-snapshot damage. Use runs
   `817-819` as the guarded real complex FDTD input preflight block.
   Run `820` records the claim boundary after that preflight gate. Two claims
   are guarded: the external input preflight gate and the fail-closed absent
   external input state. Three claims remain blocked: real external complex FDTD
   input, completed stage files with real FDTD values, and real BEM/FDTD
   comparison or downstream transfer.
   Run `821` validates the saved run `820` claim boundary. Six of six checks
   pass, confirming the five-claim shape, two guarded claims, three blocked
   claims, absent external input, zero accepted rows, zero finite FDTD value
   cells, zero provenance/status cells, blocked completed-stage/comparison/
   downstream states, figure validation, and script snapshots.
   Run `822` sensitivity-hardens that validator. The exact run `820` boundary
   passes, while fifteen damaged states fail as expected: policy-label damage,
   claim-count damage, guarded/blocked-count damage, missing guarded claims,
   false external-input presence, false accepted input, false value/provenance
   counts, blocked-support damage, comparison promotion, 3D promotion, figure
   damage, and script-snapshot damage. Use runs `820-822` as the guarded BEM
   external input preflight claim-boundary block.
   Run `823` splits the guarded 279-row complex FDTD adapter input template
   into a staged handoff packet: five stage-only CSVs and five cumulative CSVs.
   The stage shape is `1;8;30;120;120`, the cumulative shape is
   `1;9;39;159;279`, and the first stage is a one-row center
   receiver-frequency smoke packet. All ten files stay output-local; the final
   cumulative file still contains 558 blank real/imaginary FDTD value cells and
   1395 blank provenance/status cells, and no real comparison or downstream
   state is promoted.
   Run `824` validates the saved run `823` staged packet. Eight of eight checks
   pass, confirming the stage and cumulative shapes, ten output-local packet
   files, final 279-row cumulative packet, blank value/provenance fields,
   blocked external input, blocked comparison/downstream states, figure
   validation, and script snapshots.
   Run `825` sensitivity-hardens that validator. The exact run `823` packet
   passes, while thirteen damaged states fail as expected: policy-label damage,
   stage-shape damage, cumulative-shape damage, packet-manifest damage, missing
   packet files, external-path promotion, final row-count damage, final
   blank-count damage, false external-input presence, false acceptance,
   comparison promotion, figure damage, and script-snapshot damage. Use runs
   `823-825` as the guarded staged complex FDTD input handoff packet block.
   Run `826` fills only the stage-1 one-row complex FDTD input packet with
   output-local synthetic finite real/imaginary values and provenance. The row
   passes the adapter's row-level validation, proving the one-pair staged
   mechanics, but it covers only one of 279 required identities and is not
   accepted as real external input. Full input, completed stage files, real
   comparison, field transfer, and 3D/HPC remain blocked.
   Run `827` validates the saved run `826` stage-1 positive-control smoke.
   Seven of seven checks pass, confirming the one accepted synthetic row, the
   1-of-279 coverage limit, blocked full input, blocked external acceptance,
   blocked comparison/downstream states, figure validation, and script
   snapshots.
   Run `828` sensitivity-hardens that validator. The exact run `826` state
   passes, while ten damaged states fail as expected: policy-label damage, row
   rejection, full-row-count damage, synthetic-flag damage, full-input
   promotion, external-file promotion, real-acceptance promotion, comparison
   promotion, figure damage, and script-snapshot damage. Use runs `826-828` as
   the guarded stage-1 positive-control smoke block.
   Run `829` defines the exact stage-1 live complex-field return contract that
   would replace the run `826` synthetic smoke with one real FDTD row. The
   expected partial return is receiver index `15` at `1.0 GHz` with the
   12-column complex adapter schema. The partial live file and full external
   279-row input are both absent, so full preflight, completed stage files,
   real BEM/FDTD comparison, field transfer, and 3D/HPC remain blocked.
   Run `830` validates the saved run `829` contract. Nine of nine checks pass,
   confirming the one-row contract shape, receiver-frequency identity,
   12-column schema, absent partial and full external files, blocked full
   preflight, blocked acceptance, stable action sequence, blocked comparison/
   downstream states, figure validation, and script snapshots.
   Run `831` sensitivity-hardens that validator. The exact run `829` contract
   passes, while twelve damaged states fail as expected: policy-label damage,
   contract row-count damage, receiver identity damage, required-column damage,
   false partial-file presence, false full-file presence, full-row-count damage,
   acceptance promotion, action completion promotion, comparison promotion,
   figure damage, and script-snapshot damage. Use runs `829-831` as the guarded
   stage-1 live complex-field return contract block.
   Run `832` defines the stage-1 live return intake gate for the one-row FDTD
   partial file specified by run `829`. The expected partial file is absent, so
   all six acceptance gates fail closed: file presence, required columns,
   one-row shape, receiver-frequency identity, finite complex values, and
   solver provenance. Zero live rows are accepted, the partial cannot be merged
   into the full 279-row external input, and real BEM/FDTD comparison, field
   transfer, and 3D/HPC remain blocked.
   Run `833` validates the saved run `832` intake gate. Seven of seven checks
   pass, confirming the expected absent-file state, six fail-closed gates, zero
   live rows, zero accepted stage-1 rows, blocked downstream states, figure
   validation, and script snapshots.
   Run `834` sensitivity-hardens that validator. The exact run `832` absent-
   file state passes, while nineteen damaged states fail as expected: policy-
   label damage, gate-readiness damage, source-readiness damage, expected-row
   and required-column damage, partial/full-file presence promotion, gate-count
   damage, passed-gate promotion, live-row-count promotion, schema promotion,
   value/provenance promotion, acceptance promotion, merge promotion,
   comparison promotion, field-transfer promotion, 3D promotion, figure damage,
   and script-snapshot damage. Use runs `832-834` as the guarded stage-1 live
   FDTD return intake block.
   Run `835` audits alignment between the current stage-1 live-return contract
   and the older producer execution-priority map. Five of five checks pass:
   source blocks are ready, the priority stage shape is `1;8;30;120;120`, the
   stage-1 pair is receiver `15` at `1.0 GHz`, the contract remains a one-row
   absent-file partial state, and the priority map does not authorize real
   comparison. Use the existing priority map to schedule the first producer
   return, but keep comparison blocked until a real stage-1 partial file passes
   intake.
   Run `836` converts that aligned stage-1 target into a non-executed producer
   command packet. The packet contains one required row, receiver `15` at
   `1.0 GHz`, the 12-column complex adapter schema, and the expected partial
   return path under the BEM external-return folder. No FDTD command is
   executed, no external partial file is created, no full 279-row input is
   promoted, and real BEM/FDTD comparison, field transfer, and 3D/HPC remain
   blocked until the real stage-1 partial file exists and passes intake.
   Run `837` validates the saved run `836` packet. Eight of eight checks pass,
   confirming the one-row producer packet, receiver `15` at `1.0 GHz`, the
   12-column schema, expected partial-return path, non-executed command state,
   absent partial/full external files, blocked comparison/downstream states,
   figure validation, and script snapshots.
   Run `838` sensitivity-hardens that validator. The exact run `836` packet
   passes, while twenty-one damaged states fail as expected: policy-label
   damage, packet/source readiness damage, command row-count damage, receiver
   and frequency identity damage, required-column damage, target-path damage,
   false partial/full file presence, false FDTD or command execution, acceptance
   damage, stage-1/full acceptance promotion, comparison/field/3D promotion,
   figure damage, and script-snapshot damage. Use runs `836-838` as the guarded
   stage-1 real FDTD producer command-packet block.
   Run `839` audits synchronization between the BEM stage-1 producer packet and
   the 2D post-scaffold live-approval state. Seven of seven checks pass: the
   stage-1 identity is still receiver `15` at `1.0 GHz`, the partial-return
   target path matches, the 2D approval directory exists, the approval JSON is
   absent with nine required fields still missing, the BEM partial return is
   absent, the full external input is absent, FDTD has not executed, and real
   BEM/FDTD comparison remains blocked.
   Run `840` validates the saved run `839` synchronization audit. Six of six
   checks pass, confirming source readiness, sync-row shape, stage-1 identity,
   live-file absence, blocked execution/downstream states, figure validation,
   and script snapshots.
   Run `841` sensitivity-hardens that validator. The exact synchronized,
   non-executed state passes, while sixteen damaged states fail as expected:
   source-readiness damage, sync-row damage, failed sync checks, receiver and
   frequency damage, approval-directory damage, false approval-file presence,
   false approval-field completion, false partial-return/full-input promotion,
   false FDTD execution, false comparison, field/3D promotion, figure damage,
   and script-snapshot damage. Use runs `839-841` as the guarded BEM/2D
   post-scaffold synchronization block.
   Run `842` audits synchronization between the BEM stage-1 producer packet and
   the 2D approval template. Seven of seven checks pass: receiver `15` at
   `1.0 GHz`, partial-return output path, partial-return CSV columns, output-
   local template placement, blank approval provenance, absent live approval,
   and blocked execution/comparison all match the expected draft state.
   Run `843` validates the saved run `842` audit. Six of six checks pass,
   confirming source readiness, audit-row shape, target identity,
   partial-return schema identity, draft template state, blocked live approval,
   blocked execution/downstream states, figure validation, and script
   snapshots.
   Run `844` sensitivity-hardens that validator. The exact synchronized draft
   state passes, while sixteen damaged states fail as expected: source-
   readiness damage, row-count damage, failed sync checks, receiver/frequency
   damage, template-count damage, target-prefill damage, blank-field damage,
   live-approval promotion, acceptance promotion, FDTD execution promotion,
   comparison promotion, field/3D promotion, figure damage, and script-snapshot
   damage. Use runs `842-844` as the guarded BEM/2D approval-template
   synchronization block.
   Run `845` audits synchronization between the BEM stage-1 producer packet and
   the 2D parser positive control. Eight of eight checks pass: receiver `15` at
   `1.0 GHz`, partial-return output path, partial-return CSV columns,
   output-local positive-control placement, parser-shape pass state,
   positive-control-not-live status, absent live approval, and blocked
   execution/comparison all match.
   Run `846` validates the saved run `845` audit. Six of six checks pass,
   confirming source readiness, audit-row shape, target identity,
   partial-return schema identity, positive-control parser state, blocked live
   approval, blocked execution/downstream states, figure validation, and script
   snapshots.
   Run `847` sensitivity-hardens that validator. The exact synchronized parser
   positive-control state passes, while eighteen damaged states fail as
   expected: source-readiness damage, row-count damage, failed sync checks,
   receiver/frequency damage, positive-control count damage, parser-count/pass
   damage, payload-shape damage, live-root/live-approval promotion, acceptance
   promotion, FDTD execution promotion, comparison promotion, field/3D
   promotion, figure damage, and script-snapshot damage. Use runs `845-847` as
   the guarded BEM/2D parser positive-control synchronization block.
   Run `848` audits synchronization between the BEM stage-1 producer packet and
   the 2D live approval acceptance gate. Six of six checks pass: the stage-1
   identity remains receiver `15` at `1.0 GHz`, the 2D gate is fail-closed, the
   live approval file is absent, zero live approvals are accepted, the BEM
   producer is not authorized or executed, and comparison/downstream states
   remain blocked.
   Run `849` validates the saved run `848` audit. Six of six checks pass,
   confirming source readiness, audit-row shape, stage-1 identity, fail-closed
   approval gate state, blocked FDTD execution/downstream states, figure
   validation, and script snapshots.
   Run `850` sensitivity-hardens that validator. The exact fail-closed live
   approval gate state passes, while fourteen damaged states fail as expected:
   source-readiness damage, row-count damage, failed sync checks, receiver
   damage, gate-pass promotion, live-file promotion, accepted-approval
   promotion, FDTD authorization/execution promotion, comparison promotion,
   field/3D promotion, figure damage, and script-snapshot damage. Use runs
   `848-850` as the guarded BEM/2D live approval gate synchronization block.
   Run `851` returns to the analytic 2D BEM numerical branch and combines the
   validated 25-frequency and 49-frequency receiver-grid checks into one
   116-panel stress scorecard. All six stress rows pass the `0.001`
   high-band relative-L2 target and the `2.5e-05` guard margin. The controlling
   row is the 25-frequency, 13-scan layout with high-band relative L2
   `0.0009518291083452528` and margin `4.8170891654747265e-05`. The
   25f/49f worst-grid sensitivity ratio is `1.2452459822544342`, so fixed-grid
   comparison and per-frequency diagnostics remain required.
   Run `852` validates that scorecard with seven of seven checks passing:
   source readiness, row shape, pass/guard margin, controlling-case identity,
   grid-sensitivity policy, analytic-only boundary, figure output, and script
   snapshots.
   Run `853` sensitivity-hardens the validator. The exact scorecard state
   passes, while seventeen damaged or prematurely promoted states fail as
   expected: source readiness, row shape, panel identity, target error, guard
   margin, pass count, controlling-case identity, grid ratio, diagnostic
   removal, lower-panel promotion, project-FDTD promotion, 3D/GPU/field
   promotion, figure damage, and script-snapshot damage. Use runs `851-853`
   as the guarded combined frequency/receiver stress block for the analytic
   116-panel 2D BEM endpoint. Do not lower the panel policy or promote
   project-FDTD, field-transfer, or real-3D claims from this scorecard.
   Run `854` returns to the BEM stage-1 producer branch and rolls up the
   guarded stage-1/2D approval blocks from runs `835-850`. All 16 source runs
   are ready across six guard blocks, and all six blocks remain in a clean
   fail-closed state: no live approval JSON, zero accepted approvals, no
   stage-1 partial FDTD return, no FDTD execution, no real BEM/FDTD comparison,
   no field transfer, and no 3D/HPC promotion. Keep producer execution blocked
   until a real live approval JSON passes the six-gate 2D acceptance check.
   Run `855` validates the saved run `854` rollup with six of six checks
   passing: summary readiness, rollup row shape, receiver `15` at `1.0 GHz`,
   fail-closed execution/downstream state, figure metadata, and frozen script
   snapshots. The validated state remains ready but non-executed.
   Run `856` sensitivity-hardens that validator. The exact saved rollup passes,
   while seventeen damaged or prematurely promoted states fail as expected:
   false source readiness, source-count damage, row-count damage, row readiness
   damage, receiver/frequency damage, live-approval promotion, accepted-
   approval promotion, partial/full return promotion, producer authorization,
   FDTD execution, BEM/FDTD comparison, field transfer, 3D/HPC promotion,
   figure damage, and script-snapshot damage. Use runs `854-856` as the
   guarded BEM stage-1 readiness rollup block.
   Run `857` performs the required per-frequency anatomy check on the
   controlling 13-scan receiver layout from run `851`. The aggregate high-band
   relative L2 still passes on both grids: `0.0009518291083452528` for the
   25-frequency grid and `0.0007643703508458867` for the 49-frequency grid.
   The individual worst high-band bin remains larger than the aggregate
   target: `0.0020304660813911003` at `2.3125 GHz` on both grids. This
   confirms that 116 panels is a guarded aggregate analytic endpoint, not a
   per-frequency guarantee.
   Run `858` validates the saved per-frequency anatomy with seven of seven
   checks passing: source readiness, row shape, aggregate pass and guard
   margin, per-frequency diagnostic need, controlling receiver identity,
   analytic-only boundary, figure output, and script snapshots.
   Run `859` sensitivity-hardens that validator. The exact anatomy state
   passes, while eighteen damaged or prematurely promoted states fail as
   expected: source readiness, row shape, scan identity, panel identity,
   aggregate error, guard margin, frequency-bin diagnostic state, grid
   sensitivity, controlling-source identity, lower-panel promotion,
   project-FDTD promotion, 3D/GPU/field promotion, figure damage, and
   script-snapshot damage. Use runs `857-859` as the guarded per-frequency
   diagnostic block for the controlling 116-panel analytic receiver layout.
   Run `860` scores the per-frequency exceedance distribution from the saved
   run `857` frequency rows. Five of twenty-seven high-band frequency bins
   exceed the aggregate target. The worst bin remains `2.3125 GHz` with
   relative L2 `0.0020304660813911003`, and the maximum above-target fraction
   across the two frequency grids is `0.2222222222222222`. This keeps the
   116-panel result as an aggregate analytic endpoint while preserving the
   per-frequency diagnostic guard.
   Run `861` validates that scorecard with six of six checks passing:
   readiness, row shape, bin counts, worst-bin diagnostic need, analytic-only
   claim boundary, figure output, and script snapshots.
   Run `862` sensitivity-hardens that validator. The exact scorecard passes,
   while twelve damaged or prematurely promoted states fail as expected:
   readiness, row count, total-bin count, exceedance-bin count, worst-bin
   demotion, diagnostic removal, lower-panel promotion, project-FDTD
   promotion, real-3D promotion, field promotion, figure damage, and
   script-snapshot damage. Use runs `860-862` as the guarded per-frequency
   exceedance concentration block.
   Run `863` converts that result into the current policy matrix. Exactly one
   policy is accepted: 116 panels as an aggregate analytic endpoint with the
   per-frequency diagnostic guard preserved. Four policies remain blocked:
   hard per-frequency endpoint acceptance, lower-panel policy, project-FDTD
   comparison, and field/3D transfer.
   Run `864` validates the saved policy matrix with five of five checks
   passing: source readiness, five policy rows, exactly one accepted aggregate
   endpoint policy, four blocked promotion policies, preserved high-band bin
   diagnostic counts, blocked project-FDTD/field/3D claims, figure output, and
   script snapshots.
   Run `865` sensitivity-hardens that validator. The exact matrix passes,
   while fifteen damaged or prematurely promoted states fail as expected:
   source readiness, row/count damage, accepted-policy promotion, blocked-count
   damage, bin-count damage, worst-frequency damage, hard per-frequency
   promotion, lower-panel promotion, project-FDTD promotion, real-3D promotion,
   field-transfer/FWI promotion, figure damage, and script-snapshot damage.
   Use runs `863-865` as the guarded 116-panel frequency-bin policy matrix
   block.
   Run `866` decomposes the remaining above-target high-band bins into
   amplitude, phase, mixed, and scalar-gain components. Five of twenty-seven
   high-band bins remain above the aggregate target. None are amplitude
   dominant, one is phase dominant, and four are mixed. The worst bin remains
   `2.3125 GHz` with complex relative L2 `0.0020304660813910734`; its
   scalar-gain-corrected relative L2 is still `0.0019054837810734088`, only a
   `0.061553503140539645` reduction. This keeps the accepted policy at
   aggregate endpoint plus per-frequency diagnostics, with no scalar-gain
   correction, hard per-bin acceptance, project-FDTD comparison, field
   transfer, or 3D/HPC promotion.
   Run `867` validates that decomposition from saved artifacts with six of six
   checks passing: source readiness, row shape, dominance counts, worst-bin
   scalar-gain non-repair, blocked claim boundary, figure output, and script
   snapshots.
   Run `868` sensitivity-hardens that validator. The exact saved
   decomposition passes, while eighteen damaged or prematurely promoted states
   fail as expected: source readiness, row shape, high-band and above-target
   counts, amplitude/phase/mixed-count claims, dominant-mode claim,
   worst-frequency claim, worst-error demotion, scalar-gain repair,
   scalar-gain promotion, project-FDTD promotion, 3D promotion, field
   promotion, figure damage, and script-snapshot damage. Use runs `866-868` as
   the guarded amplitude/phase diagnostic block for the remaining 116-panel
   high-band frequency-bin exceedance.
   Run `869` inspects the spatial residual anatomy of the worst `2.3125 GHz`
   bin across the 13 receiver positions. The edge quarters carry
   `0.5923362105102755` of residual energy and the center half carries
   `0.40766378948972465`; the maximum local relative error is only
   `1.2785395313575958` times the median. This supports an edge-biased
   spatial-shape diagnostic, not a single-receiver spike and not scalar-gain,
   hard per-frequency, project-FDTD, field, or 3D/HPC promotion.
   Run `870` validates that spatial anatomy from saved artifacts with six of
   six checks passing: source readiness, row shape, worst-frequency identity,
   edge-biased-not-single-spike behavior, blocked claim boundary, figure
   output, and script snapshots.
   Run `871` sensitivity-hardens that validator. The exact spatial-anatomy
   state passes, while seventeen damaged or prematurely promoted states fail
   as expected: source readiness, receiver rows, edge classification,
   worst-frequency identity, target-passing demotion, edge-fraction bounds,
   single-spike promotion, scalar-gain promotion, hard per-frequency
   promotion, project-FDTD promotion, 3D promotion, field promotion, figure
   damage, and script-snapshot damage. Use runs `869-871` as the guarded
   spatial residual diagnostic block for the remaining 116-panel worst
   high-band frequency bin.
   Run `872` scores aperture-trim subsets for that same worst `2.3125 GHz`
   bin. The strict-center subset is the best subset, but its complex relative
   L2 remains `0.001938978012629881`, above the `0.001` target. The full
   aperture is `0.002030466081391074` and the edge quarters are
   `0.0021015204146441102`. This shows that edge trimming reduces the error
   only slightly and does not repair the worst-bin mismatch.
   Run `873` validates the saved aperture-trim scorecard with six of six
   checks passing: source readiness, subset row shape, no aperture-trim target
   repair, interior reduction but not solution, blocked claim boundary, figure
   output, and script snapshots.
   Run `874` sensitivity-hardens that validator. The exact aperture-trim
   scorecard passes, while sixteen damaged or prematurely promoted states fail
   as expected: source readiness, row shape, false subset pass, false target
   repair, false aperture-trim repair, aperture-trim correction promotion,
   hard per-frequency promotion, project-FDTD promotion, field/3D promotion,
   GPU-priority promotion, figure damage, and script-snapshot damage. Use
   runs `872-874` as the guarded aperture-trim no-repair block for the
   remaining 116-panel worst high-band frequency bin.
   Run `875` fits constant, affine, and quadratic aperture-dependent complex
   bias models to the same worst-bin receiver residuals. The best in-sample
   model is quadratic, reducing relative L2 only from `0.002030466081391074`
   to `0.0018381250513289863`, still above the `0.001` target. The
   leave-one-out check is worse than the uncorrected response for every
   model; the best leave-one-out relative L2 is `0.0020966945192620154`.
   This rejects smooth aperture-bias correction as a reliable repair.
   Run `876` validates that scorecard with six of six checks passing: source
   readiness, three model rows, in-sample no-repair, leave-one-out no-support,
   blocked claim boundary, figure output, and script snapshots.
   Run `877` sensitivity-hardens that validator. The exact complex-bias
   scorecard passes, while fifteen damaged or prematurely promoted states fail
   as expected: source readiness, model-row damage, false target repair,
   false in-sample pass, false leave-one-out stability, smooth-bias repair
   promotion, hard per-frequency promotion, project-FDTD promotion, field/3D
   promotion, GPU-priority promotion, figure damage, and script-snapshot
   damage. Use runs `875-877` as the guarded smooth aperture-bias no-repair
   block for the remaining 116-panel worst high-band frequency bin.
   Run `878` checks mirrored receiver-pair symmetry for the same worst
   `2.3125 GHz` bin using the saved run `869` receiver residual rows. Pair
   magnitudes are balanced with maximum pair magnitude imbalance
   `0.05160289316381502`, but pair residual energy is antisymmetric-dominant:
   symmetric fraction `0.2888732114593446`, antisymmetric fraction
   `0.7111267885406554`, with five of six pairs antisymmetric-dominant. This
   rules out a one-sided amplitude artifact while keeping symmetry correction,
   hard per-frequency acceptance, project-FDTD comparison, field transfer, and
   3D/HPC claims blocked.
   Run `879` validates that saved symmetry audit with six of six checks
   passing: source readiness, mirrored-pair row shape, antisymmetric-not
   one-sided behavior, pair/center counts, blocked claim boundary, figure
   output, and script snapshots.
   Run `880` sensitivity-hardens that validator. The exact symmetry audit
   passes, while seventeen damaged or prematurely promoted states fail as
   expected: source readiness, row removal, pair-order damage, antisymmetric
   demotion, symmetric promotion, one-sided magnitude damage, one-sided
   artifact promotion, pair-count damage, center-energy damage, symmetry
   correction promotion, hard per-frequency promotion, project-FDTD promotion,
   field/3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `878-880` as the guarded receiver-pair
   symmetry diagnostic block for the remaining 116-panel worst high-band
   frequency bin.
   Run `881` scores ideal pair-component removal oracles using the saved
   run `878` receiver-pair decomposition. Removing only the antisymmetric
   pair component improves the worst-bin relative L2 from
   `0.0020304660813910734` to `0.001195683569955468`, but this remains above
   the `0.001` target. Removing only the symmetric pair component is worse
   (`0.0017403420910436734`). Only the nonphysical lower bound that removes
   all paired residual and keeps the center receiver residual passes
   (`0.0005793593752068725`). This rejects antisymmetric-only pair-component
   removal as a repair.
   Run `882` validates that oracle scorecard with six of six checks passing:
   source readiness, scenario row shape, antisymmetric-only no-repair,
   nonphysical lower-bound pass, blocked claim boundary, figure output, and
   script snapshots.
   Run `883` sensitivity-hardens that validator. The exact oracle scorecard
   passes, while fourteen damaged or prematurely promoted states fail as
   expected: source readiness, row removal, false antisymmetric pass rows,
   antisymmetric demotion below target, false energy-budget claims, all-pair
   lower-bound failure, correction promotion, hard per-frequency promotion,
   project-FDTD promotion, field/3D promotion, GPU-priority promotion, figure
   damage, and script-snapshot damage. Use runs `881-883` as the guarded
   pair-component oracle no-repair block for the remaining 116-panel worst
   high-band frequency bin.
   Run `884` synthesizes the saved worst-bin diagnostic blocks into one
   claim-boundary table. The full worst-bin relative L2 remains
   `0.0020304660813910734`. The best physical candidate is the antisymmetric
   pair oracle from run `881`, but it remains above target at
   `0.001195683569955468`. The only target-passing row is the nonphysical
   all-pair lower bound at `0.0005793593752068725`; therefore no scalar-gain,
   aperture-trim, smooth-bias, symmetry, or pair-component repair is promoted.
   Run `885` validates that synthesis with six of six checks passing: source
   readiness, diagnostic-row stability, no physical target-passing repair,
   nonphysical lower-bound behavior, blocked claim flags, figure output, and
   script snapshots.
   Run `886` sensitivity-hardens that validator. The exact diagnostic
   synthesis passes, while fourteen damaged or prematurely promoted states
   fail as expected: synthesis-readiness damage, row removal, false physical
   repair, false best-candidate demotion, lower-bound failure,
   source/receiver model demotion, correction promotion, hard per-frequency
   promotion, project-FDTD promotion, field/3D promotion, GPU-priority
   promotion, figure damage, and script-snapshot damage. Use runs `884-886`
   as the guarded diagnostic synthesis boundary: the next useful BEM branch is
   source/receiver spatial phase modeling or boundary/source representation,
   not another scalar correction or downstream promotion.
   Run `887` tests the first source/receiver phase branch with unit-amplitude
   aperture phase corrections across the saved 13 receiver rows. The best
   in-sample phase-only model is `constant_odd_even_phase`, reducing the
   worst-bin relative L2 from `0.002030466081391074` to
   `0.0018234403083841053`, still above target. The best leave-one-out model
   is only `constant_phase`, with relative L2 `0.0019827840138898723`, also
   above target. No phase-only model passes in sample or leave-one-out. This
   keeps phase-only correction, hard per-frequency acceptance, project-FDTD
   comparison, field transfer, and 3D/HPC promotion blocked, and shifts the
   next BEM branch toward richer source/receiver representation or
   boundary/source modeling.
   Run `888` validates that phase-only scorecard with six of six checks
   passing: scorecard readiness, model-row stability, no target-passing
   phase-only repair, preserved in-sample versus leave-one-out split, blocked
   claim flags, figure output, and script snapshots. Use run `887` as a
   guarded no-repair phase-only result.
   Run `889` sensitivity-hardens that validator. The exact phase-only
   scorecard passes, while eighteen damaged or prematurely promoted states
   fail as expected: scorecard-readiness damage, row removal, false in-sample
   and leave-one-out pass rows, false target demotion, phase-repair promotion,
   holdout-split damage, unit-amplitude damage, source/receiver refinement
   demotion, correction promotion, hard per-frequency promotion, project-FDTD
   promotion, field/3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `887-889` as the guarded phase-only
   aperture no-repair block for the remaining 116-panel worst high-band
   frequency bin.
   Run `890` tests a more physical source/receiver geometry proxy by comparing
   the saved worst-bin BEM response against analytic references with small
   source and receiver position shifts. The baseline relative L2 is
   `0.0020304660813910734`. The best candidate is a common vertical
   source/receiver shift of `+0.15 mm`, reducing relative L2 to
   `0.0002966325470015585`. Thirteen of thirty-six candidates pass the
   single-bin target, and all passing candidates are vertical shifts; no
   horizontal shift passes. This is the first branch in the current worst-bin
   sequence that can close the single frequency bin, but it remains a
   single-frequency geometry proxy. Keep geometry-shift correction,
   hard per-frequency acceptance, project-FDTD comparison, field transfer, and
   3D/HPC promotion blocked until the vertical proxy survives multi-frequency
   and holdout checks.
   Run `891` validates that geometry-shift proxy scorecard with six of six
   checks passing: scorecard readiness, candidate-grid stability, vertical
   single-bin closure, no-correction claim boundary, blocked claim flags,
   figure output, and script snapshots. Use run `890` as a guarded
   single-frequency vertical-geometry proxy and move next to multi-frequency
   holdout testing.
   Run `892` tests the best `+0.15 mm` common-vertical proxy across all 25
   frequencies. It repairs the original `2.3125 GHz` worst bin
   (`0.0020304660813911003` to `0.00029663254700154477`) and improves the
   aggregate high-band relative L2 (`0.0009518291083452528` to
   `0.0007586109080035837`). It does not survive the full holdout: full-band
   relative L2 worsens (`0.0003383618947272846` to
   `0.0004561554424179171`), total per-frequency passes drop from `23` to
   `19`, high-band passes drop from `7` to `5`, and the shifted worst
   above-target bin moves to `3.0 GHz` at `0.0016529582704013506`. Use this
   as evidence that a fixed vertical shift is a useful diagnostic lead but not
   a correction. The next BEM branch should be a constrained frequency-aware
   source/receiver model or boundary/source representation change.
   Run `893` validates that multi-frequency holdout with six of six checks
   passing: source readiness, frequency-row stability, single-bin repair
   without multi-frequency pass, aggregate tradeoff preservation, blocked
   claim flags, figure output, and script snapshots. Use runs `892-893` as
   the guarded no-promotion result for the fixed vertical geometry proxy.
   Run `894` adds a pair-removal budget scorecard back to the pair-oracle
   branch. The target residual budget requires removing `82.46%` of pair
   residual energy, while ideal antisymmetric removal removes only `71.11%`,
   leaving an `11.35` percentage-point pair-removal gap and requiring
   `39.27%` of the remaining post-antisymmetric pair residual to be removed.
   This narrows the residual budget but remains oracle-only and does not
   promote a correction, hard per-frequency endpoint, project-FDTD
   comparison, field transfer, or 3D/HPC work. Run `895` validates the
   scorecard with five of five checks passing, and run `896`
   sensitivity-hardens the validator: the exact budget passes while sixteen
   damaged or prematurely promoted states fail as expected. Use runs
   `894-896` as a guarded diagnostic-only pair-removal budget block.
   Run `897` measures a frequency-local common-vertical shift oracle with
   shifts from `0.00 mm` to `0.40 mm` in `0.05 mm` increments. The oracle
   increases per-frequency passes from `23` to `25` and high-band passes from
   `7` to `9`; its worst frequency is `2.65625 GHz` with relative L2
   `0.0008518855375610986`. The selected shifts are not constant:
   `{"0.00": 1, "0.05": 16, "0.10": 7, "0.15": 1}`. This is strong evidence
   that a vertical source/receiver representation error is involved, but it is
   an oracle envelope rather than a physical correction. The next useful BEM
   branch is a constrained smooth frequency-aware source/receiver model that
   tries to reproduce this envelope without free per-frequency choice.
   Run `898` validates that oracle envelope with six of six checks passing:
   source readiness, frequency-row and candidate-row shapes, all-frequency
   oracle closure, nonconstant selected shifts, blocked claim flags, figure
   output, and script snapshots. Use runs `897-898` as the guarded target for
   a smooth frequency-aware source/receiver model; keep downstream comparison,
   field, and 3D claims blocked.
   Run `899` sensitivity-hardens that validator. The exact oracle envelope
   passes, while fifteen damaged or prematurely promoted states fail as
   expected: envelope-readiness damage, row-count damage, false oracle
   failure, pass-count damage, constant-shift damage, oracle-correction
   promotion, smooth-model demotion, project-FDTD promotion, field/3D
   promotion, GPU-priority promotion, figure damage, and script-snapshot
   damage. Use runs `897-899` as the guarded frequency-local vertical-shift
   oracle target for the next constrained smooth frequency-aware
   source/receiver model.
   Run `900` scores constrained smooth frequency-aware source/receiver models
   against the saved run `897` shifted-grid candidate table. Three of five
   smooth snapped-grid models pass all 25 frequencies. The best model is a
   gaussian-bump shift model using only `0.05 mm` and `0.10 mm` shifts
   (`{"0.05": 20, "0.10": 5}`), with worst relative L2
   `0.0008518855375610986` at `2.65625 GHz`. This is the first constrained
   smooth model in the current high-band branch that closes the sampled
   frequency grid, but it remains a snapped-grid scorecard. Use run `900` as
   the candidate source/receiver model target, and move next to
   continuous-shift validation before any project-FDTD comparison, field
   transfer, or 3D claim.
   Run `901` validates that smooth model scorecard with six of six checks
   passing: source readiness, model-row and applied-row shape, all-frequency
   smooth-grid closure, constrained model-pattern preservation, blocked claim
   flags, figure output, and script snapshots. Use runs `900-901` as the
   guarded candidate source/receiver model input for continuous-shift
   validation.
   Run `902` returns to the pair-removal budget branch and ranks the remaining
   symmetric mirrored-pair residual after ideal antisymmetric removal. The
   largest symmetric pair component, pair order `6`, contains `51.95%` of the
   post-antisymmetric remaining pair residual, exceeding the `39.27%` needed
   to close the run `894` budget gap. That oracle pruning would estimate the
   worst-bin relative L2 at `0.000928076808180761`, below the `0.001` target,
   but it is still a pair-specific residual pruning oracle rather than a
   physical correction. Run `903` validates the scorecard with five of five
   checks passing, and run `904` sensitivity-hardens the validator: the exact
   pruning scorecard passes while fourteen damaged or prematurely promoted
   states fail as expected. Use runs `902-904` as guarded evidence that the
   post-antisymmetric gap is localized in one remaining symmetric pair
   component, while keeping hard per-frequency acceptance, project-FDTD
   comparison, field transfer, GPU priority, and 3D/HPC promotion blocked.
   Run `905` sensitivity-hardens the smooth frequency-aware source/receiver
   model validator from run `901`. The exact run `900` scorecard passes, while
   sixteen damaged or prematurely promoted states fail as expected:
   scorecard-readiness damage, model-row and applied-row removal, false
   all-model pass claims, best-model swaps, above-target best-model damage,
   selected-shift damage, missing continuous-validation requirement,
   smooth-correction promotion, downstream promotion, figure damage, and
   script-snapshot damage. Use runs `900-901` and `905` as the guarded setup
   for continuous-shift validation.
   Run `906` checks the smooth run `900` source/receiver shift models at their
   continuous predicted shifts by linearly interpolating the saved run `897`
   shift grid. Exactly one model, `best_gaussian_bump`, passes all 25
   frequencies under interpolation, with max relative L2
   `0.0008751841676054046` at `2.65625 GHz`. The conservative neighboring-grid
   bracket guard does not pass: its best max relative L2 is
   `0.001367588871846657` at `2.3125 GHz`. This means the continuous-shift
   evidence is stronger than snapped-grid scoring but still surrogate-only, not
   a correction. Run `907` validates that scorecard with six of six checks
   passing, and run `908` sensitivity-hardens the validator: the exact
   interpolated scorecard passes while fifteen damaged or prematurely promoted
   states fail as expected. Use runs `906-908` as guarded continuous-shift
   surrogate evidence only; keep correction promotion, project-FDTD comparison,
   field transfer, GPU priority, and 3D/HPC claims blocked until the bracket
   gap is resolved by a stronger non-oracle check.
   Run `909` resolves the surrogate bracket gap by directly evaluating
   analytic references at the smooth gaussian-bump model's continuous off-grid
   shift values. The 116-panel CPU BEM target response stays below the
   `0.001` relative-L2 target at all 25 frequencies and all nine high-band
   frequencies. The worst continuous-shift frequency remains `2.65625 GHz`
   with relative L2 `0.0008519458802336965`, very close to the snapped-grid
   value `0.0008518855375610986`; the largest full-band continuous/snapped
   relative-L2 difference is `8.112758940537559e-05`. This shows the run
   `900` smooth model was not merely a grid-snapping artifact.
   Run `910` validates that direct continuous-shift result with six of six
   checks passing: source readiness, frequency-row shape, off-grid continuous
   model closure, snapped/continuous consistency, blocked claim flags, figure
   output, and script snapshots. Run `911` sensitivity-hardens the validator:
   the exact continuous validation state passes, while sixteen damaged or
   prematurely promoted states fail as expected. Use runs `909-911` as the
   guarded BEM-side candidate packet for project-FDTD comparison design, not
   as a completed project-FDTD comparison.
   Run `912` writes the guarded project-FDTD comparison design contract for
   the smooth continuous-shift BEM model. The contract has six required items:
   geometry identity, complex-observable identity, source/receiver model,
   FDTD return schema, comparison metric, and claim boundary. Only geometry
   identity and the BEM source/receiver model are ready now; FDTD return rows,
   metric execution, and comparison claims remain absent. All five gates are
   fail-closed: no launch packet, no FDTD execution, no FDTD return rows, no
   completed BEM/FDTD comparison, and no field or 3D transfer. Use run `912`
   as the design contract for the next launch/return packet branch.
   Run `913` validates that design contract with six of six checks passing:
   source readiness, contract-row shape, fail-closed gate state, preserved BEM
   candidate metrics, blocked execution/downstream flags, figure output, and
   script snapshots. Use runs `912-913` as the guarded design-contract block.
   Run `914` sensitivity-hardens that validator. The exact fail-closed design
   contract passes, while seventeen damaged or prematurely promoted states
   fail as expected: source-readiness damage, contract-row removal, gate-row
   removal, ready-state damage, premature FDTD-schema readiness, open
   execution gates, BEM metric damage, design demotion, false launch-packet
   presence, false execution authorization, false return-row presence, false
   comparison completion, downstream promotion, figure damage, and
   script-snapshot damage. Use runs `912-914` as the guarded design-contract
   block before any launch/return packet work.
   Run `915` writes the non-executed launch/return packet scaffold for the
   smooth continuous-shift BEM comparison design. The packet has 25 frequency
   launch slots, nine high-band slots, a 15-column complex return schema, four
   hashed packet files, and six fail-closed acceptance gates. A launch packet
   is written as a handoff artifact, but no FDTD execution is authorized, no
   return rows are present, and comparison, field, GPU, and 3D claims remain
   blocked. Run `916` validates that saved packet with seven of seven checks
   passing: packet identity/readiness, frequency slots, return schema, packet
   hashes, fail-closed gates, blocked execution/return/downstream state,
   figure output, and script snapshots. Run `917` sensitivity-hardens that
   validator: the exact packet passes while twenty-one damaged or prematurely
   promoted states fail as expected. Use runs `915-917` as the guarded
   launch/return packet block; a separate real-return intake gate is still
   required before any BEM/FDTD comparison claim.
   Run `918` validates the separate blank receiver-frequency return-template
   artifact produced for the same smooth continuous-shift comparison branch.
   The template covers all `13 x 25 = 325` receiver-frequency rows, preserves
   six blank FDTD/provenance columns across `1950` blank value cells, and keeps
   launch, execution, return-value, comparison, field-transfer, GPU, and 3D
   claims blocked. Use run `918` as the guard that the fillable row-level
   template is still non-evidence before any real FDTD return intake.
   Run `919` sensitivity-hardens that validator. The exact blank template
   passes, while twenty-three damaged or prematurely promoted states fail as
   expected, including row-identity damage, nonblank FDTD value cells, false
   execution/comparison flags, downstream promotion, missing continuous-shift
   metadata, figure damage, and script-snapshot damage. Use runs `918-919` as
   the guarded row-level return-template block; a separate real-return intake
   gate is still required before any BEM/FDTD comparison claim.
   Run `920` reconciles the broader launch/return packet with the separate
   row-level return template. Both artifacts use numeric run id `915` but have
   distinct run names and paths. The packet carries 25 frequency slots, nine
   high-band slots, 15 return-schema columns, four hashed packet files, and a
   launch handoff state. The template expands that scope into all `13 x 25 =
   325` receiver-frequency fillable rows with `1950` blank FDTD/provenance
   cells. Run `920` passes six reconciliation checks and keeps execution,
   return rows, return values, comparison, field, GPU, and 3D claims blocked.
   Run `921` validates that reconciliation with six of six checks passing:
   reconciliation readiness, packet/template counts, reconciliation rows,
   explicit duplicate-run-id boundary, blocked execution/return/downstream
   state, figure output, and script snapshots. Run `922` sensitivity-hardens
   that validator: the exact reconciliation passes while twenty-one damaged or
   prematurely promoted states fail as expected. Use runs `920-922` as the
   guarded packet/template relationship block; a real-return intake gate is
   still required before any BEM/FDTD comparison claim.
   The separate real-return intake branch is distinguished by its full run
   names. `920_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate`
   defines the current acceptance boundary: the launch packet and row-level
   return template are guarded, all 325 receiver-frequency identities are
   present, but the blank template is rejected because it has zero complex FDTD
   value rows and zero solver-provenance rows. Its validator,
   `921_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate_validator`,
   passes six of six checks and preserves the blocked execution/comparison
   state. Run `923` sensitivity-hardens that validator: the exact fail-closed
   state passes, while twenty-four damaged or prematurely promoted states fail
   as expected. Use the full-name intake branch as the current real-return
   acceptance boundary before any BEM/FDTD comparison claim.
   `924_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke`
   adds a synthetic non-evidence return smoke for that intake path. It fills
   all `325` receiver-frequency rows with deterministic synthetic complex
   values and synthetic solver provenance, so the schema mechanics pass six
   of six smoke gates. The file is explicitly synthetic: real evidence rows
   remain zero, real-return acceptance remains false, and BEM/FDTD comparison,
   field-transfer, GPU, and 3D claims remain blocked.
   Run `930` validates that synthetic smoke from saved artifacts with six of
   six checks passing: source readiness, the complete 325-row
   receiver-frequency grid, synthetic complex values and provenance, synthetic
   non-evidence flags, smoke gates, blocked downstream states, figure output,
   and script snapshots. The synthetic file remains schema exercise only; it
   does not promote real FDTD execution, real BEM/FDTD comparison, field
   transfer, GPU, or 3D claims.
   Run `931` sensitivity-hardens that validator. The exact synthetic smoke
   passes, while eighteen damaged or prematurely promoted states fail as
   expected: source readiness damage, row removal, receiver-index damage,
   complex-value damage, solver-provenance damage, synthetic-label damage,
   real-evidence promotion, real-return acceptance promotion, smoke-gate
   removal or failure, FDTD authorization/execution promotion, BEM/FDTD
   comparison promotion, field-transfer promotion, 3D promotion, GPU-priority
   promotion, figure damage, and script-snapshot damage. Use runs `930-931`
   as the guarded validation block for the synthetic return-intake smoke.
   `924_scarep_2d_cpu_bem_panel116_project_fdtd_tail_numbering_collision_audit`
   audits the resulting numeric-id collisions. Numeric ids `915`, `920`,
   `921`, and `924` are duplicated across outputs and docs, so numeric-only
   citations are blocked; references must include full artifact names or
   paths. Run `925` validates that collision policy with six of six checks
   passing, and run `926` sensitivity-hardens the validator: the exact
   collision policy passes while eighteen damaged or prematurely promoted
   states fail as expected. Use full-name references for these ids and keep
   all FDTD/comparison/field/3D claims blocked.
   Run `927` turns that policy into a machine-readable full-artifact citation
   map with 16 citation rows, covering output and doc artifacts for duplicated
   ids `915`, `920`, `921`, and `924`. Every row carries an artifact path,
   artifact name, artifact role, and canonical citation, and all 16 rows
   require full-name citation with zero numeric-only references allowed. Run
   `928` validates the map with six of six checks passing, and run `929`
   sensitivity-hardens the validator: the exact map passes while twenty-one
   damaged or prematurely promoted states fail as expected. Use runs `927-929`
   as the guarded citation-map block; this does not promote FDTD execution,
   return values, BEM/FDTD comparison, field transfer, GPU, or 3D claims.
3. CUDA/cuBLAS repair for optional scarep GPU MFS is low priority after run
   `224`; revisit only if a GPU-MFS-specific objective appears.
4. Use runs `071`-`088` as the true 3D comparison checklist before any FDTD launch, and use runs `290-531` as the Bempp-side fine-mesh reference, matched FDTD export contract, non-executed command-plan guard, archive audit, guarded target-side proxy-export branch, guarded paired scalar proxy export, guarded proxy-comparator diagnostic path, proxy-comparator anatomy audit, component-projection no-repair result, guarded receiver-operator diagnostic, holdout-readiness blocker, guarded apply-only holdout design packet, guarded non-executed holdout command plan, guarded coefficient-stability no-promotion audit, guarded smooth-coefficient no-repair audit, guarded project-grid adapter lineage audit, adapter interface-evolution map, executable payload replay checkpoint, guarded fresh-case replay boundary, full-payload fresh-case stress checkpoint, guarded full-payload replay block, guarded full-payload replay claim-boundary block, guarded post-replay real-pair execution readiness gate, guarded file-level real-pair export packet contract, guarded real-pair packet staging command-plan block, guarded real-pair packet filesystem gap-audit block, guarded real-pair packet gap claim-boundary block, guarded return-packet acceptance gate, guarded post-acceptance claim-boundary block, guarded non-evidence return-packet intake worksheet block, guarded post-intake claim-boundary block, guarded return-packet staging dependency block, guarded receiver-aperture sensitivity block, guarded aperture metadata-addendum block, guarded 35-field real-return preflight block, guarded post-aperture-preflight claim-boundary block, guarded 35-field closure block, guarded post-closure claim-boundary block, guarded non-evidence 35-field return-template block, guarded post-template-pack claim-boundary block, guarded synthetic consumer-smoke block, guarded post-synthetic-fill-smoke claim-boundary block, guarded synthetic downstream-consumer block, guarded post-synthetic-comparator-smoke claim-boundary block, guarded synthetic scattered-anatomy block, guarded post-scattered-anatomy claim-boundary block, guarded synthetic scattered normalization-policy block, guarded post-normalization-policy claim-boundary block, guarded synthetic normalized-comparator score-smoke block, guarded post-score-smoke claim-boundary block, guarded synthetic normalized-comparator threshold-ladder block, guarded post-threshold-ladder claim-boundary block, guarded non-evidence real-return scorecard-template block, guarded post-scorecard-template claim-boundary block, guarded reference-coefficient precision-budget block, guarded post-precision-budget claim-boundary block, guarded serialization round-trip block, guarded post-serialization claim-boundary block, guarded storage-refreshed scorecard-template block, guarded post-storage-refresh claim-boundary block, guarded 35-field normalized-comparator scorecard intake worksheet block, guarded post-intake-worksheet claim-boundary block, guarded scorecard return staging-plan block, guarded post-return-staging-plan claim-boundary block, guarded return-file manifest block, guarded post-return-file-manifest claim-boundary block, guarded synthetic return-file consumer-smoke block, guarded post-synthetic-return-file-fill claim-boundary block, guarded real return-file acceptance-gate block, guarded post-real-return-file-acceptance claim-boundary block, guarded real-return filesystem gap-audit block, guarded post-real-return-filesystem-gap claim-boundary block, guarded producer-route gap audit, guarded Bempp 35-field producer-coverage audit, guarded real-return producer-contract spec, guarded return-file writer interface, guarded Bempp exporter interface, guarded FDTD exporter interface, guarded real-return interface completion boundary, guarded fine-mesh BEM candidate export, guarded matched-FDTD handoff, and guarded matched-FDTD contract-check command inventory for future paired FDTD exports.
5. Treat runs `225-227` as the guarded half-space Green-function objective
   contract. Run `228` passes the first scalar half-space Green-kernel smoke;
   runs `229-230` validate and stress-test it. Runs `231-233` add, validate,
   and stress-test a scalar finite-rebar coupling smoke. Run `234` defines the
   claim boundary for that scalar coupling layer. Run `235` writes the matched
   scalar BEM/FDTD comparison contract. Runs `236-237` validate and stress-test
   that contract. Run `238` implements the BEM-side exporter into the run `235`
   schema. Run `239` validates that exporter. Runs `250-289` define and guard
   the trace-intake, synthetic extraction, negative-control, real-comparison
   boundary, threshold-calibration protocol, and first-real-pair command plan
   for future real FDTD traces while keeping actual real comparison,
   inversion-scale, field-transfer, and 3D claims blocked.
   Run `932` returns to the saved 2D half-space PEC adapter from run `016` and
   turns its panel-refinement result into an operating rule. The 16-panel BEM
   result is within `0.0004746867074423852` relative L2 of the 32-panel
   reference, runs `3.2873864069744765x` faster, saves about `69.58%` wall
   time, and its panel error is only `0.015313315458994644` of the best saved
   FDTD mismatch. Use 16 panels for preliminary half-space PEC sweeps and keep
   32 panels for final comparison checkpoints.
   Run `933` validates that panel-economy audit with six of six checks passing:
   audit readiness, two-row panel shape, 32-panel reference stability,
   16-panel preliminary metric gate, runtime savings, error scale, blocked
   downstream states, figure output, and script snapshots.
   Run `934` sensitivity-hardens that validator. The exact panel-economy
   policy passes, while sixteen damaged or prematurely promoted states fail as
   expected: audit readiness damage, row removal, reference-panel damage,
   recommended-panel damage, error-gate damage, speedup damage, wall-savings
   damage, error-fraction damage, policy demotion, project-core FDTD promotion,
   field-transfer promotion, 3D promotion, GPU-priority promotion, figure
   damage, and script-snapshot damage. Use runs `932-934` as the guarded
   half-space PEC BEM panel-economy policy block.
   Run `935` applies that 16-panel policy to a CPU-only BEM depth sweep at
   center depths `0.25`, `0.35`, and `0.45` m in the same air/concrete
   half-space. The peak amplitude is nearly flat across this range: the deep
   case is only `-0.018574056369367674` dB below the shallow case. The waveform
   and scan shape are more informative: the maximum relative L2 difference
   against the `0.35` m baseline is `0.039940245470760076`. Use this as a
   preliminary BEM depth-sensitivity result only; project-core FDTD, field
   transfer, and 3D validation remain blocked.
   Run `936` validates that depth sweep with six of six checks passing:
   source identity, three-depth 16-panel shape, weak peak-amplitude depth
   signal, waveform/scan-shape depth signal, blocked downstream scope, figure
   output, and script snapshots. Use runs `935-936` as the guarded preliminary
   16-panel BEM depth-sensitivity block; continue depth/material screening
   with waveform-shape metrics and keep 32-panel checks for selected final
   comparison checkpoints.
   Run `937` sensitivity-hardens that validator. The exact depth-sweep state
   passes, while eighteen damaged or prematurely promoted states fail as
   expected: readiness damage, row removal, depth-value damage, panel-policy
   damage, scan/frequency/time-sample damage, peak-depth metric damage,
   waveform-shape metric damage, baseline relative-L2 damage, project-core
   FDTD promotion, field-transfer promotion, 3D promotion, GPU-priority
   promotion, figure damage, and script-snapshot damage. Use runs `935-937`
   as the guarded preliminary 16-panel BEM depth-sensitivity block.
   Run `938` extends that block to a 3-by-3 BEM-only depth/material grid:
   depths `0.25`, `0.35`, and `0.45` m, and lower-half-space relative
   permittivity values `4`, `6`, and `8`. Peak amplitude remains weak: the
   depth span at relative permittivity `6` is only `0.018574056369368822` dB,
   and the material span at `0.35` m depth is `0.08605468696404216` dB. The
   waveform/scan-shape metric is more informative: relative L2 reaches
   `0.039940245470760076` across depth at relative permittivity `6`,
   `0.05706521432942532` across material at `0.35` m depth, and
   `0.0649192423436475` across the full grid. Use waveform-shape metrics for
   follow-on BEM screening; project-core FDTD, field transfer, GPU escalation,
   and 3D validation remain blocked.
   Run `939` validates that depth/material sweep with six of six checks
   passing: source identity, 3-by-3 grid shape, 16-panel policy, baseline
   metric consistency, depth-vs-material signal boundary, blocked downstream
   scope, figure output, and script snapshots. Use runs `938-939` as the
   guarded preliminary 16-panel BEM depth/material sensitivity block.
   Run `940` sensitivity-hardens that validator. The exact depth/material
   state passes, while twenty damaged or prematurely promoted states fail as
   expected: readiness damage, row removal, depth-value damage,
   relative-permittivity value damage, panel-policy damage,
   scan/frequency/time-count damage, baseline metric damage, depth/material
   sensitivity metric damage, project-core FDTD promotion, field-transfer
   promotion, 3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `938-940` as the guarded preliminary
   16-panel BEM depth/material sensitivity block.
   Run `941` uses the same 16-panel setting to isolate acquisition-geometry
   sensitivity at the baseline depth/material case. Across Tx/Rx offsets
   `0.04`, `0.06`, and `0.08` m and antenna z-positions `-0.02`, `0`, and
   `0.04` m, geometry changes are much larger than the previous
   depth/material perturbations: the peak span across Tx/Rx offset at
   antenna z `0` is `2.6214537950832346` dB, the max relative L2 across
   offset at antenna z `0` is `0.7099232724148534`, and the full-grid max
   relative L2 is `0.9115427115447009`. Future matched BEM/FDTD comparisons
   should lock source/receiver geometry before interpreting residual
   disagreement as depth or material error.
   Run `942` validates that source/receiver geometry sweep with six of six
   checks passing: source identity, 3-by-3 grid shape, 16-panel policy,
   baseline metric consistency, geometry signal boundary, blocked downstream
   scope, figure output, and script snapshots. Use runs `941-942` as the
   guarded preliminary 16-panel BEM acquisition-geometry sensitivity block.
   Run `943` sensitivity-hardens that validator. The exact source/receiver
   geometry state passes, while twenty-four damaged or prematurely promoted
   states fail as expected: readiness damage, row removal, offset-value damage,
   antenna-z value damage, baseline-setting damage, panel-policy damage,
   scan/frequency/time-count damage, baseline metric damage, geometry
   sensitivity metric damage, project-core FDTD promotion, field-transfer
   promotion, 3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `941-943` as the guarded preliminary
   16-panel BEM acquisition-geometry sensitivity block.
   Run `944` converts that sensitivity evidence into an acquisition-geometry
   lock policy for future matched BEM/FDTD comparisons. Geometry full-grid L2
   is `14.0411791425335x` the depth/material full-grid L2, the Tx/Rx offset
   peak span is `30.46264982845857x` the material peak span, and all eight
   policy rows require explicit locks. Run `945` validates the policy with six
   of six checks passing. Run `946` sensitivity-hardens the validator: the
   exact policy passes, while twenty-two damaged or prematurely promoted states
   fail as expected for source-readiness damage, row/item/order/tolerance/stage
   damage, dominance-ratio damage, project-core FDTD promotion, field-transfer
   promotion, 3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `944-946` as the guarded BEM acquisition-
   geometry lock-policy block.
   Run `947` refines the geometry result around the baseline with a `+/-5` mm
   tolerance sweep: Tx/Rx offsets `0.055`, `0.060`, and `0.065` m, and antenna
   z-positions `-0.005`, `0`, and `0.005` m. The fine sweep still shows a
   measurable geometry effect. At antenna z `0`, Tx/Rx spacing spans
   `0.6390875516677119` dB and reaches `0.16690749402586136` relative L2.
   Across antenna z at the baseline offset, the span is smaller:
   `0.03372223150313066` dB and `0.0708135992362416` relative L2. Use this as
   a preliminary tolerance-scale result; project-core FDTD, field transfer,
   GPU escalation, and 3D validation remain blocked.
   Run `948` validates the fine tolerance sweep with six of six checks
   passing: source identity, fine-grid shape, baseline and metric consistency,
   fine-geometry signal boundary, blocked downstream scope, figure output, and
   script snapshots. Use runs `947-948` as the guarded fine source/receiver
   tolerance block before selected higher-resolution checks.
   Run `949` sensitivity-hardens that validator. The exact fine-tolerance
   state passes, while twenty-four damaged or prematurely promoted states fail
   as expected: row/value/baseline/panel/shape damage, baseline and
   fine-geometry metric damage, project-core FDTD promotion, field-transfer
   promotion, 3D promotion, GPU-priority promotion, figure damage, and
   script-snapshot damage. Use runs `947-949` as the guarded fine
   source/receiver tolerance block.
   Run `950` adds a selected 32-panel resolution cross-check for the three
   baseline-height fine-offset cases. The fine offset signal survives the
   higher panel count almost exactly: the 32-panel peak offset span is
   `0.6390885783938787` dB versus `0.6390875516677119` dB for the 16-panel
   source result, and the 32-panel max relative L2 is
   `0.16690711298912922` versus `0.16690749402586136`. Use this as evidence
   that the fine Tx/Rx offset signal is not a 16-panel artifact for the
   selected baseline-height cases. Project-core FDTD matching, field transfer,
   GPU escalation, and 3D validation remain separate.
   Run `951` validates the selected 32-panel cross-check with six of six
   checks passing: cross-check identity, selected-grid shape and 32-panel
   policy, baseline and metric consistency, 32-panel/16-panel resolution
   agreement, blocked downstream scope, figure output, and script snapshots.
   Use runs `950-951` as the guarded selected 32-panel resolution cross-check
   for the fine Tx/Rx offset signal.
   Run `952` sensitivity-hardens that validator. The exact 32-panel
   cross-check state passes, while nineteen damaged or prematurely promoted
   states fail as expected: row/value/panel/shape damage, baseline and
   resolution-agreement metric damage, project-core FDTD promotion,
   field-transfer promotion, 3D promotion, GPU-priority promotion, figure
   damage, and script-snapshot damage. Use runs `950-952` as the guarded
   selected 32-panel fine-offset resolution cross-check.
6. Keep `bempp-cl` as the 3D prototype backend; keep SCUFF-EM and OpenBEM as reference/tools until licensing and integration policy are decided.
