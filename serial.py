import math
from itertools import count, islice
from time import time

# Find smallest generator g for given prime number
def serial_find_g(p):
    """
    Determine smallest generator g for a given prime number p
    
    Arguments:
    p: prime number
    
    Returns:
    all_vals: list of generator g values for the given prime p
    i: smallest generator
    """
    check = list(range(1,p))
    all_vals = []
    for i in range(2,p):
        m = 0
        sol = [0]*len(check)

        for j in range(1,p):
            sol[m] = i**j % p
            m += 1

        sol.sort()
        if sol == check:
            all_vals.append(i)
            return i
            

    return all_vals 



# Solve Baby-Step, Giant-Step algorithm with given generator g, remainder h, and prime p
def serial_bs_gs(g, h, p):

    """
    Solve Baby-Step, Giant-Step algorithm with given generator g, remainder h, and prime p
    
    Arguments:
    g: generator
    h: remainder
    p: prime number
    
    Returns:
    Solution to the baby-step, giant-step algorithm
    """

    n = math.ceil(math.sqrt(p-1))
    start1 = time()
    bs = {}
    for i in range(n):
        bs[pow(g,i,p)] = i
    serial_elapsed_bs = time() - start1

    start2 = time()
    temp = pow(g, n*(p-2), p)
    for j in range(n):
        gs = h * pow(temp,j,p) % p
        if gs in bs:
            serial_elapsed_gs = time() - start2
            return j * n + bs[gs], serial_elapsed_bs, serial_elapsed_gs

    return None # if g is not a generator for prime p



