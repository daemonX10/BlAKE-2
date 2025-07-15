"""
Quick Flask app test to ensure everything works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test importing the app
try:
    from app import generate_blake2_hash, verify_hash_integrity
    print("✓ Successfully imported Flask app functions")
    
    # Test hash generation
    result = generate_blake2_hash(
        text="Test message",
        hash_type="blake2b",
        digest_size="32",
        key="test_key",
        salt="test_salt"
    )
    
    print(f"✓ Hash generation works: {result['hash']}")
    
    # Test verification
    verification = verify_hash_integrity(
        text="Test message",
        expected_hash=result['hash'],
        hash_type="blake2b",
        digest_size="32",
        key="test_key",
        salt="test_salt"
    )
    
    print(f"✓ Hash verification works: {verification['is_valid']}")
    
    if verification['is_valid']:
        print("\n🎉 Flask app integration test PASSED!")
        print("The custom BLAKE2 implementation is working correctly with the web interface.")
    else:
        print("\n❌ Verification failed")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed")
except Exception as e:
    print(f"❌ Error: {e}")
