import ecdsa
import hashlib

# Input your number as an integer
input_number = int(input("Enter your number: "))

# Convert the integer to a hexadecimal string
hex_string = hex(input_number)[2:]

# Set the Electrum mainnet version byte (128)
version_byte = bytes.fromhex("80")

# Create a private key
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

# Get the corresponding public key
public_key = private_key.get_verifying_key()

# Compute the compressed public key
compressed_public_key = bytes.fromhex("02" + public_key.to_string().hex()) if public_key.to_string()[0] % 2 == 0 else bytes.fromhex("03" + public_key.to_string().hex())

# Create the WIF private key
wif_private_key = version_byte + bytes.fromhex(hex_string.zfill(64)) + compressed_public_key

# Add checksum
checksum = hashlib.sha256(hashlib.sha256(wif_private_key).digest()).digest()[:4]
wif_private_key += checksum

# Encode in Base58
import base58
electrum_wif = base58.b58encode(wif_private_key).decode()

print("Electrum-compatible WIF:", electrum_wif)
