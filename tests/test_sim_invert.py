import numpy as np

from xray_scattering.sim.analysis import invert_C_from_sdiff
from xray_scattering.sim.correlations import C_self_affine
from xray_scattering.sim.forward import born_s_diff
from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import generate_surface
from xray_scattering.sim.forward import simulate_measurement


def test_noiseless_inversion_recovers_C():
    sigma, xi, h = 5.0, 40.0, 0.5
    qz = 0.07
    qpar = np.linspace(0.0, 0.18, 60)
    Rmax = 10.0 * xi

    def C_of_R(R):
        return C_self_affine(R, sigma, xi, h)

    s, _ = born_s_diff(qpar, qz, C_of_R, Rmax, nR=1000)
    R = np.linspace(0.0, 3.0 * xi, 80)
    C_inv = invert_C_from_sdiff(qpar, s, qz, sigma, R, Rmax)
    C_thy = C_of_R(R)
    rel = np.max(np.abs(C_inv - C_thy)) / sigma**2
    assert rel < 0.25


def test_measurement_deterministic():
    p = SurfaceParams(N=48, L=240.0, seed=3)
    m = MeasureParams(scan="rocking", n_pts=41, noise=0.0, seed=0)
    s = generate_surface(p)
    a = simulate_measurement(s, m)
    b = simulate_measurement(s, m)
    np.testing.assert_allclose(a.intensity, b.intensity)
