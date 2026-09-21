import funcs

input_Str=funcs.read_String("inputs/prob9_str.txt")
result=funcs.palindromeRecursion(input_Str)

if(result):
    print("Its a palindrome string")
else:
    print("Its not a palindrome string")