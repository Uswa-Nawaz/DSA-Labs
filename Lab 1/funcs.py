# ============================================================
#                       PROBLEM 1
# ============================================================

# Look for the index of the given element x in the given array

# Read the array from the file
def read_from_subfolder(filename):
    numbers=[]
    with open(filename, 'r') as file:
        for line in file:
            clean_line=line.strip()
            if clean_line:
                numbers.append(int(clean_line))
    return numbers

# ask the user to enter the required value
def userInput():
    num=int(input("Enter the no. you want to search: "))
    return num

# search in the array
def SearchA(arr, n):
    #function should return the array of indices
    indices=[]
    for i in range(len(arr)):
        if arr[i]==n:
            indices.append(i)
    return indices


# ============================================================
#                       PROBLEM 2
# ============================================================

#read_from_subfolder reused in problem 2
#userInput reused in problem 2

# search in the array
def SearchB(arr, n):
    check=0
    #function should return the array of indices
    indices=[]
    for i in range(len(arr)):
        check=check+1
        if arr[i]>n:
            break
        if arr[i]==n:
            indices.append(i)

    print(f"Elements checked: {check}")
    return indices

# ============================================================
#                       PROBLEM 3
# ============================================================

#read_from_subfolder reused in problem 3

def Minimum(arr, starting, ending):
    # should return the index of minimum element between the starting and ending slot

    min_index = starting
    min_value = arr[starting]
    for i in range(starting+1, ending+1):
        if arr[i]<min_value:
            min_value=arr[i]
            min_index=i

    return min_index
        