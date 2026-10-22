# Mathematics primer: from calculus to correlation-function scattering

Companion to the [intro course](../intro-course.md). That course is physical and scan-based. **This primer is the maths underneath modeling correlation-function measurements** (what C(R) is, why intensity is its Fourier transform, how the 1988 PRB and 1996 Physica formulae appear).

**Assumed start:** algebra, derivatives, and integrals of elementary functions. **Not assumed:** Fourier analysis, complex numbers in physics, probability of random fields, or Bessel functions. Each symbol is defined at first use.

**Papers:** [Phys. Rev. B **38**, 2297 (1988)](../papers/PhysRevB.38.2297.pdf) · [Physica A **231**, 99 (1996)](../papers/1-s2.0-0378437196000854-main.pdf) · [takeaways](../paper-takeaways.md) · [equation sheet](../paper-equations.md)

**Convention used everywhere here** (same as the papers’ e<sup>-i<b>q</b>·<b>r</b></sup> Born integrals):

$$
\tilde f(\mathbf{q})=\int d^d r\, f(\mathbf{r})\,e^{-i\mathbf{q}\cdot\mathbf{r}},\qquad
f(\mathbf{r})=\frac{1}{(2\pi)^d}\int d^d q\, \tilde f(\mathbf{q})\,e^{i\mathbf{q}\cdot\mathbf{r}}.
$$

Numeric checks (run from this folder’s `code/` after `source .venv/bin/activate` at the repo root): see [code/README.md](code/README.md).

## Chapters

1. [Prerequisites](01-prerequisites.md) — complex exponentials, vectors, delta function, area integrals
2. [Fourier transforms and the Born approximation](02-fourier-and-born.md)
3. [Random variables and random fields](03-random-fields.md)
4. [Correlation functions, Wiener–Khinchin, Hankel / J<sub>0</sub>](04-correlation-functions.md)
5. [From C(R) to specular + diffuse (PRB 1988)](05-born-specular-diffuse.md)
6. [Capillary waves and logarithmic correlations](06-capillary-waves.md)
7. [Islands and pits (Physica A 1996)](07-islands-pits.md)
8. [Experiment-side maths: resolution, coherence, Fresnel, fitting](08-experiment-maths.md)
9. [Glossary and equation map](09-glossary-and-map.md)

Uncertainties (derivation details that the PDFs do not fully expand) are marked **Uncertain** in the chapters and listed at the end of chapter 9.
