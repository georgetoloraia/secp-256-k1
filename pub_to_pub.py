import binascii

p_hex = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F'
p = int(p_hex, 16)
compressed_key_hex = '02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673'
x_hex = compressed_key_hex[2:66]
x = int(x_hex, 16)
prefix = compressed_key_hex[0:2]

y_square = (pow(x, 3, p) + 7) % p
y_square_square_root = pow(y_square, (p + 1) // 4, p)
if (prefix == "02" and y_square_square_root & 1) or (prefix == "03" and not y_square_square_root & 1):
    y = (-y_square_square_root) % p
else:
    y = y_square_square_root

computed_y_hex = format(y, '064x')
computed_uncompressed_key = "04" + x_hex + computed_y_hex

print(computed_uncompressed_key)
