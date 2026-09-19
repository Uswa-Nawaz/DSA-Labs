import funcs

numbers_list=funcs.read_from_subfolder("inputs/prob6_arr.txt")
number=numbers_list[0]
inter_sum=funcs.SumIterative(number)
recurr_sum=funcs.SumRecursive(number)
print(f"Input Number: {number}")
print(f"Iterative Sum of Digits: {inter_sum}")
print(f"Recursive Sum of Digits: {recurr_sum}")