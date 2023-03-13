import random
import math


def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):                       # Time Complexity of (n) bits
    if y == 0:                              # O(n)
        return 1
    z = mod_exp(x, math.floor(y / 2), N)    # O(n)
    if y % 2 == 0:                          # O(1)
        return (z * z) % N                  #O(n^2)
    else:
        return (x * z * z) % N              #O(n^2)

                                             # TOTAL: O(N^3)
                                             # SPACE: O(N)
	

def fprobability(k):
    probability = 1 - (1/2) ** k            
    return probability


def mprobability(k):
    probability = 1 - (1/4) ** k
    return probability


def fermat(N,k):
    for i in range(k):                          
        random_int = random.randint(1, N-1)
        if mod_exp(random_int, N-1, N) != 1:
            return 'composite'
    return 'prime'

# def miller_rabin(N,k):
#     for i in range(k):
#         random_int = random.randint(2, N-2)
#         starting_power = N-1
#         if mod_exp(random_int, starting_power, N) != 1:
#             return 'composite'
#         else:
#             count = 0
#             starting_temp = starting_power
#             while starting_temp % 2 == 0:
#                 count += 1
#                 starting_temp = starting_temp /2
#             d =  starting_temp
#             s = count
#             print(d)
#             print(s)
#             while starting_power % 2 == 0:
#                 result = mod_exp(random_int, starting_power, N)
#                 if result != 1 and result != -1:
#                     print()
#                     print("Parameters: ")
#                     print(random_int, starting_power, N)
#                     print(mod_exp(random_int, starting_power, N))
#                     return 'composite'
#                 starting_power = starting_power / 2
#         return 'prime'


def miller_rabin(N,k):
    count = 0
    starting_temp = N-1
    while starting_temp % 2 == 0:
        count += 1
        starting_temp = math.floor(starting_temp / 2)
    d = starting_temp
    s = count
    for i in range(k):
        a = random.randint(2, N-2)
        x = mod_exp(a, d, N)
        yz = 1
        for j in range(s):
            yz = (x * x) % N
            print(x, yz)
            if yz == 1 and x != 1 and x != N-1:
                return 'composite'
            x = yz
        if yz != 1:
            return 'composite'
    return 'prime'