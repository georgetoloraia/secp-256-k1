# Correcting and running the provided code snippet

# Convert the hexadecimal string to an integer
K = int("a4e7377eaabacc39f5b2bd2cd4bcb5ed1855939619e491c79c0bb5793d4edbf3", 16)

# Prepare to write the output to a file
file_path = "all_updated.txt"
with open(file_path, "w") as file:
    while K:
        K >>= 1  # Perform the bitwise right shift operation
        if K > 22588426139751334071:
            file.write(f"{K}\n")  # Write the current value of K to the file

file_path  # Return the path of the created file for access
