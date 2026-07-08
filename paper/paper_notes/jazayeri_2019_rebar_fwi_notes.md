# Paper Notes: Jazayeri et al. 2019, Rebar Mapping With GPR FWI

Source PDF: `paper/Jazayeri_etal_2019_rebar_FWI.pdf`

Rendered visual pages inspected: `outputs/literature_method_work/2026-07-03_paper_vision_pages/jazayeri_2019/`

Text extraction used for equations/tables: `outputs/literature_method_work/2026-07-03_paper_vision_pages/raw_text/jazayeri_2019.txt`

## Bibliographic Details

Title: Reinforced concrete mapping using full-waveform inversion of GPR data

Authors: Sajad Jazayeri, Sarah Kruse, Istiaque Hasan, Nur Yazdani

Journal: Construction and Building Materials, 2019, volume 229, article 117102

DOI: `10.1016/j.conbuildmat.2019.117102`

## Main Problem

This paper targets exactly the reinforced-concrete rebar problem: estimating rebar location and diameter from surface-coupled common-offset GPR B-scans. The authors argue that standard hyperbola/ray methods can locate bars, but diameter is poorly constrained because small rebar diameters are often below or comparable to the radar wavelength in concrete.

The paper's central claim is that full-waveform inversion can improve rebar diameter estimates because it uses waveform shape and amplitude information, not only first-arrival or peak travel-time geometry.

## Why This Paper Is Directly Relevant

This is the closest of the four papers to our GSSI 51600S field-data goal because it uses:

- common-offset B-scans,
- commercial GPR systems,
- concrete slabs/boxes,
- metallic rebars,
- rebar radius/diameter estimation,
- concrete relative permittivity and conductivity estimation,
- source-wavelet estimation from the measured data,
- gprMax forward modeling for waveform matching.

The major field-data assumption is that the profile is perpendicular to the rebars.

## Overall Workflow

The workflow is sequential:

1. Preprocess the measured B-scan.
2. Estimate an effective source wavelet and sparse reflectivity series using sparse blind deconvolution (SBD).
3. Pick/use hyperbolic reflectivity events from the SBD result.
4. Use a ray-based finite-radius common-offset formula to produce an initial model:
   - rebar horizontal location,
   - rebar depth,
   - rebar radius/diameter,
   - concrete relative permittivity,
   - initial concrete conductivity.
5. Build a gprMax forward model:
   - concrete background,
   - metallic rebar as PEC,
   - source wavelet from SBD,
   - common-offset antenna geometry.
6. Run FWI by iteratively forward modeling and updating the starting model to reduce waveform mismatch.
7. Report final rebar diameter/location and concrete properties.

## Ray-Based Geometry

The paper derives an analytical travel-time model for a cylindrical target in common-offset geometry, explicitly including non-zero transmitter-receiver offset. This is important because commercial shielded GPR antennas have fixed non-zero antenna separation.

Parameters:

- `x_T`: transmitter position.
- `x_R`: receiver position.
- `dx`: transmitter-receiver offset.
- `x`: horizontal location of the rebar top.
- `y`: depth to the top of the rebar.
- `r`: rebar radius.
- `x_0`: horizontal location of the ray incidence point on the rebar circumference.
- `h`: depth of the ray incidence point.
- `epsilon`: relative permittivity of concrete.
- `t_0`: effective time zero.
- `c`: speed of light in free space.

The model accounts for the point of incidence on the cylinder circumference, not just a point diffractor. The transmitter-to-cylinder and cylinder-to-receiver ray distances are `d_T` and `d_R`, and the modeled two-way time is:

```text
t = (d_T + d_R) / (c / sqrt(epsilon)) + t_0
```

The rebar is treated as nearly a perfect electrical conductor, so the radar wave does not penetrate it. That makes the rebar material fixed in the FWI and leaves geometry plus concrete properties as the main unknowns.

## Sparse Blind Deconvolution

Because the source wavelet cannot be measured directly for a ground-coupled antenna, the paper estimates it from the data.

The measured data are treated as:

```text
data = source_wavelet * reflectivity + noise
```

Both source wavelet and reflectivity are unknown. Full blind deconvolution is too expensive, so they use the SBD approach from their prior work:

- Choose initial wavelet windows near hyperbola apexes.
- Time-shift selected waveforms to maximize zero-lag cross-correlation.
- Stack and normalize to form an initial wavelet.
- Solve a sparse reflectivity problem, described as an `l2-l1` problem with Split Bregman.
- Update the source wavelet using a Wiener-filter-like `l2-l2` step.
- Iterate wavelet and reflectivity estimates.

The final SBD outputs are both used:

- The estimated wavelet goes into FWI.
- The sparse reflectivity image is used for ray-based initial geometry.

## FWI Setup

Forward modeling is done with gprMax. The paper uses 3-D models for the test cases. The metallic rebar is fixed as PEC. Concrete relative permittivity and conductivity are estimated/updated.

The paper does not fully rederive the adjoint equations in this article; it relies on prior Jazayeri et al. FWI work for details. The current paper's contribution is the reinforced-concrete rebar workflow:

- finite-radius common-offset ray initial model,
- SBD-derived source wavelet and reflectivity,
- gprMax FWI refinement of rebar diameter/depth/location and concrete properties.

Stopping criterion:

```text
stop when the cost-function change between iterations is less than 0.2 percent
```

Preprocessing for real data:

- standard dewow filter,
- time-zero correction,
- low-pass filter with cutoff depending on antenna frequency,
- background/direct-wave removal when needed.

## Figure-Level Notes From Visual Reading

### Figure 1: Synthetic B-scan

The first figure shows four synthetic hyperbolas from metallic rebars in concrete. The visual point is that the hyperbolas are clear, but diameter information is not visually obvious from the travel-time curves alone.

### Figure 2: Common-offset cylinder geometry

This is the key method diagram. It shows a ground-coupled transmitter/receiver pair with fixed offset over a cylindrical rebar. The ray interaction point is on the cylinder circumference. This is more realistic than treating the rebar as a point diffractor or assuming zero antenna offset.

### Figures 4-5: Source wavelet and background-removed synthetic data

Figure 4 shows the synthetic source wavelet: derivative of a Ricker wavelet with 35 degree phase rotation. Figure 5 shows background-removed synthetic data and the windows used to estimate the initial source wavelet for SBD.

The visual takeaway is that the wavelet is not a trivial detail. The authors explicitly build the source estimate from local windows around apexes before SBD/FWI.

### Figures 6-8: Real data case 1

Case 1 is a concrete box with three 19 mm rebars at covers of 2.5, 5, and 7.5 cm. The data are acquired with a ground-coupled 2.6 GHz GSSI system, perpendicular to the bar direction.

The B-scan shows three well-separated hyperbolas. The shallowest rebar is partly mixed with/directly affected by the direct wave.

### Figures 9-10: Real data case 2

Case 2 has seven 10 mm rebars with covers from 0.5 to 15 cm. The acquisition uses a 1 GHz Noggin system, again perpendicular to bar direction. The hyperbolas overlap more than in case 1, and deeper targets have lower SNR.

### Figures 11, 14, and 16: SBD products

These figures show:

- initial wavelet estimated from selected data windows,
- SBD-updated wavelet,
- sparse reflectivity model.

In all cases, the reflectivity image is cleaner than the raw B-scan and gives more usable hyperbola traces for the ray-based initial model.

### Figures 12, 15, and 17: Misfit convergence

The synthetic FWI converges after 14 iterations.

Real data case 1 converges after 21 iterations.

Real data case 2 converges after 25 iterations.

The convergence criterion is a less than 0.2 percent change in misfit.

### Figure 18: Improvement summary

The arrow plot summarizes movement from ray-based estimates to FWI estimates in depth-diameter space. The visually important result is that FWI improves every experimental case, but the improvement is larger for diameter than for depth. Deep bars remain harder, and the shallowest bar can also be problematic because near-field/direct-wave effects are incompletely modeled.

## Synthetic Test

Synthetic geometry:

- Four metallic rebars.
- Uniform concrete.
- Rebar depths around 2.7-4 cm.
- Nominal antenna frequency: 2.4 GHz.
- Transmitter-receiver offset: 3 cm.
- Source: derivative Ricker wavelet with 35 degree phase rotation.
- Noise:
  - high-frequency Gaussian noise centered at 3 GHz, peak about 25 percent of pulse amplitude,
  - lower-frequency noise around 1.5 MHz at about 15 percent of pulse amplitude.

Key synthetic result from Table 1:

- Ray-based diameter errors average about 73 percent, with individual errors from 24.5 percent to 124 percent.
- FWI diameter errors average about 9.7 percent, with individual errors from 4.9 percent to 15.25 percent.
- Concrete relative permittivity improves from ray-based 3.89 to FWI 4.77, with true value 5.
- Concrete conductivity improves from ray-based 14.2 mS/m to FWI 11.2 mS/m, with true value 10 mS/m.

## Real Data Case 1

Physical setup:

- Concrete block about 137 cm long, 25 cm wide, 15 cm deep.
- Three standard 19 mm rebars.
- Covers: 2.5, 5, and 7.5 cm.
- Ground-coupled 2.6 GHz GSSI system.
- B-scan acquired perpendicular to bars.
- Low-pass cutoff: 3.2 GHz.

Processing:

- Background removal is used before SBD because the shallowest bar is mixed with the direct wave.
- Initial source wavelet is selected from windows near hyperbola apexes.
- SBD produces final wavelet and reflectivity image.
- Ray analysis provides initial FWI model.

Results from Table 2:

- Ray-based diameter errors:
  - 24.7 percent,
  - 43.9 percent,
  - 36.8 percent.
- FWI diameter errors:
  - 10.4 percent,
  - 0.1 percent,
  - 11.1 percent.
- Average FWI diameter error: about 7.2 percent.
- FWI also improves depth estimates.
- Concrete relative permittivity shifts from ray-based 5.11 to FWI 4.77.
- Concrete conductivity shifts from ray-based 8.22 mS/m to FWI 14.09 mS/m.

Important caveat: the authors note that case 1 is noisier than case 2, despite the higher-frequency antenna and larger bars.

## Real Data Case 2

Physical setup:

- Concrete slab containing seven 10 mm rebars.
- Covers from 0.5 to 15 cm.
- Other objects also embedded, including PVC pipes and a tennis ball.
- Common-offset B-scan with 1 GHz Sensors and Software Noggin 1000.
- Profile perpendicular to bar direction.
- Low-pass cutoff: 1.6 GHz.
- Hyperbolas overlap at their outer edges.

Results from Table 3:

- Ray-based diameter errors range from 30 percent to 162 percent, average about 61 percent.
- FWI diameter errors range from 3 percent to 51 percent, average about 17 percent.
- Best FWI results occur for middle-depth bars:
  - 7.5 cm and 5 cm covers reach about 3 percent error.
  - 1 cm and 0.5 cm covers reach about 4 percent and 6 percent error.
- The deepest 15 cm bar remains poor at 51 percent error.
- Concrete relative permittivity shifts from ray-based 6.56 to FWI 5.98.
- Concrete conductivity shifts from ray-based 28.45 mS/m to FWI 19.72 mS/m.

## Main Conclusions

The paper shows that SBD plus FWI substantially improves rebar diameter estimates over ray-based analysis alone.

The strongest final claim:

- For bars with cover depth 7.5 cm or less, final diameter errors are about 0.1-11 percent.

The broader trend:

- FWI improves diameter more strongly than depth.
- Deep bars remain difficult because lower amplitudes and lower SNR degrade both initial models and final inversion.
- Shallow bars can also be difficult because near-field and direct-wave interactions are not completely captured.
- The method is useful for estimating unknown embedded bar dimensions, but not for resolving tiny diameter changes associated with corrosion growth, which may be less than 1 mm/year.

## Key Assumptions

- Rebar is metallic and can be modeled as PEC.
- Rebar axis is perpendicular to the B-scan profile.
- Concrete background is uniform in permittivity and conductivity for the examples.
- The source wavelet can be estimated well enough from selected data windows.
- A usable initial model can be obtained from SBD reflectivity plus ray-based analysis.
- The measured profile contains enough waveform information to constrain diameter.

## Relevance to Our GSSI 51600S Field Data

This should be the first full rebar-specific paper track to adapt to our local field data because the method and acquisition mode are closest to our data.

Directly transferable pieces:

- Import a GSSI B-scan.
- Preprocess with time-zero correction, dewow, low-pass/bandpass filtering, and background/direct-wave removal.
- Estimate source wavelet from selected hyperbola-apex windows.
- Generate a sparse reflectivity image by SBD or a close equivalent.
- Fit finite-radius common-offset ray geometry for initial rebar location/depth/diameter/concrete permittivity.
- Build a gprMax model with PEC rebars and concrete background.
- Run waveform inversion from the ray/SBD starting model.

Important field-data checks before implementation:

- Confirm profile direction is perpendicular or near-perpendicular to rebars.
- Determine antenna center frequency and transmitter-receiver offset from DZT/DZX metadata or instrument notes.
- Determine trace spacing and time-zero.
- Identify isolated hyperbolas and overlapping hyperbola regions.
- Decide whether the concrete can be treated as uniform over each profile.

## How To Test This Paper Separately On Our Field Data

Keep this track paper-pure:

1. Select one GSSI profile with the clearest rebar hyperbolas.
2. Run only the Jazayeri workflow:
   - preprocessing,
   - SBD wavelet/reflectivity,
   - ray finite-radius initial model,
   - gprMax FWI refinement.
3. Do not introduce frequency-dependent `tau_epsilon` from Qin et al. in the first pass.
4. Do not treat hyperbola fitting alone as the final method; use it only to create the starting model as the paper does.
5. Report:
   - ray-based estimates,
   - FWI estimates,
   - waveform misfit curve,
   - overlay of modeled and observed B-scans,
   - estimated source wavelet,
   - inferred concrete permittivity/conductivity.

## Implementation Priority

This paper should drive the first serious field-data rebar inversion attempt.

Minimum implementation:

- DZT/DZX import and metadata extraction.
- Rebar hyperbola picking or semi-automatic SBD reflectivity ridge extraction.
- Finite-radius ray model with non-zero antenna offset.
- Initial model builder for gprMax:
  - concrete block,
  - PEC cylinders,
  - estimated antenna/source settings.
- FWI loop over:
  - rebar horizontal position,
  - cover depth,
  - diameter,
  - concrete relative permittivity,
  - concrete conductivity,
  - source wavelet if needed.

Potential simplification while staying faithful to the paper:

- Use the SBD/ray model to initialize parameters.
- Use gprMax or an equivalent FDTD forward solver for waveform simulation.
- If full adjoint gprMax parameter gradients are not available locally, use a bounded derivative-free or finite-difference optimizer only as an engineering substitute, clearly labeled as replacing the paper's FWI optimizer while preserving the paper's physical parameterization and data workflow.

## Risks and Limitations For Our Data

- If our GSSI profiles are not perpendicular to rebars, the method's core geometry assumption breaks.
- If metadata do not provide antenna offset, it must be calibrated.
- If time-zero is unstable, depth and diameter estimates will be biased.
- If there are multiple overlapping rebars, SBD/ray initial models may be poor.
- If the rebar cover is too deep relative to antenna frequency, diameter estimates will degrade strongly.
- If concrete is heterogeneous, a uniform concrete model may produce biased diameter estimates.
- If the direct wave dominates shallow targets, near-field effects may limit the inversion, as in the paper's shallowest rebar cases.

## One-Sentence Takeaway

This paper gives the most directly applicable workflow for our GSSI rebar B-scans: use SBD to estimate source wavelet/reflectivity, use finite-radius common-offset ray analysis for the starting model, then use FWI to refine rebar diameter/location and concrete properties.
