import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def import_key(key):
    """
    Attempts to import a single private key into an Electrum wallet.
    """
    try:
        # Customize this command according to your needs
        command = ['electrum', 'importprivkey', key, '-w', '/home/george/.electrum/wallets/gio']
        subprocess.run(command, check=True, capture_output=True)
        logging.info(f"Successfully imported key: {key}")
    except subprocess.CalledProcessError as e:
        # Log the error with the command that caused it
        logging.error(f"Failed to import key: {key} with error: {e}. Command: {' '.join(command)}")

def main():
    """
    Main function to load private keys and import them using ThreadPoolExecutor.
    """
    keys_file = 'allwifs.txt'
    with open(keys_file, 'r') as file:
        private_keys = [line.strip() for line in file.readlines() if line.strip()]

    # Use ThreadPoolExecutor to import keys in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all private keys for importing
        future_to_key = {executor.submit(import_key, key): key for key in private_keys}
        
        # Wait for all futures to complete, logging errors as they occur
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                future.result()  # This will re-raise any exception caught during the execution
            except Exception as exc:
                logging.error(f'Key import generated an exception: {key}. Error: {exc}')

if __name__ == '__main__':
    main()
