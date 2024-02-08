# Convert the hexadecimal number to decimal
hex_number = "a6b627abb58d7ab22588dd13d40cbdd60f0da7bb38881d171ef178c35d890f0d"
decimal_number = int(hex_number, 16)
print(decimal_number)

while decimal_number:
    decimal_number >>= 130
    print(decimal_number)