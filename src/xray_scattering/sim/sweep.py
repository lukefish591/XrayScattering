"""Diagnostic sweeps of measurement knobs vs recovered C(R) and (σ, ξ, h).

Scattering does not recover z(x,y). Scores are relative errors on the
self-affine parameters and RMS log C(R), not RMSE of a random-phase map.
Illustrative; not experimental data.

Headless::

    python -m xray_scattering.sim.sweep
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field

import numpy as np

from xray_scattering.sim.analysis import (
    fit_line_from_measurement,
    fit_self_affine,
)
from xray_scattering.sim.correlations import correlation_function
from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import Surface, generate_surface

# Sweeps run from the “good” end toward the degraded end.
AXES = ("xi_coh", "dq", "noise", "alpha_deg", "scan", "rock_range_deg")

IDEAL_HOLD = dict(
    noise=0.0,
    dq=0.0,
    xi_coh=2000.0,
    scan="rocking",
    pixel_dq=0.0,
    use_dwba=False,
    footprint=False,  # fitter does not model 1/sinα; ideal hold turns it off
)


@dataclass
class SweepPoint:
    axis: str
    value: float | str
    rel_sigma: float
    rel_xi: float
    rel_h: float
    rms_logC: float
    rms_C: float
    unidentified_xi_h: bool
    used_aux_rocking: bool
    note: str = ""


@dataclass
class AxisSweep:
    axis: str
    label: str
    unit: str
    current: float | str
    knee: float | str | None
    past_knee: bool
    points: list[SweepPoint] = field(default_factory=list)


@dataclass
class DiagnosticReport:
    illustrative: bool = True
    knee_thresh: float = 0.10
    hold_ideal: bool = False
    limiter: str = ""
    summary: str = ""
    axes: list[AxisSweep] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "illustrative": True,
            "not_experimental_data": True,
            "not_z_rmse": True,
            "knee_thresh": self.knee_thresh,
            "hold_ideal": self.hold_ideal,
            "limiter": self.limiter,
            "summary": self.summary,
            "axes": [
                {
                    "axis": a.axis,
                    "label": a.label,
                    "unit": a.unit,
                    "current": a.current,
                    "knee": a.knee,
                    "past_knee": a.past_knee,
                    "points": [asdict(p) for p in a.points],
                }
                for a in self.axes
            ],
        }


def _rel(hat: float, true: float) -> float:
    den = max(abs(true), 1e-12)
    return float(abs(hat - true) / den)


def _rms_logC(C_true, C_fit) -> tuple[float, float]:
    a = np.clip(np.asarray(C_true, dtype=float), 1e-12, None)
    b = np.clip(np.asarray(C_fit, dtype=float), 1e-12, None)
    rms_log = float(np.sqrt(np.mean((np.log(b) - np.log(a)) ** 2)))
    rms = float(np.sqrt(np.mean((b - a) ** 2))) / max(float(np.max(a)), 1e-12)
    return rms_log, rms


def score_locked_surface(
    surface: Surface,
    measure: MeasureParams,
) -> SweepPoint:
    """Forward model + fit on a locked surface. Does not rebuild z(x,y)."""
    line = fit_line_from_measurement(surface, measure)
    p = surface.params
    Rmax = max(6.0 * p.xi, 0.4 * p.L)
    R = np.linspace(0.0, min(Rmax, 0.45 * p.L), 120)
    C_true = surface.C_of_R(R)
    if line.unidentified_xi_h:
        # Aux rocking is recorded as a cheat, not as recovered ξ, h.
        cheat = fit_self_affine(line.qpar, line.intensity, line.qz_ref, Rmax, p)
        C_cheat = correlation_function(
            "gaussian" if p.family == "gaussian" else "self-affine",
            R,
            cheat["sigma"][0],
            cheat["xi"][0],
            cheat["h"][0],
        )
        rms_log, rms = _rms_logC(C_true, C_cheat)
        return SweepPoint(
            axis="",
            value="",
            rel_sigma=_rel(cheat["sigma"][0], p.sigma),
            rel_xi=float("nan"),
            rel_h=float("nan"),
            rms_logC=rms_log,
            rms_C=rms,
            unidentified_xi_h=True,
            used_aux_rocking=True,
            note=(
                "Specular has no q∥; ξ and h are unidentified. "
                "Auxiliary noiseless rocking is a cheat, not a recovery. "
                f"(cheat |Δξ|/ξ={_rel(cheat['xi'][0], p.xi):.2f})"
            ),
        )
    fit = fit_self_affine(line.qpar, line.intensity, line.qz_ref, Rmax, p)
    C_fit = correlation_function(
        "gaussian" if p.family == "gaussian" else "self-affine",
        R,
        fit["sigma"][0],
        fit["xi"][0],
        fit["h"][0],
    )
    rms_log, rms = _rms_logC(C_true, C_fit)
    return SweepPoint(
        axis="",
        value="",
        rel_sigma=_rel(fit["sigma"][0], p.sigma),
        rel_xi=_rel(fit["xi"][0], p.xi),
        rel_h=abs(fit["h"][0] - p.h),
        rms_logC=rms_log,
        rms_C=rms,
        unidentified_xi_h=False,
        used_aux_rocking=line.used_aux_rocking,
        note="",
    )


def _grid(axis: str, n: int):
    n = max(4, int(n))
    if axis == "xi_coh":
        # high (good) → low (bad)
        return list(np.logspace(np.log10(2000.0), np.log10(80.0), n))
    if axis == "dq":
        return list(np.linspace(0.0, 0.02, n))
    if axis == "noise":
        return list(np.linspace(0.0, 1.0, n))
    if axis == "alpha_deg":
        return list(np.linspace(1.2, 0.15, n))
    if axis == "rock_range_deg":
        return list(np.linspace(0.8, 0.15, n))
    if axis == "scan":
        return ["rocking", "qmap", "specular"]
    raise ValueError(axis)


def _labels(axis: str) -> tuple[str, str]:
    return {
        "xi_coh": ("coherence length ξ_coh", "Å"),
        "dq": ("resolution Δq", "Å⁻¹"),
        "noise": ("noise mix", ""),
        "alpha_deg": ("incidence α", "deg"),
        "rock_range_deg": ("rocking q-range", "deg"),
        "scan": ("scan type", ""),
    }[axis]


def _hold_measure(base: MeasureParams, hold_ideal: bool) -> MeasureParams:
    if not hold_ideal:
        return base
    d = {**base.__dict__, **IDEAL_HOLD}
    return MeasureParams(**d)


def _set_axis(m: MeasureParams, axis: str, value) -> MeasureParams:
    d = dict(m.__dict__)
    d[axis] = value
    return MeasureParams(**d)


def _knee(points: list[SweepPoint], thresh: float, axis: str):
    """First point, walking from the good end, where |Δξ|/ξ exceeds thresh."""
    if axis == "scan":
        return None
    for p in points:
        if p.unidentified_xi_h:
            continue
        if np.isfinite(p.rel_xi) and p.rel_xi > thresh:
            return p.value
    return None


def _numeric(v) -> float | None:
    if isinstance(v, (int, float)) and np.isfinite(v):
        return float(v)
    return None


def _pretty(v):
    if v is None or isinstance(v, str):
        return v
    return float(f"{float(v):.4g}")


def _rel_at_current(axis: AxisSweep) -> float:
    cur = _numeric(axis.current)
    if cur is None:
        for p in axis.points:
            if p.value == axis.current:
                return p.rel_xi if np.isfinite(p.rel_xi) else 1.0
        return 0.0
    xs, ys = [], []
    for p in axis.points:
        xv = _numeric(p.value)
        if xv is None or not np.isfinite(p.rel_xi):
            continue
        xs.append(xv)
        ys.append(p.rel_xi)
    if not xs:
        return 0.0
    return float(np.interp(cur, xs[::-1] if xs[0] > xs[-1] else xs, ys[::-1] if xs[0] > xs[-1] else ys))


def _limiter(axes: list[AxisSweep], current_scan: str, thresh: float) -> tuple[str, str]:
    if current_scan == "specular":
        return (
            "scan",
            "Limiter: scan type is specular — ξ and h are unidentified "
            "(no q∥). The live table’s auxiliary rocking kernel is a cheat, "
            "not a recovery. Illustrative.",
        )
    ranked = []
    for a in axes:
        if a.axis == "scan":
            continue
        err = _rel_at_current(a)
        ranked.append((err, a))
    ranked.sort(key=lambda t: -t[0])
    if not ranked:
        return ("", "No limiter (no continuous axes). Illustrative.")
    err, a = ranked[0]
    if a.past_knee:
        msg = (
            f"Limiter: {a.label} is past its knee "
            f"(ξ relative error > {100 * thresh:.0f}% near {_pretty(a.knee)} {a.unit}). "
            "Illustrative."
        )
    elif a.knee is not None:
        msg = (
            f"Limiter: {a.label} is closest to its knee "
            f"(knee ≈ {_pretty(a.knee)} {a.unit}; |Δξ|/ξ ≈ {100 * err:.1f}% at the current setting). "
            "Illustrative."
        )
    else:
        msg = (
            f"Limiter: {a.label} has the largest |Δξ|/ξ at the current setting "
            f"({100 * err:.1f}%), but no axis crossed the "
            f"{100 * thresh:.0f}% knee on this grid. Illustrative."
        )
    return a.axis, msg


def run_diagnostic_sweep(
    surface: Surface | None = None,
    surface_params: SurfaceParams | None = None,
    measure: MeasureParams | None = None,
    *,
    hold_ideal: bool = False,
    knee_thresh: float = 0.10,
    n_grid: int = 10,
    axes: tuple[str, ...] = AXES,
    progress=None,
) -> DiagnosticReport:
    """Lock the surface; sweep one measurement knob at a time."""
    if surface is None:
        sp = surface_params or SurfaceParams()
        surface = generate_surface(sp)
    base = measure or MeasureParams()
    held = _hold_measure(base, hold_ideal)
    jobs = []
    for axis in axes:
        grid = _grid(axis, n_grid)
        for val in grid:
            jobs.append((axis, val))
    n_jobs = len(jobs)
    grouped: dict[str, list[SweepPoint]] = {a: [] for a in axes}
    for i, (axis, val) in enumerate(jobs):
        if progress is not None:
            progress(i, n_jobs, axis, val)
        mp = _set_axis(held, axis, val)
        pt = score_locked_surface(surface, mp)
        pt.axis = axis
        pt.value = val if isinstance(val, str) else float(val)
        grouped[axis].append(pt)
    if progress is not None:
        progress(n_jobs, n_jobs, "done", "")

    out_axes: list[AxisSweep] = []
    for axis in axes:
        label, unit = _labels(axis)
        pts = grouped[axis]
        cur = getattr(base, axis)
        knee = _knee(pts, knee_thresh, axis)
        past = False
        cv = _numeric(cur)
        kv = _numeric(knee)
        if cv is not None and kv is not None:
            # grids go good → bad; past knee if current is on the bad side of knee
            first, last = _numeric(pts[0].value), _numeric(pts[-1].value)
            if first is not None and last is not None:
                if last < first:
                    past = cv <= kv + 1e-12
                else:
                    past = cv >= kv - 1e-12
        out_axes.append(
            AxisSweep(
                axis=axis,
                label=label,
                unit=unit,
                current=cur if isinstance(cur, str) else float(cur),
                knee=None if knee is None else (knee if isinstance(knee, str) else _pretty(float(knee))),
                past_knee=past,
                points=pts,
            )
        )
    lim, summary = _limiter(out_axes, str(base.scan), knee_thresh)
    return DiagnosticReport(
        knee_thresh=float(knee_thresh),
        hold_ideal=bool(hold_ideal),
        limiter=lim,
        summary=summary,
        axes=out_axes,
    )


def plot_report(report: DiagnosticReport):
    """One axes-grid of error vs swept parameter. Returns a matplotlib Figure."""
    import matplotlib.pyplot as plt

    cont = [a for a in report.axes if a.axis != "scan"]
    n = len(cont) + (1 if any(a.axis == "scan" for a in report.axes) else 0)
    cols = 2
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(8.8, 3.2 * rows))
    axes = np.atleast_1d(axes).ravel()
    i = 0
    for a in cont:
        ax = axes[i]
        i += 1
        xs = [float(p.value) for p in a.points]
        ax.plot(xs, [p.rel_sigma for p in a.points], "C0-o", ms=3, label=r"$|\hat\sigma-\sigma|/\sigma$")
        ax.plot(xs, [p.rel_xi if np.isfinite(p.rel_xi) else np.nan for p in a.points], "C1-s", ms=3, label=r"$|\hat\xi-\xi|/\xi$")
        ax.plot(xs, [p.rel_h if np.isfinite(p.rel_h) else np.nan for p in a.points], "C2-^", ms=3, label=r"$|\hat h-h|$")
        ax.plot(xs, [p.rms_logC for p in a.points], "k--", lw=1, label=r"RMS $\log C$")
        ax.axhline(report.knee_thresh, color="0.5", ls=":", lw=1)
        cv = _numeric(a.current)
        if cv is not None:
            ax.axvline(cv, color="C3", ls="--", lw=1, label="current")
        kv = _numeric(a.knee)
        if kv is not None:
            ax.axvline(kv, color="C1", ls=":", lw=1.5, label="knee")
        ax.set_xlabel(f"{a.label} ({a.unit})".strip())
        ax.set_ylabel("relative error (illustrative)")
        ax.set_title(a.label, fontsize=9)
        if a.axis == "xi_coh":
            ax.set_xscale("log")
        ax.legend(fontsize=6, loc="best")
        ax.grid(True, alpha=0.25)
    scan_ax = next((a for a in report.axes if a.axis == "scan"), None)
    if scan_ax is not None and i < len(axes):
        ax = axes[i]
        i += 1
        labels = [str(p.value) for p in scan_ax.points]
        xi_e = [p.rel_xi if np.isfinite(p.rel_xi) else 0.0 for p in scan_ax.points]
        colors = ["C3" if p.unidentified_xi_h else "C1" for p in scan_ax.points]
        ax.bar(labels, xi_e, color=colors)
        ax.set_ylabel(r"$|\hat\xi-\xi|/\xi$ (0 if unidentified)")
        ax.set_title("scan type — red = unidentified ξ,h", fontsize=9)
        for p, x in zip(scan_ax.points, labels):
            if p.unidentified_xi_h:
                ax.text(x, 0.02, "unidentified\n(cheat aux\nrocking)", ha="center", va="bottom", fontsize=7)
    for j in range(i, len(axes)):
        axes[j].axis("off")
    fig.suptitle("Diagnostic sweep (illustrative) — not z(x,y) RMSE", fontsize=10)
    fig.tight_layout()
    return fig


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Headless diagnostic sweep (illustrative).")
    p.add_argument("--n-grid", type=int, default=8)
    p.add_argument("--knee", type=float, default=0.10)
    p.add_argument("--hold-ideal", action="store_true")
    p.add_argument("--N", type=int, default=48)
    p.add_argument("--n-pts", type=int, default=41)
    p.add_argument(
        "--axes",
        default=",".join(AXES),
        help="Comma-separated axes: " + ",".join(AXES),
    )
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    axes = tuple(a.strip() for a in args.axes.split(",") if a.strip())
    for a in axes:
        if a not in AXES:
            p.error(f"unknown axis {a!r}; choose from {AXES}")
    sp = SurfaceParams(N=args.N, L=240.0 if args.N <= 64 else 384.0, seed=1)
    mp = MeasureParams(
        scan="rocking",
        n_pts=int(args.n_pts),
        noise=0.0,
        dq=0.0,
        xi_coh=2000.0,
        footprint=False,
    )
    surf = generate_surface(sp)
    rep = run_diagnostic_sweep(
        surf,
        measure=mp,
        hold_ideal=args.hold_ideal,
        knee_thresh=args.knee,
        n_grid=args.n_grid,
        axes=axes,
    )
    if args.json:
        print(json.dumps(rep.to_json(), indent=2))
    else:
        print(rep.summary)
        for a in rep.axes:
            print(f"  {a.axis}: current={a.current} knee={a.knee} past={a.past_knee}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
