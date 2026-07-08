# Figure Notes

## `local_2d_detector_false_geometry_morphology_audit.png`

This CPU-only audit compares the refreshed detector selector's top false
x-geometries with representative all-truth candidate triples from the saved
component-gate rows.

Policy label: `local_2d_detector_false_geometry_morphology_audit_cpu_no_fwi`.
Cases: `12`.
Top-200 all-truth cases: `12`.
Compressed-span cases: `3`.
Median selected/truth x-span ratio: `0.9960914454277285`.
Dominant false geometry mode: `single_truth_only_target2`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

The refreshed detector selector's top rows are not random misses: they are structured false geometries, often compressed or partial target subsets, while all-truth triples remain rank-gated but not top-ranked. This supports a detector ambiguity/morphology claim and still blocks detector-seeded FWI.

