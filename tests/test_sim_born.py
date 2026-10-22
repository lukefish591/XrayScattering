import numpy as np

from xray_scattering.sim.correlations import C_self_affine
from xray_scattering.sim.forward import born_s_diff
from xray_scattering.sim.hankel import cosine_taper, hankel0  # cosine_taper used in both tests


def test_born_matches_chapter5_formula():
    sigma, xi, h = 5.0, 40.0, 0.5
    qz = 0.08
    qpar = np.linspace(0.0, 0.2, 25)
    Rmax = 8.0 * xi

    def C_of_R(R):
        return C_self_affine(R, sigma, xi, h)

    s, sig2 = born_s_diff(qpar, qz, C_of_R, Rmax, nR=900)
    assert abs(sig2 - sigma**2) / sigma**2 < 1e-9

    R = np.linspace(0.0, Rmax, 900)
    C = C_of_R(R) * cosine_taper(R, Rmax)
    kernel = np.exp(qz**2 * C) - 1.0
    ref = np.exp(-(qz**2) * sigma**2) / qz**2 * hankel0(qpar, R, kernel)
    np.testing.assert_allclose(s, ref, rtol=1e-6, atol=1e-8)


def test_small_qz_sdiff_tracks_hankel_of_C():
    sigma, xi, h = 4.0, 36.0, 0.5
    qz = 0.02  # qz²σ² ≪ 1
    qpar = np.linspace(0.0, 0.15, 20)
    Rmax = 8.0 * xi

    def C_of_R(R):
        return C_self_affine(R, sigma, xi, h)

    s, _ = born_s_diff(qpar, qz, C_of_R, Rmax, nR=800)
    R = np.linspace(0.0, Rmax, 800)
    C = C_of_R(R) * cosine_taper(R, Rmax)
    # S ≈ e^{-qz²σ²} H[C] when e^{qz²C}-1 ≈ qz² C
    approx = np.exp(-(qz**2) * sigma**2) * hankel0(qpar, R, C)
    rel = np.max(np.abs(s - approx)) / (np.max(approx) + 1e-30)
    assert rel < 0.08
