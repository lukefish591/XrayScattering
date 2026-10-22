# Explorations: surfaces, C(R), and what scattering sees

Toy diagrams for how **rms roughness** σ, **lateral cutoff** ξ, **Hurst** h, **capillary logs**, **islands**, and **optics** change real-space maps and Born (sometimes DWBA) intensity. **Every number is illustrative.** None of this is the user’s sample or measured data.

Run from `xray-scattering/` with the venv on:

```bash
cd explorations
python 01_self_affine_sweeps.py
python 02_gaussian_and_capillary.py
python 03_smooth_graded_rough.py
python 04_islands_pits.py
python 05_dwba_yoneda.py
python 06_kiessig.py
```

Plots land in `plots/`. Maths: [chapter 5](../docs/maths/05-born-specular-diffuse.md) (Born split), [chapter 6](../docs/maths/06-capillary-waves.md), [chapter 7](../docs/maths/07-islands-pits.md), [chapter 8](../docs/maths/08-experiment-maths.md).

Display formulae use `$$`. In-sentence math is HTML/unicode.

Base self-affine toys (unless a caption says otherwise): σ=5 Å, ξ=40 Å, h=0.5. Intensities omit (Nb)², area, and flux — **shapes only**.

---

## 1. Self-affine C(R), one parameter at a time

$$
C(R)=\sigma^2\exp\bigl[-(R/\xi)^{2h}\bigr],\qquad
g(R)=2\sigma^2-2C(R).
$$

Born diffuse (PRB (2.28b), isotropic):

$$
S_{\mathrm{diff}}(\mathbf{q})\propto\frac{e^{-q_z^2\sigma^2}}{q_z^2}\int_0^\infty R\,dR\,J_0(q_\parallel R)\bigl(e^{q_z^2 C(R)}-1\bigr).
$$

Specular reduction (if C(∞)=0): e<sup>−q<sub>z</sub>²σ²</sup>.

| Figure | What to notice |
| --- | --- |
| [01_surfaces_sigma.png](plots/01_surfaces_sigma.png) | Vertical contrast scales with σ; the lateral pattern is the same. |
| [01_stats_sigma.png](plots/01_stats_sigma.png) | C(0)=σ². Diffuse overall scale grows with σ; the q<sub>∥</sub> *shape* at this q<sub>z</sub> is similar until q<sub>z</sub>σ is no longer small. |
| [01_qz_sigma.png](plots/01_qz_sigma.png) | Specular e<sup>−q<sub>z</sub>²σ²</sup> drops much faster for larger σ. |
| [01_surfaces_xi.png](plots/01_surfaces_xi.png) | Larger ξ → fatter hills (same height rms). |
| [01_stats_xi.png](plots/01_stats_xi.png) | PSD and S<sub>diff</sub> *narrow* in q<sub>∥</sub> when ξ grows (large features, sharp peak). |
| [01_surfaces_h.png](plots/01_surfaces_h.png) | h=0.2 is jagged (high-frequency texture); h=0.8 is rolling. Same σ and ξ. |
| [01_stats_h.png](plots/01_stats_h.png) | Small h: C(R) has a long tail and more high-q<sub>∥</sub> power. |
| [01_qz_h.png](plots/01_qz_h.png) | Specular DW **does not see h** (only σ). Diffuse vs q<sub>z</sub> does. |

---

## 2. Gaussian correlation vs capillary/log

Gaussian C is the h=1 member of the same family. Capillary: g(R)≈B ln((R+a)/a) until an IR cutoff ξ<sub>IR</sub> (otherwise C never saturates and there is no δ(q<sub>∥</sub>) specular).

| Figure | What to notice |
| --- | --- |
| [02_three_families_surfaces.png](plots/02_three_families_surfaces.png) | Gaussian is the smoothest of the three at the same σ; the log field is longer-ranged. |
| [02_three_families_stats.png](plots/02_three_families_stats.png) | Log C decays slowly; P(q<sub>∥</sub>) is closer to 1/q² before the IR cutoff bites. |

---

## 3. Smooth vs graded vs rough sharp

A density that depends **only on z** (a grade) has **no diffuse**. A rough *sharp* interface has Debye–Waller specular **and** S<sub>diff</sub> from C(R).

| Figure | What to notice |
| --- | --- |
| [03_density_profiles.png](plots/03_density_profiles.png) | Graded: every (x,y) sees the same ρ(z). |
| [03_smooth_graded_rough.png](plots/03_smooth_graded_rough.png) | Specular: grade falls faster than Porod. Diffuse: only the rough sharp case is nonzero. |

---

## 4. Islands and pits

Fixed height Δ, coverage φ. Specular ∝ 1−4φ(1−φ)sin²(q<sub>z</sub>Δ/2); near-specular diffuse ∝ sin²(q<sub>z</sub>Δ/2). Period 2π/Δ, **out of phase**. Disk ∣f∣² and an exclusion-hole S(q<sub>∥</sub>) (not Wu’s OCR’d (13)).

| Figure | What to notice |
| --- | --- |
| [04_island_map.png](plots/04_island_map.png) | Dart-thrown disks, min spacing; φ is local on this patch. |
| [04_phi_delta_qz.png](plots/04_phi_delta_qz.png) | Deeper specular dips as φ→1/2; oscillation period shrinks as Δ grows; dashed sin² peaks where spec dips. |
| [04_form_and_S.png](plots/04_form_and_S.png) | Larger R → narrower ∣f∣². Grey 2π/d marks the neighbour scale. |
| [04_coherence.png](plots/04_coherence.png) | If ξ<sub>coh</sub>≪d, the pair oscillation in S is washed out (Physica MW 100k lesson). |

---

## 5. DWBA / Yoneda (optional)

Pyrex n from PRB Sec. V so θ<sub>c</sub>≈0.20°. Intensity ~ ∣T(α)T(β)∣² × Born S<sub>diff</sub> on a 2θ=1.2° rock. In-medium q<sub>z</sub>' is **not** used (small except near θ<sub>c</sub>).

| Figure | What to notice |
| --- | --- |
| [05_transmission.png](plots/05_transmission.png) | ∣T∣² peaks near θ<sub>c</sub>. |
| [05_dwba_rocking.png](plots/05_dwba_rocking.png) | Wings when α=θ<sub>c</sub> or β=θ<sub>c</sub>. Born S is almost flat on this short rock; the wings are optical. |

---

## 6. Kiessig, conformal vs independent

Toy film t=400 Å on a substrate (Physica (12)-style).

| Figure | What to notice |
| --- | --- |
| [06_kiessig.png](plots/06_kiessig.png) | Specular fringe spacing 2π/t. Diffuse shows those fringes **only if** the two interfaces are conformal, and they are **in phase** with specular (unlike island 2π/Δ). |

---

## Caveats (do not over-read the toys)

- Hankel integrals use a finite R<sub>max</sub> and a cosine taper; very small h still has a long C(R) tail.
- Exclusion-hole S(q<sub>∥</sub>) can be a poor liquid structure factor; packing is kept modest so S(0)>0. Not Wu (13).
- Capillary B and the UV a=1 Å are conventional, not a surface-tension calculation.
- Graded vs rough specular envelopes are schematic (not a Parratt/matrix stack).
- Maps are one random realisation (seeded) of a Gaussian field with the chosen C(R).
