import random

public_x = random.randrange(250) #68167119367492385946477614127391411699187587739043560034303210379772692937810
public_y = random.randrange(265) #98811869135478233071017892877157889966923567543651789733849964475999540762862

point_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240  # Example point x-coordinate
point_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424  # Example point y-coordinate

# Define the parameters of the elliptic curve
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

# Perform elliptic curve point addition
def point_add(x1, y1, x2, y2):
    # Handle the point at infinity (neutral element)
    if x1 is None and y1 is None:
        return x2, y2
    if x2 is None and y2 is None:
        return x1, y1
    
    if x1 == x2 and y1 == -y2 % p:
        # Result is the point at infinity
        return None, None

    if x1 != x2:
        # Point addition
        lam = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    else:
        # Point doubling
        lam = ((3 * x1**2 + a) * pow(2 * y1, -1, p)) % p

    x3 = (lam**2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return x3, y3


def add_to_public_key(x, y, point_x, point_y):
    # Define the parameters of the elliptic curve
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7

    # Perform elliptic curve point addition
    # Handle the point at infinity (neutral element)
    if x is None and y is None:
        return point_x, point_y
    if point_x is None and point_y is None:
        return x, y

    if x == point_x and y == -point_y % p:
        # Result is the point at infinity
        return None, None

    if x != point_x:
        # Point addition
        lam = ((point_y - y) * pow(point_x - x, -1, p)) % p
    else:
        # Point doubling
        lam = ((3 * x**2 + a) * pow(2 * y, -1, p)) % p

    result_x = (lam**2 - x - point_x) % p
    result_y = (lam * (x - result_x) - y) % p
    return result_x, result_y


def subtract_from_public_key(x, y, point_x, point_y):
    # Define the parameters of the elliptic curve
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7

    # Inversion of the point to subtract
    neg_point_x = point_x
    neg_point_y = (-point_y) % p

    # Perform addition with the negated point
    return add_to_public_key(x, y, neg_point_x, neg_point_y)




'''
=======================================================================================
'''
# Perform point addition with the given public key coordinates
# for _ in range(200000):
#     result_x, result_y = point_add(public_x, public_y, public_x, public_y**2)
    

#     # Write the result to a file
#     with open('all_updated.txt', 'a') as f:
#         f.write(f"{result_x}\n{result_y}\n")
        
#     public_x = result_x
#     public_y = result_y
    
 
for _ in range(512): 
       
    result_x, result_y = add_to_public_key(public_x, public_y, point_x, point_y)
    add_x = result_x
    add_y = result_y
    print("Resulting public key after addition:")
    print("x coordinate:", result_x)
    print("y coordinate:", result_y)


    '''
    ==============================================================================================
    '''

    # Example usage:
    public_sub_x = 48880677861299690856658088055125989625640029475885893704894027831058867644162
    public_sub_y = 10423014698396768911386147068123259725300810066342609181801714270124355101281


    subtract_x, subtract_y = subtract_from_public_key(public_sub_x, public_sub_y, point_x, point_y)

    print("Resulting public key after subtraction:")
    print("x coordinate:", subtract_x)
    print("y coordinate:", subtract_y)
    
    with open('all_updated.txt', 'a') as f:
        f.write(f"{result_x}\n{result_y}\n")
        
        # f.write(f"{result_x}\n{result_y}\n{subtract_x}\n{subtract_y}\n")
        
    
    public_x = result_x
    result_y = result_y
    public_sub_x = subtract_x
    public_sub_y = subtract_y