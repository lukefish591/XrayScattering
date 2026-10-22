#!/usr/bin/env python3
"""Kiessig fringes: film thickness, conformal vs independent roughness.

Born-like two-interface toy (Physica (12) structure). Not a fitted stack.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from _common import save, style

style()

t = 400.0  # Å
rho_f, rho_s = 0.4, 1.0
s1, s2 = 4.0, 6.0
qz = np.linspace(0.04, 0.35, 500)
r1 = np.exp(-0.5 * qz**2 * s1**2)
r2 = np.exp(-0.5 * qz**2 * s2**2)
amp = rho_f * r1 + (rho_s - rho_f) * np.exp(1j * qz * t) * r2
spec = np.abs(amp) ** 2 / qz**4
conf = (rho_f**2 * r1**2 + (rho_s - rho_f) ** 2 * r2**2
        + 2 * rho_f * (rho_s - rho_f) * r1 * r2 * np.cos(qz * t)) / qz**2
indep = (rho_f**2 * r1**2 + (rho_s - rho_f) ** 2 * r2**2) / qz**2

fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7))
axes[0].semilogy(qz, spec / spec.max(), "k")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel("specular (scaled)")
axes[0].set_title(fr"Kiessig period 2π/t, t={t:.0f} Å")
dq = 2 * np.pi / t
for n in range(1, 8):
    qn = 0.04 + n * dq
    if qn < qz[-1]:
        axes[0].axvline(qn, color="0.85", lw=0.6)

axes[1].plot(qz, conf / np.max(conf), "k", label="conformal: fringes, in phase with spec")
axes[1].plot(qz, indep / np.max(indep), "C0--", label="independent: no t-fringes in diffuse")
axes[1].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[1].set_ylabel("diffuse along qz (scaled)")
axes[1].legend(fontsize=7)
fig.suptitle("Toy film on a substrate — not your stack", fontsize=9)
save(fig, "06_kiessig.png")
print("Delta qz", dq)
print("06 done")
