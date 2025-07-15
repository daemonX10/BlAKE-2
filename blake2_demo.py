"""
Comprehensive BLAKE2 Demo Script
Demonstrates all features of our custom BLAKE2 implementation
"""

from blake2_implementation import BLAKE2b, BLAKE2s, blake2b, blake2s
import time
import secrets

def demo_basic_hashing():
    """Demonstrate basic BLAKE2 hashing"""
    print("=" * 60)
    print("BASIC BLAKE2 HASHING DEMO")
    print("=" * 60)
    
    test_data = [
        b"",
        b"Hello, World!",
        b"The quick brown fox jumps over the lazy dog",
        b"a" * 100,  # 100 'a' characters
        b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
    ]
    
    for i, data in enumerate(test_data, 1):
        print(f"\nTest {i}: {data[:50]}{'...' if len(data) > 50 else ''}")
        print(f"Input length: {len(data)} bytes")
        
        # BLAKE2b
        hash_b = blake2b(data, digest_size=32)
        print(f"BLAKE2b-256: {hash_b.hex()}")
        
        # BLAKE2s  
        hash_s = blake2s(data, digest_size=32)
        print(f"BLAKE2s-256: {hash_s.hex()}")


def demo_variable_output_size():
    """Demonstrate variable output sizes"""
    print("\n" + "=" * 60)
    print("VARIABLE OUTPUT SIZE DEMO")
    print("=" * 60)
    
    data = b"Variable length output demonstration"
    sizes_b = [16, 20, 28, 32, 48, 64]  # BLAKE2b sizes
    sizes_s = [16, 20, 28, 32]          # BLAKE2s sizes
    
    print(f"\nInput: {data.decode()}")
    
    print("\nBLAKE2b with different output sizes:")
    for size in sizes_b:
        hash_val = blake2b(data, digest_size=size)
        print(f"  {size:2d} bytes: {hash_val.hex()}")
    
    print("\nBLAKE2s with different output sizes:")
    for size in sizes_s:
        hash_val = blake2s(data, digest_size=size)
        print(f"  {size:2d} bytes: {hash_val.hex()}")


def demo_keyed_hashing():
    """Demonstrate keyed hashing (MAC functionality)"""
    print("\n" + "=" * 60)
    print("KEYED HASHING (MAC) DEMO")
    print("=" * 60)
    
    data = b"This is a message to authenticate"
    key = b"secret_authentication_key_2024"
    
    print(f"Message: {data.decode()}")
    print(f"Key: {key.decode()}")
    
    # BLAKE2b MAC
    mac_b = blake2b(data, digest_size=32, key=key)
    print(f"\nBLAKE2b MAC: {mac_b.hex()}")
    
    # BLAKE2s MAC
    mac_s = blake2s(data, digest_size=32, key=key)
    print(f"BLAKE2s MAC: {mac_s.hex()}")
    
    # Verify MAC
    verify_mac_b = blake2b(data, digest_size=32, key=key)
    verify_mac_s = blake2s(data, digest_size=32, key=key)
    
    print(f"\nMAC Verification:")
    print(f"BLAKE2b: {'VALID' if mac_b == verify_mac_b else 'INVALID'}")
    print(f"BLAKE2s: {'VALID' if mac_s == verify_mac_s else 'INVALID'}")
    
    # Different key should produce different MAC
    wrong_key = b"wrong_key"
    wrong_mac_b = blake2b(data, digest_size=32, key=wrong_key)
    print(f"\nWith wrong key: {'INVALID' if mac_b != wrong_mac_b else 'ERROR: Same MAC!'}")


def demo_salt_usage():
    """Demonstrate salt usage for randomized hashing"""
    print("\n" + "=" * 60)
    print("SALT USAGE DEMO")
    print("=" * 60)
    
    data = b"Password123"
    print(f"Password: {data.decode()}")
    
    # Generate random salts
    salts = [secrets.token_bytes(16)[:16] for _ in range(3)]  # BLAKE2b salt
    salts_s = [secrets.token_bytes(8)[:8] for _ in range(3)]   # BLAKE2s salt
    
    print("\nBLAKE2b with different salts:")
    for i, salt in enumerate(salts, 1):
        hash_val = blake2b(data, digest_size=32, salt=salt)
        print(f"  Salt {i}: {salt.hex()}")
        print(f"  Hash {i}: {hash_val.hex()}")
        print()
    
    print("BLAKE2s with different salts:")
    for i, salt in enumerate(salts_s, 1):
        hash_val = blake2s(data, digest_size=32, salt=salt)
        print(f"  Salt {i}: {salt.hex()}")
        print(f"  Hash {i}: {hash_val.hex()}")
        print()


def demo_personalization():
    """Demonstrate personalization parameter"""
    print("\n" + "=" * 60)
    print("PERSONALIZATION DEMO")
    print("=" * 60)
    
    data = b"Shared data"
    applications = [
        b"App1_Hash",
        b"App2_Hash", 
        b"WebService",
        b"Database"
    ]
    
    print(f"Shared data: {data.decode()}")
    
    print("\nBLAKE2b with different personalization:")
    for app in applications:
        hash_val = blake2b(data, digest_size=32, person=app)
        print(f"  {app.decode():12}: {hash_val.hex()}")
    
    print("\nBLAKE2s with different personalization:")
    for app in applications:
        # BLAKE2s person is max 8 bytes
        person_s = app[:8]
        hash_val = blake2s(data, digest_size=32, person=person_s)
        print(f"  {person_s.decode():12}: {hash_val.hex()}")


def demo_streaming():
    """Demonstrate streaming/incremental hashing"""
    print("\n" + "=" * 60)
    print("STREAMING HASHING DEMO")
    print("=" * 60)
    
    # Create a large message in chunks
    chunks = [
        b"This is the first part of a long message. ",
        b"This is the second part with more content. ",
        b"And this is the final part of the message.",
        b" Additional data can be appended as needed."
    ]
    
    # Hash all at once
    full_message = b"".join(chunks)
    hash_all_at_once = blake2b(full_message, digest_size=32)
    
    # Hash incrementally
    hasher = BLAKE2b(digest_size=32)
    for i, chunk in enumerate(chunks, 1):
        print(f"Adding chunk {i}: {chunk.decode()}")
        hasher.update(chunk)
    
    hash_incremental = hasher.digest()
    
    print(f"\nFull message length: {len(full_message)} bytes")
    print(f"Hash (all at once):  {hash_all_at_once.hex()}")
    print(f"Hash (incremental):  {hash_incremental.hex()}")
    print(f"Results match: {'YES' if hash_all_at_once == hash_incremental else 'NO'}")


def demo_performance():
    """Demonstrate performance characteristics"""
    print("\n" + "=" * 60)
    print("PERFORMANCE DEMO")
    print("=" * 60)
    
    # Test with different data sizes
    sizes = [1024, 10240, 102400, 1024000]  # 1KB, 10KB, 100KB, 1MB
    
    for size in sizes:
        data = b"A" * size
        
        print(f"\nTesting with {size:,} bytes:")
        
        # BLAKE2b
        start_time = time.time()
        for _ in range(10):  # Run 10 times for better measurement
            blake2b(data, digest_size=64)
        blake2b_time = (time.time() - start_time) / 10
        
        # BLAKE2s
        start_time = time.time()
        for _ in range(10):  # Run 10 times for better measurement
            blake2s(data, digest_size=32)
        blake2s_time = (time.time() - start_time) / 10
        
        print(f"  BLAKE2b: {blake2b_time:.4f}s ({size/blake2b_time/1024/1024:.1f} MB/s)")
        print(f"  BLAKE2s: {blake2s_time:.4f}s ({size/blake2s_time/1024/1024:.1f} MB/s)")


def main():
    """Run all demonstrations"""
    print("COMPREHENSIVE BLAKE2 IMPLEMENTATION DEMO")
    print("Custom implementation without external libraries")
    print("Based on RFC 7693")
    
    demo_basic_hashing()
    demo_variable_output_size()
    demo_keyed_hashing()
    demo_salt_usage()
    demo_personalization()
    demo_streaming()
    demo_performance()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("All features of the custom BLAKE2 implementation demonstrated.")
    print("=" * 60)


if __name__ == "__main__":
    main()
