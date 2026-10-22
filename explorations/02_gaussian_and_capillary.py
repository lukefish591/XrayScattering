#!/usr/bin/env python3
"""Gaussian C(R) (h=1) vs self-affine h=0.5 vs capillary/log with IR cutoff.

Illustrative — not a liquid or solid sample.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from _common import (
    C_capillary,
    C_gaussian,
    C_self_affine,
    born_s_diff,
    generate_field,
    radial_psd_theory,
    save,
    style,
)

style()
rng = np.random.default_rng(11)

sigma, xi, h = 5.0, 40.0, 0.5
B, xi_ir, a_uv = 8.0, 80.0, 1.0  # Å², Å, Å
N, dx = 192, 2.0
Rmax = 500.0
R = np.linspace(0.0, Rmax, 900)
qpar = np.linspace(0.0, 0.35, 80)
qz_cut = 0.08

C_cap, sig2_cap = C_capillary(R, B, xi_ir, a_uv)
# wrap C_capillary for arrays used as C_of_R(Rgrid)


def cap_of(r):
    C, _ = C_capillary(r, B, xi_ir, a_uv)
    return C


cases = [
    (f"self-affine h={h}, ξ={xi:.0f} Å, σ={sigma:.0f} Å",
     lambda r: C_self_affine(r, sigma, xi, h)),
    (f"Gaussian (h=1), ξ={xi:.0f} Å, σ={sigma:.0f} Å",
     lambda r: C_gaussian(r, sigma, xi)),
    (f"capillary/log, B={B:.0f} Å², ξ_IR={xi_ir:.0f} Å",
     cap_of),
]

fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.2), layout="constrained")
for ax, (lab, Cf) in zip(axes, cases):
    z, x = generate_field(Cf, N, dx, rng)
    extent = [x[0], x[-1], x[0], x[-1]]
    im = ax.imshow(z, origin="lower", cmap="cividis", extent=extent)
    ax.set_title(lab, fontsize=8)
    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.grid(False)
fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02, label="z (Å)")
fig.suptitle("Three correlation families (illustrative maps)", fontsize=10)
save(fig, "02_three_families_surfaces.png")

fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.6), layout="constrained")
for lab, Cf in cases:
    C = Cf(R)
    sigma2 = float(np.asarray(C).ravel()[0])
    axes[0].plot(R, C, label=lab)
    axes[1].loglog(qpar[1:], radial_psd_theory(qpar[1:], Cf, Rmax), label=lab)
    s, _ = born_s_diff(qpar, qz_cut, Cf, Rmax)
    axes[2].semilogy(qpar, np.maximum(s, 1e-18), label=lab)
axes[0].set_xlabel("R (Å)")
axes[0].set_ylabel("C(R) (Å²)")
axes[0].set_title("C(R)")
axes[1].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
axes[1].set_ylabel("P (arb.)")
axes[1].set_title("Radial PSD")
axes[2].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
axes[2].set_ylabel(r"$S_\mathrm{diff}$ (arb.)")
axes[2].set_title(fr"Born diffuse, $q_z$={qz_cut} Å$^{{-1}}$")
for ax in axes:
    ax.legend(fontsize=6)
fig.suptitle("Without an IR cutoff a log C(R) never saturates; here ξ_IR restores C(∞)=0", fontsize=9)
save(fig, "02_three_families_stats.png")

print("capillary σ_eff Å", float(np.sqrt(sig2_cap)))
print("02 done")
