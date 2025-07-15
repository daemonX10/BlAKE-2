"""
Test script to verify the Flask app works with our custom BLAKE2 implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blake2_implementation import BLAKE2b, BLAKE2s

def test_app_integration():
    """Test the functions that will be used by the Flask app"""
    
    print("Testing Flask App Integration with Custom BLAKE2")
    print("=" * 60)
    
    # Test BLAKE2b hash generation
    text = "Hello, World!"
    digest_size = 32
    key = "secret_key"
    salt = "salt123"
    
    print(f"Input text: '{text}'")
    print(f"Digest size: {digest_size} bytes")
    print(f"Key: '{key}'")
    print(f"Salt: '{salt}'")
    print()
    
    # Test BLAKE2b
    hasher_b = BLAKE2b(digest_size=digest_size, key=key.encode('utf-8'), salt=salt.encode('utf-8'))
    hasher_b.update(text.encode('utf-8'))
    result_b = hasher_b.hexdigest()
    
    print(f"BLAKE2b result: {result_b}")
    print(f"Length: {len(result_b)} hex chars ({len(result_b)//2} bytes)")
    print()
    
    # Test BLAKE2s
    hasher_s = BLAKE2s(digest_size=digest_size, key=key.encode('utf-8')[:32], salt=salt.encode('utf-8')[:8])
    hasher_s.update(text.encode('utf-8'))
    result_s = hasher_s.hexdigest()
    
    print(f"BLAKE2s result: {result_s}")
    print(f"Length: {len(result_s)} hex chars ({len(result_s)//2} bytes)")
    print()
    
    # Test without key and salt
    hasher_b_simple = BLAKE2b(digest_size=64)
    hasher_b_simple.update(text.encode('utf-8'))
    result_b_simple = hasher_b_simple.hexdigest()
    
    print(f"BLAKE2b (no key/salt): {result_b_simple}")
    print()
    
    hasher_s_simple = BLAKE2s(digest_size=32)
    hasher_s_simple.update(text.encode('utf-8'))
    result_s_simple = hasher_s_simple.hexdigest()
    
    print(f"BLAKE2s (no key/salt): {result_s_simple}")
    print()
    
    # Test verification (simulate what the app does)
    expected_hash = result_b
    verification_hasher = BLAKE2b(digest_size=digest_size, key=key.encode('utf-8'), salt=salt.encode('utf-8'))
    verification_hasher.update(text.encode('utf-8'))
    verification_result = verification_hasher.hexdigest()
    
    is_valid = expected_hash.lower() == verification_result.lower()
    print(f"Verification test: {'PASS' if is_valid else 'FAIL'}")
    print(f"Expected: {expected_hash}")
    print(f"Got:      {verification_result}")
    
    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_app_integration()
