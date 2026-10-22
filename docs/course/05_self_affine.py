#!/usr/bin/env python3
"""Module 5 — self-affine C(R) and Born diffuse. TEACHING TOY, PRB (2.25)–(2.28b)."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j0

from toy import PLOTS, ensure_plots

ensure_plots()

# Toy parameters (Å). PRB Sec. V fit was σ=7.6 Å, h=0.2, ξ=7000 Å — too large a ξ
# for a quick integral demo, so ξ is reduced. USER: your (σ, h, ξ) are unknown.
sigma = 5.0
xi = 250.0
hs = (0.2, 0.5, 0.9)

R = np.linspace(0, 5 * xi, 800)


def C(R, h, sigma=sigma, xi=xi):
    return sigma**2 * np.exp(-((R / xi) ** (2 * h)))


qz = 0.12  # Å^-1, toy
qpar = np.linspace(0, 0.08, 80)


def s_diff(qpar, h):
    # PRB (2.28b): ∫ R dR J0(q∥ R) (exp(qz² C) - 1), times qz^{-2} e^{-qz² σ²}
    Rint = np.linspace(0.0, 12 * xi, 2500)
    CR = C(Rint, h)
    kernel = np.exp(qz**2 * CR) - 1.0
    out = np.empty_like(qpar)
    for i, q in enumerate(qpar):
        out[i] = np.trapezoid(Rint * j0(q * Rint) * kernel, Rint)
    return (np.exp(-(qz**2) * sigma**2) / qz**2) * out


fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7))
for h in hs:
    axes[0].plot(R, C(R, h) / sigma**2, label=f"h={h}")
axes[0].set_xlabel("R (Å)")
axes[0].set_ylabel(r"$C(R)/\sigma^2$")
axes[0].set_title("Height–height: small h = jagged")
axes[0].legend(fontsize=8)
for h in hs:
    axes[1].semilogy(qpar, np.maximum(s_diff(qpar, h), 1e-18), label=f"h={h}")
axes[1].set_xlabel(r"$q_\parallel$ (Å$^{-1}$) at fixed $q_z$")
axes[1].set_ylabel("toy $S_\\mathrm{diff}$ (arb.)")
axes[1].set_title("Born diffuse (toy ξ=250 Å)")
axes[1].legend(fontsize=8)
fig.suptitle("Toy self-affine roughness — not a fit to your surface", fontsize=9)
fig.tight_layout()
fig.savefig(PLOTS / "05_self_affine.png", dpi=140)
print("saved", PLOTS / "05_self_affine.png")
print("C(0) should be σ^2 =", sigma**2, "got", C(0, 0.5))
print("C(ξ)/σ^2 for h=0.5 =", C(xi, 0.5) / sigma**2, "(expect 1/e)")
