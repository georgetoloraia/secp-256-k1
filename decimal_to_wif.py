# import hashlib
# import binascii
# import base58

# def private_key_to_WIF(private_key_decimal):
#     # Step 1: Convert decimal to hex
#     private_key_hex = format(private_key_decimal, 'x')
#     private_key_hex = '0' * (64 - len(private_key_hex)) + private_key_hex  # Pad with zeros to make it 64 characters

#     # Step 2: Add prefix (0x80 for mainnet)
#     prefixed_key = '80' + private_key_hex

#     # Step 3 & 4: Double SHA-256 hash and append first 4 bytes of hash as checksum
#     first_sha256 = hashlib.sha256(binascii.unhexlify(prefixed_key)).digest()
#     second_sha256 = hashlib.sha256(first_sha256).digest()
#     checksum = binascii.hexlify(second_sha256)[:8].decode('utf-8')
#     final_key = prefixed_key + checksum
    
#     # Step 5: Base58Check encoding
#     WIF = base58.b58encode(binascii.unhexlify(final_key))
    
#     return private_key_hex, WIF.decode('utf-8')

# # Input from the user
# input_number = int(input("Enter the decimal number for the private key: "))

# # Generate hexadecimal representation and WIF
# hex_representation, wif_representation = private_key_to_WIF(input_number)

# print(f"Hexadecimal: {hex_representation}")
# print(f"WIF: {wif_representation}")


import hashlib
import binascii
import base58

def private_key_to_WIF(private_key_decimal):
    # Step 1: Convert decimal to hex
    private_key_hex = format(private_key_decimal, 'x')
    private_key_hex = '0' * (64 - len(private_key_hex)) + private_key_hex  # Pad with zeros to make it 64 characters

    # Step 2: Add prefix (0x80 for mainnet)
    prefixed_key = '80' + private_key_hex

    # Step 3 & 4: Double SHA-256 hash and append first 4 bytes of hash as checksum
    first_sha256 = hashlib.sha256(binascii.unhexlify(prefixed_key)).digest()
    second_sha256 = hashlib.sha256(first_sha256).digest()
    checksum = binascii.hexlify(second_sha256)[:8].decode('utf-8')
    final_key = prefixed_key + checksum
    
    # Step 5: Base58Check encoding
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    
    # Calculate the compressed WIF by appending '01' to the private key hex
    compressed_private_key_hex = private_key_hex + '01'
    compressed_prefixed_key = '80' + compressed_private_key_hex
    compressed_first_sha256 = hashlib.sha256(binascii.unhexlify(compressed_prefixed_key)).digest()
    compressed_second_sha256 = hashlib.sha256(compressed_first_sha256).digest()
    compressed_checksum = binascii.hexlify(compressed_second_sha256)[:8].decode('utf-8')
    compressed_final_key = compressed_prefixed_key + compressed_checksum
    compressed_WIF = base58.b58encode(binascii.unhexlify(compressed_final_key))
    
    return private_key_hex, WIF.decode('utf-8'), compressed_private_key_hex, compressed_WIF.decode('utf-8')

# Input from the user
input_number = int(input("Enter the decimal number for the private key: "))

# Generate hexadecimal representation and WIF
hex_representation, wif_representation, compressed_hex_representation, compressed_wif_representation = private_key_to_WIF(input_number)

print(f"Hexadecimal: {hex_representation}")
print(f"Uncompressed WIF: {wif_representation}")
print(f"Compressed Hexadecimal: {compressed_hex_representation}")
print(f"Compressed WIF: {compressed_wif_representation}")
