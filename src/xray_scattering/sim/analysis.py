from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit

from xray_scattering.sim.correlations import correlation_function
from xray_scattering.sim.hankel import cosine_taper, hankel0, inverse_hankel0
from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import Surface, generate_field


def empirical_correlation(z: np.ndarray, dx: float, nbins: int = 36, rmax: float | None = None):
    """Isotropic C(R) from a map via FFT autocorrelation."""
    z0 = z - z.mean()
    ac = np.fft.ifft2(np.abs(np.fft.fft2(z0)) ** 2).real / z.size
    ac = np.fft.fftshift(ac)
    N = z.shape[0]
    if rmax is None:
        rmax = 0.35 * N * dx
    bins = np.linspace(0.0, rmax, nbins + 1)
    rs = 0.5 * (bins[1:] + bins[:-1])
    vals = np.zeros(nbins)
    counts = np.zeros(nbins)
    i = np.arange(N)
    I, J = np.meshgrid(i, i, indexing="ij")
    rij = np.hypot((I - N // 2) * dx, (J - N // 2) * dx)
    b = np.digitize(rij.ravel(), bins) - 1
    a = ac.ravel()
    for k in range(nbins):
        m = b == k
        if np.any(m):
            vals[k] = a[m].mean()
            counts[k] = m.sum()
    return rs, vals


def radial_psd_from_C(q, C_of_R, Rmax: float, nR: int = 800):
    R = np.linspace(0.0, Rmax, nR)
    C = np.asarray(C_of_R(R), dtype=float) * cosine_taper(R, Rmax)
    return np.maximum(2.0 * np.pi * hankel0(q, R, C), 1e-30)


def invert_C_from_sdiff(qpar, intensity, qz: float, sigma: float, R, Rmax: float):
    """Recover C(R) from noiseless-ish S_diff via inverse Hankel of PRB (2.28b)."""
    qpar = np.asarray(qpar, dtype=float)
    intensity = np.asarray(intensity, dtype=float)
    order = np.argsort(qpar)
    q = qpar[order]
    I = np.maximum(intensity[order], 0.0)
    pref = np.exp(-(qz**2) * sigma**2) / (qz**2 + 1e-30)
    H = I / (pref + 1e-30)
    f = inverse_hankel0(R, q, H)
    arg = np.clip(1.0 + f, 1e-8, None)
    C = np.log(arg) / (qz**2 + 1e-30)
    C = C * cosine_taper(R, Rmax)
    # C(0) should be ~ sigma^2; clip wild inversion
    return np.clip(C, -5.0 * sigma**2, 5.0 * sigma**2)


def _model_sdiff(qpar, sigma, xi, h, qz, Rmax, family="self-affine"):
    R = np.linspace(0.0, Rmax, 560)

    def C_of_R(r):
        return correlation_function(family, r, sigma, xi, h)

    C = C_of_R(R) * cosine_taper(R, Rmax)
    kernel = np.exp(qz**2 * C) - 1.0
    s = hankel0(qpar, R, kernel)
    pref = np.exp(-(qz**2) * sigma**2) / (qz**2 + 1e-30)
    return pref * s


def fit_self_affine(qpar, intensity, qz: float, Rmax: float, p0: SurfaceParams):
    """Least-squares σ, ξ, h against Born S_diff. Uncertainties from pcov."""
    qpar = np.asarray(qpar, dtype=float).ravel()
    y = np.asarray(intensity, dtype=float).ravel()
    y = np.maximum(y, 0.0)
    scale = float(np.max(y) + 1e-30)
    yn = y / scale
    family = p0.family if p0.family in ("self-affine", "gaussian") else "self-affine"

    def f(q, sigma, xi, h):
        hh = 1.0 if family == "gaussian" else h
        s = _model_sdiff(q, sigma, xi, hh, qz, Rmax, family=family)
        return s / (np.max(s) + 1e-30)

    bounds = ([0.3, 5.0, 0.15], [25.0, min(Rmax, 250.0), 0.95])
    p_init = (
        float(np.clip(p0.sigma, 0.4, 24.0)),
        float(np.clip(p0.xi, 6.0, bounds[1][1] - 1)),
        float(np.clip(p0.h, 0.16, 0.94)),
    )
    try:
        popt, pcov = curve_fit(
            f,
            qpar,
            yn,
            p0=p_init,
            bounds=bounds,
            maxfev=1200,
        )
        perr = np.sqrt(np.clip(np.diag(pcov), 0.0, None))
    except Exception:
        popt = np.array(p_init)
        perr = np.array([np.nan, np.nan, np.nan])
    names = ("sigma", "xi", "h")
    return {n: (float(v), float(e)) for n, v, e in zip(names, popt, perr)}


@dataclass
class FitLine:
    """q∥ line the live app feeds to the self-affine fitter.

    Specular has no q∥: unidentified_xi_h is True and used_aux_rocking
    means the intensities came from a noiseless rocking kernel (a cheat,
    not a recovery from the specular scan).
    """

    qpar: np.ndarray
    intensity: np.ndarray
    qz_ref: float
    scan: str
    used_aux_rocking: bool
    unidentified_xi_h: bool


def fit_line_from_measurement(surface: Surface, m: MeasureParams) -> FitLine:
    """Same forward+line selection as the live two-column view."""
    from xray_scattering.sim.forward import simulate_measurement

    det = simulate_measurement(surface, m)
    if det.scan == "qmap":
        mid = det.intensity.shape[0] // 2
        return FitLine(
            qpar=np.asarray(det.x, dtype=float),
            intensity=np.asarray(det.intensity[mid], dtype=float),
            qz_ref=float(det.y[mid]),
            scan="qmap",
            used_aux_rocking=False,
            unidentified_xi_h=False,
        )
    if det.scan == "specular":
        aux = simulate_measurement(
            surface,
            MeasureParams(**{**m.__dict__, "scan": "rocking", "n_pts": 61, "noise": 0.0}),
        )
        return FitLine(
            qpar=np.abs(aux.qpar),
            intensity=np.asarray(aux.intensity, dtype=float),
            qz_ref=aux.qz_ref,
            scan="specular",
            used_aux_rocking=True,
            unidentified_xi_h=True,
        )
    return FitLine(
        qpar=np.abs(det.qpar),
        intensity=np.asarray(det.intensity, dtype=float),
        qz_ref=det.qz_ref,
        scan=det.scan,
        used_aux_rocking=False,
        unidentified_xi_h=False,
    )


def rebuild_from_C(C_of_R, N: int, dx: float, seed: int):
    """Random-phase surface with the same C(R). Not the original map."""
    rng = np.random.default_rng(int(seed) + 991)
    z, x = generate_field(C_of_R, N, dx, rng)
    return z, x


@dataclass
class AnalysisResult:
    R: np.ndarray
    C_true: np.ndarray
    C_emp: np.ndarray
    C_fit: np.ndarray
    C_inv: np.ndarray
    q: np.ndarray
    P_true: np.ndarray
    P_fit: np.ndarray
    fit: dict
    z_rebuild: np.ndarray
    note: str


def analyse(surface: Surface, qpar, intensity, qz: float) -> AnalysisResult:
    p = surface.params
    Rmax = max(6.0 * p.xi, 0.4 * p.L)
    R = np.linspace(0.0, min(Rmax, 0.45 * p.L), 180)
    C_true = surface.C_of_R(R)
    rs, C_emp_raw = empirical_correlation(surface.z, surface.dx, nbins=32, rmax=R[-1])
    C_emp = np.interp(R, rs, C_emp_raw, left=C_emp_raw[0], right=C_emp_raw[-1])
    fit = fit_self_affine(qpar, intensity, qz, Rmax, p)

    def C_fit_of(r):
        return correlation_function(
            "gaussian" if p.family == "gaussian" else "self-affine",
            r,
            fit["sigma"][0],
            fit["xi"][0],
            fit["h"][0],
        )

    C_fit = C_fit_of(R)
    try:
        C_inv = invert_C_from_sdiff(qpar, intensity, qz, fit["sigma"][0], R, Rmax)
    except Exception:
        C_inv = np.full_like(R, np.nan)
    q = np.linspace(1e-3, 0.25, 80)
    P_true = radial_psd_from_C(q, surface.C_of_R, Rmax)
    P_fit = radial_psd_from_C(q, C_fit_of, Rmax)
    z_reb, _ = rebuild_from_C(C_fit_of, surface.N, surface.dx, seed=p.seed + 3)
    note = (
        "Rebuilt map is a random-phase draw from the fitted C(R). "
        "It is NOT the original surface — scattering measures intensity, not phase."
    )
    return AnalysisResult(
        R=R,
        C_true=C_true,
        C_emp=C_emp,
        C_fit=C_fit,
        C_inv=C_inv,
        q=q,
        P_true=P_true,
        P_fit=P_fit,
        fit=fit,
        z_rebuild=z_reb,
        note=note,
    )
