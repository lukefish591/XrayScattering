"""Diagnostic scores are C(R) / (σ, ξ, h), not z RMSE. Specular is unidentified."""

from __future__ import annotations

import json
import math

import numpy as np

from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import generate_surface
from xray_scattering.sim.sweep import (
    plot_report,
    run_diagnostic_sweep,
    score_locked_surface,
)


def _surface():
    return generate_surface(SurfaceParams(N=48, L=240.0, seed=1, family="self-affine"))


def test_noiseless_rocking_recovers_small_errors():
    surf = _surface()
    m = MeasureParams(
        scan="rocking",
        n_pts=61,
        noise=0.0,
        dq=0.0,
        xi_coh=2000.0,
        pixel_dq=0.0,
        rock_range_deg=0.6,
        alpha_deg=0.55,
        footprint=False,
        use_dwba=False,
    )
    pt = score_locked_surface(surf, m)
    assert not pt.unidentified_xi_h
    assert pt.rel_sigma < 0.12
    assert pt.rel_xi < 0.15
    assert pt.rel_h < 0.12
    assert pt.rms_logC < 0.25


def test_degrading_coherence_increases_xi_error():
    surf = _surface()
    good = MeasureParams(
        scan="rocking",
        n_pts=51,
        noise=0.0,
        dq=0.0,
        xi_coh=2000.0,
        pixel_dq=0.0,
        footprint=False,
    )
    bad = MeasureParams(**{**good.__dict__, "xi_coh": 80.0})
    e_good = score_locked_surface(surf, good)
    e_bad = score_locked_surface(surf, bad)
    assert e_bad.rel_xi > e_good.rel_xi
    assert e_bad.rel_xi > 0.10


def test_adding_noise_increases_xi_or_h_error():
    surf = _surface()
    good = MeasureParams(
        scan="rocking",
        n_pts=51,
        noise=0.0,
        dq=0.0,
        xi_coh=2000.0,
        seed=4,
        footprint=False,
    )
    noisy = MeasureParams(**{**good.__dict__, "noise": 1.0})
    e_good = score_locked_surface(surf, good)
    e_noisy = score_locked_surface(surf, noisy)
    assert (e_noisy.rel_xi > e_good.rel_xi) or (e_noisy.rel_h > e_good.rel_h)
    assert e_noisy.rms_logC >= e_good.rms_logC * 0.9


def test_specular_flagged_unidentified():
    surf = _surface()
    m = MeasureParams(scan="specular", n_pts=41, noise=0.0, dq=0.0, xi_coh=2000.0)
    pt = score_locked_surface(surf, m)
    assert pt.unidentified_xi_h
    assert pt.used_aux_rocking
    assert math.isnan(pt.rel_xi) and math.isnan(pt.rel_h)
    assert "cheat" in pt.note.lower()
    assert "unidentified" in pt.note.lower()


def test_run_diagnostic_sweep_marks_specular_and_limiter():
    surf = _surface()
    m = MeasureParams(
        scan="rocking", n_pts=41, noise=0.0, dq=0.0, xi_coh=600.0, footprint=False
    )
    rep = run_diagnostic_sweep(
        surf,
        measure=m,
        n_grid=5,
        axes=("xi_coh", "noise", "scan"),
        knee_thresh=0.10,
        hold_ideal=True,
    )
    scan_ax = next(a for a in rep.axes if a.axis == "scan")
    spec = next(p for p in scan_ax.points if p.value == "specular")
    assert spec.unidentified_xi_h
    assert math.isnan(spec.rel_xi)
    coh = next(a for a in rep.axes if a.axis == "xi_coh")
    assert coh.points[0].rel_xi <= coh.points[-1].rel_xi + 0.05
    assert rep.limiter in ("xi_coh", "noise", "scan")
    assert "illustrative" in rep.summary.lower()
    payload = rep.to_json()
    assert payload["not_z_rmse"] and payload["not_experimental_data"]
    json.dumps(payload)
    fig = plot_report(rep)
    assert fig is not None
    import matplotlib.pyplot as plt

    plt.close(fig)


def test_sweep_cli_json(tmp_path):
    from xray_scattering.sim.sweep import main

    rc = main(["--n-grid", "4", "--N", "48", "--axes", "scan", "--json"])
    assert rc == 0
