"""
Complete BLAKE2 Implementation from Scratch
This module implements both BLAKE2b and BLAKE2s hash functions without using external libraries.
Based on RFC 7693: The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC)
"""

import struct


class BLAKE2b:
    """
    BLAKE2b implementation optimized for 64-bit platforms
    Produces digests of any size between 1 and 64 bytes
    """
    
    # BLAKE2b initialization vectors (first 64 bits of fractional parts of sqrt of first 8 primes)
    IV = [
        0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
        0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
        0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
        0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179
    ]
    
    # Message schedule sigma for BLAKE2b (12 rounds)
    SIGMA = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
        [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
        [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
        [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
        [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
        [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
        [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
        [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
        [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3]
    ]
    
    def __init__(self, digest_size=64, key=b"", salt=b"", person=b""):
        """
        Initialize BLAKE2b hasher
        
        Args:
            digest_size: Output size in bytes (1-64)
            key: Key for keyed hashing (max 64 bytes)
            salt: Salt value (max 16 bytes)  
            person: Personalization string (max 16 bytes)
        """
        if not (1 <= digest_size <= 64):
            raise ValueError("Digest size must be between 1 and 64 bytes")
        if len(key) > 64:
            raise ValueError("Key must be 64 bytes or less")
        if len(salt) > 16:
            raise ValueError("Salt must be 16 bytes or less")
        if len(person) > 16:
            raise ValueError("Personalization must be 16 bytes or less")
            
        self.digest_size = digest_size
        self.key = key
        self.salt = salt
        self.person = person
        self.buffer = b""
        self.counter = 0
        self.finalized = False
        
        # Initialize state
        self.h = list(self.IV)
        
        # Create parameter block
        param_block = self._create_parameter_block()
        
        # XOR parameter block with IV
        for i in range(8):
            param_word = struct.unpack('<Q', param_block[i*8:(i+1)*8])[0]
            self.h[i] ^= param_word
            
        # If keyed, process key as first block
        if self.key:
            key_block = self.key + b'\x00' * (128 - len(self.key))
            self._compress(key_block, 128, False)
    
    def _create_parameter_block(self):
        """Create the 64-byte parameter block for BLAKE2b"""
        param = bytearray(64)
        
        # General parameters
        param[0] = self.digest_size  # digest length
        param[1] = len(self.key)     # key length
        param[2] = 1                 # fanout
        param[3] = 1                 # depth
        
        # Leaf length (0 for unlimited)
        struct.pack_into('<I', param, 4, 0)
        
        # Node offset (0 for first node)
        struct.pack_into('<Q', param, 8, 0)
        
        # XOF length (0 for non-XOF)
        struct.pack_into('<Q', param, 16, 0)
        
        # Node depth and inner length (0 for leaf node)
        param[24] = 0
        param[25] = 0
        
        # Reserved (14 bytes)
        # param[26:40] already zero
        
        # Salt (16 bytes)
        salt_padded = self.salt + b'\x00' * (16 - len(self.salt))
        param[32:48] = salt_padded
        
        # Personal (16 bytes)  
        person_padded = self.person + b'\x00' * (16 - len(self.person))
        param[48:64] = person_padded
        
        return bytes(param)
    
    def _rotr64(self, value, amount):
        """64-bit right rotation"""
        return ((value >> amount) | (value << (64 - amount))) & 0xFFFFFFFFFFFFFFFF
    
    def _g(self, v, a, b, c, d, x, y):
        """BLAKE2b G function - core mixing function"""
        v[a] = (v[a] + v[b] + x) & 0xFFFFFFFFFFFFFFFF
        v[d] = self._rotr64(v[d] ^ v[a], 32)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
        v[b] = self._rotr64(v[b] ^ v[c], 24)
        v[a] = (v[a] + v[b] + y) & 0xFFFFFFFFFFFFFFFF
        v[d] = self._rotr64(v[d] ^ v[a], 16)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFFFFFFFFFF
        v[b] = self._rotr64(v[b] ^ v[c], 63)
    
    def _compress(self, block, counter, is_final):
        """BLAKE2b compression function"""
        # Initialize working vector
        v = list(self.h) + list(self.IV)
        
        # Mix counter and final flag
        v[12] ^= counter & 0xFFFFFFFFFFFFFFFF
        v[13] ^= (counter >> 64) & 0xFFFFFFFFFFFFFFFF
        if is_final:
            v[14] ^= 0xFFFFFFFFFFFFFFFF
            
        # Convert block to 16 64-bit words
        m = list(struct.unpack('<16Q', block))
        
        # 12 rounds of mixing
        for round_num in range(12):
            sigma = self.SIGMA[round_num]
            
            # Column rounds
            self._g(v, 0, 4, 8, 12, m[sigma[0]], m[sigma[1]])
            self._g(v, 1, 5, 9, 13, m[sigma[2]], m[sigma[3]])
            self._g(v, 2, 6, 10, 14, m[sigma[4]], m[sigma[5]])
            self._g(v, 3, 7, 11, 15, m[sigma[6]], m[sigma[7]])
            
            # Diagonal rounds
            self._g(v, 0, 5, 10, 15, m[sigma[8]], m[sigma[9]])
            self._g(v, 1, 6, 11, 12, m[sigma[10]], m[sigma[11]])
            self._g(v, 2, 7, 8, 13, m[sigma[12]], m[sigma[13]])
            self._g(v, 3, 4, 9, 14, m[sigma[14]], m[sigma[15]])
        
        # Update state
        for i in range(8):
            self.h[i] ^= v[i] ^ v[i + 8]
    
    def update(self, data):
        """Add data to be hashed"""
        if self.finalized:
            raise ValueError("Cannot update finalized hash")
            
        self.buffer += data
        
        # Process complete 128-byte blocks
        while len(self.buffer) >= 128:
            block = self.buffer[:128]
            self.buffer = self.buffer[128:]
            self.counter += 128
            self._compress(block, self.counter, False)
    
    def digest(self):
        """Get the final hash digest"""
        if self.finalized:
            return self._digest_value
            
        # Pad final block
        final_block = self.buffer + b'\x00' * (128 - len(self.buffer))
        final_counter = self.counter + len(self.buffer)
        
        # Process final block
        self._compress(final_block, final_counter, True)
        
        # Extract digest
        digest_bytes = b''
        for i in range(8):
            digest_bytes += struct.pack('<Q', self.h[i])
        
        self._digest_value = digest_bytes[:self.digest_size]
        self.finalized = True
        return self._digest_value
    
    def hexdigest(self):
        """Get the final hash digest as hexadecimal string"""
        return self.digest().hex()


class BLAKE2s:
    """
    BLAKE2s implementation optimized for 8-32 bit platforms
    Produces digests of any size between 1 and 32 bytes
    """
    
    # BLAKE2s initialization vectors (first 32 bits of fractional parts of sqrt of first 8 primes)
    IV = [
        0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
        0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
    ]
    
    # Message schedule sigma for BLAKE2s (10 rounds)
    SIGMA = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
        [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
        [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
        [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
        [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
        [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
        [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
        [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
        [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
    ]
    
    def __init__(self, digest_size=32, key=b"", salt=b"", person=b""):
        """
        Initialize BLAKE2s hasher
        
        Args:
            digest_size: Output size in bytes (1-32)
            key: Key for keyed hashing (max 32 bytes)
            salt: Salt value (max 8 bytes)
            person: Personalization string (max 8 bytes)
        """
        if not (1 <= digest_size <= 32):
            raise ValueError("Digest size must be between 1 and 32 bytes")
        if len(key) > 32:
            raise ValueError("Key must be 32 bytes or less")
        if len(salt) > 8:
            raise ValueError("Salt must be 8 bytes or less")
        if len(person) > 8:
            raise ValueError("Personalization must be 8 bytes or less")
            
        self.digest_size = digest_size
        self.key = key
        self.salt = salt
        self.person = person
        self.buffer = b""
        self.counter = 0
        self.finalized = False
        
        # Initialize state
        self.h = list(self.IV)
        
        # Create parameter block
        param_block = self._create_parameter_block()
        
        # XOR parameter block with IV
        for i in range(8):
            param_word = struct.unpack('<I', param_block[i*4:(i+1)*4])[0]
            self.h[i] ^= param_word
            
        # If keyed, process key as first block
        if self.key:
            key_block = self.key + b'\x00' * (64 - len(self.key))
            self._compress(key_block, 64, False)
    
    def _create_parameter_block(self):
        """Create the 32-byte parameter block for BLAKE2s"""
        param = bytearray(32)
        
        # General parameters
        param[0] = self.digest_size  # digest length
        param[1] = len(self.key)     # key length
        param[2] = 1                 # fanout
        param[3] = 1                 # depth
        
        # Leaf length (0 for unlimited)
        struct.pack_into('<I', param, 4, 0)
        
        # Node offset (0 for first node)
        struct.pack_into('<Q', param, 8, 0)
        
        # Salt (8 bytes)
        salt_padded = self.salt + b'\x00' * (8 - len(self.salt))
        param[16:24] = salt_padded
        
        # Personal (8 bytes)
        person_padded = self.person + b'\x00' * (8 - len(self.person))
        param[24:32] = person_padded
        
        return bytes(param)
    
    def _rotr32(self, value, amount):
        """32-bit right rotation"""
        return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF
    
    def _g(self, v, a, b, c, d, x, y):
        """BLAKE2s G function - core mixing function"""
        v[a] = (v[a] + v[b] + x) & 0xFFFFFFFF
        v[d] = self._rotr32(v[d] ^ v[a], 16)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFF
        v[b] = self._rotr32(v[b] ^ v[c], 12)
        v[a] = (v[a] + v[b] + y) & 0xFFFFFFFF
        v[d] = self._rotr32(v[d] ^ v[a], 8)
        v[c] = (v[c] + v[d]) & 0xFFFFFFFF
        v[b] = self._rotr32(v[b] ^ v[c], 7)
    
    def _compress(self, block, counter, is_final):
        """BLAKE2s compression function"""
        # Initialize working vector
        v = list(self.h) + list(self.IV)
        
        # Mix counter and final flag
        v[12] ^= counter & 0xFFFFFFFF
        v[13] ^= (counter >> 32) & 0xFFFFFFFF
        if is_final:
            v[14] ^= 0xFFFFFFFF
            
        # Convert block to 16 32-bit words
        m = list(struct.unpack('<16I', block))
        
        # 10 rounds of mixing
        for round_num in range(10):
            sigma = self.SIGMA[round_num]
            
            # Column rounds
            self._g(v, 0, 4, 8, 12, m[sigma[0]], m[sigma[1]])
            self._g(v, 1, 5, 9, 13, m[sigma[2]], m[sigma[3]])
            self._g(v, 2, 6, 10, 14, m[sigma[4]], m[sigma[5]])
            self._g(v, 3, 7, 11, 15, m[sigma[6]], m[sigma[7]])
            
            # Diagonal rounds
            self._g(v, 0, 5, 10, 15, m[sigma[8]], m[sigma[9]])
            self._g(v, 1, 6, 11, 12, m[sigma[10]], m[sigma[11]])
            self._g(v, 2, 7, 8, 13, m[sigma[12]], m[sigma[13]])
            self._g(v, 3, 4, 9, 14, m[sigma[14]], m[sigma[15]])
        
        # Update state
        for i in range(8):
            self.h[i] ^= v[i] ^ v[i + 8]
    
    def update(self, data):
        """Add data to be hashed"""
        if self.finalized:
            raise ValueError("Cannot update finalized hash")
            
        self.buffer += data
        
        # Process complete 64-byte blocks
        while len(self.buffer) >= 64:
            block = self.buffer[:64]
            self.buffer = self.buffer[64:]
            self.counter += 64
            self._compress(block, self.counter, False)
    
    def digest(self):
        """Get the final hash digest"""
        if self.finalized:
            return self._digest_value
            
        # Pad final block
        final_block = self.buffer + b'\x00' * (64 - len(self.buffer))
        final_counter = self.counter + len(self.buffer)
        
        # Process final block
        self._compress(final_block, final_counter, True)
        
        # Extract digest
        digest_bytes = b''
        for i in range(8):
            digest_bytes += struct.pack('<I', self.h[i])
        
        self._digest_value = digest_bytes[:self.digest_size]
        self.finalized = True
        return self._digest_value
    
    def hexdigest(self):
        """Get the final hash digest as hexadecimal string"""
        return self.digest().hex()


def blake2b(data=b"", digest_size=64, key=b"", salt=b"", person=b""):
    """
    Convenience function for BLAKE2b hashing
    
    Args:
        data: Data to hash
        digest_size: Output size in bytes (1-64)
        key: Key for keyed hashing (max 64 bytes)
        salt: Salt value (max 16 bytes)
        person: Personalization string (max 16 bytes)
    
    Returns:
        Hash digest as bytes
    """
    hasher = BLAKE2b(digest_size, key, salt, person)
    hasher.update(data)
    return hasher.digest()


def blake2s(data=b"", digest_size=32, key=b"", salt=b"", person=b""):
    """
    Convenience function for BLAKE2s hashing
    
    Args:
        data: Data to hash
        digest_size: Output size in bytes (1-32)
        key: Key for keyed hashing (max 32 bytes)
        salt: Salt value (max 8 bytes)
        person: Personalization string (max 8 bytes)
    
    Returns:
        Hash digest as bytes
    """
    hasher = BLAKE2s(digest_size, key, salt, person)
    hasher.update(data)
    return hasher.digest()


# Test functions to verify implementation
def test_blake2_implementation():
    """Test the BLAKE2 implementation with known test vectors"""
    
    print("Testing BLAKE2 Implementation")
    print("=" * 50)
    
    # Test BLAKE2b with empty input
    hasher_b = BLAKE2b(64)
    hasher_b.update(b"")
    result_b = hasher_b.hexdigest()
    expected_b = "786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce"
    print(f"BLAKE2b empty: {'PASS' if result_b == expected_b else 'FAIL'}")
    print(f"Expected: {expected_b}")
    print(f"Got:      {result_b}")
    print()
    
    # Test BLAKE2s with empty input
    hasher_s = BLAKE2s(32)
    hasher_s.update(b"")
    result_s = hasher_s.hexdigest()
    expected_s = "69217a3079908094e11121d042354a7c1f55b6482ca1a51e1b250dfd1ed0eef9"
    print(f"BLAKE2s empty: {'PASS' if result_s == expected_s else 'FAIL'}")
    print(f"Expected: {expected_s}")
    print(f"Got:      {result_s}")
    print()
    
    # Test BLAKE2b with "abc"
    hasher_b2 = BLAKE2b(64)
    hasher_b2.update(b"abc")
    result_b2 = hasher_b2.hexdigest()
    expected_b2 = "ba80a53f981c4d0d6a2797b69f12f6e94c212f14685ac4b74b12bb6fdbffa2d17d87c5392aab792dc252d5de4533cc9518d38aa8dbf1925ab92386edd4009923"
    print(f"BLAKE2b 'abc': {'PASS' if result_b2 == expected_b2 else 'FAIL'}")
    print(f"Expected: {expected_b2}")
    print(f"Got:      {result_b2}")
    print()
    
    # Test BLAKE2s with "abc"
    hasher_s2 = BLAKE2s(32)
    hasher_s2.update(b"abc")
    result_s2 = hasher_s2.hexdigest()
    expected_s2 = "508c5e8c327c14e2e1a72ba34eeb452f37458b209ed63a294d999b4c86675982"
    print(f"BLAKE2s 'abc': {'PASS' if result_s2 == expected_s2 else 'FAIL'}")
    print(f"Expected: {expected_s2}")
    print(f"Got:      {result_s2}")
    print()
    
    # Test BLAKE2b with key
    key = b"The quick brown fox jumps over the lazy dog"
    hasher_b3 = BLAKE2b(64, key=key)
    hasher_b3.update(b"The quick brown fox jumps over the lazy dog")
    result_b3 = hasher_b3.hexdigest()
    print(f"BLAKE2b with key: {result_b3}")
    print()
    
    # Test BLAKE2s with salt
    salt = b"12345678"
    hasher_s3 = BLAKE2s(32, salt=salt)
    hasher_s3.update(b"Hello, World!")
    result_s3 = hasher_s3.hexdigest()
    print(f"BLAKE2s with salt: {result_s3}")


if __name__ == "__main__":
    test_blake2_implementation()
