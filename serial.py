
# Find smallest generator g for given prime number
def serial_find_g(p):
    check = list(range(1,p))
    for i in range(2,p):
        m = 0
        sol = [0]*len(check)

        for j in range(1,p):
            sol[m] = i**j % p
            m += 1

        sol.sort()
        if sol == check:
            return i   

# Solve Baby-Step, Giant-Step algorithm with given generator g, remainder h, and prime p
def serial_bs_gs(g, h, p):
