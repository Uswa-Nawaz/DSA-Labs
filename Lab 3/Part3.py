# Task 1
def printMatrix(A, starting_index, rows, columns):
    start_row = starting_index[0]
    start_col = starting_index[1]

    for r in range(start_row, start_row + rows):
        for c in range(start_col, start_col + columns):
            print(A[r][c], end=" ")
        print()


# Task 2
def MatAdd(A, B):
    rows = len(A)
    cols = len(A[0])
    result = []

    for r in range(rows):
        new_row = []
        for c in range(cols):
            new_row.append(A[r][c] + B[r][c])
        result.append(new_row)

    return result


# Task 3
def MatAddPartial(A, B, start, size):
    start_row = start[0]
    start_col = start[1]
    result = []

    for r in range(size):
        new_row = []
        for c in range(size):
            a_value = A[start_row + r][start_col + c]
            b_value = B[start_row + r][start_col + c]
            new_row.append(a_value + b_value)
        result.append(new_row)

    return result


# Task 4
def MatMul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    result = []

    for r in range(rows_A):
        new_row = []
        for c in range(cols_B):
            total = 0
            for k in range(cols_A):
                total = total + A[r][k] * B[k][c]
            new_row.append(total)
        result.append(new_row)

    return result


# Task 5 & 6
def split_matrix(M):
    n = len(M)
    half = n // 2
    top_left = []
    top_right = []
    bottom_left = []
    bottom_right = []

    for r in range(half):
        top_left.append(M[r][:half])
        top_right.append(M[r][half:])
    for r in range(half, n):
        bottom_left.append(M[r][:half])
        bottom_right.append(M[r][half:])

    return top_left, top_right, bottom_left, bottom_right


def join_matrix(top_left, top_right, bottom_left, bottom_right):
    result = []
    for r in range(len(top_left)):
        result.append(top_left[r] + top_right[r])
    for r in range(len(bottom_left)):
        result.append(bottom_left[r] + bottom_right[r])
    return result

def MatSub(A, B):
    rows = len(A)
    cols = len(A[0])
    result = []

    for r in range(rows):
        new_row = []
        for c in range(cols):
            new_row.append(A[r][c] - B[r][c])
        result.append(new_row)

    return result

# Task 5
def MatMulRecursive(A, B):
    n = len(A)

    # stopping rule: 1x1 matrices, just multiply the two numbers
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # cut both matrices into quadrants
    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    # each quadrant of the answer: two smaller multiplications, added
    c11 = MatAdd(MatMulRecursive(a11, b11), MatMulRecursive(a12, b21))
    c12 = MatAdd(MatMulRecursive(a11, b12), MatMulRecursive(a12, b22))
    c21 = MatAdd(MatMulRecursive(a21, b11), MatMulRecursive(a22, b21))
    c22 = MatAdd(MatMulRecursive(a21, b12), MatMulRecursive(a22, b22))

    # glue the four quadrants back together
    return join_matrix(c11, c12, c21, c22)



# Task 6
def MatMulStrassen(A, B):
    n = len(A)

    # stopping rule: 1x1 matrices, just multiply the two numbers
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # cut both matrices into quadrants
    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    # the 7 products
    m1 = MatMulStrassen(MatAdd(a11, a22), MatAdd(b11, b22))
    m2 = MatMulStrassen(MatAdd(a21, a22), b11)
    m3 = MatMulStrassen(a11, MatSub(b12, b22))
    m4 = MatMulStrassen(a22, MatSub(b21, b11))
    m5 = MatMulStrassen(MatAdd(a11, a12), b22)
    m6 = MatMulStrassen(MatSub(a21, a11), MatAdd(b11, b12))
    m7 = MatMulStrassen(MatSub(a12, a22), MatAdd(b21, b22))

    # build the four quadrants of the answer
    c11 = MatAdd(MatSub(MatAdd(m1, m4), m5), m7)
    c12 = MatAdd(m3, m5)
    c21 = MatAdd(m2, m4)
    c22 = MatAdd(MatSub(MatAdd(m1, m3), m2), m6)

    # glue the four quadrants back together
    return join_matrix(c11, c12, c21, c22)



# test the function 1
M = [[1,  2,  3,  4,  5],
     [6,  7,  8,  9,  10],
     [11, 12, 13, 14, 15],
     [16, 17, 18, 19, 20]]

print("Task 1: printMatrix(M, (1, 2), 2, 3)")
printMatrix(M, (1, 2), 2, 3)

#test the function 2
A = [[3, 4, 5],
     [2, 5, 7]]
B = [[1, 1, 1],
     [2, 2, 2]]

print()
print("Task 2: MatAdd(A, B)")
printMatrix(MatAdd(A, B), (0, 0), 2, 3)

#test the function 3
ten = [[10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10]]
print()
print("Task 3: MatAddPartial(M, ten, (1, 2), 2)")
printMatrix(MatAddPartial(M, ten, (1, 2), 2), (0, 0), 2, 2)

#test the function 4
P = [[1, 2, 3],
     [4, 5, 6]]
Q = [[7, 8],
     [9, 10],
     [11, 12]]

print()
print("Task 4: MatMul(P, Q)")
printMatrix(MatMul(P, Q), (0, 0), 2, 2)

#test the function 5 & 6
G = [[1,  2,  3,  4],
        [5,  6,  7,  8],
        [9,  10, 11, 12],
        [13, 14, 15, 16]]
H = [[1, 2, 0, 1],
        [0, 1, 3, 0],
        [2, 0, 1, 1],
        [1, 1, 0, 2]]
expected = MatMul(G, H)

print()
print("Task 5: MatMulRecursive(G, H)")
printMatrix(MatMulRecursive(G, H), (0, 0), 4, 4)
print("Same answer as MatMul:", MatMulRecursive(G, H) == expected)

print()
print("Task 6: MatMulStrassen(G, H)")
printMatrix(MatMulStrassen(G, H), (0, 0), 4, 4)
print("Same answer as MatMul:", MatMulStrassen(G, H) == expected)
