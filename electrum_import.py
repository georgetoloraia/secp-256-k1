import subprocess
from concurrent.futures import ThreadPoolExecutor

# Function to import a single private key
def import_key(key):
    try:
        # Customize the command below according to your wallet's CLI import command
        command = ['electrum', 'importprivkey', key, '-w', '/home/george/.electrum/wallets/gio']
        subprocess.run(command, check=True)
        print(f"Successfully imported key: {key}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to import key: {key} with error: {e}")

# Load private keys from a file
keys_file = 'allwifs.txt'
with open(keys_file, 'r') as file:
    private_keys = [line.strip() for line in file.readlines() if line.strip()]

# Use ThreadPoolExecutor to import keys in parallel
with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your system's capabilities
    executor.map(import_key, private_keys)


        # command = [electrum_path, 'importprivkey', key, '-w', '/home/george/.electrum/wallets/gio']