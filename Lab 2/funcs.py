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


# ============================================================
#                       PROBLEM 3
# ============================================================

def Merge(array, p, q, r):
    left = array[p:q]
    right = array[q:r]

    i = 0  # pointer into left
    j = 0  # pointer into right
    k = p  # pointer into array (where we write next)

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            array[k] = left[i]
            i += 1
        else:
            array[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        array[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        array[k] = right[j]
        j += 1
        k += 1


def MergeSort(array, start, end):
    if end - start <= 1:
        return
    mid = (start + end) // 2
    MergeSort(array, start, mid)
    MergeSort(array, mid, end)
    Merge(array, start, mid, end)

# ============================================================
#                       PROBLEM 4
# ============================================================

THRESHOLD = 50

def HybridMergeSort(array, start, end):
    # Small piece, insertion sort is faster, so use it and stop splitting
    if end - start <= THRESHOLD:
        InsertionSort(array, start, end)
        return

    # Big piece, split, sort both halves, merge same as MergeSort
    mid = (start + end) // 2
    HybridMergeSort(array, start, mid)
    HybridMergeSort(array, mid, end)
    Merge(array, start, mid, end)
