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
