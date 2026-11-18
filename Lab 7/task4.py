SIZE = 10
EMPTY = -1
DELETED = -2
table = [EMPTY] * SIZE

def h(k):
    return k % SIZE

def insert_key(k):
    for i in range(SIZE):
        idx = (h(k) + i * i) % SIZE          # only change: i*i
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k
            return True
    return False                             # no free slot found

def search_key(k):
    for i in range(SIZE):
        idx = (h(k) + i * i) % SIZE
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

# ---- Exercise 1: verify the dry run ----
for k in [12, 22, 32, 42]:
    insert_key(k)
display()

# ---- Exercise 2: indexes visited for a given H(K) ----
def visited(hk, size):
    return [(hk + i * i) % size for i in range(size)]

seq = visited(0, 10)
print("\nH(K)=0, size 10 sequence:", seq)
print("Visited:", sorted(set(seq)))
print("Never visited:", [x for x in range(10) if x not in seq])

# ---- Exercise 3: fill 0,1,4,5,6,9 and insert a key with H(K)=0 ----
table[:] = [EMPTY] * SIZE
for k in [10, 11, 14, 15, 16, 19]:           # each lands on its own index
    insert_key(k)
print()
display()
print("Insert 20 (H=0):", "success" if insert_key(20) else "FAILED")

# ---- Exercise 4: table size 11 ----
seq11 = visited(0, 11)
print("\nH(K)=0, size 11 sequence:", seq11)
print("Visited:", sorted(set(seq11)))
print("Never visited:", [x for x in range(11) if x not in seq11])