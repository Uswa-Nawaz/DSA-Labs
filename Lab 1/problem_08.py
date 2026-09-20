import funcs

arr1=funcs.read_from_subfolder("inputs/prob8_arr1.txt")
arr2=funcs.read_from_subfolder("inputs/prob8_arr2.txt")

print(f"Array 1 : {arr1}")
print(f"Array 2 : {arr2}")
merged_sorted=funcs.SortedMerge(arr1, arr2)

print(f"Sorted merged : {merged_sorted}")