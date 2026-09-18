# Calculate sum of integers
def printArray (arr, start, end):
 if start == end:
    print(arr[start])
 else:
    print(arr[start])
    printArray (arr, start+1, end)

arr = [1,2,3,4,5,6,7,8,9,10]
printArray (arr, 0, len(arr)-1)