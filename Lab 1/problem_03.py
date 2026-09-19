import funcs

numbers=funcs.read_from_subfolder("inputs/prob3_arr.txt")
start=int(input("Enter starting Index: "))
end=int(input("Enter ending Index: "))
result=funcs.Minimum(numbers, start, end)
print(f"The index of minimum number between {start} and {end} : {result}")