from time import time
from serial import *
from parallel import *
import math

# use serial_find_g for 15 bit primes or smaller (ie. p = 2**15-19, gives g = 2). this increases time
# for larger primes, try below
# for p = 2**32-5, use g = 2 takes ~ 0.2s
# for p = 2**38-45, use g = 2 takes ~ 2s



p = 2**32-5
h = 1501
g = 2
n = math.ceil(math.sqrt(p-1))

# ser_sol = serial_bs_gs(g,h,p)
# sol, bs, gs = parallel_bs_gs(g,h,p)
# print('serial: ', ser_sol)
# print('parallel: ', sol)

start = time()
serial_solu = serial_bs_gs(g, h, p)
serial_elapsed = time() - start

parallel_solu, pbs, pgs, parallel_elapsed_bs, parallel_elapsed_gs = parallel_bs_gs(g,h,p)

print(serial_solu)
print(parallel_solu)


print('serial time elapsed: ', serial_elapsed*1000, 'ms')
print('parallel time elapsed: ', parallel_elapsed_bs + parallel_elapsed_gs, 'ms')
# print('given: ', h, '=', g, '^x mod', p, ', x =', serial_solu)

print('check serial: ',pow(g,serial_solu,p), ' = ', h)
print('check parallel: ',pow(g,int(parallel_solu[0]),p), ' = ', h)
