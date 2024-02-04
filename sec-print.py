class ECPoint:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity  # Point at infinity (neutral element)

    def __repr__(self):
        if self.infinity:
            return "Infinity"
        return f"({hex(self.x)}, {hex(self.y)})"

class Secp256k1:
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    G = ECPoint(
        x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    )
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 1

    @staticmethod
    def point_add(p1, p2):
        print(f"\n--- Point Addition: {p1} + {p2} ---")
        if p1.infinity:
            print(f"Point {p1} is at infinity, returning {p2}\n")
            return p2
        if p2.infinity:
            print(f"Point {p2} is at infinity, returning {p1}\n")
            return p1

        if p1.x == p2.x and p1.y != p2.y:
            print(f"Points {p1} and {p2} are vertical reflections, returning Infinity\n")
            return ECPoint(None, None, infinity=True)

        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                print(f"Tangent at {p1} is vertical, returning Infinity\n")
                return ECPoint(None, None, infinity=True)
            print(f"Point doubling case, points are the same\n")
            lam_num = (3 * p1.x**2 + Secp256k1.a)
            lam_den = (2 * p1.y)
            lam = (lam_num * pow(lam_den, -1, Secp256k1.p)) % Secp256k1.p
            print(f"λ numerator: {lam_num}")
            print(f"λ denominator: {lam_den}")
            print(f"λ LAM: {lam}")
            file.write(f"{lam_den}\n")
            file.write(f"{lam}\n")
        else:
            print(f"General case, different points\n")
            lam_num = (p2.y - p1.y)
            lam_den = (p2.x - p1.x)
            lam = (lam_num * pow(lam_den, -1, Secp256k1.p)) % Secp256k1.p
            print(f"λ numerator: {lam_num}")
            print(f"λ denominator: {lam_den}")
            file.write(f"{lam_den}\n")
            file.write(f"{lam}\n")

        print(f"Calculated λ (slope): {lam}")
        x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        result = ECPoint(x3, y3)
        print(f"Resulting Point after addition: {result}")
        return result

    @staticmethod
    def scalar_mult(k, point):
        print(f"\n--- Scalar Multiplication: {hex(k)} * {point} ---")
        result = ECPoint(None, None, infinity=True)  # Start with the point at infinity
        addend = point

        while k:
            if k & 1:
                print(f"\nAdding {result} to {addend} because of a '1' in the binary expansion of k")
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_add(addend, addend)
            print(f"\nDoubling point to {addend} for next bit")
            k >>= 1

        print(f"\nFinal result of Scalar Multiplication: {result}")
        return result

    @staticmethod
    def generate_public_key(private_key):
        print(f"\n--- Generating Public Key from Private Key: {hex(private_key)} ---")
        public_key = Secp256k1.scalar_mult(private_key, Secp256k1.G)
        print(f"\nGenerated Public Key: {public_key}")
        return public_key


# Open the file at the beginning of your script
file = open('numbers.txt', 'w')

# Example usage:
private_key = 0xf
public_key = Secp256k1.generate_public_key(private_key)
print(f"\nFinal Public Key: {public_key}")

# Close the file at the end of your script
file.close()