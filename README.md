# Coulomb-Inspired Gate (CIG)

**A Bijective, Position-Weighted, Input-Dependent Boolean Transformation for Quantum-Resistant Cryptography**

## Overview

The Coulomb-Inspired Gate (CIG) is a novel single-bit Boolean transformation inspired by the Coulomb force law from electrostatics. It defines a fundamentally new class of Boolean functions that exhibit position sensitivity and input-dependent behavior—properties absent from all classical Boolean gate families.

**Key Innovation:** Unlike AND, OR, XOR, and threshold logic gates, the CIG's output depends not only on the Hamming weight (count) of its inputs but also on their *spatial arrangement* in the bit neighborhood.

## Features

- ✅ **Bijective** for every possible 6-bit gate pattern (64/64 perfect bijection)
- ✅ **8-bit block transformation** achieves 256/256 bijection and 50.1% avalanche effect after two rounds
- ✅ **Position-sensitive**: weights scale with distance (1/|k|) and direction
- ✅ **Non-linear over GF(2)**: 1920/4096 linearity violations
- ✅ **Not a 7-input perceptron**: Linear programming proves mathematical impossibility
- ✅ **Deterministic closed-form**: No parameters; derived entirely from Coulomb's law
- ✅ **Lightweight**: Minimal computational overhead for IoT and embedded systems

## Mathematical Definition

### Coulomb Force Model

For a passing bit $p \in \{0,1\}$ through gate pattern $G = (g_{-3}, g_{-2}, g_{-1}, g_{+1}, g_{+2}, g_{+3})$:

$$F(p, G) = \sum_{k \in \{-3,-2,-1,+1,+2,+3\}} \frac{\operatorname{sgn}(k)}{|k|} \cdot Q(g_k, p)$$

where:
- **Charge function**: $Q(g, p) = +1$ if $g \neq p$ (opposite charge, attraction), $-1$ if $g = p$ (same charge, repulsion)
- **Weight vector**: $\mathbf{w} = (-\frac{1}{3}, -\frac{1}{2}, -1, +1, +\frac{1}{2}, +\frac{1}{3})$
- **Decision rule**:
  - If $p = 0$ (electron): output = 1 iff $F > 0$
  - If $p = 1$ (positron): output = 0 iff $F > 0$ (complementary behavior)

### Physical Intuition

- Logical **0** represents an electron ($e^-$)
- Logical **1** represents a positron ($e^+$)
- Same-charge neighbors **repel** the passing particle (subtract force)
- Opposite-charge neighbors **attract** the passing particle (add force)
- Net force determines whether the particle deflects and changes state

## Project Structure

```
EIDA-IOT/
├── README.md                        # This file
├── CIG_whitepaper.md                # Academic whitepaper (Markdown)
├── coulomb_8bit_transform.py        # Main CIG implementation (8-bit blocks)
├── eida_112.py                      # 112-bit EIDA variant tests
├── eida_128.py                      # 128-bit EIDA variant tests
├── coulomb_8bit_output.txt          # Test results from 8-bit variant
├── eida_results.txt                 # 112-bit test results
├── eida128_results.txt              # 128-bit test results
├── eida2_results.txt                # Additional test results
└── belgeler/                        # Documentation & whitepaper (excluded from git)
    ├── CIG_whitepaper.tex           # LaTeX source
    ├── CIG_whitepaper.pdf           # Compiled PDF
    ├── EIDA_COULOMB_KAPIT_KANITLARI_*.md
    └── EIDA_SESSION_OZET_*.md
```

## Installation & Usage

### Requirements

- Python 3.8+
- No external dependencies (pure Python implementation)

### Basic Usage

```python
from coulomb_8bit_transform import (
    coulomb_force_6,
    coulomb_bit,
    pass_through_8bit,
    int_to_bits,
    bits_to_int
)

# Create an 8-bit input and gate
state = int_to_bits(0b10101010, 8)  # Input: 170
gate = int_to_bits(0b00111001, 8)   # Gate: 57

# Apply CIG transformation
result = pass_through_8bit(state, gate)

print(f"Input:  {state} = {bits_to_int(state)}")
print(f"Gate:   {gate} = {bits_to_int(gate)}")
print(f"Output: {result} = {bits_to_int(result)}")
```

### Run Tests

```bash
python3 coulomb_8bit_transform.py
```

This executes:
1. Single transformation test with detailed analysis
2. Avalanche effect test (1 bit flip → output changes)
3. Bijection sampling (16 random gates × 256 inputs)
4. Ardışık dönüşüm demo (5 sequential rounds)

Output is saved to `coulomb_8bit_output.txt`.

## Experimental Results

| Property | Result | Status |
|----------|--------|--------|
| Bijection (all 64 gate patterns) | 64/64 | ✅ |
| Bijection (8-bit block) | 256/256 | ✅ |
| GF(2) linearity violations | 1920/4096 | ✗ Non-linear |
| 7D linear separability (LP) | INFEASIBLE | ✗ Non-perceptron |
| Symmetric function test | Refuted | ✗ Position-sensitive |
| Avalanche (1 pass) | 12.5% | ⚠️ Weak |
| Avalanche (2 passes) | 50.1% | ✅ Excellent |
| F=0 edge cases | 8/64 | ✅ All bijective |

## Non-Classical Properties

### Not Symmetric

A symmetric Boolean function depends only on Hamming weight (bit count), not position. CIG violates this:

```
Gate₁ = (1,1,1,0,0,0) → weight=3 → output = 0
Gate₂ = (0,0,0,1,1,1) → weight=3 → output = 1
```

Same Hamming weight, opposite outputs. **Conclusion:** CIG is position-sensitive.

### Not Linear over GF(2)

Classical linear functions satisfy $f(x \oplus y) = f(x) \oplus f(y)$ for all inputs. CIG violates this **1920 out of 4096 times**.

### Not a 7-Input Perceptron

Perceptrons are linear separable in their input space. Testing CIG as a 7-dimensional classifier (6 gate bits + 1 passing bit):

**Linear Program Result:** INFEASIBLE

This proves CIG cannot be represented by any 7-input perceptron, even with mixed weights and thresholds.

## Comparison with Related Primitives

| Gate Type | Position-Sensitive | Input-Dependent Weights | Bijective | Closed Form |
|-----------|-------------------|------------------------|-----------|------------|
| Classical (AND/OR/XOR) | ❌ | ❌ | ⚠️ (XOR only) | ✅ |
| Threshold Logic Gate (TLG) | ❌ | ❌ | ❌ | ✅ |
| Receptron (random nanoscale) | ⚠️ | ✅ (random) | ❌ | ❌ |
| **CIG (ours)** | **✅** | **✅ (deterministic)** | **✅** | **✅** |

## Why CIG?

### Cryptographic Motivation

- **Bijection guarantee** ensures 1-1 input-output mapping (no collisions)
- **Position sensitivity** provides non-trivial mixing with minimal computation
- **Avalanche effect** (50.1%) ensures small input changes → large output changes
- **Parameter-free** eliminates key schedule vulnerabilities
- **Lightweight** ideal for resource-constrained IoT devices

### For Post-Quantum IoT

As quantum computers threaten RSA/ECC, symmetric cryptography shifts to lattice-based and classical hard-problem schemes. CIG offers:
- Deterministic construction (no random parameters)
- Provable mathematical properties
- Minimal silicon footprint
- Direct physical interpretation (electrostatics)

## Future Work

1. **Derive closed-form inverse** for decryption without precomputation
2. **Characterize the Boolean function class** containing CIG
3. **Analyze algebraic degree** and nonlinearity in cryptographic sense
4. **Multi-block circular architecture** with fixed-capacity gates per round
5. **Hardware implementation** (FPGA/ASIC) for IoT edge devices

## Academic References

- **Whitepaper**: See [CIG_whitepaper.md](CIG_whitepaper.md) for full technical details
- **Receptron**: H. Chen et al., "Receptron: A physical neural network with random nanoscale weights," *npj Unconventional Computing*, 2025
- **Threshold Logic**: S. Muroga, *Threshold Logic and Its Applications*, Wiley-Interscience, 1971
- **LP Solver**: J. Huangfu & J. Hall, "Parallelizing the dual revised simplex method," *Mathematical Programming Computation*, 10(1):119–142, 2018

## Author

**Güven Acar**  
EIDA Project | Izmir, Turkey  
[guven@melp.dev](mailto:guven@melp.dev)

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Citation

If you use CIG in your research, please cite:

```bibtex
@software{acar2026cig,
  author = {Acar, Güven},
  title = {Coulomb-Inspired Gate (CIG): A Bijective, Position-Weighted Boolean Transformation},
  year = {2026},
  url = {https://github.com/guvenacar/Coulomb-Inspired-Gate},
  note = {EIDA Project, Izmir, Turkey}
}
```

## Contributing

Contributions are welcome! Areas of interest:
- Hardware implementations (Verilog, VHDL)
- Performance benchmarks on embedded systems
- Integration with cryptographic primitives
- Theoretical analysis of Boolean function properties

---

**Status:** Active Development  
**Last Updated:** May 2026  
**Maintainer:** Güven Acar
