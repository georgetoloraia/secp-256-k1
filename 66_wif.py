from bit import Key
import csv

# Replace these with your actual min and max values
min_value = 36893489178211254272
max_value = 73786694819861495808

def convert_to_wif_and_save(min_val, max_val):
    with open('compressed_wifs.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for i in range(min_val, max_val + 1):
            # Convert the number to a 32-byte (64 hex characters) format, padding with zeros if necessary
            hex_format = format(i, '064x')
            
            # Create a Key object from the hex private key and get the WIF
            wif_compressed = Key.from_hex(hex_format).to_wif()
            
            # Write the WIF to the file
            writer.writerow([wif_compressed])
    
    print(f"WIF compressed private keys from {min_val} to {max_val} have been saved to compressed_wifs.csv")

# Call the function with your range
convert_to_wif_and_save(min_value, max_value)
