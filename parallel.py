import math
import numpy as np
from numba import cuda, jit

TPB = 64

def g_split(g):
  lim = 2**64-1
  for i in range(64):
    if g**i > lim:
      split = i-1
      return split
  return i

@cuda.jit(device = True)
def d_pow(a,b,m):
  return (a**b) % m

@cuda.jit(device = True)
def break_pow(g, i, p, split):
  mult = g**split%p
  section = np.uint(math.ceil(i/split))
  power = np.uint(i-split*(section-1))
  if i <= split:
    return (g**i%p)
  else:
    count = 1
    ans = np.uint(round(g**power%p))
    while count<section:
      a = np.uint(ans * mult)
      ans = np.uint((ans * mult) %p)
      count += 1
    return  ans
      

@cuda.jit
def bs_kernel(g, p, bs_tab, n, split):
    i = cuda.grid(1)

    if i < n:
      bs_tab[i] = break_pow(np.uint(g), np.uint(i), np.uint(p), np.uint(split))


@cuda.jit
def gs_kernel(temp, n, h, p, d_gs,bs_tab, sol, split, mid_val):
    j = cuda.grid(1)

    if j < n:
      mid_val[j] = break_pow(np.uint(temp), np.uint(j), np.uint(p), np.uint(split))

      d_gs[j] = h * mid_val[j] % p
    for a in range(n):
      if d_gs[j] == round(bs_tab[a]):
        sol[0] = j*n + a
        return

      




def parallel_bs_gs(g, h, p):
  n = math.ceil(math.sqrt(p-1))
  split_g = g_split(g)

  bs_tab = cuda.device_array(n,dtype=np.uint)

  blockDims = TPB
  gridDims = (n+TPB-1)//TPB
    
  start = cuda.event()
  end = cuda.event()
  start.record()
  bs_kernel[gridDims, blockDims](g, p, bs_tab, n, split_g)
  end.record()
  end.synchronize()
  parallel_elapsed_bs = cuda.event_elapsed_time(start,end)

  temp = pow(g, n*(p-2), p)
  split_temp = g_split(temp)
  sol = cuda.device_array(1, dtype=np.uint)
  mid_val = cuda.device_array(n, dtype=np.uint)
  d_gs = cuda.device_array(n)

  start1 = cuda.event()
  end1 = cuda.event()
  start1.record()
  gs_kernel[gridDims, blockDims](temp, n, h, p, d_gs, bs_tab, sol, split_temp, mid_val)
  end1.record()
  end1.synchronize()
  parallel_elapsed_gs = cuda.event_elapsed_time(start1,end1)
  
  return  sol.copy_to_host(), bs_tab.copy_to_host(), d_gs.copy_to_host(), parallel_elapsed_bs, parallel_elapsed_gs
    
