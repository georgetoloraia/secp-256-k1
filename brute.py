
from george import *


# def brute_force_private_key(p, G, n):
#     current = ECPoint(None, None, True)  # Start with the point at infinity
#     for k in range(1, n):
#         current = Secp256k1.point_add(current, G)
#         if current.x == p.x and current.y == p.y:
#             return k  # Private key found
#     return None  # Private key not found

# existing = (
#     x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
#     y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
# )

# # existing_public_key = (x, y)
# brut = brute_force_private_key(existing, Secp256k1.G, Secp256k1.n)

from george import *  # Assuming george.py defines ECPoint, Secp256k1, and related functions
import random

# def brute_force_private_key(public_key, G, n):
#     """
#     Attempt to find the private key for a given public key by brute force.
#     This is computationally infeasible for large n, such as in real ECC parameters.
#     """
#     current = ECPoint(None, None, True)  # Start with the point at infinity
#     # k = random.randint(7237005577332262213973186563042994240829374041602535252466099000494570602496, 115792089237316195423570985008687907852837564279074904382605163141518161494336)
#     while k & n:
#         current = Secp256k1.point_add(current, G)
#         with open(output_file, 'a') as file:  # Open file in append mode
#             if k > 11111111111111111111111111111111:
#                 file.write(f"{k}\n")  # Write k to file, followed by a newline
#         # print(current.x)
#         if current.x == public_key.x and current.y == public_key.y:
#             return k  # Private key foundcl
#         k >>= 1
#         # print(k)
#     return None  # Private key not found

def reverse_ec_multiplication(target_public_key, G, p):
    current = target_public_key
    count = 0
    while not (current.x == G.x and current.y == G.y) and count < p:
        current = point_subtract(current, G)  # Define this function based on your ECC library
        with open(output_file, 'a') as file:
            mypriv = str(current.x)
            if mypriv not in output_file:
                file.write(f"{mypriv}\n")
        count += 1
    return count if count < p else None


# Define the existing public key as an ECPoint
existing_public_key = ECPoint(
    0xb0bd634234abbb1ba1e986e884185c61cf43e001f9137f23c2c409273eb16e65,
    0x37a576782eba668a7ef8bd3b3cfb1edb7117ab65129b8a2e681f3c1e0908ef7b
)

# File to store all k values attempted
output_file = "all_updated.txt"

# Attempt to brute-force the private key (this is for educational purposes and not practical)
# for _ in range(100):
private_key_guess = reverse_ec_multiplication(existing_public_key, Secp256k1.G, Secp256k1.n)

if private_key_guess:
    print(f"Private Key Found: {private_key_guess}")
else:
    print("Private Key Not Found.")



# # Calculate P1 = 2G directly to confirm
# P1 = Secp256k1.scalar_mult(2, G)

# # Given the logic, k should be 2, let's calculate P2 using this k value
# P2 = Secp256k1.scalar_mult(2, G)  # This should be identical to P1 as per our logic

# # Calculate P1 again by subtracting P2 from P3, which should give us 2G again
# P1_again = point_subtract(P3, P2)

# # Display P1, P2, and P1 again coordinates to confirm they match
# # print(P1.x, P1.y)
# # print(P2.x, P2.y)
# # print(P1_again.x, P1_again.y)
