import random

def generate_large_random_number():
    min_val = 7237005577332262213973186563042994240829374041602535252466099000494570602496
    max_val = 115792089237315784047431654707177369110974345328014318355491175612947292487680
    secure_random = random.SystemRandom()
    return secure_random.randrange(min_val, max_val + 1)

def save_to_file(number):
    with open('all_updated.txt', 'a') as file:
        file.write(f'{number}\n')

# Define the number of random numbers you want to generate
number_of_random_numbers = 10000

for _ in range(number_of_random_numbers):
    # Generate a random number
    random_number = generate_large_random_number()
    
    # Save the random number to all_numbers.txt
    save_to_file(random_number)
    
    # print(f'Random number {random_number} has been saved to all_updated.txt')
