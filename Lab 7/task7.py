def string_hash(name, n):
    total = 0
    for ch in name:
        total += ord(ch)
    return total % n

def weighted_hash(name, n):
    total = 0
    for ch in name:
        total = total * 31 + ord(ch)
    return total % n

class StudentTable:
    def __init__(self, size, hash_fn):
        self.size = size
        self.hash_fn = hash_fn
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def insert(self, roll, name):
        chain = self.table[self.hash_fn(name, self.size)]
        if chain:
            self.collisions += 1          # slot already had a record
        chain.append((roll, name))

    def search(self, name):
        for roll, nm in self.table[self.hash_fn(name, self.size)]:
            if nm == name:
                return roll
        return None

    def display(self):
        for i, chain in enumerate(self.table):
            items = " -> ".join(nm for _, nm in chain) or "None"
            print(f"{i}: {items}")

    def collision_groups(self):
        return [[nm for _, nm in c] for c in self.table if len(c) > 1]

students = [(1, "Ali"), (2, "Sara"), (3, "Usman"), (4, "Ayesha"),
            (5, "Hamza"), (6, "Fatima"), (7, "Bilal"), (8, "Zainab")]

# ---- Exercise 1: store and display ----
plain = StudentTable(7, string_hash)
for roll, name in students:
    plain.insert(roll, name)
print("Plain ASCII sum:")
plain.display()

# ---- Exercise 2: search by name ----
for q in ["Hamza", "Bilal", "Omar"]:
    roll = plain.search(q)
    print(f"Search {q}:", roll if roll is not None else "Not found")

# ---- Exercise 3: colliding names ----
print("Collision groups:", plain.collision_groups())

# ---- Exercise 4: weighted hash ----
weighted = StudentTable(7, weighted_hash)
for roll, name in students:
    weighted.insert(roll, name)
print("\nWeighted (x31):")
weighted.display()
print("Collision groups:", weighted.collision_groups())
print("\nCollisions -> plain:", plain.collisions,
      "| weighted:", weighted.collisions)