import funcs

numbers=funcs.read_from_subfolder("inputs/prob10_arr.txt")

print(f"Unsorted Array : {numbers}")
result=funcs.Sort10(numbers)

print(f"Sorted Array : {result}")