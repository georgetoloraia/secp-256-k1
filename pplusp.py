# Assuming the ECPoint class, Secp256k1 class, and methods (point_add, point_negate, point_subtract) are defined as earlier
from classSECP import ECPoint, Secp256k1


def point_subtract(P3, P2):
        negated_P2 = Secp256k1.point_negate(P2)
        return Secp256k1.point_add(P3, negated_P2)

def scalar_multiply(k, P):
    """Performs scalar multiplication of a point P by a scalar k."""
    result = ECPoint(None, None, True)  # Start with the point at infinity
    addend = P

    while k > 0:
        if k & 1:
            result = Secp256k1.point_add(result, addend)
        addend = Secp256k1.point_add(addend, addend)  # Double the point
        k >>= 1
        print(k)

    return result

# Example usage:

# Define the base point G (Secp256k1.G is already defined in the Secp256k1 class)
G = Secp256k1.G

# Point Doubling: 2G
P1 = Secp256k1.point_add(G, G)

# Scalar Multiplication: kG (for example, k=3)
k = 154654654651653165465165316531651532152153215321
P2 = scalar_multiply(k, G)

# Assuming you want to find P1 such that P1 + P2 = P3 (and you know P2 and P3)
# Let's say P3 is 4G for this example, which we can calculate
P3 = scalar_multiply(4, G)

# Now, find P1 given P3 and P2
P1_again = point_subtract(P3, P2)

print(f"P1: ({P1.x}, {P1.y})")
print(f"P2: ({P2.x}, {P2.y})")
print(f"P3: ({P3.x}, {P3.y})")
print(f"P1 again (P3 - P2): ({P1_again.x}, {P1_again.y})")
