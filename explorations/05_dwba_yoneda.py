#!/usr/bin/env python3
"""DWBA-style |T(α)T(β)|² wings on a Born S_diff kernel.

Optics: PRB Sec. V Pyrex n (illustration). Not the user's sample.
S_diff from a self-affine C(R) at the vacuum q (in-medium q_z' omitted except a note).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from _common import C_self_affine, born_s_diff, fresnel_rt, save, style

style()

delta, beta = 6.3e-6, 8.5e-8
n = 1.0 - delta + 1j * beta
theta_c = np.sqrt(2 * delta)
lam = 1.46  # Å
k = 2.0 * np.pi / lam

sigma, xi, h = 5.0, 40.0, 0.5
Rmax = 6.0 * xi
Cf = lambda r: C_self_affine(r, sigma, xi, h)

# Rocking at fixed 2θ = 1.2° so α=θ_c and β=θ_c both sit on the cut
two_theta = np.deg2rad(1.2)
off = np.deg2rad(np.linspace(-0.55, 0.55, 401))
alpha = two_theta / 2 + off
beta_a = two_theta / 2 - off
ok = (alpha > np.deg2rad(0.04)) & (beta_a > np.deg2rad(0.04))
alpha, beta_a = alpha[ok], beta_a[ok]
qx = k * (np.cos(beta_a) - np.cos(alpha))
qz = k * (np.sin(alpha) + np.sin(beta_a))
_, T_a, _ = fresnel_rt(alpha, n, k0=1.0)
_, T_b, _ = fresnel_rt(beta_a, n, k0=1.0)
yoneda = np.abs(T_a) ** 2 * np.abs(T_b) ** 2

s_born = []
for qxi, qzi in zip(qx, qz):
    val, _ = born_s_diff(np.array([abs(qxi)]), float(qzi), Cf, Rmax)
    s_born.append(val[0])
s_born = np.maximum(np.array(s_born), 1e-30)
i_dwba = yoneda * s_born

fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.5))
axes[0].plot(np.rad2deg(alpha), yoneda, "k")
axes[0].axvline(np.rad2deg(theta_c), color="C3", ls="--",
               label=fr"α=θ_c≈{np.rad2deg(theta_c):.2f}°")
axes[0].axvline(np.rad2deg(two_theta - theta_c), color="C1", ls=":",
               label="β=θ_c")
axes[0].set_xlabel("α (deg)  [β = 2θ − α]")
axes[0].set_ylabel(r"$|T(\alpha)T(\beta)|^2$")
axes[0].set_title("Fresnel |T|²|T|²")
axes[0].legend(fontsize=7)
axes[1].plot(np.rad2deg(alpha), s_born / s_born.max(), "k")
axes[1].set_xlabel("α (deg)")
axes[1].set_ylabel(r"Born $S_\mathrm{diff}$ (scaled)")
axes[1].set_title("Born kernel (almost flat on this rock)")
axes[2].semilogy(np.rad2deg(alpha), i_dwba, "k")
axes[2].axvline(np.rad2deg(theta_c), color="C3", ls="--")
axes[2].axvline(np.rad2deg(two_theta - theta_c), color="C1", ls=":")
axes[2].set_xlabel("α (deg)")
axes[2].set_ylabel("DWBA-style I (arb.)")
axes[2].set_title("Product: Yoneda wings")
fig.suptitle("Toy 2θ=1.2° rock, Pyrex n from PRB Sec. V — not your sample", fontsize=9)
save(fig, "05_dwba_rocking.png")

# |T(α)|² vs α for context
al = np.deg2rad(np.linspace(0.02, 0.8, 400))
_, T, _ = fresnel_rt(al, n)
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.plot(np.rad2deg(al), np.abs(T) ** 2, "k")
ax.axvline(np.rad2deg(theta_c), color="C3", ls="--")
ax.set_xlabel("α (deg)")
ax.set_ylabel(r"$|T|^2$")
ax.set_title("|T| peaks near θ_c (Yoneda condition)")
save(fig, "05_transmission.png")
print("theta_c deg", float(np.rad2deg(theta_c)))
print("05 done")
