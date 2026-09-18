# Travarsal of array in forward direction
arr=["U", "E", "T"]

for a in range(len(arr)):
    print(arr[a])

# reverse by using slicing 
array = [32, 1, 9, 31, 12, 22] 
print(array[::-1])

#Traverse in backward direction using reverse method
array.reverse() 
print(array)

#Traverse through an array using for loop 
for i in range(len(array)-1, -1, -1): 
    print(array[i])