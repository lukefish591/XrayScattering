import numpy as np

from xray_scattering.sim.correlations import correlation_function
from xray_scattering.sim.params import SurfaceParams
from xray_scattering.sim.surface import generate_surface
from xray_scattering.sim.analysis import empirical_correlation


def test_surface_reproduces_sigma_and_C():
    p = SurfaceParams(family="self-affine", sigma=6.0, xi=32.0, h=0.45, N=128, L=384.0, seed=7)
    s = generate_surface(p)
    rms = float(s.z.std())
    assert abs(rms - p.sigma) / p.sigma < 0.08
    r, Cemp = empirical_correlation(s.z, s.dx, nbins=28, rmax=2.5 * p.xi)
    Cthy = correlation_function(p.family, r, p.sigma, p.xi, p.h)
    # near origin, relative error on C
    m = r < 1.2 * p.xi
    rel = np.max(np.abs(Cemp[m] - Cthy[m])) / (p.sigma**2)
    assert rel < 0.35


def test_deterministic_seed():
    p = SurfaceParams(N=64, L=256.0, seed=42)
    a = generate_surface(p)
    b = generate_surface(p)
    np.testing.assert_allclose(a.z, b.z)
    c = generate_surface(SurfaceParams(N=64, L=256.0, seed=43))
    assert not np.allclose(a.z, c.z)


def test_gaussian_family_is_h1():
    p = SurfaceParams(family="gaussian", sigma=4.0, xi=40.0, h=0.2, N=48, L=240.0, seed=1)
    s = generate_surface(p)
    r0 = np.array([0.0, 40.0])
    C = s.C_of_R(r0)
    C_h1 = correlation_function("self-affine", r0, 4.0, 40.0, 1.0)
    np.testing.assert_allclose(C, C_h1)
