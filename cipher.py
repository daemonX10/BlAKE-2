import math
from typing import Tuple

class UltimateCipher:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet_length = len(self.alphabet)

    def _gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def _mod_inverse(self, a: int, m: int) -> int:
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    def affine_encrypt(self, text: str, a: int, b: int) -> str:
        if self._gcd(a, self.alphabet_length) != 1:
            raise ValueError("Key 'a' must be coprime with alphabet length")
        
        result = ""
        for char in text.upper():
            if char in self.alphabet:
                x = self.alphabet.index(char)
                y = (a * x + b) % self.alphabet_length
                result += self.alphabet[y]
            else:
                result += char
        return result

    def affine_decrypt(self, text: str, a: int, b: int) -> str:
        if self._gcd(a, self.alphabet_length) != 1:
            raise ValueError("Key 'a' must be coprime with alphabet length")
        
        a_inv = self._mod_inverse(a, self.alphabet_length)
        result = ""
        for char in text.upper():
            if char in self.alphabet:
                y = self.alphabet.index(char)
                x = (a_inv * (y - b)) % self.alphabet_length
                result += self.alphabet[x]
            else:
                result += char
        return result

    def vigenere_encrypt(self, text: str, key: str) -> str:
        key = key.upper()
        result = ""
        key_length = len(key)
        text_length = len(text)
        
        for i in range(text_length):
            if text[i].upper() in self.alphabet:
                text_idx = self.alphabet.index(text[i].upper())
                key_idx = self.alphabet.index(key[i % key_length])
                new_idx = (text_idx + key_idx) % self.alphabet_length
                result += self.alphabet[new_idx]
            else:
                result += text[i]
        return result

    def vigenere_decrypt(self, text: str, key: str) -> str:
        key = key.upper()
        result = ""
        key_length = len(key)
        text_length = len(text)
        
        for i in range(text_length):
            if text[i].upper() in self.alphabet:
                text_idx = self.alphabet.index(text[i].upper())
                key_idx = self.alphabet.index(key[i % key_length])
                new_idx = (text_idx - key_idx) % self.alphabet_length
                result += self.alphabet[new_idx]
            else:
                result += text[i]
        return result

    def transposition_encrypt(self, text: str, key: int) -> str:
        # Create matrix
        matrix = []
        for i in range(0, len(text), key):
            row = text[i:i + key]
            if len(row) < key:
                row += ' ' * (key - len(row))
            matrix.append(row)
        
        # Read columns
        result = ""
        for col in range(key):
            for row in matrix:
                result += row[col]
        return result.rstrip()

    def transposition_decrypt(self, text: str, key: int) -> str:
        # Calculate number of rows
        rows = math.ceil(len(text) / key)
        
        # Create matrix
        matrix = [['' for _ in range(key)] for _ in range(rows)]
        
        # Fill matrix
        index = 0
        for col in range(key):
            for row in range(rows):
                if index < len(text):
                    matrix[row][col] = text[index]
                    index += 1
        
        # Read rows
        result = ""
        for row in matrix:
            result += ''.join(row)
        return result.rstrip()

    def xor_encrypt(self, text: str, key: str) -> str:
        result = ""
        key_length = len(key)
        for i, char in enumerate(text):
            key_char = key[i % key_length]
            # Convert to bytes for XOR operation
            text_byte = ord(char)
            key_byte = ord(key_char)
            result_byte = text_byte ^ key_byte
            # Convert back to character, ensuring it's printable
            result += chr(result_byte)
        return result

    def xor_decrypt(self, text: str, key: str) -> str:
        return self.xor_encrypt(text, key)  # XOR is symmetric

    def encrypt(self, text: str, affine_a: int, affine_b: int, vigenere_key: str, xor_key: str) -> str:
        # Apply ciphers in sequence
        result = self.affine_encrypt(text, affine_a, affine_b)
        result = self.vigenere_encrypt(result, vigenere_key)
        result = self.transposition_encrypt(result, len(vigenere_key))
        result = self.xor_encrypt(result, xor_key)
        return result

    def decrypt(self, text: str, affine_a: int, affine_b: int, vigenere_key: str, xor_key: str) -> str:
        # Apply ciphers in reverse sequence
        result = self.xor_decrypt(text, xor_key)
        result = self.transposition_decrypt(result, len(vigenere_key))
        result = self.vigenere_decrypt(result, vigenere_key)
        result = self.affine_decrypt(result, affine_a, affine_b)
        return result 