from classSECP import Secp256k1
# def double_and_add(base, exponent):
#     result = 1
#     binary_exponent = bin(exponent)[2:]  # Convert exponent to binary and remove '0b' prefix
#     for bit in binary_exponent[1:]:  # Start from the second bit, ignoring the first one
#         result *= result  # Double the result
#         if bit == '1':
#             result *= base  # Add if the bit is '1'
#         print("bit : ", bit)
#         # print("result : ", result)
#     return result

# # Example usage:
# base = 55066263022277343669578718895168534326250603453777594175500187360389116729240
# exponent = 7
# result = double_and_add(base, exponent)
# print("Result:", result)

# Define the parameters of the elliptic curve
p = 2**256 - 2**32 - 977
a = 0
b = 7

# Define the modular inverse function
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0

def divide_points(point1, point2, a, p):
    """Division of points on elliptic curve"""
    if point1 is None or point2 is None:
        return None

    # Inversion of point2
    point2_inv = (point2[0], -point2[1] % p)

    # Multiplication of point1 by the inverse of point2
    return add_points(point1, point2_inv)

# Define the point addition operation on the elliptic curve
def add_points(point1, point2):
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        return None  # Points are inverses, result is point at infinity

    if x1 == x2:
        lam = (3 * x1 * x1 + a) * modinv(2 * y1, p)
    else:
        lam = (y2 - y1) * modinv(x2 - x1, p)

    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return x3, y3

# Define the point doubling operation on the elliptic curve
def double_point(point):
    if point is None:
        return None

    x, y = point
    lam = (3 * x * x + a) * modinv(2 * y, p)

    x3 = (lam**2 - 2 * x) % p
    y3 = (lam * (x - x3) - y) % p

    return x3, y3

# Define the reverse_double_and_add function
def reverse_double_and_add(current_public_key, base_point):
    previous_steps = []
    current_point = current_public_key
    binary_y = bin(current_point[1])[2:]

    for bit in binary_y[1:]:
        current_point = double_point(current_point)
        if bit == '1':
            current_point = add_points(current_point, base_point)
        previous_steps.append(current_point)

    return previous_steps



def reverse_double_and_add(current_public_key, base_point):
    # Initialize the list to store the previous steps
    previous_steps = []

    # Initialize the current point to the current public key
    current_point = current_public_key

    # Reverse the binary representation of the y-coordinate
    # The x-coordinate will always be the same in this context
    binary_y = bin(current_point[1])[2:]

    # Loop through the binary representation, skipping the first bit (most significant bit)
    for bit in binary_y[1:]:
        # Double the current point
        current_point = double_point(current_point)

        # If the bit is '1', add the base point to the current point
        if bit == '1':
            current_point = add_points(current_point, base_point)

        # Append the current point to the list of previous steps
        previous_steps.append(current_point)

    return previous_steps

current_public_key = (0, 0)
base_point = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)  # Base point of the curve

bublik = 115792089237316195423570985008687907852837564279074904382605163141518161494337

# Read the contents of all_updated.txt into a set to check for duplicates
with open('all_updated.txt', 'r') as f:
    existing_results = set(map(str.strip, f.readlines()))

for i in range(750000):
    previous_steps = divide_points(current_public_key, base_point, a, p)
    # print("previous_step = ", previous_steps)
    
    if i > 720000:
        for step in previous_steps:
            result = bublik - previous_steps[0]
            result_str = str(abs(result))
            mimateba = bublik - previous_steps[1]
            orjer = bublik + int(result_str)
            orjerNaklebi = bublik - int(result_str)
            orjerNaklebi_str = str(abs(int(orjerNaklebi)))  # Convert to int before taking absolute value

            # Check if result_str or any derived values are not already written
            if result_str not in existing_results and \
               str(abs(mimateba)) not in existing_results and \
               str(abs(orjer)) not in existing_results and \
               orjerNaklebi_str not in existing_results:  # Use orjerNaklebi_str here
                # Open the file in append mode and write the values
                with open('all_updated.txt', 'a') as f:
                    f.write(f"{result_str}\n")
                    if int(mimateba) < int(bublik):
                        f.write(f"{mimateba}\n")
                    if int(orjer) < int(bublik):
                        f.write(f"{orjer}\n")
                    if int(orjerNaklebi_str) < int(bublik):
                        f.write(f"{orjerNaklebi_str}\n")
                # Update the set of existing results
                existing_results.add(result_str)
                existing_results.add(str(abs(mimateba)))
                existing_results.add(str(abs(orjer)))
                existing_results.add(orjerNaklebi_str)
    
    current_public_key = double_point(previous_steps)
    # base_point = double_point(current_public_key)


