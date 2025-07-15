# BLAKE2 Complete Study Notes
## Comprehensive Guide for Exam and Presentation

---

## Table of Contents
1. [BLAKE2 Overview](#blake2-overview)
2. [Key Components](#key-components)
3. [Initialization Vectors (IV)](#initialization-vectors-iv)
4. [Sigma Permutation Tables](#sigma-permutation-tables)
5. [Parameter Block](#parameter-block)
6. [G Function (Core Mixing)](#g-function-core-mixing)
7. [Compression Function](#compression-function)
8. [Complete Algorithm Flow](#complete-algorithm-flow)
9. [BLAKE2b vs BLAKE2s Differences](#blake2b-vs-blake2s-differences)
10. [Security Features](#security-features)

---

## BLAKE2 Overview

**BLAKE2** is a cryptographic hash function designed to be:
- **Faster** than MD5, SHA-1, SHA-2, and SHA-3
- **More secure** than MD5 and SHA-1
- **Highly customizable** with various parameters

### Key Features:
- Two main variants: **BLAKE2b** (64-bit) and **BLAKE2s** (32-bit)
- Variable output size
- Optional keying for MAC functionality
- Salt and personalization support
- Tree hashing capabilities

---

## Key Components

### 1. **State Vector (h)**
- BLAKE2b: 8 × 64-bit words
- BLAKE2s: 8 × 32-bit words
- Stores the current hash state

### 2. **Working Vector (v)**
- BLAKE2b: 16 × 64-bit words
- BLAKE2s: 16 × 32-bit words
- Used during compression rounds

### 3. **Message Block**
- BLAKE2b: 128 bytes (16 × 64-bit words)
- BLAKE2s: 64 bytes (16 × 32-bit words)
- Input data processed in chunks

---

## Initialization Vectors (IV)

### What are IVs?
**Initialization Vectors** are constants used to initialize the hash state. They ensure that the algorithm starts with a known, secure state.

### BLAKE2b IV Values:
```python
IV = [
    0x6A09E667F3BCC908,  # First 64 bits of fractional part of sqrt(2)
    0xBB67AE8584CAA73B,  # First 64 bits of fractional part of sqrt(3)
    0x3C6EF372FE94F82B,  # First 64 bits of fractional part of sqrt(5)
    0xA54FF53A5F1D36F1,  # First 64 bits of fractional part of sqrt(7)
    0x510E527FADE682D1,  # First 64 bits of fractional part of sqrt(11)
    0x9B05688C2B3E6C1F,  # First 64 bits of fractional part of sqrt(13)
    0x1F83D9ABFB41BD6B,  # First 64 bits of fractional part of sqrt(17)
    0x5BE0CD19137E2179   # First 64 bits of fractional part of sqrt(19)
]
```

### BLAKE2s IV Values:
```python
IV = [
    0x6A09E667,  # First 32 bits of fractional part of sqrt(2)
    0xBB67AE85,  # First 32 bits of fractional part of sqrt(3)
    0x3C6EF372,  # First 32 bits of fractional part of sqrt(5)
    0xA54FF53A,  # First 32 bits of fractional part of sqrt(7)
    0x510E527F,  # First 32 bits of fractional part of sqrt(11)
    0x9B05688C,  # First 32 bits of fractional part of sqrt(13)
    0x1F83D9AB,  # First 32 bits of fractional part of sqrt(17)
    0x5BE0CD19   # First 32 bits of fractional part of sqrt(19)
]
```

### Why These Values?
- **Mathematical Constants**: Based on square roots of prime numbers
- **No Hidden Trapdoors**: Publicly verifiable generation method
- **Good Distribution**: Provide excellent avalanche effect

---

## Sigma Permutation Tables

### What is Sigma?
**Sigma (σ)** is a permutation table that determines which message words are used in each round of the G function. It ensures thorough mixing of input data.

### BLAKE2b Sigma (12 rounds):
```python
SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],  # Round 0
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],   # Round 1
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],   # Round 2
    # ... and so on for 12 rounds total
]
```

### BLAKE2s Sigma (10 rounds):
- Same pattern but only 10 rounds instead of 12

### Purpose of Sigma:
1. **Prevents Patterns**: Each round uses different message word combinations
2. **Ensures Mixing**: All message words influence all state words
3. **Cryptographic Strength**: Makes differential and linear attacks harder

---

## Parameter Block

### What is the Parameter Block?
A structured data block that contains configuration parameters for the hash function.

### BLAKE2b Parameter Block (64 bytes):
```
Offset | Size | Field
-------|------|-------
0      | 1    | Digest length (1-64)
1      | 1    | Key length (0-64)
2      | 1    | Fanout (1 for sequential)
3      | 1    | Depth (1 for sequential)
4      | 4    | Leaf length (0 = unlimited)
8      | 8    | Node offset
16     | 8    | XOF length (0 for regular hash)
24     | 1    | Node depth
25     | 1    | Inner length
26     | 14   | Reserved (zeros)
32     | 16   | Salt
48     | 16   | Personal
```

### BLAKE2s Parameter Block (32 bytes):
- Similar structure but smaller fields and total size

### Parameter Block Usage:
1. **Created during initialization**
2. **XORed with IV** to create initial state
3. **Customizes the hash function** behavior

---

## G Function (Core Mixing)

### What is the G Function?
The **G function** is the heart of BLAKE2. It mixes four words of the state using two message words.

### BLAKE2b G Function:
```python
def _g(self, v, a, b, c, d, x, y):
    # Round 1: Add and rotate
    v[a] = (v[a] + v[b] + x) & 0xFFFFFFFFFFFFFFFF
    v[d] = rotr64(v[d] ^ v[a], 32)
    
    # Round 2: Add and rotate  
    v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
    v[b] = rotr64(v[b] ^ v[c], 24)
    
    # Round 3: Add and rotate
    v[a] = (v[a] + v[b] + y) & 0xFFFFFFFFFFFFFFFF
    v[d] = rotr64(v[d] ^ v[a], 16)
    
    # Round 4: Add and rotate
    v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
    v[b] = rotr64(v[b] ^ v[c], 63)
```

### G Function Steps Explained:

#### Step 1: `v[a] = v[a] + v[b] + x`
- **Add** three values together
- **x** is a message word (from sigma permutation)
- **Overflow** is handled by masking to 64 bits

#### Step 2: `v[d] = rotr64(v[d] ^ v[a], 32)`
- **XOR** v[d] with the new v[a]
- **Rotate right** by 32 bits
- **Diffusion**: Changes propagate through the state

#### Step 3: `v[c] = v[c] + v[d]`
- **Add** the rotated value to v[c]
- **Continues** the mixing process

#### Step 4: `v[b] = rotr64(v[b] ^ v[c], 24)`
- **XOR** and **rotate** by 24 bits
- **Different rotation** amount for varied mixing

#### Steps 5-8: Repeat with different rotations
- Use second message word **y**
- Rotate by **16** and **63** bits
- **Complete mixing** of all four words

### Rotation Amounts:
- **BLAKE2b**: 32, 24, 16, 63 bits
- **BLAKE2s**: 16, 12, 8, 7 bits
- **Chosen** for optimal diffusion properties

---

## Compression Function

### What is Compression?
The **compression function** processes one block of input data and updates the hash state.

### Compression Steps:

#### 1. Initialize Working Vector
```python
v = list(self.h) + list(self.IV)
# v[0-7] = current state
# v[8-15] = IV constants
```

#### 2. Mix Counter and Final Flag
```python
v[12] ^= counter & 0xFFFFFFFFFFFFFFFF     # Low counter bits
v[13] ^= (counter >> 64) & 0xFFFFFFFFFFFFFFFF  # High counter bits
if is_final:
    v[14] ^= 0xFFFFFFFFFFFFFFFF  # Final block flag
```

#### 3. Convert Block to Words
```python
m = list(struct.unpack('<16Q', block))  # 16 message words
```

#### 4. Perform Mixing Rounds
```python
for round_num in range(12):  # 12 rounds for BLAKE2b
    sigma = self.SIGMA[round_num]
    
    # Column rounds (parallel processing)
    self._g(v, 0, 4, 8, 12, m[sigma[0]], m[sigma[1]])
    self._g(v, 1, 5, 9, 13, m[sigma[2]], m[sigma[3]])
    self._g(v, 2, 6, 10, 14, m[sigma[4]], m[sigma[5]])
    self._g(v, 3, 7, 11, 15, m[sigma[6]], m[sigma[7]])
    
    # Diagonal rounds (different mixing pattern)
    self._g(v, 0, 5, 10, 15, m[sigma[8]], m[sigma[9]])
    self._g(v, 1, 6, 11, 12, m[sigma[10]], m[sigma[11]])
    self._g(v, 2, 7, 8, 13, m[sigma[12]], m[sigma[13]])
    self._g(v, 3, 4, 9, 14, m[sigma[14]], m[sigma[15]])
```

#### 5. Update State
```python
for i in range(8):
    self.h[i] ^= v[i] ^ v[i + 8]
# XOR lower and upper halves with current state
```

---

## Complete Algorithm Flow

### 1. **Initialization Phase**
```
┌─────────────────┐
│   Initialize    │
│   Parameters    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Create Param   │
│     Block       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  h = IV XOR     │
│  param_block    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Process Key     │
│ (if present)    │
└─────────────────┘
```

### 2. **Update Phase** (for each data chunk)
```
┌─────────────────┐
│  Add data to    │
│    buffer       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Buffer full?   │
│  (128/64 bytes) │
└─────────┬───────┘
          │ YES
          ▼
┌─────────────────┐
│   Compress      │
│     Block       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Update counter  │
└─────────────────┘
```

### 3. **Finalization Phase**
```
┌─────────────────┐
│  Pad final      │
│    block        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Compress      │
│  final block    │
│ (with final=1)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Extract        │
│   digest        │
└─────────────────┘
```

---

## BLAKE2b vs BLAKE2s Differences

| Feature | BLAKE2b | BLAKE2s |
|---------|---------|---------|
| **Word Size** | 64-bit | 32-bit |
| **Block Size** | 128 bytes | 64 bytes |
| **Max Digest** | 64 bytes | 32 bytes |
| **Rounds** | 12 | 10 |
| **Key Size** | 0-64 bytes | 0-32 bytes |
| **Salt Size** | 16 bytes | 8 bytes |
| **Person Size** | 16 bytes | 8 bytes |
| **Rotations** | 32,24,16,63 | 16,12,8,7 |
| **Target Platform** | 64-bit systems | 8-32 bit systems |

---

## Security Features

### 1. **Avalanche Effect**
- **Small input change** → **Large output change**
- **Single bit flip** changes ~50% of output bits

### 2. **Preimage Resistance**
- **Computationally infeasible** to find input for given output
- **One-way function** property

### 3. **Collision Resistance**
- **Hard to find** two inputs with same output
- **Birthday attack** complexity: 2^(n/2)

### 4. **Customization Security**
- **Salt**: Prevents rainbow table attacks
- **Personalization**: Domain separation
- **Key**: Provides MAC functionality

### 5. **Side-Channel Resistance**
- **Constant-time** operations (when implemented properly)
- **No secret-dependent** memory access patterns

---

## Key Exam Points

### Remember These Formulas:
1. **G Function Structure**: 4 add-rotate-xor steps
2. **State Update**: `h[i] ^= v[i] ^ v[i+8]`
3. **Counter Mixing**: XOR with v[12] and v[13]
4. **Final Flag**: XOR 0xFFFF...FF with v[14]

### Important Constants:
- **BLAKE2b**: 64-bit words, 128-byte blocks, 12 rounds
- **BLAKE2s**: 32-bit words, 64-byte blocks, 10 rounds
- **IV**: Square roots of first 8 primes
- **Sigma**: 12/10 round permutation schedule

### Security Properties:
- **Fast**: Faster than SHA-2/SHA-3
- **Secure**: No known practical attacks
- **Flexible**: Variable output, keying, salt, personalization
- **Simple**: Easier to implement than SHA-3

---

## Presentation Tips

### Key Slides to Include:
1. **BLAKE2 Overview** - Why it's important
2. **Architecture Diagram** - Visual representation
3. **G Function Flow** - Core algorithm
4. **Compression Process** - Step-by-step
5. **Security Analysis** - Strength comparison
6. **Performance Benchmarks** - Speed comparison
7. **Use Cases** - Real-world applications

### Demo Ideas:
- **Live coding** of simple hash
- **Visualization** of state changes
- **Performance comparison** with other hash functions
- **Security test** showing avalanche effect

---

*This completes your comprehensive BLAKE2 study guide. Each section builds upon the previous ones, so study them in order for best understanding.*
