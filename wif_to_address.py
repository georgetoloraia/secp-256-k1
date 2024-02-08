import hashlib
from Crypto.Hash import RIPEMD160
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures


# Elliptic curve parameters (secp256k1)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
R = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# Base58 alphabet
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_decode(s):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * 58
    return decoded.to_bytes((decoded.bit_length() + 7) // 8, byteorder='big')

def base58_encode(b):
    num = int.from_bytes(b, byteorder='big')
    encoded = ''
    while num > 0:
        num, rem = divmod(num, 58)
        encoded = BASE58_ALPHABET[rem] + encoded
    # Add '1' for each leading 0 byte
    for byte in b:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    return encoded

def point_add(point1, point2):
    if point1 is None:
        return point2
    if point2 is None:
        return point1
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2 and y1 != y2:
        return None
    if x1 == x2:
        m = (3 * x1 * x1 + A) * pow(2 * y1, P - 2, P)
    else:
        m = (y2 - y1) * pow(x2 - x1, P - 2, P)
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    return (x3 % P, -y3 % P)

def point_mul(point, n):
    result = None
    addend = point
    while n:
        if n & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        n >>= 1
    return result

def pubkey_to_address(pubkey):
    sha = hashlib.sha256(pubkey).digest()
    ripemd160 = RIPEMD160.new(sha).digest()
    network_byte = b'\x00'
    network_and_ripemd160 = network_byte + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(network_and_ripemd160).digest()).digest()[:4]
    binary_address = network_and_ripemd160 + checksum
    mimdinare = 0
    mimdinare += 1
    print(mimdinare)
    return base58_encode(binary_address)

def wif_to_address(wif):
    # Decode the WIF
    decoded_wif = base58_decode(wif)

    # Drop the first byte (version byte) and the last 4 bytes (checksum)
    private_key = int.from_bytes(decoded_wif[1:-4], 'big')

    # Get the public key point
    public_point = point_mul((Gx, Gy), private_key)

    # Get the public key
    public_key = b'\x04' + public_point[0].to_bytes(32, 'big') + public_point[1].to_bytes(32, 'big')

    # Get the address
    address = pubkey_to_address(public_key)
    
    return address

def process_wif(wif):
    try:
        address = wif_to_address(wif.strip())
        return address
    except Exception as e:
        print(f"Error processing WIF {wif}: {e}")
        return None

def process_wifs_concurrently(input_file, output_file, max_workers=10):
    with open(input_file, 'r') as file:
        wifs = file.readlines()

    addresses = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_wif = {executor.submit(process_wif, wif): wif for wif in wifs}
        for future in as_completed(future_to_wif):
            wif = future_to_wif[future]
            try:
                address = future.result()
                addresses.append(address)
            except Exception as e:
                print(f"Error processing WIF {wif}: {e}")

    with open(output_file, 'w') as file:
        for address in addresses:
            if address:
                file.write(address + '\n')

# File names
input_file = 'allwifs.txt'
output_file = 'addresses.txt'

# Process the WIFs and write the output concurrently
process_wifs_concurrently(input_file, output_file)