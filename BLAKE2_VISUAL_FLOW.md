# BLAKE2 Visual Flow Diagrams and Process Maps
## Complete Visual Guide for Understanding BLAKE2

---

## 1. Overall BLAKE2 Algorithm Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    BLAKE2 COMPLETE FLOW                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   INPUT DATA    │
│  + Parameters   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  INITIALIZATION │
│  • Create IV    │
│  • Parameter    │
│    Block        │
│  • XOR with IV  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   KEY BLOCK     │
│   (if keyed)    │
│  Pad to 128B    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   DATA BLOCKS   │
│   Split into    │
│   128-byte      │
│   chunks        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│   COMPRESSION   │◄───┤  For Each Block │
│    FUNCTION     │    │   (128 bytes)   │
│  • 12 Rounds    │    └─────────────────┘
│  • G Functions  │
│  • State Update │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  FINAL BLOCK    │
│  • Zero pad     │
│  • Set final    │
│    flag         │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   EXTRACT       │
│   DIGEST        │
│  Truncate to    │
│  desired size   │
└─────────────────┘
```

---

## 2. G Function Detailed Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     G FUNCTION FLOW                            │
│              (Core of BLAKE2 Algorithm)                        │
└─────────────────────────────────────────────────────────────────┘

INPUT: v[a], v[b], v[c], v[d], x, y (message words)

┌─────────────────┐
│    STEP 1       │
│  v[a] += v[b]   │
│  v[a] += x      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 2       │
│ v[d] ^= v[a]    │
│ v[d] = rotr(    │
│   v[d], 32)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 3       │
│  v[c] += v[d]   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 4       │
│ v[b] ^= v[c]    │
│ v[b] = rotr(    │
│   v[b], 24)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 5       │
│  v[a] += v[b]   │
│  v[a] += y      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 6       │
│ v[d] ^= v[a]    │
│ v[d] = rotr(    │
│   v[d], 16)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 7       │
│  v[c] += v[d]   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    STEP 8       │
│ v[b] ^= v[c]    │
│ v[b] = rotr(    │
│   v[b], 63)     │
└─────────────────┘

OUTPUT: Modified v[a], v[b], v[c], v[d]
```

---

## 3. Compression Function Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  COMPRESSION FUNCTION                          │
│                  (Process One Block)                           │
└─────────────────────────────────────────────────────────────────┘

INPUT: 128-byte block, counter, is_final flag

┌─────────────────┐
│  Initialize     │
│  Working Vector │
│  v[0:7] = h     │
│  v[8:15] = IV   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Mix Counter   │
│ v[12] ^= low    │
│ v[13] ^= high   │
│ v[14] ^= final  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Parse Block    │
│  into 16 words  │
│  m[0] to m[15]  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐  ┌───────────────────┐
│   Round Loop    │  │  Round 0 to 11    │
│                 │◄─┤  (12 iterations)  │
│ ┌─────────────┐ │  └───────────────────┘
│ │ Column G's  │ │
│ │ (4 calls)   │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │ Diagonal G's│ │
│ │ (4 calls)   │ │
│ └─────────────┘ │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Update State   │
│  h[i] ^= v[i]   │
│       ^= v[i+8] │
└─────────────────┘

OUTPUT: Updated state h[0:7]
```

---

## 4. Round Structure (One Complete Round)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ONE COMPLETE ROUND                          │
│                   (Column + Diagonal)                          │
└─────────────────────────────────────────────────────────────────┘

Working Vector Layout:
┌─────┬─────┬─────┬─────┐
│ v0  │ v1  │ v2  │ v3  │
├─────┼─────┼─────┼─────┤
│ v4  │ v5  │ v6  │ v7  │
├─────┼─────┼─────┼─────┤
│ v8  │ v9  │ v10 │ v11 │
├─────┼─────┼─────┼─────┤
│ v12 │ v13 │ v14 │ v15 │
└─────┴─────┴─────┴─────┘

COLUMN ROUNDS (Vertical Mixing):
┌─────────────────┐
│   Column 0      │
│ G(v0,v4,v8,v12) │
│  m[σ[0]], m[σ[1]]│
└─────────────────┘
┌─────────────────┐
│   Column 1      │
│ G(v1,v5,v9,v13) │
│  m[σ[2]], m[σ[3]]│
└─────────────────┘
┌─────────────────┐
│   Column 2      │
│G(v2,v6,v10,v14) │
│  m[σ[4]], m[σ[5]]│
└─────────────────┘
┌─────────────────┐
│   Column 3      │
│G(v3,v7,v11,v15) │
│  m[σ[6]], m[σ[7]]│
└─────────────────┘

DIAGONAL ROUNDS (Diagonal Mixing):
┌─────────────────┐
│  Diagonal 0     │
│G(v0,v5,v10,v15) │
│  m[σ[8]], m[σ[9]]│
└─────────────────┘
┌─────────────────┐
│  Diagonal 1     │
│G(v1,v6,v11,v12) │
│ m[σ[10]],m[σ[11]]│
└─────────────────┘
┌─────────────────┐
│  Diagonal 2     │
│ G(v2,v7,v8,v13) │
│ m[σ[12]],m[σ[13]]│
└─────────────────┘
┌─────────────────┐
│  Diagonal 3     │
│ G(v3,v4,v9,v14) │
│ m[σ[14]],m[σ[15]]│
└─────────────────┘
```

---

## 5. State Evolution Through Rounds

```
┌─────────────────────────────────────────────────────────────────┐
│              STATE EVOLUTION VISUALIZATION                     │
└─────────────────────────────────────────────────────────────────┘

Initial State (after parameter block XOR):
h[0] = IV[0] ^ param_0
h[1] = IV[1] ^ param_1
...
h[7] = IV[7] ^ param_7

For Each Block:
┌─────────────────┐
│   h[0:7]        │ ────┐
│ (current state) │     │
└─────────────────┘     │
                        ▼
┌─────────────────┐  ┌─────────────────┐
│     IV[0:7]     │  │  Working Vector │
│  (constants)    │  │     v[0:15]     │
└─────────────────┘  │                 │
                     │ v[0:7] = h[0:7] │
                     │ v[8:15] = IV    │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  12 Rounds of   │
                     │  G Functions    │
                     │  (480 G calls)  │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  Feed Forward   │
                     │ h[i] ^= v[i] ^  │
                     │        v[i+8]   │
                     └─────────────────┘

Result: Updated h[0:7] for next iteration
```

---

## 6. Message Scheduling (Sigma) Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                 MESSAGE SCHEDULING                             │
│                    (Sigma Tables)                              │
└─────────────────────────────────────────────────────────────────┘

Message Block: m[0] m[1] m[2] m[3] m[4] m[5] m[6] m[7] 
               m[8] m[9] m[10] m[11] m[12] m[13] m[14] m[15]

Round 0 (Identity):
σ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

G Functions use:
┌─────┬─────┬──────┬──────┐
│ G0  │ G1  │  G2  │  G3  │ Column
├─────┼─────┼──────┼──────┤
│m[0] │m[2] │ m[4] │ m[6] │
│m[1] │m[3] │ m[5] │ m[7] │
└─────┴─────┴──────┴──────┘

┌─────┬─────┬──────┬──────┐
│ G4  │ G5  │  G6  │  G7  │ Diagonal  
├─────┼─────┼──────┼──────┤
│m[8] │m[10]│ m[12]│ m[14]│
│m[9] │m[11]│ m[13]│ m[15]│
└─────┴─────┴──────┴──────┘

Round 1 (Permuted):
σ = [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3]

G Functions use:
┌──────┬──────┬──────┬──────┐
│  G0  │  G1  │  G2  │  G3  │ Column
├──────┼──────┼──────┼──────┤
│m[14] │ m[4] │ m[9] │m[13] │
│m[10] │ m[8] │m[15] │ m[6] │
└──────┴──────┴──────┴──────┘

...and so on for all 12 rounds
```

---

## 7. Parameter Block Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                  PARAMETER BLOCK LAYOUT                        │
│                      (64 bytes)                                │
└─────────────────────────────────────────────────────────────────┘

Byte Layout:
┌─────┬──────┬────────────────────────────────────────────────────┐
│ 0   │  1   │ digest_size (1-64)                                │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 1   │  1   │ key_length (0-64)                                 │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 2   │  1   │ fanout (1 for sequential)                         │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 3   │  1   │ depth (1 for sequential)                          │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 4   │  4   │ leaf_length (0 = unlimited)                       │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 8   │  8   │ node_offset (0 for first node)                    │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 16  │  8   │ xof_length (0 for standard hash)                  │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 24  │  1   │ node_depth (0 for leaf)                           │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 25  │  1   │ inner_length (0 for leaf)                         │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 26  │  6   │ reserved (zeros)                                   │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 32  │  16  │ salt (padded with zeros)                           │
├─────┼──────┼────────────────────────────────────────────────────┤
│ 48  │  16  │ personalization (padded with zeros)                │
└─────┴──────┴────────────────────────────────────────────────────┘

Example for digest_size=32, key="abc", salt="salt", person="test":
┌──────┬──────────────────────────────────────────────────────────┐
│ Hex  │ Value                                                    │
├──────┼──────────────────────────────────────────────────────────┤
│ 20   │ digest_size = 32                                         │
│ 03   │ key_length = 3                                           │
│ 01   │ fanout = 1                                               │
│ 01   │ depth = 1                                                │
│ 00000000 │ leaf_length = 0                                     │
│ 0000000000000000 │ node_offset = 0                             │
│ 0000000000000000 │ xof_length = 0                              │
│ 00   │ node_depth = 0                                           │
│ 00   │ inner_length = 0                                         │
│ 000000000000 │ reserved                                         │
│ 73616c7400000000000000000000000000 │ "salt" + padding           │
│ 74657374000000000000000000000000 │ "test" + padding             │
└──────┴──────────────────────────────────────────────────────────┘
```

---

## 8. Key Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    KEY PROCESSING                              │
│                  (MAC Mode Setup)                              │
└─────────────────────────────────────────────────────────────────┘

Input: key = "secret_key" (variable length ≤ 64 bytes)

Step 1: Pad Key to Block Size
┌─────────────────┐
│   Original Key  │
│ "secret_key"    │ (10 bytes)
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Padded Key    │
│ "secret_key" +  │
│ 118 zero bytes  │ (128 bytes total)
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Process as    │
│   First Block   │
│ counter = 128   │
│ is_final = False│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   State After   │
│   Key Block     │
│ h[0:7] updated  │
└─────────────────┘

Then: Process actual message blocks normally
```

---

## 9. Rotation Operation Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                   ROTATION OPERATIONS                          │
└─────────────────────────────────────────────────────────────────┘

64-bit Right Rotation by 32:
Original: 0x123456789ABCDEF0
         ┌─ Bits 0-31 ──┐ ┌─ Bits 32-63 ─┐
         │ 9ABCDEF0     │ │ 12345678     │
         └──────────────┘ └──────────────┘
                 │               │
                 ▼               ▼
Result:   0xDEF0123456789ABC
         ┌─ From 32-63 ──┐ ┌─ From 0-31 ──┐
         │ DEF0         │ │ 123456789ABC │
         └──────────────┘ └──────────────┘

Implementation:
value = 0x123456789ABCDEF0
right_part = value >> 32        # 0x0000000012345678
left_part = value << (64-32)    # 0xDEF0000000000000
result = right_part | left_part # 0xDEF0123456789ABC
masked = result & 0xFFFFFFFFFFFFFFFF
```

---

## 10. Complete Example Trace

```
┌─────────────────────────────────────────────────────────────────┐
│                 BLAKE2b("abc") TRACE                           │
└─────────────────────────────────────────────────────────────────┘

Input: b"abc" (3 bytes)

Step 1: Initialization
├─ digest_size = 64
├─ key = b"" (empty)  
├─ salt = b"" (empty)
└─ person = b"" (empty)

Step 2: Parameter Block
├─ [64, 0, 1, 1, 0, 0, 0, 0, ...]
└─ XOR with IV → h[0:7]

Step 3: Message Processing  
├─ Buffer: b"abc"
├─ Length: 3 bytes (< 128)
└─ No complete blocks to process

Step 4: Finalization
├─ Pad: b"abc" + 125 zero bytes
├─ Counter: 3 (actual message length)
├─ is_final: True
└─ Process padded block

Step 5: Compression
├─ v[0:7] = h[0:7] (current state)
├─ v[8:15] = IV
├─ v[12] ^= 3 (counter)
├─ v[14] ^= 0xFFFFFFFFFFFFFFFF (final)
├─ m[0] = 0x0000000000636261 ("abc" + padding)
├─ m[1:15] = 0 (all zeros)
└─ 12 rounds of G functions

Step 6: Output
├─ Extract h[0:7] as bytes
├─ Result: ba80a53f981c4d0d6a2797b69f12f6e9...
└─ Expected: ba80a53f981c4d0d6a2797b69f12f6e9... ✓
```

---

## Study Tips for Exam/Presentation

### Key Visualization Points:
1. **Draw the 4x4 matrix** for working vector
2. **Show column vs diagonal** mixing patterns  
3. **Trace one G function** step by step
4. **Demonstrate sigma permutation** for one round
5. **Show parameter block** byte layout

### Important Diagrams to Practice:
1. Overall algorithm flow
2. G function internal steps
3. Round structure (column + diagonal)
4. State evolution through compression
5. Message scheduling pattern

### Presentation Flow Suggestion:
1. **Overview**: Why BLAKE2 is important
2. **Architecture**: High-level components
3. **Deep Dive**: G function mechanics
4. **Security**: How features provide security
5. **Performance**: Why it's fast
6. **Demo**: Live example or animation

This visual guide should help you understand the flow and explain it clearly in your exam and presentation!
