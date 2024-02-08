import hashlib

# Base58 alphabet
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, idx = divmod(num, 58)
        result = alphabet[idx] + result

    return prefix + result

def convert_to_wif(hex_number, compressed=True):
    # Step 1: Prepend the version byte (0x80 for Bitcoin)
    version_byte = '80'
    payload_hex = version_byte + hex_number
    
    # For compressed WIF, append '01' at the end of the payload
    if compressed:
        payload_hex += '01'
    
    # Convert hex to bytes
    payload = bytes.fromhex(payload_hex)
    
    # Step 2 & 3: Create a checksum (double SHA-256 and take the first 4 bytes)
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    
    # Step 4: Append the checksum
    payload_checksum = payload + checksum
    
    # Step 5: Base58Check encoding
    wif = encode_base58(payload_checksum)
    
    return wif

def main():
    input_file = 'all_hex.txt'  # The file with the hexadecimal numbers
    # input_file = 'pub-hunt.txt'  # The file with the hexadecimal numbers
    output_file_wif_all = 'allwifs.txt'  # File for uncompressed WIFs
    #output_file_compressed = 'allwifs_compressed.txt'  # File for compressed WIFs
    
    try:
        with open(input_file, 'r') as file:
            hex_numbers = file.readlines()
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading {input_file}: {e}")
        return

    try:
        with open(output_file_wif_all, 'w') as file_uncompressed:   #, open(output_file_wif_all, 'w') as file_compressed:
            for hex_number in hex_numbers:
                hex_number = hex_number.strip()
                
                # Convert to uncompressed and compressed WIF
                wif_uncompressed = convert_to_wif(hex_number, compressed=False)
                wif_compressed = convert_to_wif(hex_number, compressed=True)
                
                # Write to respective files
                file_uncompressed.write(wif_uncompressed + '\n')
                file_uncompressed.write(wif_compressed + '\n')
    except Exception as e:
        print(f"An error occurred during conversion or file writing: {e}")

if __name__ == "__main__":
    main()
