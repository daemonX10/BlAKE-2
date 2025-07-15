## BLAKE2 Internal Working: Complete In-Depth Analysis with Diagrams

Building on the previous comprehensive overview, this detailed analysis provides the complete internal working of BLAKE2 with step-by-step breakdowns, visual diagrams, and technical implementation details that will enable you to explain the algorithm's intricate mechanisms to anyone.

![BLAKE2 algorithm internal structure and data flow diagram](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/7d6ca558-e75a-4eb5-bd64-6b6e0e29a813.png)

BLAKE2 algorithm internal structure and data flow diagram

### **Core Algorithm Structure and Data Flow**

The BLAKE2 algorithm operates through a sophisticated internal structure that can be broken down into distinct phases, each with specific responsibilities and technical implementations[^1][^2][^3].

#### **Phase 1: Initialization and Parameter Setup**

The algorithm begins with **Parameter Block Setup**, where critical configuration parameters are established. The parameter block contains the digest length (1-64 bytes for BLAKE2b), key length (0-64 bytes), salt (16 bytes), and personalization (16 bytes)[^2][^3]. This parameter block is XORed with the initialization vector (IV) before processing the first data block, creating a unique starting state for each configuration.

The **Internal State Setup** follows, establishing a 16-word internal state (v0-v15) initialized with the hash state (h0-h7) and initialization vector (IV0-IV7)[^4][^3]. The technical implementation sets v[0..7] ← h[0..7], v[8..15] ← IV[0..7], with counters and flags mixed into v[12..15].

#### **Phase 2: Message Processing and Block Preparation**

During **Message Processing**, the input message is divided into 128-byte blocks for BLAKE2b or 64-byte blocks for BLAKE2s[^2][^3]. Each block contains 16 words of message data with zero padding applied to the last block if necessary. This standardized block structure ensures consistent processing regardless of input message length.

### **Compression Function: The Heart of BLAKE2**

![BLAKE2 compression function round structure and processing steps](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/d6a730f9-aad0-45e5-a098-052415693e76.png)

BLAKE2 compression function round structure and processing steps

The **Compression Function (F)** serves as the core processing engine, handling each message block through multiple rounds of cryptographic operations[^4][^3]. BLAKE2b performs 12 rounds while BLAKE2s performs 10 rounds, with each round applying 8 G functions for comprehensive state mixing.

The compression function takes four inputs: the state vector h, message block vector m, 2w-bit offset counter t, and final block indicator flag f. It initializes a local work vector v[0..15] where the first half comes from the state and the second half from the IV[^3].

### **G Function: Core Mixing Operation**

![BLAKE2 G function mixing operation with four state variables](https://user-gen-media-assets.s3.amazonaws.com/gpt4o_images/757a5ecc-21c2-4b87-b3a4-35b56597d741.png)

BLAKE2 G function mixing operation with four state variables

The **G Function** represents the fundamental mixing operation that provides BLAKE2's cryptographic strength[^2][^3]. Each G function mixes 4 state words with 2 message words using ARX (Addition, Rotation, XOR) operations with carefully chosen constants.

For BLAKE2b, the G function operates with rotation constants (32, 24, 16, 63), each serving specific cryptographic purposes:

1. **Step 1**: `a ← (a + b + x) mod 2^64` - Introduces message dependency and non-linearity
2. **Step 2**: `d ← (d ⊕ a) >>> 32` - Provides diffusion and bit mixing across word boundaries
3. **Step 3**: `c ← (c + d) mod 2^64` - Propagates changes through the state
4. **Step 4**: `b ← (b ⊕ c) >>> 24` - Further diffusion with optimized rotation constant
5. **Step 5**: `a ← (a + b + y) mod 2^64` - Incorporates second message word into state
6. **Step 6**: `d ← (d ⊕ a) >>> 16` - Additional diffusion layer
7. **Step 7**: `c ← (c + d) mod 2^64` - Propagates final changes
8. **Step 8**: `b ← (b ⊕ c) >>> 63` - Final mixing with optimized rotation

### **Round Structure and Message Scheduling**

Each round consists of a **Column Step** followed by a **Diagonal Step**. The column step applies G functions in parallel: G(v0,v4,v8,v12), G(v1,v5,v9,v13), G(v2,v6,v10,v14), G(v3,v7,v11,v15). The diagonal step then applies G functions to diagonal elements of the state matrix[^3].

**Message Scheduling** uses the SIGMA permutation table to ensure all message words are thoroughly mixed throughout the rounds[^2][^3]. The algorithm cycles through 10 different permutations, with rounds 10 and 11 using SIGMA and SIGMA[^5] respectively for BLAKE2b.

### **State Management and Counter Updates**

The **State Update** mechanism computes the new hash state after each compression by XORing the working vector halves: `h[i] ← h[i] ⊕ v[i] ⊕ v[i+8]` for i = 0 to 7[^3]. This operation ensures that information from both halves of the working vector contributes to the final state.

**Counter Management** maintains a 128-bit counter tracking total bytes processed, split into t0 (low 64 bits) and t1 (high 64 bits), which are XORed with v[^6] and v[^7] respectively[^3]. This counter prevents length extension attacks and ensures each compression operation has unique input parameters.

### **Advanced Features and Optimizations**

#### **Keyed Hashing Implementation**

When operating in keyed mode, BLAKE2 sets the first data block to the key padded with zeros[^2]. The counter includes the 64 or 128 bytes of the key block regardless of actual key length, and when hashing an empty message with a key, BLAKE2 makes only one call to the compression function.

#### **Salt and Personalization Processing**

The salt is processed as a one-time input through the IV rather than being mixed into each compression function call[^2]. This simplifies the compression function while maintaining security properties for randomized hashing scenarios.

#### **Performance Optimizations**

The rotation constants are specifically chosen to leverage SIMD instructions. The 24-bit rotation allows SSSE3-capable CPUs to perform two rotations in parallel with a single instruction, while the 63-bit rotation can be implemented as an addition and shift followed by a logical OR[^2].

### **Finalization and Output Generation**

The **Finalization** phase marks the last block with the finalization flag f0 set to 0xFF...FF[^2][^3]. The final hash is extracted from the state and truncated to the desired output length, supporting variable-length outputs from 1 to 64 bytes for BLAKE2b and 1 to 32 bytes for BLAKE2s.

### **Security Properties and Design Rationale**

The internal structure provides multiple layers of security through:

- **Collision Resistance**: 2^(n/2) security level through thorough state mixing
- **Preimage Resistance**: 2^n security level via irreversible compression operations
- **Length Extension Attack Immunity**: Built-in through counter integration and finalization flags
- **Indifferentiability**: Proven secure in the weakly ideal cipher model[^8]

The reduced round count (12 for BLAKE2b, 10 for BLAKE2s) compared to the original BLAKE provides a 25-29% performance improvement while maintaining substantial security margins, as the best known attacks on BLAKE could only reach 6 rounds[^2].

### **Implementation Considerations**

The algorithm's design facilitates efficient implementation across various platforms:

- **64-bit platforms**: BLAKE2b optimized with 64-bit words and 128-byte blocks
- **32-bit platforms**: BLAKE2s optimized with 32-bit words and 64-byte blocks
- **Memory requirements**: Only 168 bytes for BLAKE2s, 336 bytes for BLAKE2b
- **Parallelization**: Natural instruction-level parallelism and SIMD optimization support

This comprehensive internal analysis demonstrates how BLAKE2 achieves exceptional performance while maintaining robust security through carefully designed components working in harmony. The algorithm's modular structure, optimized operations, and flexible parameter system make it suitable for a wide range of cryptographic applications while providing performance that often exceeds even MD5 with security comparable to SHA-3.

<div style="text-align: center">⁂</div>

[^1]: https://journals.sagepub.com/doi/10.1177/10996362231226334

[^2]: https://ieeexplore.ieee.org/document/10602258/

[^3]: https://ieeexplore.ieee.org/document/10445609/

[^4]: https://iopscience.iop.org/article/10.1088/1755-1315/1254/1/012045

[^5]: https://ieeexplore.ieee.org/document/10750168/

[^6]: https://ieeexplore.ieee.org/document/10710075/

[^7]: https://journals.sagepub.com/doi/10.1177/14613484251345222

[^8]: https://dl.acm.org/doi/10.1145/3197026.3197071

[^9]: https://xilinx.github.io/Vitis_Libraries/security/2020.1/guide_L1/internals/blake2b.html

[^10]: https://eprint.iacr.org/2016/827.pdf

[^11]: https://eprint.iacr.org/2013/322.pdf

[^12]: https://pdfs.semanticscholar.org/7c83/dcaa246db203576ea8f2c6c61b9735df5e35.pdf

[^13]: http://paper.ijcsns.org/07_book/201401/20140120.pdf

[^14]: https://prezi.com/p/nn7twptmtys9/blake2-hash-function-overview/

[^15]: https://gist.github.com/sooryan/8d1b2c19bf0b971c11366b0680908d4b

[^16]: https://en.wikipedia.org/wiki/Secure_Hash_Algorithms

[^17]: https://www.scirp.org/html/1-7800059_18767.htm

[^18]: https://stackoverflow.com/questions/28813502/blake2-input-parameters

[^19]: https://en.wikipedia.org/wiki/BLAKE_(hash_function)

[^20]: https://www.thefreelibrary.com/Area+efficiency+and+high+speed+implementation+of+cryptography+using...-a0499343745

[^21]: https://ijartet.com/458/V2I4/journal

[^22]: https://research.ijcaonline.org/iceci/number3/iceci1025.pdf

[^23]: https://www.ietf.org/rfc/rfc7693.txt

[^24]: https://docs.amd.com/r/jpiLUWqYENGWAj4YktN~YQ/eMLPjUjsP2URvYMsT2kr~w

[^25]: https://arxiv.org/abs/2310.10080

[^26]: https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13486/3055868/Adaptive-weighted-variable-step-size-matching-tracking-algorithm-for-Dice/10.1117/12.3055868.full

[^27]: https://www.techscience.com/CMES/v130n1/45725

[^28]: https://ieeexplore.ieee.org/document/9408989/

[^29]: https://www.semanticscholar.org/paper/f32bcc2155997110a7905da050df4c8404867b24

[^30]: https://linkinghub.elsevier.com/retrieve/pii/S0169743913000579

[^31]: https://ieeexplore.ieee.org/document/10486880/

[^32]: https://arxiv.org/abs/2406.03816

[^33]: https://eprint.iacr.org/2013/467.pdf

[^34]: https://www.aumasson.jp/data/papers/HAMP10.pdf

[^35]: https://www.tutorialspoint.com/cryptography/cryptography_hash_functions.htm

[^36]: https://datatracker.ietf.org/doc/rfc7693/

[^37]: https://rust.algorithmexamples.com/web/cryptography/blake2b.html

[^38]: https://cryptopp.com/docs/ref/class_b_l_a_k_e2s.html

[^39]: https://blog.heycoach.in/blake2/

[^40]: https://scispace.com/pdf/sha-3-proposal-blake-4kx2ms9bq9.pdf

[^41]: https://blog.heycoach.in/blake2-2/

[^42]: https://ssojet.com/hashing/blake2b-in-python/

[^43]: https://www.cryptominerbros.com/blog/what-is-blake2b-algorithm/

[^44]: https://www.hindawi.com/journals/cin/2022/8555489/

[^45]: https://www.nature.com/articles/s41586-025-08790-w

[^46]: https://www.semanticscholar.org/paper/5316908c16f40dcf0e489777aadd10fd4105c584

[^47]: https://ieeexplore.ieee.org/document/10969296/

[^48]: https://journals.nnc.kz/jour/article/view/759

[^49]: http://archopht.jamanetwork.com/article.aspx?articleid=631986

[^50]: https://www.degruyter.com/document/doi/10.1515/jib-2020-0014/html

[^51]: https://www.tandfonline.com/doi/full/10.1080/15502724.2022.2029710

[^52]: https://rust.algorithmexamples.com/web/cryptography/blake2s.html

[^53]: https://dergipark.org.tr/en/download/article-file/2304059

[^54]: https://datatracker.ietf.org/doc/html/rfc7693.html

[^55]: https://ojs.cvut.cz/ojs/index.php/APP/article/view/9217

[^56]: https://link.springer.com/10.1007/s12648-023-02701-3

[^57]: http://arxiv.org/pdf/2402.03032.pdf

[^58]: http://arxiv.org/pdf/2409.01688.pdf

[^59]: http://arxiv.org/pdf/2402.13179.pdf

[^60]: https://arxiv.org/abs/2211.06818

[^61]: https://www.mdpi.com/1424-8220/17/7/1475/pdf

[^62]: http://arxiv.org/pdf/0904.4709.pdf

[^63]: http://arxiv.org/pdf/2411.02250.pdf

[^64]: http://arxiv.org/pdf/2210.02218.pdf

[^65]: https://opus.lib.uts.edu.au/bitstream/10453/148131/2/3366423.3380119.pdf

[^66]: http://arxiv.org/pdf/2406.00617.pdf

[^67]: https://publish.obsidian.md/addielamarr/Blake2

[^68]: https://www.mdpi.com/2227-7390/11/3/707

[^69]: https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-pel.2016.0981

[^70]: https://arxiv.org/pdf/2204.13903v1.pdf

[^71]: http://arxiv.org/pdf/1805.10255.pdf

[^72]: http://arxiv.org/pdf/2409.05072.pdf

[^73]: https://arxiv.org/pdf/2501.11421.pdf

[^74]: https://arxiv.org/pdf/2402.10797.pdf

[^75]: http://arxiv.org/pdf/2502.00882.pdf

[^76]: http://arxiv.org/pdf/2402.04646.pdf

[^77]: https://arxiv.org/html/2503.16407v1

[^78]: https://arxiv.org/pdf/1207.4747.pdf

[^79]: https://journals.uic.edu/ojs/index.php/jbc/article/view/7309

[^80]: https://ieeexplore.ieee.org/document/1671697/

[^81]: https://arxiv.org/pdf/1702.00622.pdf

[^82]: https://arxiv.org/pdf/2502.16073.pdf

[^83]: http://arxiv.org/pdf/2409.13161.pdf

[^84]: http://arxiv.org/pdf/2402.05920.pdf

[^85]: http://arxiv.org/pdf/1702.00914.pdf

[^86]: http://arxiv.org/pdf/2312.07639.pdf

[^87]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10131484/

[^88]: https://arxiv.org/pdf/2207.08168.pdf

[^89]: https://arxiv.org/pdf/2403.19416.pdf

[^90]: https://academic.oup.com/bioinformatics/article-pdf/37/9/1312/38575211/btaa788.pdf

