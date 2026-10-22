# Paper takeaways for simulated X-ray scattering models

Source PDFs (keep these as the originals):

- `docs/papers/PhysRevB.38.2297.pdf`
- `docs/papers/1-s2.0-0378437196000854-main.pdf`

This note is for building **simulated specular + off-specular (diffuse) X-ray scattering**. Neither paper supplies a dataset for this project. Numbers below are **from the papers’ own examples**, not user measurements.

---

## 1. Sinha, Sirota, Garoff, Stanley — *X-ray and neutron scattering from rough surfaces*

**Phys. Rev. B 38, 2297 (1988).** Received 30 November 1987.

This is the **core scattering theory**. Material is treated as homogeneous except for a surface (atomic structure ignored while qa ≪ 1). Intensity splits into **specular** (true δ(q<sub>x</sub>)δ(q<sub>y</sub>) ridges) and **diffuse** (from height–height correlations).

### Methods

- **Born approximation** far from total external reflection: volume scattering rewritten as a surface integral over height z(x,y).
- Height difference [z(<b>r</b>)-z(<b>0</b>)] is taken as a **Gaussian random variable** with g(R)=⟨[z(R)-z(0)]<sup>2</sup>⟩.
- **Self-affine solid roughness** with a finite cutoff <i>ξ</i>:

$$
C(R)=\langle z(R)z(0)\rangle=\sigma^2\exp\big[-(R/\xi)^{2h}\big],\qquad 0<h<1
$$

  so g(R)=2σ<sup>2</sup>[1- exp(-(R/ξ)<sup>2h</sup>)]. Without a cutoff there is **no true specular** (all intensity is diffuse). Small <i>h</i> is jagged; h→ 1 is rolling. Surface fractal dimension D<sub>s</sub>=3-h.
- **Liquid surfaces:** capillary waves give logarithmic g(R). Specular only reappears because of a **finite-size / coherence / gravity cutoff**.
- **Randomly oriented surfaces (SAS):** orientational average recovers Porod S(q)∼ q<sup>-4</sup> for smooth surfaces, and S(q)∼ A<sub>1</sub>/q<sup>4</sup>+A<sub>2</sub>/q<sup>3+h</sup> for self-affine roughness. Lateral roughness of a *sharp* interface falls **slower** than q<sup>-4</sup>; a *graded* (interdiffused) interface falls **faster**.
- **Distorted-wave Born approximation (DWBA)** near the critical angle θ<sub>c</sub>: perturb the exact Fresnel solution of a smooth surface. Specular interpolates toward the Nevot–Croce form ∣R∣<sup>2</sup>≃∣R<sub>F</sub>∣<sup>2</sup> exp(-q<sub>z</sub> q<sub>z</sub>'σ<sup>2</sup>) when q<sub>z</sub>σ≲ 1. Born is the right limit for q<sub>z</sub>σ≫ 1. DWBA specular is **not** reliable below θ<sub>c</sub> (misses unitarity losses into diffuse).
- Diffuse in DWBA ≈ Born S(<b>q</b>) times ∣T(k<sub>1</sub>)∣<sup>2</sup>∣T(k<sub>2</sub>)∣<sup>2</sup>, with q<sub>z</sub> replaced by the **in-medium** q<sub>z</sub>'. That produces **Yoneda (“angel wing”) peaks** when θ<sub>1</sub> or θ<sub>2</sub>=θ<sub>c</sub>.

A **transverse scan at small q<sub>z</sub>** is approximately the Fourier transform of C(X,Y). In general, diffuse intensity is **not** that Fourier transform.

### Paper’s own experimental illustration (not our data)

Polished Pyrex at NSLS X10A, λ=1.46 Å, θ<sub>c</sub>=0.20°. Self-consistent fits of specular, near-specular diffuse, and rocking curves: σ=7.6± 0.2 Å, h=0.2± 0.02, ξ=7000± 1000 Å. The simple self-affine form is only approximate for that glass.

---

## 2. Sinha et al. — *Off-specular X-ray scattering studies of the morphology of thin films*

**Physica A 231, 99–110 (1996).** Corresponding author S. K. Sinha (APS / Argonne), with Y. P. Feng, C. A. Melendres, D. D. Lee, T. P. Russell, S. K. Satija, E. B. Sirota, M. K. Sanyal.

This is an **application / morphology paper**. It **cites the 1988 PRB as the DWBA/Born roughness theory** and specialises it to **islands or pits** of essentially constant height on an otherwise flat film—not a continuous self-affine height field.

### Geometry and scans

Incident grazing angle <i>α</i>, exit <i>β</i>; <b>q</b>=<b>k</b><sub>1</sub>-<b>k</b><sub>0</sub>. Standard maps: **specular ridge**, **longitudinal diffuse** (q<sub>∥</sub> small, vary q<sub>z</sub>), **transverse / rocking** (vary q<sub>∥</sub> at fixed q<sub>z</sub>).

### Island / pit model (Born, then DWBA)

Assume no correlation between island height and lateral size. Then S(<b>q</b>)=S<sub>spec</sub>+S<sub>diff</sub>:

- **Specular** depends on coverage <i>φ</i> and the Fourier transform h(q<sub>z</sub>) of the height (depth) distribution of islands/pits. For islands of **fixed thickness** <i>Δ</i>, h(q<sub>z</sub>)=e<sup>-iq<sub>z</sub>Δ</sup>. Specular and island-induced diffuse along q<sub>z</sub> oscillate with period 2π/Δ and are **out of phase**.
- **Diffuse** depends on island form factor f(q<sub>∥</sub>), in-plane structure factor S(q<sub>∥</sub>) of island centres, coverage, and ∣1-h(q<sub>z</sub>)∣<sup>2</sup>.
- **DWBA intensity:** I(<b>q</b>)=∣T(α)∣<sup>2</sup>∣T(β)∣<sup>2</sup> S(<b>q</b>) with <i>S</i> evaluated using the in-medium <i>q</i> (difference from vacuum <i>q</i> is usually small except near θ<sub>c</sub>).
- **Kiessig fringes** (period 2π/t from total film thickness <i>t</i>) appear in specular always, and in **diffuse only if the two interfaces have conformal roughness**—and then they are **in phase** between specular and diffuse.
- In-plane correlations only show as side peaks if neighbour spacing is **inside the X-ray coherence length** across the surface (paper: typically **10–20 µm** at a synchrotron). Off-specular scattering is the **2D analogue of small-angle scattering**, at much smaller <i>q</i> / larger real-space scales.

### Paper’s own examples (not our data)

**PS/PMMA (50:50) islands on Si** (X10A). X-ray contrast between blocks is negligible → uniform film + constant-height islands. MW 30 000: film t=1496 Å ≈ 9.5 bilayers, bilayer/Δ=176 Å; island lateral size ∼ 5 μm. Specular and longitudinal diffuse show the predicted out-of-phase <i>Δ</i>-modulations; conformal roughness puts Kiessig fringes on the diffuse as well. MW 100 000: islands ∼ 25 μm **larger than coherence**, so island modulations **vanish from the diffuse**.

**Cu pitting in 0.01 M NaHCO3** (transmission electrochemical cell; Cu ∼ 1500 Å on Si). Smooth-electrode specular/rocking (DWBA + self-affine model from the 1988 paper): rms σ≈ 18 Å at -0.9 V, 22 Å at +0.2 V; lateral correlation **<100 Å**. After holds at +0.5 V, transverse scans show **side lobes** from pit–pit correlations. Fits use a 2D hard-sphere S(q<sub>∥</sub>), average pit radius <i>R</i>, spacing <i>d</i>, and local density inside a coherent patch (not the global density). Reported evolution: <i>d</i> from ∼ 8.5 to 7.5 μm; pit size ∼ 4 μm at 9 min; growth as **clusters**. Early pits are **asymmetric** (grain orientation); q<sub>z</sub> dependence of side-lobe intensity is modelled as a **bimodal depth** (surface vs ∼ 40 Å buried), interpreted as oxide-film breaking—not a number to reuse unless the same system is measured.

---

## How the two papers relate

| | 1988 PRB | 1996 Physica A |
| --- | --- | --- |
| Role | Foundational S<sub>spec</sub>+S<sub>diff</sub> for **continuous** roughness (self-affine / capillary / SAS) | Uses that theory, then a **discrete island/pit** Born + DWBA model |
| Height statistics | Gaussian C(R) with σ,h,ξ (or log capillary waves) | Height distribution h(z) of islands/pits; often a single <i>Δ</i> |
| In-plane | Power-law / cutoff in C(R); Yoneda from ∣T∣<sup>2</sup> | Form factor + liquid-like S(q<sub>∥</sub>); side peaks if d < coherence |
| When to use | Polished/grown/liquid **roughness**; SAS from internal surfaces | Incomplete wetting **islands**, **holes**, **pits**, other 2D “particles” |

A simulation stack for this project should treat them as **two morphology classes on the same scattering engine**: (1) correlated random height field → PRB formulae; (2) coverage, island/pit shape, and 2D structure factor → Physica formulae; both optionally multiplied by Fresnel ∣T(α)T(β)∣<sup>2</sup>.

---

## Quantities a scattering simulation must expose

**Kinematics / instrument**

- Wavelength <i>λ</i>, <b>k</b><sub>0</sub>,<b>k</b><sub>1</sub>, grazing α,β, <b>q</b>=(q<sub>∥</sub>,q<sub>z</sub>), θ<sub>c</sub> from refractive index n=1-δ+iβ.
- Scan type: specular (α=β), longitudinal diffuse, rocking / q<sub>∥</sub>.
- Resolution (often Gaussian, wide out-of-plane), illuminated area ∝ 1/ sinα, **coherence length** on the surface (cuts off S(q<sub>∥</sub>) and can erase island peaks).
- DWBA vs Born: use DWBA near θ<sub>c</sub> and for Yoneda wings; Born at large q<sub>z</sub>σ.

**Continuous roughness (PRB)**

- Contrast: scattering-length density (neutrons) or electron density <i>ρ</i> / Δρ (X-rays).
- <i>σ</i>, Hurst <i>h</i>, cutoff <i>ξ</i>; optional non-Gaussian w(z).
- Liquid vs solid: logarithmic vs saturating g(R).
- Distinguish **rough sharp interface** vs **graded** density ρ(z) (no diffuse if purely <i>z</i>-graded).

**Islands / pits (Physica)**

- Coverage <i>φ</i>, island thickness/depth <i>Δ</i> or full h(z), average area A<sub>0</sub> / radius <i>R</i>.
- In-plane S(q<sub>∥</sub>): random, hard-sphere (Wu), or clustered; mean spacing <i>d</i>.
- Film thickness <i>t</i>, substrate vs film densities ρ<sub>1</sub>,ρ<sub>2</sub>, extra rms σ<sub>1</sub>,σ<sub>2</sub>, **conformal** vs independent interfaces (Kiessig in diffuse).
- Coherence vs island size: if islands ≳ coherence, they drop out of diffuse and only affect the specular average.

**What not to do yet**

Do not treat the Pyrex, PS/PMMA, or Cu-pit numbers as this project’s experimental data. Put user measurements in `data/experimental/` and describe them in `docs/context/`. Implement models against these papers after that description exists.

Compact equation list: [`paper-equations.md`](paper-equations.md).
