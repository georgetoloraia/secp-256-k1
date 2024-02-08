import secrets

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
        unique_hex_values = set()  # Set to store unique x values in hex

        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
                log_steps.append((f'{number} - Add', result.x, result.y))  # Log the result of point addition
                if not result.infinity:
                    unique_hex_values.add(hex(result.x)[2:].zfill(64))  # Add x value of result to set
                number += 1
                k >>= 1
            addend = Secp256k1.point_add(addend, addend)
            log_steps.append((f'{number} - Double', addend.x, addend.y))  # Log the result of point doubling
            if not addend.infinity:
                unique_hex_values.add(hex(addend.x)[2:].zfill(64))  # Add x value of addend to set
            number += 1
            k >>= 1

        return result, log_steps, unique_hex_values

    @staticmethod
    def generate_public_key(private_key):
        public_key, log_steps, unique_hex_values = Secp256k1.scalar_mult(private_key, Secp256k1.G)
        return public_key, log_steps, unique_hex_values

# ... (rest of the code remains the same)
for prv in range(500):
    prv = 256
# private_key = 0x24944f33566d9ed9c410ae72f89454ac6f0cfee446590c01751f094e185e8978
    private_key = secrets.randbits(prv)

# Generate public key and get unique hex values
    public_key, log_steps, unique_hex_values = Secp256k1.generate_public_key(private_key)

# Read existing hex values from the file
    existing_hex_values = set()
    try:
        with open('all_hex.txt', 'r') as file:
            existing_hex_values = set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        pass  # It's okay if the file does not exist

# Add new unique hex values
    new_unique_hex_values = unique_hex_values - existing_hex_values

# Write the unique hex values to a file, if there are any new ones
    if new_unique_hex_values:
        with open('all_hex.txt', 'a') as f:
            for hex_val in new_unique_hex_values:
                f.write(f"{hex_val}\n")

    print(f"All unique hex values written to all_hex.txt. {private_key}")

