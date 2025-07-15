# BLAKE2 Hash Generator - Demo Configuration

## Sample Input Data for Testing

### Test Text
```
Hello World! This is a test message for the BLAKE2 hash generator application. 123
```

### Sample BLAKE2 Configurations

#### Configuration 1 - Basic BLAKE2b
- **Hash Type**: BLAKE2b (64-byte hash)
- **Digest Size**: 32 bytes (256 bits)
- **Key**: (empty)
- **Salt**: (empty)

#### Configuration 2 - Keyed BLAKE2s (MAC)
- **Hash Type**: BLAKE2s with Key (MAC)
- **Digest Size**: 32 bytes (256 bits)
- **Key**: secretkey123
- **Salt**: randomsalt

#### Configuration 3 - Maximum Security BLAKE2b
- **Hash Type**: BLAKE2b with Key (MAC)
- **Digest Size**: 64 bytes (512 bits)
- **Key**: MyStrongSecretKey!2024#
- **Salt**: UniqueRandomSalt

## BLAKE2 Specifications

### BLAKE2b (64-bit optimized)
- **Max Digest Size**: 64 bytes (512 bits)
- **Max Key Size**: 64 bytes
- **Max Salt Size**: 16 bytes
- **Best For**: 64-bit platforms, servers, high-security applications

### BLAKE2s (32-bit optimized)
- **Max Digest Size**: 32 bytes (256 bits)
- **Max Key Size**: 32 bytes
- **Max Salt Size**: 8 bytes
- **Best For**: 8-32 bit platforms, embedded systems, mobile devices

## Available Digest Sizes
- **16 bytes (128 bits)**: Fast, basic security
- **20 bytes (160 bits)**: SHA-1 equivalent
- **28 bytes (224 bits)**: SHA-224 equivalent
- **32 bytes (256 bits)**: SHA-256 equivalent (recommended)
- **48 bytes (384 bits)**: SHA-384 equivalent
- **64 bytes (512 bits)**: SHA-512 equivalent (maximum security)

## How to Use
1. Enter your text in the text area
2. Choose BLAKE2 variant (b/s, with/without key)
3. Select digest size based on security needs
4. Optionally add key for MAC functionality
5. Optionally add salt for uniqueness
6. Click "Generate Hash" to see the result
7. Use the copy buttons to copy the results

## Security Features
- **Speed**: Faster than SHA-3, SHA-2, SHA-1, and MD5
- **Security**: At least as secure as SHA-3
- **Keyed Hashing**: Built-in MAC functionality
- **Salting**: Built-in protection against rainbow tables
- **Flexibility**: Variable digest size
- **No Length Extension**: Resistant to length extension attacks

## Use Cases
- **Password Hashing**: Use with strong keys and salts
- **Digital Signatures**: Fast verification
- **Message Authentication**: Keyed hashing (MAC)
- **Checksums**: File integrity verification
- **Cryptocurrency**: Used in various blockchain applications
- **General Hashing**: Replace MD5/SHA-1 in legacy systems

## Application Features
- Modern, responsive UI design
- Real-time form validation with BLAKE2-specific checks
- Copy-to-clipboard functionality
- Detailed hash information display
- Professional gradient design with animations
- Mobile-friendly interface
- Keyboard shortcuts (Ctrl+Enter to submit)
- Security level indicators based on digest size
