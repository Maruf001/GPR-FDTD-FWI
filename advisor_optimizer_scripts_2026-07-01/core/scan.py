"""
B-scan acquisition: multi-position GPR scanning.

Manages a series of forward FDTD simulations with a moving
transmitter-receiver pair along a scan line at the concrete surface.
Assembles individual A-scan traces into a B-scan radargram.
"""
import numpy as np
from core.fdtd import FDTDSimulator
from core.source import ricker_wavelet, generate_time_array
from core.utils import pos_to_index
import config as cfg


class Scanner:
    """
    Multi-position GPR scanner.

    For each scan position:
        1. Reset FDTD fields
        2. Set Tx and Rx positions
        3. Run forward simulation
        4. Record the A-scan trace at Rx
    """

    def __init__(self, model):
        """
        Initialize scanner with a material model.

        Parameters
        ----------
        model : MaterialModel
            The material model to simulate.
        """
        self.model = model
        self.simulator = FDTDSimulator(model)

        # Generate scan positions
        self.scan_x = np.arange(cfg.SCAN_START_X, cfg.SCAN_END_X + 1e-10,
                                cfg.SCAN_STEP)
        self.n_scans = len(self.scan_x)

        # Time array and source wavelet
        self.time = generate_time_array(cfg.NT, cfg.DT)
        self.wavelet = ricker_wavelet(self.time, cfg.F_CENTER)

        # Convert Tx/Rx z-positions to grid indices
        self.src_iz = pos_to_index(cfg.TX_Z, cfg.DZ, cfg.NPML)
        self.rec_iz = pos_to_index(cfg.RX_Z, cfg.DZ, cfg.NPML)

    def run_scan(self, scan_step=None, save_animation_for=-1, verbose=True):
        """
        Execute B-scan acquisition.

        Parameters
        ----------
        scan_step : float, optional
            Override scan step size (e.g., for inversion with coarser sampling).
        save_animation_for : int
            If >= 0, save field snapshots for this scan index (for animation).
        verbose : bool
            Print progress.

        Returns
        -------
        result : dict
            'bscan': ndarray (nt, n_scans) -- B-scan image
            'scan_x': ndarray -- x-coordinates of scan positions [m]
            'time': ndarray -- time array [s]
            'snapshots': list of (step, Ez) if animation requested
        """
        if scan_step is not None:
            scan_x = np.arange(cfg.SCAN_START_X, cfg.SCAN_END_X + 1e-10,
                               scan_step)
        else:
            scan_x = self.scan_x

        n_scans = len(scan_x)
        bscan = np.zeros((cfg.NT, n_scans), dtype=np.float64)
        snapshots = []

        for i, x_pos in enumerate(scan_x):
            if verbose and i % 10 == 0:
                print(f"  Scan position {i+1}/{n_scans} "
                      f"(x = {x_pos*1000:.1f} mm)")

            # Transmitter position
            src_ix = pos_to_index(x_pos, cfg.DX, cfg.NPML)
            # Receiver position (offset from Tx)
            rec_ix = pos_to_index(x_pos + cfg.TX_RX_OFFSET, cfg.DX, cfg.NPML)

            # Ensure receiver is within domain
            rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)

            save_every = 20 if i == save_animation_for else 0

            result = self.simulator.run(
                self.wavelet, self.src_iz, src_ix,
                self.rec_iz, rec_ix,
                save_fields_every=save_every,
            )

            bscan[:, i] = result['trace']
            if i == save_animation_for:
                snapshots = result['snapshots']

        return {
            'bscan': bscan,
            'scan_x': scan_x,
            'time': self.time,
            'snapshots': snapshots,
        }

    def get_scan_positions(self, scan_step=None):
        """Return arrays of (src_iz, src_ix, rec_iz, rec_ix) for each scan."""
        if scan_step is not None:
            scan_x = np.arange(cfg.SCAN_START_X, cfg.SCAN_END_X + 1e-10,
                               scan_step)
        else:
            scan_x = self.scan_x

        positions = []
        for x_pos in scan_x:
            src_ix = pos_to_index(x_pos, cfg.DX, cfg.NPML)
            rec_ix = pos_to_index(x_pos + cfg.TX_RX_OFFSET, cfg.DX, cfg.NPML)
            rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)
            positions.append((self.src_iz, src_ix, self.rec_iz, rec_ix))
        return positions, scan_x
