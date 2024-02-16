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
        # print(x3, y3)
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
        # P1_neg = Secp256k1.point_add(P1)
        P2_neg = Secp256k1.point_negate(P2)
        # print(P2_neg.x, P2_neg.y)
        return Secp256k1.point_add(P1, P2_neg)
    
    @staticmethod
    def scalar_subtract(k, point):
        '''
        point_subtract(k, point): 
        ყოფს წერტილს სკალარზე (მთლიანი რიცხვი). 
        ეს არის საკვანძო ოპერაცია ECC-ში, 
        რომელიც გამოიყენება კერძო გასაღებებიდან საჯარო გასაღებების გენერირებისთვის და სხვა კრიპტოგრაფიული მიზნებისთვის.
        '''
        result = ECPoint(None, None, infinity=True)
        addend = point
        while k:
            if k & 115792089237316195423570985008687907853269984665640564039457584007908834671663:  # If the least significant bit is 1
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_subtract(addend, addend)  # Doubling the point
            k >>= 1#15792089237316195423570985008687907853269984665640564039457584007908834671663  # Shift right by 1 bit
            print(k)
            with open('all_updated.txt', 'a') as f:
                f.write(f"{addend.x}\n{addend.y}")
            # if k > 115792089237316195423570985008687907853269984665640564039457584007908834671663:
            #     break
        return result
    
    @staticmethod
    def generate_priv_key(private_key, pub):
        '''
        generate_public_key(private_key): 
        ქმნის საჯარო გასაღებს მოცემული პირადი გასაღებიდან გენერატორის 
        წერტილით პირადი გასაღების სკალარული გამრავლებით G.
        '''
        return Secp256k1.scalar_subtract(private_key, pub)


public_key = ECPoint(
    0x6c117bb5baa1e55d994453776f284a0542d2149aab967e9572227f7985bf6702,
    0x170b379e47ad394d28495200e0af77aa8d3a54c35c19353284ba3fdc63e02261
)


adjusted_public_key = Secp256k1.point_subtract(public_key, Secp256k1.G)
k = 1
priv_key = Secp256k1.generate_priv_key(k, adjusted_public_key)
# print(priv_key.x, priv_key.y)

# priv_key = Secp256k1.generate_priv_key(k, {adjusted_public_key.x, adjusted_public_key.y})
# public_key = adjusted_public_key
