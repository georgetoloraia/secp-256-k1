
# class ECPoint:
#     def __init__(self, x, y, infinity=False):
#         self.x = x
#         self.y = y
#         self.infinity = infinity  # Point at infinity (neutral element)

# class Secp256k1:
#     p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
#     a = 0
#     b = 7
#     G = ECPoint(
#         x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
#         y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
#     )
#     n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
#     h = 1

#     @staticmethod
#     def point_negate(P):
#         if P.infinity:
#             return P
#         return ECPoint(P.x, -P.y % Secp256k1.p, P.infinity)
    
#     @staticmethod
#     def point_add(p1, p2):
#         if p1.infinity:
#             return p2
#         if p2.infinity:
#             return p1
#         if p1.x == p2.x and p1.y != p2.y:
#             return ECPoint(None, None, infinity=True)
#         if p1.x == p2.x and p1.y == p2.y:
#             if p1.y == 0:
#                 return ECPoint(None, None, infinity=True)
#             lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
#         else:
#             lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
#         x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
#         y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
#         return ECPoint(x3, y3)

#     @staticmethod
#     def scalar_mult(k, point):
#         result = ECPoint(None, None, True)
#         addend = point
#         while k:
#             if k & 1:
#                 result = Secp256k1.point_add(result, addend)
#             addend = Secp256k1.point_add(addend, addend)
#             k >>= 1
#         return result

#     @staticmethod
#     def generate_public_key(private_key):
#         return Secp256k1.scalar_mult(private_key, Secp256k1.G)

# def point_subtract(P3, P2):
#     negated_P2 = Secp256k1.point_negate(P2)
#     return Secp256k1.point_add(P3, negated_P2)

# def scalar_multiply(k, P):
#     result = ECPoint(None, None, True)
#     addend = P
#     while k:
#         if k & 1:
#             result = Secp256k1.point_add(result, addend)
#         addend = Secp256k1.point_add(addend, addend)
#         k >>= 1
#     return result

# # Example usage:
# G = Secp256k1.G
# P1 = Secp256k1.point_add(G, G)
# k = 115792089237316195423570985008687907852837564279074904382605163141518161494336
# P2 = scalar_multiply(k, G)
# P3 = scalar_multiply(4, G)
# P1_again = point_subtract(P3, P2)

# print(f"P1: ({P1.x}, {P1.y})")
# print(f"P2: ({P2.x}, {P2.y})")
# print(f"P3: ({P3.x}, {P3.y})")
# print(f"P1 again (P3 - P2): ({P1_again.x}, {P1_again.y})")


# # file_path = 'george.txt'
# # with open(file_path, 'a') as file:
# #     file.write(f"P1: ({P1.x}, {P1.y})"
# #                f"P2: ({P2.x}, {P2.y})"
# #                f"P3: ({P3.x}, {P3.y})"
# #                f"P1 again (P3 - P2): ({P1_again.x}, {P1_again.y})")

# # file_path




class ECPoint:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity  # Point at infinity (neutral element)

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
    def point_negate(P):
        if P.infinity:
            return P
        return ECPoint(P.x, -P.y % Secp256k1.p, P.infinity)
    
    @staticmethod
    def point_add(p1, p2):
        if p1.infinity:
            return p2
        if p2.infinity:
            return p1
        if p1.x == p2.x and p1.y != p2.y:
            return ECPoint(None, None, infinity=True)
        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)
            # lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
            lam = ((p1.x - 2 + Secp256k1.a) / pow(p1.y, 1, Secp256k1.p / 2)) % Secp256k1.p
        else:
            # lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
            lam = ((p2.y + p1.y) / pow(p2.x + p1.x, 1, Secp256k1.p)) % Secp256k1.p
        # x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        # y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        x3 = (lam*2 - p1.x - p2.x) % Secp256k1.p
        y3 = ((p1.x - x3) - p1.y) % Secp256k1.p
        return ECPoint(x3, y3)

    @staticmethod
    def scalar_mult(k, point):
        result = ECPoint(None, None, True)
        addend = point
        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_add(addend, addend)
            k >>= 1
            print(k)
        return result

    @staticmethod
    def generate_public_key(private_key):
        return Secp256k1.scalar_mult(private_key, Secp256k1.G)

def point_subtract(P3, P2):
    negated_P2 = Secp256k1.point_negate(P2)
    return Secp256k1.point_add(P3, negated_P2)

G = Secp256k1.G
P3 = Secp256k1.scalar_mult(4, G)  # Calculate P3 = 4G

# Display P3 coordinates
print(P3.x, P3.y)
