# Intro course: simulated X-ray scattering data models

Self-paced. You do not need prior surface-scattering background. Work the modules in order; each has a short Python toy in [`course/`](course/README.md).

**Papers (read as you go, not all at once):**

- Sinha, Sirota, Garoff, Stanley, *X-ray and neutron scattering from rough surfaces*, [Phys. Rev. B **38**, 2297 (1988)](papers/PhysRevB.38.2297.pdf) — theory.
- Sinha et al., *Off-specular X-ray scattering studies of the morphology of thin films*, [Physica A **231**, 99 (1996)](papers/1-s2.0-0378437196000854-main.pdf) — islands/pits.
- Narrative: [paper-takeaways.md](paper-takeaways.md) · equations: [paper-equations.md](paper-equations.md)
- Mathematics (Fourier, C(R), Born split, islands): [maths primer](maths/README.md)

Toy scripts use **Pyrex λ and n from PRB Sec. V** only so θ<sub>c</sub> is realistic. That is **not your sample**. Fill [experiment-questionnaire.md](experiment-questionnaire.md) in Module 8.

From `xray-scattering/`: `source .venv/bin/activate` then `cd course`.

---

## Module 1 — Kinematics and q-space

**Goals.** Define **q** = **k₁** − **k₀**; map grazing **α** (incidence) and **β** (exit) onto **q∥** and **q<sub>z</sub>**; recognise the three standard scans.

**Idea.** Both papers draw the same geometry (PRB Fig. 1; Physica Fig. 1). Angles are from the *surface*, not the surface normal. Specular: α = β ⇒ q<sub>x</sub> = q<sub>y</sub> = 0, q<sub>z</sub> = 2k sin α. **Longitudinal diffuse:** walk up in q<sub>z</sub> beside the ridge. **Rocking / transverse:** fix 2θ ≈ α+β (≈ fixed q<sub>z</sub>) and vary α−β (q∥).

**Exercise.** `python 01_kinematics.py` → [`course/plots/01_qspace.png`](course/plots/01_qspace.png). Sketch where a Yoneda wing would sit (α or β = θ<sub>c</sub>) on that map — you compute θ<sub>c</sub> in Module 2.

**Self-check.** If α=β and you increase both, do you move along q<sub>z</sub> or q<sub>x</sub>? (Along q<sub>z</sub>.) If you rock at fixed 2θ, which component changes most? (q<sub>x</sub>.)

---

## Module 2 — Refractive index, θ<sub>c</sub>, Fresnel

**Goals.** Connect n = 1−δ+iβ, **θ<sub>c</sub>**, and Fresnel **R**, **T**.

**Idea.** X-rays see n < 1, so there is **total external reflection** for α < θ<sub>c</sub>. PRB (2.16), (4.8)–(4.10): θ<sub>c</sub> ≃ √[2(1−n)] for real n; R and T from matching k<sub>z</sub> in vacuum and in the medium. Below θ<sub>c</sub>, ∣R∣² ≈ 1 (smooth, no absorption); ∣T∣² **peaks near θ<sub>c</sub>** — that peak will make Yoneda wings (Module 4). Born/Porod q<sub>z</sub>⁻⁴ is only the *large-angle* limit of Fresnel (PRB Sec. II.A).

**Exercise.** `python 02_fresnel.py` → [`02_fresnel.png`](course/plots/02_fresnel.png). Compare √(2δ) with the 0.20° quoted in PRB Sec. V.

**Self-check.** Why is ∣T∣² large near θ<sub>c</sub> important for *diffuse* intensity even if you never sit on the specular ridge? (DWBA multiplies by ∣T(α)∣²∣T(β)∣².)

---

## Module 3 — Specular vs diffuse

**Goals.** Split **S = S<sub>spec</sub> + S<sub>diff</sub>**; know which scan measures which.

**Idea.** PRB Sec. II: if height differences are Gaussian and the height–height **C(R)** *saturates* at large R (cutoff ξ), S<sub>spec</sub> is a **δ(q<sub>x</sub>)δ(q<sub>y</sub>)** ridge × e^{−q<sub>z</sub>²σ²} times the smooth reflectivity. Everything else is diffuse and is the Fourier–Bessel transform of (e^{q<sub>z</sub>² C(R)}−1). **Without a cutoff, there is no true specular** (liquid capillary waves unless gravity/coherence cut them off). Physica Eq. (4) is the same split for islands. Diffuse under the ridge can swamp weak specular at large q<sub>z</sub> (PRB Introduction).

**Exercise.** `python 03_specular_vs_diffuse.py` → [`03_spec_diff.png`](course/plots/03_spec_diff.png). Note the Debye–Waller-like falloff vs q<sub>z</sub> and the rocking cartoon.

**Self-check.** A “specular” detector scan with wide slits still contains diffuse. What extra scan do you need to subtract it? (Longitudinal or transverse offset from α=β, as in PRB Sec. V.)

---

## Module 4 — Born vs DWBA, Nevot–Croce, Yoneda

**Goals.** Know **when Born fails**, what **Nevot–Croce** is, and why **Yoneda** peaks appear.

**Idea.** Born fails when ∣R∣~1 (near θ<sub>c</sub>). DWBA (PRB Sec. IV) perturbs the *exact Fresnel states* of a smooth surface. Specular for q<sub>z</sub> σ ≲ 1 interpolates to Nevot–Croce ∣R∣² ≃ ∣R<sub>F</sub>∣² exp(−q<sub>z</sub> q<sub>z</sub>′ σ²) (PRB (4.34)); for q<sub>z</sub> σ ≫ 1 use Born, not the DWBA specular formula (PRB Fig. 5 discussion). Diffuse in DWBA is Born S(**q′**) × ∣T(k₁)∣²∣T(k₂)∣² with in-medium q<sub>z</sub>′ (PRB (4.41); Physica (8)). Yoneda / “angel wings”: ∣T∣ peaks when α or β = θ<sub>c</sub> (PRB Fig. 6).

**Exercise.** `python 04_dwba_yoneda.py` → [`04_yoneda.png`](course/plots/04_yoneda.png). Match the two peaks to α=θ<sub>c</sub> and β=θ<sub>c</sub> on a 2θ=1° rock.

**Self-check.** Below θ<sub>c</sub>, should you trust first-order DWBA for ∣R∣<1 from roughness losses? (No — PRB Sec. IV, unitarity / second-order.)

---

## Module 5 — Self-affine roughness (σ, h, ξ)

**Goals.** Read **C(R) = σ² exp[−(R/ξ)^{2h}]**; see how **h** changes texture and the diffuse line shape.

**Idea.** PRB (2.6)–(2.9), (2.25): 0<h<1; small h is jagged; D<sub>s</sub> = 3−h. σ = rms; ξ = lateral cutoff (without it, no specular). Diffuse: PRB (2.28b)–(2.29). At *small* q<sub>z</sub>, a transverse scan ≈ FT of C(R) (PRB (4.43)); **not** true at general q<sub>z</sub>. Paper’s Pyrex illustration (Sec. V): σ≈7.6 Å, h≈0.2, ξ≈7000 Å — **illustration, not your surface**. SAS / Porod: randomly oriented smooth surfaces ~ q⁻⁴; self-affine ~ A₁/q⁴ + A₂/q^{3+h} (PRB Sec. III). Sharp *lateral* roughness falls slower than q⁻⁴; a *graded* ρ(z) falls faster and has **no** diffuse if it is only z-dependent.

**Exercise.** `python 05_self_affine.py` → [`05_self_affine.png`](course/plots/05_self_affine.png). The script uses a **smaller toy ξ** so the integral is quick; compare the three h curves.

**Self-check.** If you only fit specular ∣R∣(q<sub>z</sub>), which parameters are you mostly blind to? (h and ξ — you need diffuse / rocking.)

---

## Module 6 — Islands and pits

**Goals.** Coverage **φ**, height **Δ**, form factor **f(q∥)**, structure factor **S(q∥)**, **coherence**.

**Idea.** Physica: discrete islands/pits, not a continuous Gaussian field. It *cites the PRB* for DWBA. Height FT h(q<sub>z</sub>); for fixed Δ, h(q<sub>z</sub>)=e^{−i q<sub>z</sub> Δ} (Eq. 9). Specular (11) and diffuse (10): both oscillate with period 2π/Δ **out of phase**. In-plane: f(q∥) (island shape) × S(q∥) (arrangement). Side peaks only if neighbour spacing ≲ **coherence length** (Physica: typically 10–20 µm); MW 100k islands ~25 µm **vanished** from diffuse. Pit example used a 2D hard-sphere S(q∥) (Wu); fitted R, d, φ₀ are **per coherent patch**, not necessarily the whole sample.

**Exercise.** `python 06_islands.py` → [`06_islands.png`](course/plots/06_islands.png). The in-plane peak is a **toy Gaussian at 2π/d**, not Wu’s formula.

**Self-check.** If AFM shows 30 µm islands and your beam coherence is 15 µm, do you expect off-specular island peaks? (No — only a specular average.)

---

## Module 7 — Kiessig fringes and conformal roughness

**Goals.** Separate **film-thickness** fringes from **island-height** fringes; know when diffuse shows Kiessig.

**Idea.** Physica (12): substrate + film densities, extra σ₁ (air/film) and σ₂ (film/substrate). Period 2π/t (**Kiessig**) vs 2π/Δ (islands). Kiessig appear in **diffuse iff the two interfaces are conformal**; then they are **in phase** with specular (unlike island oscillations). Independent roughness: diffuse envelope, no t-fringes.

**Exercise.** `python 07_kiessig.py` → [`07_kiessig.png`](course/plots/07_kiessig.png). Check that Δq<sub>z</sub> between specular fringes is 2π/t.

**Self-check.** Specular has fast fringes; diffuse is smooth. What does that say about interface conformality? (Little or no conformal roughness.)

---

## Module 8 — Plan a simulation (your experiment)

**Goals.** Choose a morphology class; list the numbers a model must take; write them down **for your sample**.

**Idea.** One engine, two classes (see takeaways table):

1. Continuous height field → PRB (σ, h, ξ, n, scans, resolution).
2. Islands/pits → Physica (φ, Δ, f, S, coherence, plus film t and conformal flag).
3. DWBA ∣T(α)T(β)∣² near θ<sub>c</sub>; Born at large q<sub>z</sub> σ.

**Exercise.** `python 08_print_plan.py` then fill [experiment-questionnaire.md](experiment-questionnaire.md). Leave unknowns blank. Do **not** paste Pyrex/PS-PMMA/Cu numbers unless that is actually your system.

**Self-check.** Can you point to: (a) specular vs diffuse scans you have or will take, (b) one morphology class, (c) λ and a guess at θ<sub>c</sub>? If not, those are the next questions to answer — not more code.

---

## After the course

Implement real models in `src/xray_scattering/` against the questionnaire and the papers, not against `course/` toys. Put measurements in `data/experimental/`.
