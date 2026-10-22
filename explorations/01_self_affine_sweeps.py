#!/usr/bin/env python3
"""Self-affine C(R)=σ² exp[-(R/ξ)^{2h}]: sweep σ, ξ, h one at a time.

Illustrative parameters only — not an experimental surface.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from _common import (
    C_self_affine,
    born_s_diff,
    born_s_diff_qz,
    generate_field,
    radial_psd_theory,
    save,
    specular_dw,
    style,
)

style()
rng = np.random.default_rng(7)

BASE = dict(sigma=5.0, xi=40.0, h=0.5)  # Å, Å, —
N, dx = 192, 2.0
Rmax = 25.0 * 80.0
R = np.linspace(0.0, 400.0, 800)
qpar = np.linspace(0.0, 0.25, 80)
qz_cut = 0.08
qz = np.linspace(0.03, 0.25, 80)

SWEEPS = {
    "sigma": [("σ = 2 Å", {**BASE, "sigma": 2.0}),
             ("σ = 5 Å (base)", BASE),
             ("σ = 10 Å", {**BASE, "sigma": 10.0})],
    "xi": [("ξ = 20 Å", {**BASE, "xi": 20.0}),
          ("ξ = 40 Å (base)", BASE),
          ("ξ = 80 Å", {**BASE, "xi": 80.0})],
    "h": [("h = 0.2 jagged", {**BASE, "h": 0.2}),
         ("h = 0.5 (base)", BASE),
         ("h = 0.8 rolling", {**BASE, "h": 0.8})],
}


def Cfun(p):
    return lambda r: C_self_affine(r, p["sigma"], p["xi"], p["h"])


def panel_surfaces(key, items, fname):
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.2), layout="constrained")
    for ax, (lab, p) in zip(axes, items):
        z, x = generate_field(Cfun(p), N, dx, rng)
        extent = [x[0], x[-1], x[0], x[-1]]
        im = ax.imshow(z, origin="lower", cmap="cividis", extent=extent,
                       vmin=-3 * BASE["sigma"], vmax=3 * BASE["sigma"])
        ax.set_title(lab)
        ax.set_xlabel("x (Å)")
        ax.set_ylabel("y (Å)")
        ax.grid(False)
    fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02, label="z (Å)")
    fig.suptitle("Illustrative self-affine height maps (same colour scale)", fontsize=10)
    save(fig, fname)


def panel_stats(key, items, fname):
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.6), layout="constrained")
    axC, axg, axP, axS = axes.ravel()
    for lab, p in items:
        Cf = Cfun(p)
        C = Cf(R)
        g = 2 * p["sigma"] ** 2 - 2 * C
        axC.plot(R, C, label=lab)
        axg.plot(R, g, label=lab)
        P = radial_psd_theory(qpar[1:], Cf, Rmax)
        axP.loglog(qpar[1:], np.maximum(P, 1e-8 * np.max(P)), label=lab)
        s, _ = born_s_diff(qpar, qz_cut, Cf, Rmax)
        axS.semilogy(qpar, np.maximum(s, 1e-8 * np.max(np.abs(s))), label=lab)
    axC.set_xlabel("R (Å)")
    axC.set_ylabel("C(R) (Å²)")
    axC.set_title("Height–height C(R)")
    axg.set_xlabel("R (Å)")
    axg.set_ylabel("g(R) (Å²)")
    axg.set_title("g(R)=2σ²−2C")
    axP.set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
    axP.set_ylabel(r"$P(q_\parallel)$ (arb.)")
    axP.set_title("Radial PSD = Hankel of C")
    axS.set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
    axS.set_ylabel(r"$S_\mathrm{diff}$ (arb.)")
    axS.set_title(fr"Born diffuse at $q_z$={qz_cut} Å$^{{-1}}$")
    for ax in axes.ravel():
        ax.legend()
    fig.suptitle(f"Sweep {key} — shapes only, not measured data", fontsize=10)
    save(fig, fname)


def panel_qz(items, fname):
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6))
    for lab, p in items:
        Cf = Cfun(p)
        s, _ = born_s_diff_qz(qz, Cf, Rmax)
        axes[0].semilogy(qz, np.maximum(s, 1e-18), label=lab)
        axes[1].semilogy(qz, specular_dw(qz, p["sigma"]), label=lab)
    axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
    axes[0].set_ylabel(r"$S_\mathrm{diff}(q_\parallel=0)$ (arb.)")
    axes[0].set_title("Diffuse vs $q_z$")
    axes[1].set_xlabel(r"$q_z$ (Å$^{-1}$)")
    axes[1].set_ylabel(r"$e^{-q_z^2\sigma^2}$")
    axes[1].set_title("Born specular reduction")
    for ax in axes:
        ax.legend()
    fig.suptitle("Same σ,ξ,h sweeps — illustrative", fontsize=10)
    save(fig, fname)


for key, items in SWEEPS.items():
    panel_surfaces(key, items, f"01_surfaces_{key}.png")
    panel_stats(key, items, f"01_stats_{key}.png")

panel_qz(SWEEPS["sigma"], "01_qz_sigma.png")
panel_qz(SWEEPS["h"], "01_qz_h.png")
print("01 done")
