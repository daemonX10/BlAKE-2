#!/usr/bin/env python3
"""
BLAKE2 Interactive Demo and Learning Tool
This script provides step-by-step demonstrations of BLAKE2 operations
for educational purposes - perfect for exams and presentations!
"""

import sys
import struct
from blake2_implementation import BLAKE2b, BLAKE2s

class BLAKE2Demo:
    """Interactive demonstration of BLAKE2 internals"""
    
    def __init__(self):
        self.show_details = True
        
    def print_section(self, title):
        """Print a formatted section header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
    
    def print_subsection(self, title):
        """Print a formatted subsection header"""
        print(f"\n--- {title} ---")
    
    def hex_format(self, data, width=16):
        """Format binary data as hex with spacing"""
        if isinstance(data, int):
            # Convert integer to hex string
            hex_str = f"{data:016x}" if data.bit_length() > 32 else f"{data:08x}"
            return hex_str
        elif isinstance(data, (bytes, bytearray)):
            # Convert bytes to hex string with spacing
            hex_chars = data.hex()
            return ' '.join(hex_chars[i:i+2] for i in range(0, len(hex_chars), 2))
        else:
            return str(data)
    
    def demo_initialization_vectors(self):
        """Demonstrate IV generation and purpose"""
        self.print_section("INITIALIZATION VECTORS (IV) EXPLANATION")
        
        print("BLAKE2 uses mathematical constants derived from square roots of primes:")
        print("\nBLAKE2b IV (64-bit words):")
        
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        for i, (iv_val, prime) in enumerate(zip(BLAKE2b.IV, primes)):
            print(f"IV[{i}] = 0x{iv_val:016x}  # sqrt({prime}) fractional part")
        
        print("\nBLAKE2s IV (32-bit words):")
        for i, (iv_val, prime) in enumerate(zip(BLAKE2s.IV, primes)):
            print(f"IV[{i}] = 0x{iv_val:08x}      # sqrt({prime}) fractional part")
        
        print("\nWhy these values?")
        print("• Mathematical: Based on well-known constants")
        print("• No hidden backdoors: Publicly verifiable")
        print("• Good distribution: Provide excellent mixing")
        
    def demo_parameter_block(self):
        """Demonstrate parameter block creation"""
        self.print_section("PARAMETER BLOCK DEMONSTRATION")
        
        # Create a BLAKE2b instance with various parameters
        hasher = BLAKE2b(digest_size=32, key=b"mykey", salt=b"mysalt", person=b"demo")
        param_block = hasher._create_parameter_block()
        
        print("Parameter Block for BLAKE2b(digest_size=32, key='mykey', salt='mysalt', person='demo'):")
        print(f"Raw bytes: {self.hex_format(param_block)}")
        
        print("\nByte-by-byte breakdown:")
        print(f"Byte 0: {param_block[0]:02x} = digest_size (32)")
        print(f"Byte 1: {param_block[1]:02x} = key_length (5)")
        print(f"Byte 2: {param_block[2]:02x} = fanout (1)")
        print(f"Byte 3: {param_block[3]:02x} = depth (1)")
        
        leaf_length = struct.unpack('<I', param_block[4:8])[0]
        print(f"Bytes 4-7: {leaf_length:08x} = leaf_length (0)")
        
        node_offset = struct.unpack('<Q', param_block[8:16])[0]
        print(f"Bytes 8-15: {node_offset:016x} = node_offset (0)")
        
        xof_length = struct.unpack('<Q', param_block[16:24])[0]  
        print(f"Bytes 16-23: {xof_length:016x} = xof_length (0)")
        
        print(f"Bytes 32-47: {self.hex_format(param_block[32:48])} = salt ('mysalt' + padding)")
        print(f"Bytes 48-63: {self.hex_format(param_block[48:64])} = person ('demo' + padding)")
        
    def demo_g_function(self):
        """Demonstrate G function step by step"""
        self.print_section("G FUNCTION STEP-BY-STEP DEMONSTRATION")
        
        # Create a simple example
        v = [0x123456789ABCDEF0, 0xFEDCBA9876543210, 0xAAAAAAAAAAAAAAAA, 0x5555555555555555]
        x = 0x1111111111111111
        y = 0x2222222222222222
        
        print("Input values:")
        print(f"v[a] = 0x{v[0]:016x}")
        print(f"v[b] = 0x{v[1]:016x}")  
        print(f"v[c] = 0x{v[2]:016x}")
        print(f"v[d] = 0x{v[3]:016x}")
        print(f"x    = 0x{x:016x}")
        print(f"y    = 0x{y:016x}")
        
        # Manual G function implementation for demonstration
        print("\nStep-by-step G function execution:")
        
        print("\nStep 1: v[a] = v[a] + v[b] + x")
        old_a = v[0]
        v[0] = (v[0] + v[1] + x) & 0xFFFFFFFFFFFFFFFF
        print(f"v[a] = 0x{old_a:016x} + 0x{v[1]:016x} + 0x{x:016x}")
        print(f"     = 0x{v[0]:016x}")
        
        print("\nStep 2: v[d] = rotr64(v[d] ^ v[a], 32)")
        old_d = v[3]
        v[3] = v[3] ^ v[0]
        print(f"v[d] = 0x{old_d:016x} ^ 0x{v[0]:016x} = 0x{v[3]:016x}")
        v[3] = ((v[3] >> 32) | (v[3] << 32)) & 0xFFFFFFFFFFFFFFFF
        print(f"rotr64(0x{(v[3] << 32 | v[3] >> 32) & 0xFFFFFFFFFFFFFFFF:016x}, 32) = 0x{v[3]:016x}")
        
        print("\nStep 3: v[c] = v[c] + v[d]")
        old_c = v[2]
        v[2] = (v[2] + v[3]) & 0xFFFFFFFFFFFFFFFF
        print(f"v[c] = 0x{old_c:016x} + 0x{v[3]:016x} = 0x{v[2]:016x}")
        
        print("\nStep 4: v[b] = rotr64(v[b] ^ v[c], 24)")
        old_b = v[1]
        v[1] = v[1] ^ v[2]
        print(f"v[b] = 0x{old_b:016x} ^ 0x{v[2]:016x} = 0x{v[1]:016x}")
        v[1] = ((v[1] >> 24) | (v[1] << 40)) & 0xFFFFFFFFFFFFFFFF
        print(f"rotr64(prev_value, 24) = 0x{v[1]:016x}")
        
        # Continue with remaining steps...
        print("\n[Steps 5-8 continue with second message word y...]")
        
        print("\nFinal values:")
        for i, val in enumerate(v):
            print(f"v[{i}] = 0x{val:016x}")
    
    def demo_sigma_permutation(self):
        """Demonstrate sigma permutation tables"""
        self.print_section("SIGMA PERMUTATION DEMONSTRATION")
        
        print("BLAKE2b uses 12 rounds with different message word orderings:")
        print("\nMessage words: m[0] m[1] m[2] m[3] m[4] m[5] m[6] m[7] m[8] m[9] m[10] m[11] m[12] m[13] m[14] m[15]")
        
        for round_num in range(min(4, len(BLAKE2b.SIGMA))):  # Show first 4 rounds
            sigma = BLAKE2b.SIGMA[round_num]
            print(f"\nRound {round_num}:")
            print(f"Sigma: {sigma}")
            
            print("G function calls:")
            print(f"  Column G0: m[{sigma[0]}], m[{sigma[1]}]   Column G1: m[{sigma[2]}], m[{sigma[3]}]")
            print(f"  Column G2: m[{sigma[4]}], m[{sigma[5]}]   Column G3: m[{sigma[6]}], m[{sigma[7]}]")
            print(f"  Diag G4:   m[{sigma[8]}], m[{sigma[9]}]   Diag G5:   m[{sigma[10]}], m[{sigma[11]}]")
            print(f"  Diag G6:   m[{sigma[12]}], m[{sigma[13]}]  Diag G7:   m[{sigma[14]}], m[{sigma[15]}]")
        
        print("\n... (8 more rounds with different permutations)")
        print("\nKey property: Each round uses all 16 message words exactly once!")
    
    def demo_compression_function(self):
        """Demonstrate compression function"""
        self.print_section("COMPRESSION FUNCTION DEMONSTRATION")
        
        # Create a simple message block (exactly 128 bytes)
        message = b"Hello, BLAKE2! This is a demo message block of exactly 128 bytes for BLAKE2b processing!" + b"x" * 37
        
        print(f"Input block (128 bytes): {self.hex_format(message[:32])}...")
        
        # Create hasher and show initial state
        hasher = BLAKE2b(64)
        print(f"\nInitial state h[0:7]:")
        for i, val in enumerate(hasher.h):
            print(f"h[{i}] = 0x{val:016x}")
        
        print(f"\nProcessing block with counter=128, is_final=False")
        hasher._compress(message, 128, False)
        
        print(f"\nState after compression:")
        for i, val in enumerate(hasher.h):
            print(f"h[{i}] = 0x{val:016x}")
        
        print("\nNote: The state has been thoroughly mixed by 12 rounds of G functions!")
    
    def demo_full_hash_example(self):
        """Demonstrate complete hash computation"""
        self.print_section("COMPLETE HASH EXAMPLE")
        
        test_inputs = [
            b"",
            b"abc", 
            b"The quick brown fox jumps over the lazy dog",
            b"a" * 1000  # Multi-block input
        ]
        
        for i, data in enumerate(test_inputs):
            print(f"\nExample {i+1}: {len(data)} bytes")
            if len(data) <= 50:
                print(f"Input: {data}")
            else:
                print(f"Input: {data[:47]}... ({len(data)} bytes total)")
            
            # BLAKE2b
            hasher_b = BLAKE2b(32)  # 32-byte output for easier display
            hasher_b.update(data)
            result_b = hasher_b.hexdigest()
            print(f"BLAKE2b-256: {result_b}")
            
            # BLAKE2s  
            hasher_s = BLAKE2s(32)
            hasher_s.update(data)
            result_s = hasher_s.hexdigest()
            print(f"BLAKE2s-256: {result_s}")
            
            # Show number of blocks processed
            blocks_b = (len(data) + 127) // 128  # Ceiling division
            blocks_s = (len(data) + 63) // 64
            print(f"Blocks processed - BLAKE2b: {blocks_b}, BLAKE2s: {blocks_s}")
    
    def demo_keyed_hashing(self):
        """Demonstrate keyed hashing (MAC functionality)"""
        self.print_section("KEYED HASHING (MAC) DEMONSTRATION")
        
        message = b"This is a secret message"
        key1 = b"secret_key_123"
        key2 = b"different_key_456"
        
        print(f"Message: {message}")
        print(f"Key 1: {key1}")
        print(f"Key 2: {key2}")
        
        # Hash with first key
        hasher1 = BLAKE2b(32, key=key1)
        hasher1.update(message)
        mac1 = hasher1.hexdigest()
        
        # Hash with second key  
        hasher2 = BLAKE2b(32, key=key2)
        hasher2.update(message)
        mac2 = hasher2.hexdigest()
        
        # Hash without key
        hasher3 = BLAKE2b(32)
        hasher3.update(message)
        hash3 = hasher3.hexdigest()
        
        print(f"\nMAC with key1: {mac1}")
        print(f"MAC with key2: {mac2}")
        print(f"Hash (no key): {hash3}")
        
        print("\nObservations:")
        print("• Different keys produce completely different outputs")
        print("• Keyed and unkeyed hashes are totally different")
        print("• This provides Message Authentication Code functionality")
    
    def demo_avalanche_effect(self):
        """Demonstrate avalanche effect"""
        self.print_section("AVALANCHE EFFECT DEMONSTRATION")
        
        # Two inputs differing by one bit
        input1 = b"Hello, World!"
        input2 = b"Hello, World?"  # Last character changed
        
        hasher1 = BLAKE2b(32)
        hasher1.update(input1)
        hash1 = hasher1.digest()
        
        hasher2 = BLAKE2b(32)
        hasher2.update(input2)
        hash2 = hasher2.digest()
        
        print(f"Input 1: {input1}")
        print(f"Input 2: {input2}")
        print(f"         {'':>len(str(input1))}^ (1 character difference)")
        
        print(f"\nHash 1: {self.hex_format(hash1)}")
        print(f"Hash 2: {self.hex_format(hash2)}")
        
        # Count different bits
        different_bits = 0
        for b1, b2 in zip(hash1, hash2):
            different_bits += bin(b1 ^ b2).count('1')
        
        total_bits = len(hash1) * 8
        percentage = (different_bits / total_bits) * 100
        
        print(f"\nBit differences: {different_bits} out of {total_bits} ({percentage:.1f}%)")
        print("Good avalanche effect: ~50% of bits should change")
    
    def demo_variable_output_size(self):
        """Demonstrate variable output sizes"""
        self.print_section("VARIABLE OUTPUT SIZE DEMONSTRATION")
        
        message = b"Fixed input message"
        sizes = [1, 8, 16, 32, 48, 64]  # Different output sizes
        
        print(f"Input: {message}")
        print("\nVariable output sizes:")
        
        for size in sizes:
            hasher = BLAKE2b(size)
            hasher.update(message)
            result = hasher.hexdigest()
            print(f"{size:2d} bytes: {result}")
        
        print("\nNote: Each size produces a different hash value")
        print("Smaller outputs are truncated versions, not scaled")
    
    def interactive_menu(self):
        """Interactive menu for demonstrations"""
        print("BLAKE2 Interactive Learning Tool")
        print("Perfect for exam preparation and presentations!")
        
        demos = [
            ("Initialization Vectors (IV)", self.demo_initialization_vectors),
            ("Parameter Block", self.demo_parameter_block),
            ("G Function Step-by-Step", self.demo_g_function),
            ("Sigma Permutation", self.demo_sigma_permutation),
            ("Compression Function", self.demo_compression_function),
            ("Complete Hash Examples", self.demo_full_hash_example),
            ("Keyed Hashing (MAC)", self.demo_keyed_hashing),
            ("Avalanche Effect", self.demo_avalanche_effect),
            ("Variable Output Size", self.demo_variable_output_size),
            ("Run All Demos", self.run_all_demos)
        ]
        
        while True:
            print("\n" + "="*50)
            print("Choose a demonstration:")
            for i, (name, _) in enumerate(demos, 1):
                print(f"{i:2d}. {name}")
            print(" 0. Exit")
            
            try:
                choice = int(input("\nEnter your choice (0-{}): ".format(len(demos))))
                if choice == 0:
                    break
                elif 1 <= choice <= len(demos):
                    demos[choice-1][1]()
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def run_all_demos(self):
        """Run all demonstrations in sequence"""
        demos = [
            self.demo_initialization_vectors,
            self.demo_parameter_block,
            self.demo_g_function,
            self.demo_sigma_permutation,
            self.demo_compression_function,
            self.demo_full_hash_example,
            self.demo_keyed_hashing,
            self.demo_avalanche_effect,
            self.demo_variable_output_size
        ]
        
        for demo in demos:
            demo()
            print("\n" + "-"*60)
            input("Press Enter for next demo...")

def main():
    """Main function"""
    print("BLAKE2 Educational Demo")
    print("For exam preparation and presentations")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Auto-run all demos
        demo = BLAKE2Demo()
        demo.run_all_demos()
    else:
        # Interactive menu
        demo = BLAKE2Demo()
        demo.interactive_menu()

if __name__ == "__main__":
    main()
