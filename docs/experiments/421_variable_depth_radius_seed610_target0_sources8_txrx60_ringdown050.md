# Experiment 421: Seed610 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Run 887 tests seed610 target 0 at full ringdown050 with 8 sources. The row is
exact/moderate and technically accepted, but only by `5.897e-07` above the
5.0e-04 cutoff.

Diagnostic objective rows all preserve truth. Base, highband, late_high,
veryhigh, and early_high clear cutoff; late is below cutoff.

Interpretation: seed610 is now the closest accepted target-0 row. Together
with seed21's failure and seed55's low reserve, this keeps the target-0 lower
tail active even though most Fibonacci seeds pass full ringdown050.

Validation: JSON and CSV artifacts parse; CSV rows are confidence=1,
diagnostics=6, top candidates=72, state history=2, candidates=12; the figure is
1549x903 RGBA with nonwhite_fraction=0.251477 and full dynamic range.
