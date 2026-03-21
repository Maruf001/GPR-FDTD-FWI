"""
Benchmarking utilities for CPU vs GPU comparison.

Measures wall-clock time for forward simulation on both CPU and GPU,
and reports hardware information.
"""
import time
import numpy as np
import platform


def get_hardware_info():
    """Collect hardware information for benchmarking context."""
    info = {
        'platform': platform.platform(),
        'processor': platform.processor(),
        'python': platform.python_version(),
    }

    try:
        import cupy as cp
        device = cp.cuda.Device(0)
        info['gpu_name'] = device.attributes['DeviceName'] if hasattr(device, 'attributes') else 'Unknown'
        info['gpu_memory_mb'] = device.mem_info[1] / (1024 ** 2)
        info['cuda_version'] = cp.cuda.runtime.runtimeGetVersion()
    except Exception:
        info['gpu_name'] = 'N/A (CuPy not available)'
        info['gpu_memory_mb'] = 0
        info['cuda_version'] = 'N/A'

    return info


def benchmark_forward(model, config, n_runs=3):
    """
    Benchmark forward simulation on CPU and GPU.

    Parameters
    ----------
    model : MaterialModel
    config : module
    n_runs : int
        Number of runs to average.

    Returns
    -------
    dict with 'cpu_time', 'gpu_time', 'speedup', 'hardware'
    """
    from core.fdtd import FDTDSimulator
    from core.source import ricker_wavelet, generate_time_array
    from core.utils import pos_to_index

    t = generate_time_array(config.NT, config.DT)
    wavelet = ricker_wavelet(t, config.F_CENTER)
    src_iz = pos_to_index(config.TX_Z, config.DZ, config.NPML)
    src_ix = pos_to_index(0.25, config.DX, config.NPML)
    rec_iz = pos_to_index(config.RX_Z, config.DZ, config.NPML)
    rec_ix = pos_to_index(0.27, config.DX, config.NPML)

    # CPU benchmark
    cpu_times = []
    for _ in range(n_runs):
        sim = FDTDSimulator(model)
        t0 = time.perf_counter()
        sim.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
        cpu_times.append(time.perf_counter() - t0)
    cpu_time = np.mean(cpu_times)

    # GPU benchmark
    gpu_time = None
    try:
        from gpu.fdtd_gpu import FDTDSimulatorGPU
        import cupy as cp

        gpu_times = []
        for _ in range(n_runs):
            sim_gpu = FDTDSimulatorGPU(model, config)
            cp.cuda.Device(0).synchronize()
            t0 = time.perf_counter()
            sim_gpu.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
            cp.cuda.Device(0).synchronize()
            gpu_times.append(time.perf_counter() - t0)
        gpu_time = np.mean(gpu_times)
    except Exception as e:
        print(f"GPU benchmark skipped: {e}")

    speedup = cpu_time / gpu_time if gpu_time else None

    return {
        'cpu_time': cpu_time,
        'gpu_time': gpu_time,
        'speedup': speedup,
        'hardware': get_hardware_info(),
    }
