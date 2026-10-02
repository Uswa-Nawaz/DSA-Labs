import time
from funcs import (
    RandomArray, InsertionSort, MergeSort,
    HybridMergeSort, BubbleSort, SelectionSort
)

# step 1, read n values from Nvalues.txt
n_values = []
with open("Nvalues.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            n_values.append(int(line))

# step 2, time each algorithm for each n
results = []
for n in n_values:
    base_array = RandomArray(n)

    arr = base_array.copy()
    start_time = time.time()
    InsertionSort(arr, 0, len(arr))
    insertion_time = time.time() - start_time

    arr = base_array.copy()
    start_time = time.time()
    MergeSort(arr, 0, len(arr))
    merge_time = time.time() - start_time

    arr = base_array.copy()
    start_time = time.time()
    HybridMergeSort(arr, 0, len(arr))
    hybrid_time = time.time() - start_time

    arr = base_array.copy()
    start_time = time.time()
    SelectionSort(arr, 0, len(arr))
    selection_time = time.time() - start_time

    arr = base_array.copy()
    start_time = time.time()
    BubbleSort(arr, 0, len(arr))
    bubble_time = time.time() - start_time

    results.append((n, insertion_time, merge_time, hybrid_time, selection_time, bubble_time))
    print("Finished n =", n)

# step 3, save to RunTime.csv
with open("RunTime.csv", "w") as f:
    f.write("n,InsertionSort,MergeSort,HybridMergeSort,SelectionSort,BubbleSort\n")
    for row in results:
        f.write(",".join(str(x) for x in row) + "\n")