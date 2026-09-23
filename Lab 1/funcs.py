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


# ============================================================
#                       PROBLEM 4
# ============================================================

#read_from_subfolder reused in problem 4

def sort4(arr):
    #should reuse the above function and should return an array that is sorted
    n=len(arr)
    for i in range(n-1):
        mini=Minimum(arr, i, n-1)
        if mini != i:
            arr[i], arr[mini]=arr[mini], arr[i]

    return arr


# ============================================================
#                       PROBLEM 5
# ============================================================

# function to read the string values from the file
def read_String(filename):

    with open(filename, "r") as file:
        lines=file.read()
        return lines
    
#function to find the reverse
def StringReverse(str, starting, ending):
    sub_Str=str[starting:ending+1]
    reversed_str=sub_Str[::-1]
    return reversed_str

# ============================================================
#                       PROBLEM 6
# ============================================================

def SumIterative(number):
    digit_sum=0
    while number>0:
        lastDigit=number%10
        number=number//10
        digit_sum=digit_sum+lastDigit

    return digit_sum

def SumRecursive(number):
    if number==0:
        return number
    else:
       return (number%10) + SumRecursive(number // 10)

# ============================================================
#                       PROBLEM 7
# ============================================================

def RowWiseSum(Mat):
    result=[]
    for row in Mat:
        row_sum=0
        for value in row:
            row_sum=row_sum+value

        result.append(row_sum)

    return result

def ColumnWiseSum(Mat):
    result = []

    for column in range(len(Mat[0])):
        col_sum = 0

        for row in range(len(Mat)):
            col_sum = col_sum + Mat[row][column]

        result.append(col_sum)

    return result

# ============================================================
#                       PROBLEM 8
# ============================================================

# function should compare the current smallest element of both array one by one
# pick the smallest one to place the new array

def SortedMerge(Arr1, Arr2):
    i=0
    j=0

    merged=[]

    while i<len(Arr1) and j<len(Arr2):
        if Arr1[i] <= Arr2[j]:
            merged.append(Arr1[i])
            i += 1
        else:
            merged.append(Arr2[j])
            j += 1

    while i<len(Arr1):
        merged.append(Arr1[i])
        i=i+1
    
    while j<len(Arr2):
        merged.append(Arr2[j])
        j=j+1

    return merged

# ============================================================
#                       PROBLEM 9
# ============================================================

#function should reuse itself (recursion)
# should be same forward and backward using recursion
def palindromeRecursion(str):
    if len(str)<=1:
        return True
    if str[0]!=str[-1]:
        return False

    return palindromeRecursion(str[1:-1])


# ============================================================
#                       PROBLEM 10
# ============================================================

def Sort10(Arr):
    # Sort the array in standard ascending order
    Arr.sort()

    negatives = []
    positives = []
    for num in Arr:
        if num < 0:
            negatives.append(num)
        else:
            positives.append(num)

    # Combine them alternatively
    result = []

    neg_index = 0
    pos_index = 0
    
    while neg_index < len(negatives) and pos_index < len(positives):
        result.append(negatives[neg_index])
        result.append(positives[pos_index])
        neg_index += 1
        pos_index += 1

    result.extend(negatives[neg_index:])
    result.extend(positives[pos_index:])
    
    return result
    
