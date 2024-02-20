def main():
    # input_file = 'bolotest.txt'  # The file with the decimal numbers
    input_file = 'all_updated.txt'
    output_file_hex = 'all_hex.txt'  # The file to write the 64-character hexadecimal strings to

    try:
        with open(input_file, 'r') as file:
            numbers = file.readlines()
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading {input_file}: {e}")
        return

    try:
        with open(output_file_hex, 'w') as file_hex:
            for number in numbers:
                number = number.strip()
                
                # Convert number to hex, remove the '0x' prefix, and pad with zeros to make it 64 characters
                hex_number = hex(int(number))[2:].zfill(64)
                
                # Write the 64-character hex string to the file
                file_hex.write(hex_number + '\n')
    except Exception as e:
        print(f"An error occurred during conversion or file writing: {e}")

if __name__ == "__main__":
    main()
    