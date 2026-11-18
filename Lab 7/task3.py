SIZE = 10 # array will contain 10 positions
EMPTY = -1 #-1 represents empty
DELETED = -2 #-2 represents a deleted position
table = [EMPTY] * SIZE #creates array containing ten -1 values

# This function calculates the initial index
# where a number should be inserted.
def h(k):
    return k % SIZE

def insert_key(k):
    for i in range(SIZE):
        idx = (h(k) + i) % SIZE # formula
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k # space available, insert the no.
            return True
    return False # table is full, all 10 positions are occupied

def search_key(k):
    for i in range(SIZE):             # never more than SIZE probes
        idx = (h(k) + i) % SIZE
        if table[idx] == EMPTY:       # a truly empty slot ends the search
            return -1
        if table[idx] == k:
            return idx
        # DELETED or another key: keep probing
    return -1

def delete_key(k):
    idx = search_key(k)
    if idx == -1:
        return False
    table[idx] = DELETED              # NOT EMPTY
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

# Exercise 3: insert that also counts probes
def insert_counted(k):
    for i in range(SIZE):
        idx = (h(k) + i) % SIZE
        if table[idx] == EMPTY or table[idx] == DELETED:
            table[idx] = k
            return i + 1              # number of slots checked
    return -1                         # full

# ---- Exercise 1 + 3: insert test keys, count probes ----
keys = [23, 43, 13, 27, 33]
probe_counts = []
for k in keys:
    p = insert_counted(k)
    probe_counts.append(p)
    print(f"Insert {k}: {p} probe(s)")
display()
print("Probes:", probe_counts)
print("Average probes:", sum(probe_counts) / len(probe_counts))

print("Search 13:", search_key(13))   # 5
print("Search 99:", search_key(99))   # -1

# ---- Exercise 2: the deletion problem ----
print("\n--- Deletion problem ---")
# (a) wrongly mark slot EMPTY
table[4] = EMPTY                      # "delete" 43 the wrong way
print("EMPTY marker, search 13:", search_key(13))    # -1  (wrong!)

# (b) correctly mark slot DELETED
table[4] = DELETED
print("DELETED marker, search 13:", search_key(13))  # 5   (correct)

# ---- Exercise 4: fill the table, then insert one more ----
print("\n--- Fill the table ---")
for k in [10, 11, 12, 18, 19]:        # these fill indexes 0, 1, 2, 8, 9
    insert_key(k)
table[4] = 43                         # put 43 back so all 10 slots are full
display()
if not insert_key(99):
    print("Table is full, cannot insert 99")