# 1D array of random ints using numpy

import numpy as np

min = 0
max = 20
n = 5

# generate 5 integers from 0 up to but not including 20
array = np.random.randint(min, max + 1, n)

print(array)