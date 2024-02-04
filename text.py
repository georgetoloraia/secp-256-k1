# a = 44886295857190546091508615621464465421050773292389158775895365558788257183826
# b = 105763930690168876419447522708898122231025455770824018376675628205220653735917

# ab = a + b

# maximum = 115792089237316195423570985008687907853269984665640564039457584007908834671663

# sex = 115792089237316195423570985008687907852837564279074904382605163141518161494337

# res = maximum - ab

# result = res - sex

# total = a - result

# full = total // 130

# print(res)
# print(result)
# print(total)
# print(full)
# print(a - b)

import os
import ecdsa
import secrets

# Select the curve (using secp256k1 as an example)
curve = ecdsa.SECP256k1

# Generate a private key
private_key = secrets.randbelow(curve.order)

print("Private Key:", hex(private_key))
