import funcs

number=funcs.userInput()
arr=funcs.read_from_subfolder("inputs/prob2_arr.txt")
result=funcs.SearchB(arr, number)
print(f"The indices are: {result}")