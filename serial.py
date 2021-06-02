import math
from itertools import count, islice

# Find smallest generator g for given prime number
def serial_find_g(p):
    """
    Determine smallest generator g for a given prime number p
    
    Arguments:
    p: prime number
    
    Returns:
    all_vals: list of values < p to test discrete log
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
    dictionary of values - solution to the baby-step, giant-step algorithm
    """

    n = math.ceil(math.sqrt(p-1))
    bs = {}
    for i in range(n):
        bs[pow(g,i,p)] = i

    temp = pow(g, n*(p-2), p)
    for j in range(n):
        gs = h * pow(temp,j,p) % p
        if gs in bs:
            return j * n + bs[gs]

    return None



