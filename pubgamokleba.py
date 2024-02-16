# curent_x = 48880677861299690856658088055125989625640029475885893704894027831058867644162
# curent_y = 10423014698396768911386147068123259725300810066342609181801714270124355101281

# G_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
# G_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424


# for _ in range(5000):
#     back_x = curent_x - G_x
#     back_y = curent_y - G_y
#     if "-" is back_x:
#         back_x.replace("-", "")
#         curent_x = back_x
#     else:
#         curent_x = back_x
      
#     if "-" is back_y:
#         back_y.replace("-", "")
#         curent_y = back_y
#     else:
#         curent_y = back_y
        
#     with open('all_updated.txt', 'a') as f:
#         f.write(f"{back_x}\n{back_y}\n")
    
    

# print(f"generatet suscefuly")


'''
=================== es wava ra ===================================================
'''
curent_x = 48880677861299690856658088055125989625640029475885893704894027831058867644162
curent_y = 10423014698396768911386147068123259725300810066342609181801714270124355101281

G_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

for _ in range(50000):
    back_x = curent_x - G_x
    back_y = curent_y - G_y
    
    if back_x < 0:
        back_x = -back_x
        G_x = back_x
    else:
        G_x = back_x
      
    if back_y < 0:
        back_y = -back_y
        G_y = back_y
    else:
        G_y = back_y
        
    with open('all_updated.txt', 'a') as f:
        f.write(f"{back_x}\n{back_y}\n")
    
print("Generated successfully.")



'''
=================== es ar mushaobs kargad =============================================
'''
# # Given coordinates
# current_x = 48880677861299690856658088055125989625640029475885893704894027831058867644162
# current_y = 10423014698396768911386147068123259725300810066342609181801714270124355101281

# # Generator point
# G_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
# G_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

# # Scalar multiplication
# scalar = current_x  # Use current_x as the scalar

# # Initialize the result as the identity element (point at infinity)
# result_x = 0
# result_y = 0

# # Perform scalar multiplication
# for bit in bin(scalar)[2:]:
#     # Double the result point
#     result_x, result_y = result_x * 2, result_y * 2
    
#     # If the current bit of the scalar is 1, add the generator point
#     if bit == '1':
#         # Perform point addition
#         result_x = G_x
#         result_y = G_y

#         # Ensure result is on the curve by taking modulo prime
#         # result_x %= G_x
#         # result_y %= G_y

# # Write the result to a file
# with open('all_updated.txt', 'a') as f:
#     f.write(f"{result_x}\n{result_y}\n")

# print("Point generated successfully.")
