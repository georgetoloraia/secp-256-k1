from classSECP import ECPoint, Secp256k1

class Secp256k1(Secp256k1):  # Extend the existing Secp256k1 class
    @staticmethod
    def find_private_key(public_key, generator_point):
        """
        Find the private key given a public key and generator point.
        This function uses a brute force approach and is not practical for large numbers.
        """
        current_point = ECPoint(None, None, infinity=True)  # Start with the point at infinity
        for d in range(1, Secp256k1.n):
            current_point = Secp256k1.point_add(current_point, generator_point)
            print(current_point.x, public_key.x)
            if current_point.x == public_key.x and current_point.y == public_key.y:
                return d  # Private key found
        return None  # Private key not found (this should not happen if the public key is valid)

# Example usage:
generator_point = Secp256k1.G
# Assuming public_key is defined or obtained elsewhere in your code

# for example pub:
public_key_x = 0x633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852
public_key_y = 0xb078a17cc1558a9a4fa0b406f194c9a2b71d9a61424b533ceefe27408b3191e3
public_key = ECPoint(public_key_x, public_key_y)

private_key_guess = Secp256k1.find_private_key(public_key, generator_point)
if private_key_guess is not None:
    print(f"Private Key: {hex(private_key_guess)}")
else:
    print("Private Key not found.")
