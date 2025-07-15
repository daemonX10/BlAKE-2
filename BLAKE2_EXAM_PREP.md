# BLAKE2 Exam Preparation Guide
## Complete Study Checklist and Key Points

---

## Exam Question Types You Should Expect

### 1. **Conceptual Questions**
- What is BLAKE2 and why was it created?
- How does BLAKE2 differ from SHA-2 and SHA-3?
- What are the security advantages of BLAKE2?

### 2. **Technical Implementation Questions**
- Explain the G function and its 8 steps
- What is the purpose of the sigma permutation?
- How does the compression function work?
- What is the parameter block and why is it important?

### 3. **Mathematical Questions**
- Calculate specific G function operations
- Show how rotation operations work
- Demonstrate state evolution through one round

### 4. **Security Analysis Questions**
- Explain the avalanche effect in BLAKE2
- How does keyed hashing provide MAC functionality?
- What prevents length extension attacks?

---

## Key Facts to Memorize

### BLAKE2b Specifications:
- **Word Size**: 64-bit
- **Block Size**: 128 bytes
- **State Size**: 8 × 64-bit words (512 bits)
- **Rounds**: 12
- **Max Output**: 64 bytes
- **Max Key**: 64 bytes
- **Rotations**: 32, 24, 16, 63 bits

### BLAKE2s Specifications:
- **Word Size**: 32-bit
- **Block Size**: 64 bytes
- **State Size**: 8 × 32-bit words (256 bits)
- **Rounds**: 10
- **Max Output**: 32 bytes
- **Max Key**: 32 bytes
- **Rotations**: 16, 12, 8, 7 bits

### Initialization Vectors:
- Based on **square roots of first 8 primes**: 2, 3, 5, 7, 11, 13, 17, 19
- Take **fractional parts** of square roots
- Convert to **64-bit** (BLAKE2b) or **32-bit** (BLAKE2s) integers

---

## Step-by-Step Algorithm (MUST KNOW)

### 1. Initialization Phase:
```
1. Create parameter block (64 bytes for BLAKE2b)
2. Initialize state: h[0:7] = IV[0:7] XOR param_block_words
3. If keyed: process padded key as first block
```

### 2. Update Phase (for each complete block):
```
1. Add data to buffer
2. When buffer ≥ block_size:
   a. Extract one block
   b. Increment counter
   c. Call compression function
   d. Update state
```

### 3. Finalization Phase:
```
1. Pad remaining data with zeros
2. Set final flag = true
3. Process final block
4. Extract digest (truncate if needed)
```

---

## G Function - CRITICAL TO UNDERSTAND

### The Complete G Function (BLAKE2b):
```python
def G(v, a, b, c, d, x, y):
    # Step 1
    v[a] = (v[a] + v[b] + x) & 0xFFFFFFFFFFFFFFFF
    v[d] = rotr64(v[d] ^ v[a], 32)
    
    # Step 2  
    v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
    v[b] = rotr64(v[b] ^ v[c], 24)
    
    # Step 3
    v[a] = (v[a] + v[b] + y) & 0xFFFFFFFFFFFFFFFF
    v[d] = rotr64(v[d] ^ v[a], 16)
    
    # Step 4
    v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
    v[b] = rotr64(v[b] ^ v[c], 63)
```

### What Each Step Does:
1. **Addition + Rotation**: Mixes message word x with state
2. **Propagation**: Spreads changes through the quartet
3. **Second Message**: Incorporates message word y
4. **Final Mix**: Completes the mixing process

---

## Compression Function Flow (ESSENTIAL)

### Working Vector Setup:
```
v[0:7]  = h[0:7]  (current state)
v[8:15] = IV[0:7] (constants)
```

### Counter and Final Flag:
```
v[12] ^= counter_low
v[13] ^= counter_high  
if final_block:
    v[14] ^= 0xFFFFFFFFFFFFFFFF
```

### Round Structure:
```
For round = 0 to 11:
    sigma = SIGMA[round]
    
    # Column rounds (4 G functions)
    G(v, 0, 4, 8, 12, m[sigma[0]], m[sigma[1]])
    G(v, 1, 5, 9, 13, m[sigma[2]], m[sigma[3]])
    G(v, 2, 6, 10, 14, m[sigma[4]], m[sigma[5]])
    G(v, 3, 7, 11, 15, m[sigma[6]], m[sigma[7]])
    
    # Diagonal rounds (4 G functions)
    G(v, 0, 5, 10, 15, m[sigma[8]], m[sigma[9]])
    G(v, 1, 6, 11, 12, m[sigma[10]], m[sigma[11]])
    G(v, 2, 7, 8, 13, m[sigma[12]], m[sigma[13]])
    G(v, 3, 4, 9, 14, m[sigma[14]], m[sigma[15]])
```

### State Update:
```
For i = 0 to 7:
    h[i] ^= v[i] ^ v[i+8]
```

---

## Security Features (EXAM FAVORITES)

### 1. **Avalanche Effect**
- **Definition**: Small input change → Large output change
- **Target**: ~50% of output bits should flip
- **Achieved by**: Rotation + XOR operations in G function

### 2. **Preimage Resistance**
- **Definition**: Hard to find input for given output
- **Strength**: 2^n operations for n-bit output
- **Mechanism**: One-way compression function

### 3. **Collision Resistance**
- **Definition**: Hard to find two inputs with same output
- **Strength**: 2^(n/2) operations (birthday attack)
- **Protection**: Strong mixing in compression function

### 4. **Length Extension Prevention**
- **Attack**: Add data to message without knowing original
- **Prevention**: Counter in compression function
- **Mechanism**: Different counter for each block

### 5. **MAC Security** (when keyed)
- **Purpose**: Message authentication
- **Strength**: Key provides authentication
- **Implementation**: Key as first block

---

## Common Exam Calculations

### 1. Rotation Example:
```
rotr64(0x123456789ABCDEF0, 32) = ?

Step 1: Split 64-bit value
  High 32: 0x12345678
  Low 32:  0x9ABCDEF0

Step 2: Swap positions  
  Result: 0x9ABCDEF012345678
```

### 2. G Function Step Calculation:
```
Given: v[a]=0x1000, v[b]=0x2000, x=0x0100
Calculate: v[a] = v[a] + v[b] + x

Step 1: Add values
  0x1000 + 0x2000 + 0x0100 = 0x3100

Step 2: Mask to 64 bits (if needed)
  0x3100 & 0xFFFFFFFFFFFFFFFF = 0x3100
```

### 3. Block Count Calculation:
```
Message length: 1000 bytes
Block size (BLAKE2b): 128 bytes

Complete blocks: 1000 ÷ 128 = 7 complete blocks
Remaining: 1000 - (7 × 128) = 1000 - 896 = 104 bytes
Total blocks processed: 7 + 1 (final) = 8 blocks
```

---

## Presentation Talking Points

### Why BLAKE2 is Important:
1. **Speed**: Faster than SHA-2, SHA-3, MD5
2. **Security**: No known practical attacks
3. **Flexibility**: Variable output, keying, salt, personalization
4. **Simplicity**: Easier to implement correctly

### Key Innovations:
1. **ARX Design**: Add-Rotate-XOR operations
2. **Parallel-friendly**: SIMD optimization possible
3. **Tree hashing**: Supports parallel processing
4. **Built-in MAC**: No need for HMAC construction

### Real-world Usage:
1. **Argon2**: Password hashing (Argon2 uses BLAKE2b)
2. **WireGuard**: VPN protocol
3. **Signal**: Secure messaging
4. **Various cryptocurrencies**: Bitcoin Cash, others

---

## Demo Script Commands

Run the interactive demo for live examples:
```bash
python blake2_demo_interactive.py
```

Key demos to show:
1. **G Function**: Step-by-step calculation
2. **Avalanche Effect**: One bit change → 50% output change
3. **Keyed Hashing**: Same message, different keys
4. **Variable Output**: Different digest sizes

---

## Practice Problems

### Problem 1: Basic Understanding
**Q**: Explain why BLAKE2 uses 12 rounds for BLAKE2b but only 10 for BLAKE2s.
**A**: BLAKE2b targets 64-bit platforms with more computational power, so it can afford more rounds for additional security margin. BLAKE2s targets smaller platforms where fewer rounds provide better performance while maintaining adequate security.

### Problem 2: Security Analysis  
**Q**: How does the counter prevent length extension attacks?
**A**: The counter is XORed into the working vector before compression. Each block has a different counter value, so an attacker cannot simply append data to extend the message - the counter would be wrong for the additional blocks.

### Problem 3: Implementation Details
**Q**: Why are message words permuted differently in each round?
**A**: The sigma permutation ensures that all message words interact with all state words over the course of the compression function. This provides thorough mixing and prevents differential/linear attacks that might exploit fixed word positions.

### Problem 4: Performance Analysis
**Q**: Calculate the number of operations in one BLAKE2b compression.
**A**: 
- 12 rounds × 8 G functions per round = 96 G function calls
- Each G function: 8 operations (4 additions, 4 XORs, 4 rotations)
- Total: 96 × 8 = 768 primitive operations per block

---

## Last-Minute Review Checklist

### Core Concepts ✓
- [ ] BLAKE2 purpose and advantages
- [ ] BLAKE2b vs BLAKE2s differences
- [ ] ARX (Add-Rotate-XOR) design principle

### Technical Details ✓
- [ ] G function 8-step process
- [ ] Compression function flow
- [ ] Parameter block structure
- [ ] Sigma permutation purpose

### Security Properties ✓
- [ ] Avalanche effect mechanism
- [ ] Preimage/collision resistance
- [ ] Length extension prevention
- [ ] MAC functionality

### Implementation ✓
- [ ] Initialization process
- [ ] Block processing loop
- [ ] Finalization steps
- [ ] Output extraction

### Calculations ✓
- [ ] Rotation operations
- [ ] Block count calculations
- [ ] G function step execution
- [ ] State evolution tracking

---

## Final Exam Tips

### Before the Exam:
1. **Run the demo script** multiple times
2. **Practice drawing** the compression function flow
3. **Memorize** the rotation amounts and round counts
4. **Understand** why each security feature works

### During the Exam:
1. **Read questions carefully** - distinguish BLAKE2b from BLAKE2s
2. **Show your work** for calculations
3. **Use diagrams** when explaining algorithms
4. **Reference specific numbers** (rounds, block sizes, etc.)

### For Presentations:
1. **Start with motivation** - why BLAKE2 exists
2. **Use visual aids** - flow diagrams are essential
3. **Include live demo** - show avalanche effect
4. **Compare performance** - speed vs other hash functions
5. **Explain real-world usage** - where it's actually used

**Good luck with your exam and presentation!** 🍀
