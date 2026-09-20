import funcs

A = [
    [1, 13, 13],
    [5, 11, 6],
    [4, 4, 9]
]

rowSum=funcs.RowWiseSum(A)
columnSum=funcs.ColumnWiseSum(A)
print(f"Row sum : {rowSum}")
print(f"Column sum : {columnSum}")