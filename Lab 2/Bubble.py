import time
from funcs import RandomArray, BubbleSort

array = RandomArray(30000)

start_time = time.time()
BubbleSort(array, 0, len(array))
end_time = time.time()

runtime = end_time - start_time
print("Runtime of BubbleSort for 30000 integers is", runtime, "seconds")

with open("SortedBubbleSort.csv", "w") as f:
    for num in array:
        f.write(str(num) + "\n")