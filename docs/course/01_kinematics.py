#!/usr/bin/env python3
"""Module 1 — q-space kinematics. TEACHING TOY, not experimental data."""

import matplotlib.pyplot as plt
import numpy as np

from toy import K, PLOTS, ensure_plots, q_of

ensure_plots()

# Toy grazing angles (radians). USER: replace with your instrument range when known.
alpha = np.deg2rad(np.linspace(0.05, 2.5, 200))
beta_spec = alpha
qx_s, qz_s = q_of(alpha, beta_spec)

# Longitudinal-ish diffuse: small offset from specular (Physica Fig. 1)
offset = np.deg2rad(0.05)
qx_d, qz_d = q_of(alpha, alpha + offset)

# Rocking at fixed 2θ = 1.5°
two_theta = np.deg2rad(1.5)
off = np.deg2rad(np.linspace(-0.6, 0.6, 200))
a_rock = two_theta / 2 + off
b_rock = two_theta / 2 - off
ok = (a_rock > 0.02) & (b_rock > 0.02)
qx_r, qz_r = q_of(a_rock[ok], b_rock[ok])

fig, ax = plt.subplots(figsize=(6.2, 4.4))
ax.plot(qx_s, qz_s, "k-", lw=2, label="specular ridge (α = β)")
ax.plot(qx_d, qz_d, "C0--", label="longitudinal diffuse (β = α + 0.05°)")
ax.plot(qx_r, qz_r, "C1", label="rocking / transverse (2θ = 1.5°)")
ax.set_xlabel(r"$q_x$ (Å$^{-1}$)")
ax.set_ylabel(r"$q_z$ (Å$^{-1}$)")
ax.set_title("Toy q-space map (k = 2π/1.46 Å from PRB Sec. V wavelength)")
ax.legend(fontsize=8)
ax.axvline(0, color="0.8", lw=0.8)
fig.tight_layout()
fig.savefig(PLOTS / "01_qspace.png", dpi=140)
print("k =", K, "Å^-1")
print("saved", PLOTS / "01_qspace.png")
print("At α=β=0.5°: qx, qz =", q_of(np.deg2rad(0.5), np.deg2rad(0.5)))
