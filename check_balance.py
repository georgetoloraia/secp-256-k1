from bit import Key

# Path to your file containing private keys
file_path = 'all_hex.txt'

# Open the file and read each line
with open(file_path, 'r') as file:
    private_keys = file.readlines()

# Iterate over each private key, remove any whitespace, and check balance
for private_key in private_keys:
    private_key = private_key.strip()  # Remove whitespace/newline characters

    try:
        # Convert private key to Bitcoin address
        key = Key.from_hex(private_key)
        address = key.address

        # Check balance
        balance = key.get_balance('btc')

        print(f"Address: {address}")
        print(f"Balance: {balance} BTC")
    except Exception as e:
        print(f"Failed to process key {private_key}: {e}")
