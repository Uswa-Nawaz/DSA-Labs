import funcs

numbers=funcs.read_from_subfolder("inputs/prob4_arr.txt")

print(f"Unsorted array: {numbers}")
result=funcs.sort4(numbers)
print(f"Sorted array: {result}")

