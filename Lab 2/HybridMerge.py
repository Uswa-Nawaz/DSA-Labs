import time
from funcs import RandomArray, HybridMergeSort

array = RandomArray(30000)

start_time = time.time()
HybridMergeSort(array, 0, len(array))
end_time = time.time()

runtime = end_time - start_time
print("Runtime of HybridMergeSort for 30000 integers is", runtime, "seconds")

with open("SortedHybridSort.csv", "w") as f:
    for num in array:
        f.write(str(num) + "\n")