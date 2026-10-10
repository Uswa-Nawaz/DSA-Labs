# Part 3: Linear Time Sorting

def counting_sort(arr):
    smallest = min(arr)
    largest = max(arr)
    k = largest - smallest

    count = [0] * (k + 1)
    output = [0] * len(arr)

    # count how many times each value appears
    for x in arr:
        count[x - smallest] += 1

    # running totals
    for i in range(1, k + 1):
        count[i] += count[i - 1]

    # place elements, going backwards
    for i in range(len(arr) - 1, -1, -1):
        j = arr[i] - smallest
        count[j] -= 1
        output[count[j]] = arr[i]

    return output


arr1 = [-5, -10, 0, -3, 8, 5, -1, 10]
print("Counting sort input :", arr1)
print("Counting sort output:", counting_sort(arr1))

def sort_by_digit(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10

    for x in arr:
        digit = (x // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]

    return output


def radix_sort(arr):
    largest = max(arr)
    exp = 1
    while largest // exp > 0:
        arr = sort_by_digit(arr, exp)
        exp = exp * 10
    return arr


arr2 = [110, 45, 65, 50, 90, 602, 24, 2, 66]
print("Radix sort input :", arr2)
print("Radix sort output:", radix_sort(arr2))

def insertion_sort(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j = j - 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(arr):
    n = len(arr)

    # 1) make n empty buckets
    buckets = []
    for i in range(n):
        buckets.append([])

    # 2) put each number in its bucket
    for x in arr:
        index = int(n * x)
        buckets[index].append(x)

    # 3) sort each bucket
    for b in buckets:
        insertion_sort(b)

    # 4) join all buckets
    result = []
    for b in buckets:
        result = result + b

    return result


arr3 = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
print("Bucket sort input :", arr3)
print("Bucket sort output:", bucket_sort(arr3))