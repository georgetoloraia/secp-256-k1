# import secrets

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
#     def point_add(p1, p2):
#         # Handle the identity element (point at infinity)
#         if p1.infinity:
#             return p2
#         if p2.infinity:
#             return p1

#         # Handle the case where p1 and p2 are reflections of each other over the x-axis
#         if p1.x == p2.x and p1.y != p2.y:
#             return ECPoint(None, None, infinity=True)

#         # Handle the case where p1 and p2 are the same point (point doubling)
#         if p1.x == p2.x and p1.y == p2.y:
#             if p1.y == 0:
#                 return ECPoint(None, None, infinity=True)  # Tangent is vertical
#             lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
#         else:
#             lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
        
#         x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
#         y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
#         return ECPoint(x3, y3)

#     @staticmethod
#     def scalar_mult(k, point):
#         result = ECPoint(None, None, infinity=True)  # Start with the point at infinity
#         addend = point
#         log_steps = []  # List to store steps for logging
#         number = 0
#         unique_hex_values = set()  # Set to store unique x values in hex

#         while k:
#             if k & 1:
#                 result = Secp256k1.point_add(result, addend)
#                 log_steps.append((f'{number} - Add', result.x, result.y))  # Log the result of point addition
#                 if not result.infinity:
#                     unique_hex_values.add(hex(result.x)[2:].zfill(64))  # Add x value of result to set
#                 number += 1
#                 k >>= 1
#             addend = Secp256k1.point_add(addend, addend)
#             log_steps.append((f'{number} - Double', addend.x, addend.y))  # Log the result of point doubling
#             if not addend.infinity:
#                 unique_hex_values.add(hex(addend.x)[2:].zfill(64))  # Add x value of addend to set
#             number += 1
#             k >>= 1

#         return result, log_steps, unique_hex_values

#     @staticmethod
#     def generate_public_key(private_key):
#         public_key, log_steps, unique_hex_values = Secp256k1.scalar_mult(private_key, Secp256k1.G)
#         return public_key, log_steps, unique_hex_values

'''
=====================================================================================================================

'''

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
        '''
        point_add(p1, p2): 
        ამატებს ორ წერტილს მრუდზე. 
        ეს მეთოდი ახორციელებს ელიფსური მრუდების დამატების წესებს, 
        მათ შორის წერტილის დამუშავებას უსასრულობაში და გაორმაგების წერტილებში.
        '''
        if p1.infinity:
            return p2
        if p2.infinity:
            return p1
        if p1.x == p2.x and p1.y != p2.y:
            return ECPoint(None, None, infinity=True)
        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)
            lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
        else:
            lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
        x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        with open('all_updated.txt', 'a') as f:
            f.write(f"{x3}\n{y3}\n")
        return ECPoint(x3, y3)

    @staticmethod
    def point_negate(P):
        '''
        point_negate(P): 
        უარყოფს მრუდის წერტილს. 
        ელიფსური მრუდების კონტექსტში, წერტილის უარყოფა (x, y) იწვევს (x, -y).
        '''
        if P.infinity:
            return P
        return ECPoint(P.x, -P.y % Secp256k1.p, P.infinity)

    @staticmethod
    def point_subtract(P1, P2):
        '''
        point_subtract(P1, P2): 
        აკლებს ერთ წერტილს მეორეს პირველი პუნქტის მიმატებით მეორის უარყოფაზე.
        '''
        P2_neg = Secp256k1.point_negate(P2)
        return Secp256k1.point_add(P1, P2_neg)

    @staticmethod
    def scalar_mult(k, point):
        '''
        scalar_mult(k, point): 
        ამრავლებს წერტილს სკალარზე (მთლიანი რიცხვი). 
        ეს არის საკვანძო ოპერაცია ECC-ში, 
        რომელიც გამოიყენება კერძო გასაღებებიდან საჯარო გასაღებების გენერირებისთვის და სხვა კრიპტოგრაფიული მიზნებისთვის.
        '''
        result = ECPoint(None, None, infinity=True)
        addend = point
        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_add(addend, addend)
            k >>= 1
        return result

    @staticmethod
    def generate_public_key(private_key):
        '''
        generate_public_key(private_key): 
        ქმნის საჯარო გასაღებს მოცემული პირადი გასაღებიდან გენერატორის 
        წერტილით პირადი გასაღების სკალარული გამრავლებით G.
        '''
        return Secp256k1.scalar_mult(private_key, Secp256k1.G)

public_key = ECPoint(
    0x6c117bb5baa1e55d994453776f284a0542d2149aab967e9572227f7985bf6702,
    0x170b379e47ad394d28495200e0af77aa8d3a54c35c19353284ba3fdc63e02261
)

# with open('allhex.txt', 'a') as f:
for i in range(100000):

    adjusted_public_key = Secp256k1.point_subtract(public_key, Secp256k1.G)
    public_key = adjusted_public_key
    # f.write(f"{public_key.x:064x}\n{public_key.y:064x}\n")
    # print(f"Public Key: ({hex(public_key.x)}, {hex(public_key.y)})")
    # print(f"Adjusted Public Key: ({hex(adjusted_public_key.x)}, {hex(adjusted_public_key.y)})")
    # public_key.x >>= 1
    # public_key.y >>= 1
    # print(i)
    # if i > 49750000:
    # Format and save x and y coordinates in hexadecimal format without '0x'
    # f.write(f"{public_key.x:064x}\n{public_key.y:064x}\n")


# for _ in range(1111111111111111111):
#     adjusted_public_key = Secp256k1.point_subtract(public_key, Secp256k1.G)
#     public_key = adjusted_public_key
#     count = 0
#     if public_key == Secp256k1.G:
#         print(public_key)
#         break
#     count += 1
#     print(count)



# ... (rest of the code remains the same)
# for prv in range(500):
# prv = 256
# pivate_key = 0x24944f33566d9ed9c410ae72f89454ac6f0cfee446590c01751f094e185e8978
# private_key = secrets.randbits(prv)
# Gnerate public key and get unique hex values
# public_key, log_steps, unique_hex_values = Secp256k1.generate_public_key(private_key)
# Rad existing hex values from the file
# existing_hex_values = set()
# try:
#     with open('all_hex.txt', 'r') as file:
#         existing_hex_values = set(line.strip() for line in file.readlines())
# except FileNotFoundError:
#     pass  # It's okay if the file does not exist
# # Ad new unique hex values
# new_unique_hex_values = unique_hex_values - existing_hex_values
# # Wite the unique hex values to a file, if there are any new ones
# if new_unique_hex_values:
#     with open('all_hex.txt', 'a') as f:
#         for hex_val in new_unique_hex_values:
#             f.write(f"{hex_val}\n")
# print(f"All unique hex values written to all_hex.txt. {private_key}")
