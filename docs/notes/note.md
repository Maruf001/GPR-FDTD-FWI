• You are asking the right question. The key point is:

  In the synthetic experiments, we know the truth, but the optimizer is treated as if it does not know the
  truth.

  We use the known truth only to create a controlled test.

  Think of it like this:

  1. We secretly choose the true scene:

  target0: x=150 mm, z=80 mm, radius=5 mm
  target1: x=250 mm, z=100 mm, radius=6 mm
  target2: x=350 mm, z=120 mm, radius=8 mm

  2. We run FDTD once on that true scene.

  That gives us synthetic “measured” radar data:

  reference waveform = FDTD(true scene)

  3. Then we hide the true scene from the optimizer.

  The optimizer only sees the reference waveform. Its job is:

  Find the x, z, radius values that would produce a waveform most similar to this reference waveform.

  So yes, the optimizer is trying to “fit” the FDTD-generated data.

  For a candidate guess, it asks:

  candidate scene = maybe x=250 mm, z=100 mm, radius=5 mm
  candidate waveform = FDTD(candidate scene)
  misfit = difference(candidate waveform, reference waveform)

  Then it tries another guess:

  candidate scene = maybe x=250 mm, z=100 mm, radius=6 mm
  candidate waveform = FDTD(candidate scene)
  misfit = difference(candidate waveform, reference waveform)

  If the second candidate has lower misfit, the optimizer says: radius 6 mm explains the observed waveform
  better than radius 5 mm.

  So the goal is not to use the known answer directly. The goal is to test whether waveform matching can recover
  the known answer.

  In short:

  reference data = FDTD(true hidden scene)
  candidate data = FDTD(candidate guessed scene)
  objective/misfit = difference between them
  optimizer goal = find candidate with lowest difference

  The important distinction:

  - During experiment design, we know the ground truth.
  - During inversion/optimization, the algorithm is only allowed to use the waveform data.
  - After optimization, we compare the recovered result to the known truth to judge whether the method worked.

  And no, the optimizer is not “simulating without FDTD” in the basic interpretation. Conceptually, each
  candidate needs a forward radar response, and FDTD is the forward simulator. In practice, some parts may be
  cached, precomputed, approximated, or searched over a grid, but the underlying comparison is still:

  "Does this candidate model produce a radar waveform like the reference waveform?"




In summary:

  1. We define a true synthetic rebar scene
     Example: three rebars at known x, z, and radius values.

  2. We run FDTD on that true scene
     FDTD means finite-difference time-domain simulation. It numerically simulates the radar pulse traveling
     through the concrete, scattering from rebars, and being recorded by receivers.

  3. That output becomes the “reference” or “observed” data
     It is usually a set of receiver time traces, often viewed as a B-scan. This is the waveform data the
     optimizer tries to match.

  4. The optimizer tests candidate scenes
     For example: “what if target1 radius is 5 mm instead of 6 mm?” or “what if the rebar depth is slightly
     different?”

  5. For each candidate, we run or evaluate a simulated radar response
     That candidate produces its own simulated waveform/B-scan.

  6. The objective compares candidate response vs reference response
     The score is the waveform mismatch. Lower mismatch means the candidate explains the reference data better.

  So when I said:

  > simulated radar response and the reference data

  I meant:

  > candidate FDTD-generated waveform compared against the synthetic observed waveform generated from the known
  > true model.

  For real field data, the situation changes. The measured GPR data becomes the observed/reference waveform, but
  we usually do not know the true rebar geometry. So with field data we can minimize waveform mismatch, but we
  cannot say “exact geometry recovered” unless we have independent ground truth, drawings, coring, survey
  measurements, or another validation source.
