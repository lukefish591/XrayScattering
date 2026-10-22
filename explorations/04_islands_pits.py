#!/usr/bin/env python3
"""Islands/pits: coverage φ, height Δ, size R, spacing d, coherence.

Toys using disk form factor and an exclusion-hole S(q∥). Not Wu (13).
Not the user's film.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from scipy.special import j0

from _common import disk_form_factor, save, s_hard_disk_hole, style

style()
rng = np.random.default_rng(3)


def place_disks(L, radius, d_min, n_try=4000):
    pts = []
    for _ in range(n_try):
        p = rng.uniform(0, L, size=2)
        if all(np.hypot(*(p - q)) >= d_min for q in pts):
            pts.append(p)
    return np.array(pts) if pts else np.zeros((0, 2))


def height_map(L, N, pts, radius, delta):
    x = np.linspace(0, L, N)
    X, Y = np.meshgrid(x, x, indexing="ij")
    z = np.zeros((N, N))
    for px, py in pts:
        z += ((X - px) ** 2 + (Y - py) ** 2 <= radius**2).astype(float)
    z = np.clip(z, 0, 1) * delta
    phi = float((z != 0).mean())
    return z, x, phi


# --- real-space coverage ---
L, Npix = 800.0, 256  # Å
radius, d_min, delta = 40.0, 110.0, 12.0
pts = place_disks(L, radius, d_min)
z, x, phi_map = height_map(L, Npix, pts, radius, delta)

fig, ax = plt.subplots(figsize=(4.6, 4.2))
im = ax.imshow(z, origin="lower", cmap="cividis", extent=[0, L, 0, L])
ax.set_xlabel("x (Å)")
ax.set_ylabel("y (Å)")
ax.set_title(fr"Toy islands Δ={delta:.0f} Å, R={radius:.0f} Å, φ≈{phi_map:.2f}")
ax.grid(False)
fig.colorbar(im, ax=ax, fraction=0.046, label="z (Å)")
save(fig, "04_island_map.png")

# --- φ and Δ along qz (specular vs diffuse, |f|~1) ---
qz = np.linspace(0.02, 0.45, 400)
phis = [0.1, 0.3, 0.5]
deltas = [8.0, 12.0, 20.0]
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7))
for phi in phis:
    spec = 1.0 - 4 * phi * (1 - phi) * np.sin(qz * 12.0 / 2.0) ** 2
    axes[0].plot(qz, spec, label=fr"φ={phi}, Δ=12 Å")
for dlt in deltas:
    spec = 1.0 - 4 * 0.3 * (1 - 0.3) * np.sin(qz * dlt / 2.0) ** 2
    sin2 = np.sin(qz * dlt / 2.0) ** 2
    axes[1].plot(qz, spec, label=fr"spec Δ={dlt:.0f} Å")
    axes[1].plot(qz, sin2, "--", label=fr"sin²(qz Δ/2) Δ={dlt:.0f} Å")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel(r"$1-4\phi(1-\phi)\sin^2(q_z\Delta/2)$")
axes[0].set_title("Specular vs coverage")
axes[0].legend()
axes[1].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[1].set_ylabel("scaled")
axes[1].set_title("Spec dips where diffuse peaks")
axes[1].legend(fontsize=7)
fig.suptitle("Physica (10)–(11) toys — period 2π/Δ", fontsize=9)
save(fig, "04_phi_delta_qz.png")

# --- size R and spacing d in q∥ ---
q = np.linspace(0.001, 0.25, 400)
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7))
for Risl in (20.0, 40.0, 70.0):
    ff = disk_form_factor(q, Risl) ** 2
    axes[0].semilogy(q, np.maximum(ff, 1e-6), label=fr"R={Risl:.0f} Å")
axes[0].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
axes[0].set_ylabel(r"$|f|^2$ (disk)")
axes[0].set_title("Form factor: larger islands → narrower peak")
axes[0].legend()

for d in (80.0, 120.0, 180.0):
    rho = 0.35 / (np.pi * d**2)  # keeps S(0)>0; not a fitted packing
    S = s_hard_disk_hole(q, d, rho)
    axes[1].plot(q, S, label=fr"d={d:.0f} Å")
    axes[1].axvline(2 * np.pi / d, color="0.7", lw=0.6)
axes[1].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
axes[1].set_ylabel("S(q∥) exclusion-hole toy")
axes[1].set_title("Grey lines: 2π/d")
axes[1].legend()
fig.suptitle("In-plane: size vs neighbour spacing (illustrative)", fontsize=9)
save(fig, "04_form_and_S.png")

# --- coherence: damp (g-1) ---
d = 120.0
rho = 0.35 / (np.pi * d**2)
r = np.linspace(0.0, 2000.0, 2500)
g_m1 = np.where(r < d, -1.0, 0.0)
fig, ax = plt.subplots(figsize=(6.4, 3.6))
for xi_coh, lab in [(np.inf, "ξ_coh ≫ d (side peak ok)"),
                    (400.0, "ξ_coh = 400 Å"),
                    (80.0, "ξ_coh = 80 Å ≪ d")]:
    win = np.ones_like(r) if np.isinf(xi_coh) else np.exp(-r / xi_coh)
    S = []
    for qq in q:
        S.append(1.0 + 2 * np.pi * rho * np.trapezoid(r * g_m1 * win * j0(qq * r), r))
    ax.plot(q, S, label=lab)
ax.axvline(2 * np.pi / d, color="0.7", lw=0.7)
ax.set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
ax.set_ylabel("S(q∥)")
ax.set_title("Coherence window kills neighbour peaks if ξ_coh ≪ d")
ax.legend(fontsize=8)
save(fig, "04_coherence.png")

print("n islands", len(pts), "phi_map", phi_map)
print("04 done")
