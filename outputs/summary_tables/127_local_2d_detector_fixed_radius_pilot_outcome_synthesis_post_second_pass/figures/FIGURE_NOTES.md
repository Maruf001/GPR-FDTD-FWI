# Figure Notes

## `local_2d_detector_fixed_radius_pilot_outcome_synthesis.png`

This CPU-only figure synthesizes the completed fixed-radius detector
seed pilots against the exact-radius non-overlap preflight and repair
design. It is a selector, not a launch queue.

Policy label: `local_2d_detector_fixed_radius_pilot_outcome_synthesis_cpu_selector`.
Pilot runs included: `3`.
Best case: `target2_close14|seed21|nominal`.
Best final L-infinity error: `1.0` mm.
Selected next action: ``.
GPU cap for any selected probe: `90.0` percent.
RAM cap for any selected probe: `80.0` percent.

Scope boundary:

The artifact authorizes at most one guarded second-pass probe. It does
not authorize broad GPU queues, detector-inferred radius/material claims,
field transfer, 3D/HPC work, neural-network training, or FWI.

