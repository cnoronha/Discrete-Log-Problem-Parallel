from time import time
from serial import *

# use serial_find_g for 15 bit primes or smaller (ie. p = 2**15-19, gives g = 2). this increases time
# for larger primes, try below
# for p = 2**32-5, use g = 2 takes ~ 0.2s
# for p = 2**38-45, use g = 2 takes ~ 2s

start = time()

p = 1019
h = 75
g = serial_find_g(p)
print(g)
serial_solu = serial_bs_gs(g, h, p)

serial_elapsed = time() - start
print('serial time elapsed: ', serial_elapsed*1000, 'ms')
print('given: ', h, '=', g, '^x mod', p, ', x =', serial_solu)

start2 = time()
if serial_solu != None and serial_solu <1000:
    print('check:', g**serial_solu % p, '=' , g, '^', serial_solu, 'mod', p)
    print(time()-start2)

