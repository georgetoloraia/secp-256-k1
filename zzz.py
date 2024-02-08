import os
import hashlib

# Base58 alphabet
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(b):
    # Convert bytes to integer
    n = int.from_bytes(b, 'big')
    result = ''
    
    while n > 0:
        n, remainder = divmod(n, 58)
        result = ALPHABET[remainder] + result

    # Add '1' for each leading 0 byte
    for byte in b:
        if byte == 0:
            result = '1' + result
        else:
            break

    return result

def wif_conversion(private_key, version_byte, compression_byte=None):
    # Add version byte
    extended_key = version_byte + private_key
    
    # Add compression byte if the key is compressed
    if compression_byte:
        extended_key += compression_byte

    # Perform double SHA-256 hashing on the extended key
    first_sha256 = hashlib.sha256(extended_key).digest()
    second_sha256 = hashlib.sha256(first_sha256).digest()

    # Take the first 4 bytes of the second hash as the checksum
    checksum = second_sha256[:4]

    # Add the checksum to the extended key
    extended_key_with_checksum = extended_key + checksum

    # Convert to WIF by Base58 encoding
    wif_key = base58_encode(extended_key_with_checksum)
    
    return wif_key

# Define version byte for mainnet Bitcoin addresses
version_byte = b'\x80'  # Mainnet version byte
compression_byte = b'\x01'  # Compression flag

# Generate 50 random WIF compressed and uncompressed private keys
keys = []
for _ in range(100):
    private_key = os.urandom(32)  # Generate a 256-bit (32 bytes) private key
    wif_compressed = wif_conversion(private_key, version_byte, compression_byte)
    wif_uncompressed = wif_conversion(private_key, version_byte)
    keys.append(f"{wif_compressed}\n{wif_uncompressed}")
    file = open("abc.txt", "a")

    file.write(f"{wif_compressed}\n")
    file.write(f"{wif_uncompressed}\n")


file.close()