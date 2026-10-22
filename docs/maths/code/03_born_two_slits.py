#!/usr/bin/env python3
"""Ch.2 — two point scatterers: |1 + exp(−i q d)|² = 4 cos²(q d / 2)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

d = 12.0  # Å separation along x
q = np.linspace(-1.5, 1.5, 400)
I = np.abs(1 + np.exp(-1j * q * d)) ** 2
I_th = 4 * np.cos(q * d / 2) ** 2
assert np.allclose(I, I_th)

fig, ax = plt.subplots(figsize=(5.8, 3.5))
ax.plot(q, I, "k")
ax.set_xlabel(r"$q_x$ (Å$^{-1}$)")
ax.set_ylabel("Born intensity (arb.)")
ax.set_title(rf"Two points separated by d={d:.0f} Å")
fig.tight_layout()
fig.savefig(OUT / "03_born_two_slits.png", dpi=130)
print("two-slit identity: OK")
print("saved", OUT / "03_born_two_slits.png")
