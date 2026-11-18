EMPTY = -1
DELETED = -2
SIZE = 11

def name_value(name):
    return sum(ord(ch) for ch in name)

class Phonebook:
    def __init__(self, technique):
        self.tech = technique              # "chaining", "linear" or "double"
        self.size = SIZE
        self.collisions = 0
        if technique == "chaining":
            self.table = [[] for _ in range(SIZE)]
        else:
            self.table = [EMPTY] * SIZE

    def _probe(self, name, i):
        s = name_value(name)
        if self.tech == "linear":
            return (s % self.size + i) % self.size
        return (s % self.size + i * (8 - s % 8)) % self.size   # double

    def search(self, name):
        """Return the phone number, or None if the name is absent."""
        if self.tech == "chaining":
            for n, p in self.table[name_value(name) % self.size]:
                if n == name:
                    return p
            return None
        for i in range(self.size):
            slot = self.table[self._probe(name, i)]
            if slot == EMPTY:
                return None
            if slot != DELETED and slot[0] == name:
                return slot[1]
        return None

    def add(self, name, phone):
        """Return 'ok', 'duplicate' or 'full'."""
        if self.search(name) is not None:
            return "duplicate"
        if self.tech == "chaining":
            chain = self.table[name_value(name) % self.size]
            if chain:
                self.collisions += 1
            chain.append((name, phone))
            return "ok"
        for i in range(self.size):
            idx = self._probe(name, i)
            slot = self.table[idx]
            if slot == EMPTY or slot == DELETED:
                self.table[idx] = (name, phone)
                return "ok"
            if i == 0:                       # home slot occupied
                self.collisions += 1
        return "full"

    def delete(self, name):
        if self.tech == "chaining":
            chain = self.table[name_value(name) % self.size]
            for entry in chain:
                if entry[0] == name:
                    chain.remove(entry)
                    return True
            return False
        for i in range(self.size):
            idx = self._probe(name, i)
            slot = self.table[idx]
            if slot == EMPTY:
                return False
            if slot != DELETED and slot[0] == name:
                self.table[idx] = DELETED    # NOT EMPTY
                return True
        return False

    def display(self):
        for i, slot in enumerate(self.table):
            if self.tech == "chaining":
                items = "".join(f"{n}({p}) -> " for n, p in slot)
                print(f"{i}: {items}None")
            elif slot == EMPTY:
                print(f"{i}: -")
            elif slot == DELETED:
                print(f"{i}: X")
            else:
                print(f"{i}: {slot[0]} ({slot[1]})")


TEST_NAMES = ["Ali", "Sara", "Usman", "Ayesha", "Hamza",
              "Fatima", "Bilal", "Zainab", "Hassan", "Maryam"]

def load_test_data(pb):
    for n, name in enumerate(TEST_NAMES, start=1):
        pb.add(name, f"030000000{n}" if n < 10 else "0300000010")

def main():
    print("Collision technique: 1) Chaining  2) Linear Probing  3) Double Hashing")
    tech = {"1": "chaining", "2": "linear", "3": "double"}.get(input("Choice: "))
    if tech is None:
        print("Invalid choice")
        return
    pb = Phonebook(tech)
    if input("Load the 10 test contacts? (y/n): ").lower() == "y":
        load_test_data(pb)

    while True:
        print("\n1) Add  2) Search  3) Delete  4) Display  "
              "5) Total collisions  6) Exit")
        choice = input("Choice: ")
        if choice == "1":
            name = input("Name: ").strip().title()
            phone = input("Phone: ").strip()
            result = pb.add(name, phone)
            if result == "ok":
                print("Contact added")
            elif result == "duplicate":
                print(f"'{name}' already exists. Duplicate names are not allowed.")
            else:
                print("Phonebook is FULL. Delete a contact first.")
        elif choice == "2":
            name = input("Name: ").strip().title()
            phone = pb.search(name)
            print(f"{name}: {phone}" if phone is not None else "Not found")
        elif choice == "3":
            name = input("Name: ").strip().title()
            print("Deleted" if pb.delete(name) else "Not found")
        elif choice == "4":
            pb.display()
        elif choice == "5":
            print("Total collisions:", pb.collisions)
        elif choice == "6":
            break
        else:
            print("Invalid choice")

main()