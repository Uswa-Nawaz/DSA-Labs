def division_hash(k, n):
    return k % n

def mid_square_hash(k, n):
    sq = str(k * k)
    start = (len(sq) - 2) // 2 
    middle = int(sq[start:start + 2])
    return middle % n

def folding_hash(k, n):
    s = str(k)
    total = 0
    i = len(s)
    while i > 0:                         # take 2-digit parts from the right
        total += int(s[max(0, i - 2):i])
        i -= 2
    return total % n

keys = [56, 123, 456, 789, 1024]
n = 10
for k in keys:
    print(f"Key {k} | Division: {division_hash(k, n)} | "
          f"MidSquare: {mid_square_hash(k, n)} | Folding: {folding_hash(k, n)}")

# Exercise 2: compare n = 7 and n = 10
for size in (7, 10):
    indexes = [division_hash(k, size) for k in keys]
    print(f"n={size}: {indexes} -> repeated indexes: {len(indexes) - len(set(indexes))}")