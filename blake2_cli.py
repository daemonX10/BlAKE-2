"""
Command Line Interface for BLAKE2 Hashing
Usage: python blake2_cli.py [options]
"""

import argparse
import sys
from blake2_implementation import BLAKE2b, BLAKE2s

def main():
    parser = argparse.ArgumentParser(description='BLAKE2 Hash Calculator (Custom Implementation)')
    parser.add_argument('text', nargs='?', help='Text to hash (use -f for file input)')
    parser.add_argument('-f', '--file', help='File to hash')
    parser.add_argument('-a', '--algorithm', choices=['blake2b', 'blake2s'], 
                       default='blake2b', help='Hash algorithm (default: blake2b)')
    parser.add_argument('-s', '--size', type=int, help='Digest size in bytes (default: 64 for blake2b, 32 for blake2s)')
    parser.add_argument('-k', '--key', help='Key for keyed hashing')
    parser.add_argument('--salt', help='Salt value')
    parser.add_argument('--person', help='Personalization string')
    parser.add_argument('-v', '--verify', help='Expected hash for verification')
    
    args = parser.parse_args()
    
    # Determine input data
    if args.file:
        try:
            with open(args.file, 'rb') as f:
                data = f.read()
            print(f"File: {args.file}")
            print(f"Size: {len(data)} bytes")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            return 1
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1
    elif args.text:
        data = args.text.encode('utf-8')
        print(f"Text: {args.text}")
    else:
        print("Error: Please provide text to hash or use -f for file input")
        parser.print_help()
        return 1
    
    # Set default digest size
    if args.size is None:
        args.size = 64 if args.algorithm == 'blake2b' else 32
    
    # Validate parameters
    if args.algorithm == 'blake2b':
        if not (1 <= args.size <= 64):
            print("Error: BLAKE2b digest size must be between 1 and 64 bytes")
            return 1
        max_key_size = 64
        max_salt_size = 16
        max_person_size = 16
    else:  # blake2s
        if not (1 <= args.size <= 32):
            print("Error: BLAKE2s digest size must be between 1 and 32 bytes")
            return 1
        max_key_size = 32
        max_salt_size = 8
        max_person_size = 8
    
    # Prepare parameters
    key = args.key.encode('utf-8') if args.key else b""
    salt = args.salt.encode('utf-8') if args.salt else b""
    person = args.person.encode('utf-8') if args.person else b""
    
    # Validate parameter sizes
    if len(key) > max_key_size:
        print(f"Error: Key too long (max {max_key_size} bytes for {args.algorithm})")
        return 1
    if len(salt) > max_salt_size:
        print(f"Error: Salt too long (max {max_salt_size} bytes for {args.algorithm})")
        return 1
    if len(person) > max_person_size:
        print(f"Error: Personalization too long (max {max_person_size} bytes for {args.algorithm})")
        return 1
    
    try:
        # Create hasher and compute hash
        if args.algorithm == 'blake2b':
            hasher = BLAKE2b(digest_size=args.size, key=key, salt=salt, person=person)
        else:
            hasher = BLAKE2s(digest_size=args.size, key=key, salt=salt, person=person)
        
        hasher.update(data)
        hash_result = hasher.hexdigest()
        
        # Display results
        print(f"\nAlgorithm: {args.algorithm.upper()}")
        print(f"Digest size: {args.size} bytes ({args.size * 8} bits)")
        if key:
            print(f"Key: {args.key}")
        if salt:
            print(f"Salt: {args.salt}")
        if person:
            print(f"Personalization: {args.person}")
        
        print(f"\nHash: {hash_result}")
        
        # Verification if requested
        if args.verify:
            expected = args.verify.lower().replace(' ', '').replace(':', '')
            actual = hash_result.lower()
            
            if expected == actual:
                print("\n✓ VERIFICATION PASSED: Hash matches expected value")
                return 0
            else:
                print("\n✗ VERIFICATION FAILED: Hash does not match expected value")
                print(f"Expected: {expected}")
                print(f"Actual:   {actual}")
                return 1
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
