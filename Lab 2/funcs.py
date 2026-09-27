# ============================================================
#                       PROBLEM 1
# ============================================================
import random

def RandomArray(size):
    array=[]
    for i in range(size):
        num= random.randint(0, 1000000)
        array.append(num)
    return array

# ============================================================
#                       PROBLEM 2
# ============================================================

def InsertionSort(array, start, end):
    for i in range(start + 1, end):
        key = array[i]
        j = i - 1
        while j >= start and array[j] > key:
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = key

