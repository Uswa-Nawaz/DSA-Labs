import funcs

number=funcs.userInput()
arr=funcs.read_from_subfolder("inputs/prob1_arr.txt")
result=funcs.SearchA(arr, number)
print(f"The indices are: {result}")
