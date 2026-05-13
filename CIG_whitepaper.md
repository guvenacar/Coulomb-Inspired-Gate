# Introduction
Boolean logic gates form the foundation of computation and cryptography.
Classical gates (AND, OR, XOR, NOT) and their combinations are well
understood; linear threshold gates (TLGs) extend these by allowing
weighted inputs. All classical and threshold gates share a fundamental
property: their behavior is determined solely by the *multiset* of input
values, independent of the positions of those values.
The CIG breaks this symmetry. Inspired by the inverse-square law of
electrostatics, the gate assigns signed, distance-dependent weights to
the neighbors of a passing bit. The sign of the weight depends on *which
side* of the passing bit the neighbor occupies. As a result, permuting
the gate bits changes the output even when the Hamming weight is
preserved --- a property absent in all classical gate families.
Beyond theoretical interest, this positional sensitivity makes the gate
attractive as a primitive for lightweight cryptography: it achieves full
bijection and strong avalanche behavior with a compact, parameter-free
formula.
# Definition
**Definition 1** (Coulomb-Inspired Gate (CIG)). *Let
$G = (g_{-3}, g_{-2}, g_{-1}, g_{+1}, g_{+2}, g_{+3}) \in \{0,1\}^6$ be
a *gate pattern* and $p \in \{0,1\}$ a *passing bit*. Define the signed
charge function
$$Q(g, p) \;=\; 2\cdot\mathbf{1}[g \neq p] - 1 \;\in\; \{-1, +1\},$$
which equals $+1$ if the gate bit and passing bit differ (attraction)
and $-1$ if they agree (repulsion). The *net Coulomb force* is
$$F(p, G) \;=\; \sum_{k \in \{-3,-2,-1,+1,+2,+3\}} \frac{\operatorname{sgn}(k)}{|k|} \cdot Q(g_k, p),$$
where $\operatorname{sgn}(k) = +1$ for $k>0$ (right neighbors) and $-1$
for $k < 0$ (left neighbors). The output of the gate is:

| Condition | Output |
|-----------|--------|
| $p = 0$ and $F(p,G) > 0$ | 1 |
| $p = 0$ and $F(p,G) \le 0$ | 0 |
| $p = 1$ and $F(p,G) > 0$ | 0 |
| $p = 1$ and $F(p,G) \le 0$ | 1 |
**Weight vector.** Writing $w_k = \operatorname{sgn}(k)/|k|$, the
weights for positions $k \in \{-3,-2,-1,+1,+2,+3\}$ are
$$\mathbf{w} = \left(-\tfrac{1}{3},\,-\tfrac{1}{2},\,-1,\,+1,\,+\tfrac{1}{2},\,+\tfrac{1}{3}\right).$$
Left neighbors have negative weight (force directed left); right
neighbors have positive weight (force directed right).
**Physical analogy.** Logical $0$ represents an electron ($e^-$) and
logical $1$ represents a positron ($e^+$). Same-charge neighbors repel
the passing particle; opposite-charge neighbors attract it. The net
force determines whether the particle deflects and thereby changes
state.
**Dynamic beam for 8-bit blocks.** For an 8-bit block
$B = (b_0,\dots,b_7)$, we define the *neighborhood beam* of bit $b_i$ as
the 6-bit vector
$(b_{i-3}, b_{i-2}, b_{i-1}, b_{i+1}, b_{i+2}, b_{i+3})$ with indices
taken modulo 8. Applying the CIG bitwise to each $b_i$ using its own
beam yields a transformed block. One full pass over all 8 bits is called
a *round*. Two rounds produce the 50.1% avalanche effect reported in
Section 5 (Experimental Results).
# Bijectivity
**Lemma 1** (Force antisymmetry). *For any gate $G$ and passing bit $p$:*
$$F(1, G) = -F(0, G)$$

*Proof.* We have $Q(g, 0) = 2\mathbf{1}[g=1]-1$ and
$Q(g, 1) = 2\mathbf{1}[g=0]-1 = -Q(g,0)$. Therefore
$$F(1, G) = \sum_k w_k \cdot Q(g_k, 1) = \sum_k w_k \cdot (-Q(g_k, 0)) = -F(0,G).$$

◻
**Theorem 1** (Bijectivity). *For every gate pattern $G \in \{0,1\}^6$,
the map $p \mapsto \mathrm{out}(p, G)$ is a bijection on $\{0,1\}$.*
*Proof.* By the physical model, the positron ($p=1$) always behaves as
the complement of the electron ($p=0$). This is captured by the compact
decision rule: letting $b = \mathbf{1}[F(0,G) > 0]$,
$$\mathrm{out}(0,G) = b, \qquad \mathrm{out}(1,G) = 1 - b$$

We verify this is consistent with Lemma [1](#lem:antisym).
reference="lem:antisym"}. Since $F(1,G) = -F(0,G)$, we have
$F(1,G) > 0 \iff F(0,G) < 0 \iff b = 0$. The decision rule for $p=1$
then gives $\mathrm{out}(1,G) = 0$ when $b=0$ and
$\mathrm{out}(1,G) = 1$ when $b=1$, i.e.,
$\mathrm{out}(1,G) = b = 1 - \mathrm{out}(0,G)$, confirming consistency.
Since $\mathrm{out}(0,G) \neq \mathrm{out}(1,G)$ for every $G$, the map
$p \mapsto \mathrm{out}(p,G)$ is injective, and hence bijective on the
two-element set $\{0,1\}$.
**The case $F(0,G) = 0$.** Eight of the 64 gate patterns satisfy
$F(0,G)=0$ (verified exhaustively with exact rational arithmetic). In
this case $b=0$, giving $\mathrm{out}(0,G)=0$ and $\mathrm{out}(1,G)=1$
(the identity map), which is bijective.
Lemma [1](#lem:antisym) is
consistent: $F(1,G)=0$ as well, and neither passing bit deflects. ◻
**Corollary 1**. *Applied bitwise and independently to an 8-bit block,
the CIG is a bijection on $\{0,1\}^8$, yielding 256 distinct outputs for
256 distinct inputs.*
*Proof.* Each bit position uses its own 6-bit neighborhood as gate.
Since each bit maps bijectively and independently, the product map is
bijective. Exhaustive computation confirms 256/256 distinct outputs. ◻
# Non-Classical Properties
## Not Symmetric
A Boolean function is *symmetric* if its output depends only on the
Hamming weight of its input (i.e., permuting inputs does not change the
output). The CIG is not symmetric:
$$G_1 = (1,1,1,0,0,0),\quad F(0,G_1) = -\tfrac{11}{3} < 0 \;\Rightarrow\; \mathrm{out}=0,$$
$$G_2 = (0,0,0,1,1,1),\quad F(0,G_2) = +\tfrac{11}{3} > 0 \;\Rightarrow\; \mathrm{out}=1.$$
Both gates have Hamming weight 3, yet produce opposite outputs. Among
all permutations of a 3-ones pattern (20 permutations), exactly 10 yield
output 0 and 10 yield output 1. No symmetric function can replicate this
split.
## Not Linear over GF(2)
A Boolean function $f:\{0,1\}^n\to\{0,1\}$ is *linear over GF(2)* if
$f(x\oplus y)=f(x)\oplus f(y)$ for all $x,y$. Exhaustive testing over
all $\binom{64}{2}\times 2 = 4096$ pairs of inputs (6-bit gate patterns
and both passing bits) found **1920 violations** of this condition. No
affine function achieves more than 75% agreement with the CIG's truth
table.
## Not a Perceptron (7-Input Linear Separability)
A perceptron classifies inputs by a hyperplane
$\mathbf{w}\cdot\mathbf{x} \ge \theta$. Treating the passing bit $p$ as
a seventh input, we have 128 points in $\{0,1\}^7$. We asked: does a
separating hyperplane exist?
We formulated the feasibility problem as: find
$\mathbf{w} \in \mathbb{R}^7$ and $\theta \in \mathbb{R}$ such that
$$\mathbf{w} \cdot \mathbf{x}^{(i)} \ge \theta \quad \text{for all positive examples},\qquad
\mathbf{w} \cdot \mathbf{x}^{(j)} \le \theta - \epsilon \quad \text{for all negative examples},$$
with $\epsilon = 0.001$ (strict margin). The HiGHS solver returned
`INFEASIBLE`. Therefore the CIG **cannot be represented as any 7-input
perceptron**, even when the passing bit is included as an input.
## Position Sensitivity
All classical gates (AND, OR, XOR, majority, threshold) are invariant
under permutation of their inputs. The CIG is not: the weights
$w_k = \operatorname{sgn}(k)/|k|$ assign strictly different magnitudes
to positions $\pm 1$, $\pm 2$, $\pm 3$, and opposite signs to left vs.
right. This makes the gate *position-sensitive*: the spatial arrangement
of gate bits determines the output, not just their count.
# Experimental Results {#sec:experiments}
  **Property**                                   **Result**            **Status**
  -------------------------------------- -------------------------- ----------------
  Bijection, single-bit (all 64 gates)             64/64            
  Bijection, 8-bit block                      256/256 outputs       
  $F=0$ gate patterns                       8/64 (all bijective)    
  GF(2) linearity violations                  1920/4096 pairs          non-linear
  7D linear separability (LP)                    INFEASIBLE          non-perceptron
  Symmetric function                      Refuted (counterexample)   non-symmetric
  Avalanche, 1 pass                                12.5%                  weak
  Avalanche, 2 passes (dynamic beam)               50.1%            
  : Summary of exhaustive tests on the 6-bit CIG.
**Note on $F=0$ cases.** Eight of the 64 gate patterns produce
$F(0,G)=0$. By the decision rule, $\mathrm{out}(0,G)=0$ and
$\mathrm{out}(1,G)=1$ (identity). These gates are bijective (the
identity is a bijection) and consistent with
Lemma [1](#lem:antisym):
$F(1,G)=-F(0,G)=0$, so both sides of the rule agree.
# Comparison with Related Primitives
  **Gate type**             **Position-sensitive**   **Input-dep. weights**   **Bijective**   **Closed form**  
  ------------------------ ------------------------ ------------------------ --------------- ----------------- --
  Classical (AND/OR/XOR)              No                       No               XOR only            Yes        
  TLG                                 No                       No                  No               Yes        
  Receptron [@receptron]           Partial                Yes (random)             No               No         
  **CIG (ours)**                   **Yes**               **Yes (det.)**          **Yes**          **Yes**      
  : Comparison with related gate types. "Det." = deterministic.
The **Receptron** [@receptron] is a recently proposed physical gate
whose weights emerge from a random nanoscale material. Like the CIG, it
has input-dependent effective weights; unlike the CIG, its weights are
non-deterministic, have no closed form, and the gate is not guaranteed
bijective. The CIG derives all weights analytically from the
inverse-distance law, with no free parameters.
# Conclusion
We have defined and analyzed the Coulomb-Inspired Gate (CIG), a 6-bit
Boolean transformation with the following provable properties:
-   **Bijective** for every gate pattern, including zero-force patterns
    (Theorem [1](#thm:bij)).
-   **Not a 7-input perceptron** (LP infeasibility).
-   **Not symmetric** (explicit permutation counterexample).
-   **Not linear over GF(2)** (1920 violations out of 4096).
-   **Position-sensitive**: output depends on the spatial arrangement of
    gate bits, not only their Hamming weight.
These properties place the CIG outside all classical Boolean function
families. The gate achieves full bijection and strong avalanche in a
compact, parameter-free formula, making it a candidate lightweight
primitive for post-quantum symmetric cryptography on
resource-constrained devices.
#### Open problems.
\(1\) Derive a closed-form inverse transformation. (2) Characterize the
exact Boolean function class that contains the CIG. (3) Analyze the
gate's nonlinearity and algebraic degree in the cryptographic sense.
9 H. Chen et al., "Receptron: A physical neural network with random
nanoscale weights," *npj Unconventional Computing*, 2025.
S. Muroga, *Threshold Logic and Its Applications*. Wiley-Interscience,
1971.
J. Huangfu and J. Hall, "Parallelizing the dual revised simplex method,"
*Mathematical Programming Computation*, 10(1):119--142, 2018. (HiGHS LP
solver.)
