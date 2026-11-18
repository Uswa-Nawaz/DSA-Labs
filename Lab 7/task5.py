SIZE = 11
EMPTY = -1
DELETED = -2
table = [EMPTY] * SIZE

def h1(k):
    return k % 11

def h2(k):
    return 8 - (k % 8)

def insert_key(k):
    for i in range(SIZE):
        idx = (h1(k) + i * h2(k)) % SIZE
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k
            return True
    return False

def search_key(k):
    for i in range(SIZE):                      # same probe sequence as insert
        idx = (h1(k) + i * h2(k)) % SIZE
        if table[idx] == EMPTY:
            return -1
        if table[idx] == k:
            return idx
    return -1

def delete_key(k):
    idx = search_key(k)
    if idx == -1:
        return False
    table[idx] = DELETED
    return True

def display():
    for i in range(SIZE):
        if table[i] == EMPTY:
            value = "-"
        elif table[i] == DELETED:
            value = "X"
        else:
            value = table[i]
        print(f"{i}: {value}")

# ---- Exercise 3 helpers: probe sequences ----
def double_sequence(k):
    """Indexes double hashing checks until it finds the key's slot."""
    seq = []
    for i in range(SIZE):
        idx = (h1(k) + i * h2(k)) % SIZE
        seq.append(idx)
        if table[idx] == k:
            break
    return seq

def linear_sequences(keys, size=11):
    """Insert keys with linear probing (size 11) and return each probe list."""
    t = [EMPTY] * size
    result = {}
    for k in keys:
        seq = []
        for i in range(size):
            idx = (k % size + i) % size
            seq.append(idx)
            if t[idx] == EMPTY:
                t[idx] = k
                break
        result[k] = seq
    return result

# ---- Exercise 1: verify the dry run ----
for k in [10, 21, 32, 43]:
    insert_key(k)
print("After 10, 21, 32, 43:")
display()

# ---- Exercise 2: full key set ----
table[:] = [EMPTY] * SIZE
keys = [10, 21, 32, 43, 54, 65, 76]
for k in keys:
    insert_key(k)
print("\nAfter all 7 keys:")
display()

# ---- Exercise 3: compare probe sequences ----
lin = linear_sequences(keys)
print("\nKey | Double hashing | Linear probing")
for k in keys:
    print(f"{k:>3} | {double_sequence(k)} | {lin[k]}")

# ---- Search and delete test ----
print("\nSearch 54:", search_key(54))     # 1
delete_key(54)
print("After delete, search 54:", search_key(54))   # -1