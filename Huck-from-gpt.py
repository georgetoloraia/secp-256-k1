import random

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
        # with open('all_updated.txt', 'a') as f:
        #     f.write(f"{x3}\n{y3}\n")
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
    def scalar_mult(k, point):
        result = ECPoint(None, None, infinity=True)
        addend = point

        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_add(addend, addend)
            k >>= 1

        return result
    
    # @staticmethod
    # def scalar_subtract(k, point):
    #     '''
    #     point_subtract(k, point): 
    #     ყოფს წერტილს სკალარზე (მთლიანი რიცხვი). 
    #     ეს არის საკვანძო ოპერაცია ECC-ში, 
    #     რომელიც გამოიყენება კერძო გასაღებებიდან საჯარო გასაღებების გენერირებისთვის და სხვა კრიპტოგრაფიული მიზნებისთვის.
    #     '''
    #     result = ECPoint(None, None, infinity=True)
    #     addend = point
    #     while k:
    #         if k & 115792089237316195423570985008687907853269984665640564039457584007908834671663:  # If the least significant bit is 1
    #             result = Secp256k1.point_add(result, addend)
    #         addend = Secp256k1.point_subtract(addend, addend)  # Doubling the point
    #         k >>= 1#15792089237316195423570985008687907853269984665640564039457584007908834671663  # Shift right by 1 bit
    #         print(k)
    #         with open('all_updated.txt', 'a') as f:
    #             f.write(f"{addend.x}\n{addend.y}")
    #         # if k > 115792089237316195423570985008687907853269984665640564039457584007908834671663:
    #         #     break
    #     return result
    
    @staticmethod
    def generate_series_of_multiples(point, n):
        series = []
        for i in range(1, n + 1):
            multiple = Secp256k1.scalar_mult(i, point)
            series.append(multiple)
        return series
    
    # @staticmethod
    # def reverse_series_from_point(start_point, n):
    #     series = [start_point]
    #     current_point = start_point
    #     for _ in range(1, n):
    #         # Subtract G from the current point
    #         current_point = Secp256k1.point_subtract(current_point, Secp256k1.G)
    #         series.append(current_point)
    #     series.reverse()  # Reverse the series to start from P, 2P, ..., nP
    #     return series
    
    @staticmethod
    def reverse_series_from_point(start_point, n):
        series = [start_point]
        current_point = start_point
        for _ in range(1, n):
            current_point = Secp256k1.point_subtract(current_point, Secp256k1.G)
            series.append(current_point)
        series.reverse()  # Reverse the series to start from P, 2P, ..., nP
        print(series)
        return series


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


# adjusted_public_key = Secp256k1.point_subtract(public_key, Secp256k1.G)
# k = 1
# priv_key = Secp256k1.generate_priv_key(k, adjusted_public_key)
# print(priv_key.x, priv_key.y)

# priv_key = Secp256k1.generate_priv_key(k, {adjusted_public_key.x, adjusted_public_key.y})
# public_key = adjusted_public_key


'''
================= FOR P1..P2..P3..P4..P5..P6...NP =================
'''
# G = Secp256k1.G  # Generator point of Secp256k1
# n = 6 # For example, to generate up to 6P
# series_of_multiples = Secp256k1.generate_series_of_multiples(G, n)

# for i, point in enumerate(series_of_multiples, start=1):
#     print(f"{i}P = ({point.x}, {point.y})")


'''
=============== FOR NP........6P..5P..4P..3P..2P..1P ==== REVERSE =======

'''

# Assuming `series_of_multiples` contains [P, 2P, ..., 6P] as previously calculated
#start_point = series_of_multiples[-1]  # This would be 6P in your example

# start_point = public_key
# n = random.randint(65165654151665165316565516516516516565465416565151, 165165654151665165316565516516516516565465416565151)  # The number of points in the series
# n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# reversed_series = Secp256k1.reverse_series_from_point(start_point, n)
# find = None
# while start_point - Secp256k1.G != Secp256k1.generate_priv_key(start_point - Secp256k1.G, Secp256k1.G):

start_point = public_key
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
reversed_series = Secp256k1.reverse_series_from_point(start_point, n)

for i, point in enumerate(reversed_series, start=1):
    with open('all_updated.txt', 'a') as f:
        f.write(f"{point.x}\n{point.y}\n")
    print(f"{i}P = ({point.x}, {point.y})")


# for _ in range(n):
#     reversed_series = Secp256k1.reverse_series_from_point(start_point, n)
#     start_point = reversed_series
    

# for i, point in enumerate(reversed_series, start=1):
#     with open('all_updated.txt', 'a') as f:
#         f.write(f"{point.x}\n{point.y}\n")
#     print(f"{i}P = ({point.x}, {point.y})")
#     # print("Suscefully end")
