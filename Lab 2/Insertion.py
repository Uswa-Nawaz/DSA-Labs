import time
import funcs

# generating the array
array=funcs.RandomArray(30000)

# time the sorting
start_Time=time.time()
funcs.InsertionSort(array, 0, len(array))
end_Time=time.time()

run_time=end_Time-start_Time
print(f"Runtime of InsertionSort for 30000 integers is {run_time} seconds")

# saving in csv
with open("SortedInsertionSort", "w") as f:
    for num in array:
        f.write(str(num) + "\n")