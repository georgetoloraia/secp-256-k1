# Read the hex values from 'all_hex.txt'
with open('all_hex.txt', 'r') as file:
    hex_values_from_file = file.read().splitlines()

# Given hexadecimal number
hex_num1 = "633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852"

# Convert hex_num1 to an integer
int_num1 = int(hex_num1, 16)

# Initialize a list to store the results
results = []

# Perform the subtraction for each hex value in the file
for hex_val in hex_values_from_file:
    # Convert the current hex value from the file to an integer
    int_num2 = int(hex_val, 16)
    
    # Perform the subtraction
    if int_num1 > int_num2:
        result_int = int_num1 - int_num2
    
        # Convert the result back to hex and store it in the list
        result_hex = hex(result_int)
        result_hex = result_hex[2:].zfill(64)
        results.append(result_hex)

result_file_path = 'pub-hunt.txt'  # Using a writable directory
with open(result_file_path, 'w') as file:
    for result in results:
        file.write(result + '\n')

result_file_path  # Returning the path to the saved file

# # Save the results to 'pub-hunt.txt'
# with open('pub-hunt.txt', 'w') as file:
#     for result in results:
#         file.write(result + '\n')

# # Return the path to the saved file
# 'pub-hunt.txt'
