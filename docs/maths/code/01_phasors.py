#!/usr/bin/env python3
"""Ch.1 — Euler formula and phasor addition. Teaching check, not data."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

theta = np.linspace(0, 2 * np.pi, 400)
e = np.exp(1j * theta)
assert np.allclose(e.real, np.cos(theta))
assert np.allclose(e.imag, np.sin(theta))
assert np.allclose(np.abs(e), 1.0)

# Two unit waves with phase difference dphi
dphi = np.linspace(0, 2 * np.pi, 300)
sum_amp = 1 + np.exp(1j * dphi)
intensity = np.abs(sum_amp) ** 2  # 2 + 2 cos(dphi) = 4 cos²(dphi/2)

fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.5))
axes[0].plot(e.real, e.imag)
axes[0].set_aspect("equal")
axes[0].set_title(r"$e^{i\theta}$ on the unit circle")
axes[0].set_xlabel("Re")
axes[0].set_ylabel("Im")
axes[1].plot(dphi, intensity, "k")
axes[1].plot(dphi, 4 * np.cos(dphi / 2) ** 2, "C1--", label=r"$4\cos^2(\Delta\phi/2)$")
axes[1].set_xlabel(r"phase difference $\Delta\phi$")
axes[1].set_ylabel(r"$|1+e^{i\Delta\phi}|^2$")
axes[1].legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "01_phasors.png", dpi=130)
print("Euler identity: OK")
print("saved", OUT / "01_phasors.png")
