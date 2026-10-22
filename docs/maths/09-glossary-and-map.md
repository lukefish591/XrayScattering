# 9. Glossary and equation map

## Glossary (first-use definitions)

| Symbol | Meaning |
| --- | --- |
| <i>i</i> | √(-1) |
| λ, k<sub>0</sub>=2π/λ | wavelength; vacuum wave number |
| <b>k</b><sub>0</sub>, <b>k</b><sub>1</sub> | incident and scattered wave vectors |
| α, β (or θ<sub>1</sub>,θ<sub>2</sub>) | grazing incidence and exit angles |
| <b>q</b>=<b>k</b><sub>1</sub>-<b>k</b><sub>0</sub> | wave-vector transfer |
| q<sub>z</sub>, <b>q</b><sub>∥</sub>=(q<sub>x</sub>,q<sub>y</sub>) | surface-normal and in-plane parts of <b>q</b> |
| ρ, Δρ | scattering-length / electron-density (contrast) |
| A(<b>q</b>)=ρ̃(<b>q</b>) | Born amplitude |
| z(x,y) | surface height above the mean plane |
| σ=√(⟨z<sup>2</sup>⟩) | rms roughness |
| C(<b>R</b>)=⟨z(<b>R</b>)z(<b>0</b>)⟩ | height–height correlation |
| g(<b>R</b>)=⟨[z(<b>R</b>)-z(<b>0</b>)]<sup>2</sup>⟩=2σ<sup>2</sup>-2C | structure function |
| P(<b>q</b><sub>∥</sub>) | height power spectral density |
| <i>h</i> | Hurst / roughness exponent (0<h<1) |
| <i>ξ</i> | lateral cutoff of C(R) |
| D<sub>s</sub>=3-h | self-affine surface fractal dimension |
| <i>φ</i> | island area coverage |
| <i>Δ</i> | island height or pit depth |
| h(q<sub>z</sub>) | FT of the island height pdf |
| f(<b>q</b><sub>∥</sub>) | island form factor |
| S(<b>q</b><sub>∥</sub>) | in-plane structure factor of centres |
| g<sub>pair</sub>(r) | pair correlation of island centres |
| n=1-δ+iβ | X-ray refractive index |
| θ<sub>c</sub>≈√(2δ) | critical angle for total external reflection |
| R, T | Fresnel reflection and transmission amplitudes |
| q<sub>z</sub>' | q<sub>z</sub> inside the medium |
| ξ<sub>coh</sub> | beam coherence length on the surface |
| R<sub>res</sub> | instrument resolution kernel |
| J<sub>0</sub> | Bessel function of the first kind, order 0 |

## Equation map

```
plane wave  e^{i k·r}
        │
        ▼
phase difference  q = k1 − k0     (ch. 1–2)
        │
        ▼
Born:  A(q) = ∫ ρ(r) e^{-i q·r} d³r = FT[ρ]     (ch. 2)
        │
        ▼
homogeneous bulk + surface z(x,y)
        │
        ▼
A ∝ (Δρ / q_z) ∫ d²R  e^{-i q_z z(R)} e^{-i q∥·R}     (PRB 2.4)
        │
        ├── Gaussian heights ─────────────────────────────┐
        │     <e^{-i qz Δz}> = exp(− qz² g / 2)            │
        │     g = 2σ² − 2C                                 │
        │     S ∝ e^{-qz²σ²} / qz²  × FT[ e^{qz² C} ]      │
        │              │                                   │
        │              ├── 1  →  (2π)² δ(q∥)  specular     │
        │              └── e^{qz² C}−1 → diffuse (J0)      │
        │     C(R)=σ² exp[−(R/ξ)^{2h}]   (self-affine)     │
        │     log g(R) + cutoff   (capillary)              │
        │                                                  │
        └── two-level islands/pits ───────────────────────┤
              <e^{-iqz z}> = (1−φ)+φ h(qz)  → specular     │
              |f|² S(q∥) and |1−h|² = 4 sin²(qz Δ/2)       │
              S(q∥)=1+ρ FT[g_pair−1]                       │
                                                           ▼
                              × |T(α)|²|T(β)|²   (DWBA)
                              convolve R_res; cutoff ξ_coh
                              → I_meas  ⇄  fit C(R) or (φ,Δ,…)
```

Wiener–Khinchin sits on the left branch: P(q<sub>∥</sub>)=FT[C]. Only for q<sub>z</sub>σ≪ 1 is S<sub>diff</sub>∝ P.

## Flagged uncertainties

1. **PRB (2.3) surface-integral identity.** Chapter 2 derives (2.4) from a <i>Θ</i>-function density instead of repeating their <b>A</b>· d<b>S</b> identity. Prefactors (Nb)<sup>2</sup> are not needed for correlation modelling.
2. **Gaussian heights** are an assumption (PRB “central assumption”), false for two-level islands (Physica) and imperfect for the Pyrex example (PRB Sec. V).
3. **Nevot–Croce** is quoted as the small-q<sub>z</sub>σ reduction of DWBA (4.33) → (4.34). Full F<sub>±</sub> algebra is not re-derived here; read PRB Sec. IV for matrix elements.
4. **Physica (13)** (Wu 2D hard-sphere S(q<sub>∥</sub>)) is unreadable in the PDF extract. Use S=1+ρ FT[g<sub>pair</sub>-1] or a documented formula from Wu, J. Chem. Phys. 101, 4198 (1994).
5. **Capillary A,B** in g=A+B ln R depend on UV cutoff convention; treat as experimental parameters.

None of these block implementing a forward model once the [questionnaire](../experiment-questionnaire.md) is filled.
