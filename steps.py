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
    def point_add(p1, p2):
        # Handle the identity element (point at infinity)
        if p1.infinity:
            return p2
        if p2.infinity:
            return p1

        # Handle the case where p1 and p2 are reflections of each other over the x-axis
        if p1.x == p2.x and p1.y != p2.y:
            return ECPoint(None, None, infinity=True)

        # Handle the case where p1 and p2 are the same point (point doubling)
        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)  # Tangent is vertical
            lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
        else:
            lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
        
        x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        return ECPoint(x3, y3)

    @staticmethod
    def scalar_mult(k, point):
        result = ECPoint(None, None, infinity=True)  # Start with the point at infinity
        addend = point
        log_steps = []  # List to store steps for logging
        number = 0

        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
                log_steps.append((f'{number} - Add', result.x, result.y))  # Log the result of point addition
                number += 1
                k >>= 1
            addend = Secp256k1.point_add(addend, addend)
            log_steps.append((f'{number} - Double', addend.x, addend.y))  # Log the result of point doubling
            number += 1
            k >>= 1
            print(k)

        return result, log_steps

    @staticmethod
    def generate_public_key(private_key):
        return Secp256k1.scalar_mult(private_key, Secp256k1.G)


# Example usage:
private_key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # This should be a large, random number in a real application
public_key, log_steps = Secp256k1.generate_public_key(private_key)

# Prepare data to write to file
result_data = f"Public Key: ({hex(public_key.x)}, {hex(public_key.y)})\n"
result_data += "\nLog Steps (x, y):\n"
result_data += "\n".join([f"{step[0]}: ({hex(step[1])}, {hex(step[2])})" for step in log_steps])

# Write the public key and steps to a file
result_file_path = 'result.txt'
with open(result_file_path, 'w') as file:
    file.write(result_data)

# Write the steps to a separate file
steps_file_path = 'steps_log.txt'
with open(steps_file_path, 'w') as f:
    for step in log_steps:
        f.write(f"{hex(step[1])}\n{hex(step[2])}\n")

print(f"Public key and log steps written to {result_file_path} and {steps_file_path}, respectively.")
