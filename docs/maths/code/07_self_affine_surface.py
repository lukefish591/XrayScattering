#!/usr/bin/env python3
"""Ch.5 — synthesise a field with C(R)=σ² exp[−(R/ξ)^{2h}], recover C, Born kernel."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j0

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(2)
N = 256
dx = 2.0
sigma, xi, h = 4.0, 18.0, 0.4
x = (np.arange(N) - N // 2) * dx
X, Y = np.meshgrid(x, x, indexing="ij")
R = np.hypot(X, Y)
C = sigma**2 * np.exp(-((R / xi) ** (2 * h)))
C_wrap = np.fft.ifftshift(C)
P = np.fft.fft2(C_wrap).real
P = np.maximum(P, 0.0)
noise = rng.normal(size=(N, N))
z = np.fft.ifft2(np.fft.fft2(np.fft.ifftshift(noise)) * np.sqrt(P)).real
z *= sigma / (z.std() + 1e-15)

# Radial C_emp
def radial_corr(field, nbins=40, rmax=5 * xi):
    # pair product via FFT: C_hat = ifft(|fft(z)|²)
    z0 = field - field.mean()
    f = np.fft.fft2(z0)
    ac = np.fft.ifft2(np.abs(f) ** 2).real / field.size
    ac = np.fft.fftshift(ac)
    bins = np.linspace(0, rmax, nbins + 1)
    rs = 0.5 * (bins[1:] + bins[:-1])
    vals = np.zeros(nbins)
    counts = np.zeros(nbins)
    for i in range(N):
        for j in range(N):
            rij = np.hypot((i - N // 2) * dx, (j - N // 2) * dx)
            b = np.searchsorted(bins, rij) - 1
            if 0 <= b < nbins:
                vals[b] += ac[i, j]
                counts[b] += 1
    counts = np.maximum(counts, 1)
    return rs, vals / counts

rs, C_emp = radial_corr(z)
C_thy = sigma**2 * np.exp(-((rs / xi) ** (2 * h)))

# Born F(R)=exp(qz² C)-1 Hankel vs from definition at q∥=0: ∫ R dR (e^{qz²C}-1)
qz = 0.08
Rint = np.linspace(0, 6 * xi, 400)
Cint = sigma**2 * np.exp(-((Rint / xi) ** (2 * h)))
s0_thy = np.trapezoid(Rint * (np.exp(qz**2 * Cint) - 1), Rint)
# q∥ scan
qpar = np.linspace(0, 0.25, 35)
s_diff = np.array(
    [np.trapezoid(Rint * j0(q * Rint) * (np.exp(qz**2 * Cint) - 1), Rint) for q in qpar]
)

fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.3))
im = axes[0].imshow(z, cmap="cividis", origin="lower")
axes[0].set_title("toy self-affine height")
axes[0].axis("off")
axes[1].plot(rs, C_emp, "k", label="from map")
axes[1].plot(rs, C_thy, "C1--", label="input C(R)")
axes[1].set_xlabel("R")
axes[1].set_ylabel("C")
axes[1].legend(fontsize=7)
axes[2].semilogy(qpar, np.maximum(s_diff, 1e-18), "k")
axes[2].set_xlabel(r"$q_\parallel$")
axes[2].set_ylabel(r"Hankel of $e^{q_z^2 C}-1$")
axes[2].set_title("Born diffuse kernel")
fig.tight_layout()
fig.savefig(OUT / "07_self_affine.png", dpi=130)
rel = np.max(np.abs(C_emp[rs < 2 * xi] - C_thy[rs < 2 * xi])) / sigma**2
print("C mismatch / σ² (R<2ξ)", float(rel))
print("S_diff(q∥=0) integral", float(s0_thy))
print("saved", OUT / "07_self_affine.png")
assert rel < 0.35, rel
