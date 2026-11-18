class ChainHash:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_fn(self, k):
        return k % self.size

    def insert(self, k):
        chain = self.table[self.hash_fn(k)]
        if k in chain:                      # Exercise 4: no duplicates
            return False
        chain.append(k)
        return True

    def search(self, k):
        return k in self.table[self.hash_fn(k)]

    def remove(self, k):
        chain = self.table[self.hash_fn(k)]
        if k in chain:
            chain.remove(k)
            return True
        return False

    def display(self):
        for i, chain in enumerate(self.table):
            items = "".join(f"{x} -> " for x in chain)
            print(f"{i}: {items}None")

    def chain_lengths(self):                # Exercise 2
        return [len(chain) for chain in self.table]

    def longest_chain(self):                # Exercise 3
        return max(self.chain_lengths())


# ---- Reference demo ----
h = ChainHash(10)
for k in [15, 25, 35, 12, 22, 7]:
    h.insert(k)
h.display()
print("Search 25:", h.search(25))
h.remove(25)
h.display()

# ---- Exercise 2 and 3: 20 keys, table size 7 ----
t = ChainHash(7)
for k in [15, 25, 35, 45, 55, 12, 22, 32, 42, 7,
          14, 21, 28, 3, 10, 17, 24, 31, 38, 49]:
    t.insert(k)
for i, length in enumerate(t.chain_lengths()):
    print(f"Chain {i}: length {length}")
print("Longest chain:", t.longest_chain())


# ---- Exercise 1: menu ----
def menu():
    size = int(input("Table size: "))
    h = ChainHash(size)
    while True:
        print("\n1) Insert  2) Search  3) Delete  4) Display  5) Exit")
        choice = input("Choice: ")
        if choice == "1":
            k = int(input("Key: "))
            print("Inserted" if h.insert(k) else "Duplicate, not inserted")
        elif choice == "2":
            k = int(input("Key: "))
            print("Found" if h.search(k) else "Not found")
        elif choice == "3":
            k = int(input("Key: "))
            print("Deleted" if h.remove(k) else "Key not present")
        elif choice == "4":
            h.display()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

menu()