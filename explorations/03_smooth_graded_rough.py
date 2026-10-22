#!/usr/bin/env python3
"""Smooth vs graded (ρ(z) only) vs rough sharp interface.

Graded: no diffuse if the density depends only on z.
Rough sharp: Debye–Waller on specular + Born diffuse from C(R).
Illustrative Born envelopes — not a Parratt fit to data.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from _common import C_self_affine, born_s_diff_qz, save, specular_dw, style

style()

sigma = 6.0  # Å  (roughness OR grade width)
xi, h = 40.0, 0.5
qz = np.linspace(0.04, 0.40, 250)
Rmax = 6.0 * xi

# Smooth sharp: R_F ~ 1/qz^4 in the large-angle Born/Porod limit
rf = 1.0 / qz**4
# Graded error-function profile of rms width σ: extra e^{-qz²σ²} on the
# *amplitude*, so intensity ~ e^{-qz²σ²} / qz^4  (faster than Porod; no diffuse)
# Graded (z-only) intensity falls faster than a rough-sharp Debye–Waller.
graded = np.exp(-2.0 * (qz**2) * sigma**2) * rf
# Rough sharp (Gaussian heights, cutoff): same DW on specular, PLUS diffuse
rough_spec = specular_dw(qz, sigma) * rf
Cf = lambda r: C_self_affine(r, sigma, xi, h)
diff, _ = born_s_diff_qz(qz, Cf, Rmax)
# put diffuse on a comparable arbitrary scale vs specular envelope
diff_plot = np.maximum(diff, 1e-30)
diff_plot = diff_plot * (rough_spec.max() / diff_plot.max()) * 0.15

fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8))
axes[0].semilogy(qz, rf / rf[0], "k", label="smooth sharp (Porod ~ qz^{-4})")
axes[0].semilogy(qz, graded / rf[0], "C0", label=fr"graded ρ(z), width σ={sigma:.0f} Å")
axes[0].semilogy(qz, rough_spec / rf[0], "C3", label=fr"rough sharp specular, σ={sigma:.0f} Å")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel("specular envelope (scaled)")
axes[0].set_title("Specular")
axes[0].legend(fontsize=7)

axes[1].axhline(1e-16, color="k", lw=1, label="smooth: no diffuse")
axes[1].axhline(1e-16, color="C0", ls="--", lw=1, label="graded in z only: no diffuse")
axes[1].semilogy(qz, diff_plot / rf[0], "C3", label="rough sharp: Born S_diff")
axes[1].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[1].set_ylabel("diffuse (scaled, arb.)")
axes[1].set_title(r"Diffuse at $q_\parallel=0$ (toy scale)")
axes[1].legend(fontsize=7)
fig.suptitle("Same σ used as grade width OR as rms roughness — illustration, not data", fontsize=9)
save(fig, "03_smooth_graded_rough.png")

# Sketch ρ(z)
z = np.linspace(-40, 40, 400)
rho_sharp = np.where(z < 0, 1.0, 0.0)
rho_grade = 0.5 * (1.0 - np.tanh(z / (np.sqrt(2) * sigma)))
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.plot(z, rho_sharp, "k", label="sharp interface")
ax.plot(z, rho_grade, "C0", label="graded error-function-like")
ax.set_xlabel("z (Å), outward")
ax.set_ylabel(r"relative density $\rho(z)$")
ax.set_title("Why graded has no diffuse: every (x,y) sees the same ρ(z)")
ax.legend()
save(fig, "03_density_profiles.png")
print("03 done")
