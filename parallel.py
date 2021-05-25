import math
import numpy as np
from numba import cuda, jit, int64


@cuda.jit(device = True)
def d_pow(a,b,m):
  return (a**b) % m

@cuda.jit
def bs_kernel(d_g, d_p, bs_idx, bs_tab):
    i = cuda.grid(1)
    n = bs_idx.shape[0]

    if i < n:
      bs_idx[i] = i
      bs_tab[i] = d_pow(d_g, i, p)

@cuda.jit
def gs_kernel(temp, h, p, bs_idx, bs_tab, d_gs, sols):
    j = cuda.grid(1)
    n = bs_idx.shape[0]

    if j < n:
      d_gs[j] = h * d_pow(temp,j,p) % p
      


def parallel_bs_gs(g, h, p):
  n = math.ceil(math.sqrt(p-1))

  bs_idx = cuda.device_array(n, dtype=np.int64)
  bs_tab = cuda.device_array(n, dtype=np.int64)

  blockDims = TPB
  gridDims = (n+TPB-1)//TPB

  bs_kernel[gridDims, blockDims](g, p, bs_idx, bs_tab)

  temp = pow(g, n*(p-2), p)
  sol = cuda.device_array(1, dtype=np.int64)
  d_gs = cuda.device_array(n, dtype=np.int64)

  gs_kernel[gridDims, blockDims](temp, h, p, bs_idx, bs_tab, d_gs, sol)

  return  sol.copy_to_host(), d_gs.copy_to_host(), bs_tab.copy_to_host(), bs_idx.copy_to_host()
    
