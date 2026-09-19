import funcs

university=funcs.read_String("inputs/prob5_arr.txt")

print(f"String : {university}")

start=int(input("Enter starting index: "))
end=int(input("Enter ending index: "))
result=funcs.StringReverse(university, start, end)
# print in reverse
print(f"Reversed string : {result}")