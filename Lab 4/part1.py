import random

def partition(A, p, r):
    x=A[r] #pivot
    i=p-1

    for j in range(p, r):
        if A[j] <= x: #check current element is less than or equal to the pivot
            i=i+1 
            A[i], A[j]=A[j], A[i] #swaps the current element with the element

    A[i+1], A[r]=A[r], A[i+1] #put the pivot into correct final position
    return i+1

#quick sort function
def quicksort(A, p, r):
    if p<r:
        q=partition(A, p, r)

        quicksort(A, p, q-1)
        quicksort(A, q+1, r)


# generate one random arrray of size 10
A=[random.randint(1, 100) for _ in range(10)]

print("Original Array: ", A)

# apply quick sort
quicksort(A, 0, len(A)-1)

print("Sorted Array: ", A)
