EMPTY = -1
DELETED = -2
KEYS = [23, 43, 13, 27, 33, 53, 63, 14, 24, 34]

# ---------- Chaining ----------
def run_chaining(keys, size=10):
    table = [[] for _ in range(size)]
    collisions = probes = fails = 0
    for k in keys:
        chain = table[k % size]
        if chain:
            collisions += 1
        probes += len(chain)          # nodes walked to reach the end
        chain.append(k)
    return table, collisions, probes, fails

# ---------- Open addressing (shared engine) ----------
def run_open(keys, size, probe):
    table = [EMPTY] * size
    collisions = probes = fails = 0
    for k in keys:
        placed = False
        for i in range(size):
            idx = probe(k, i)
            probes += 1
            free = table[idx] == EMPTY or table[idx] == DELETED
            if i == 0 and not free:
                collisions += 1
            if free:
                table[idx] = k
                placed = True
                break
        if not placed:
            fails += 1
            print(f"  Insert FAILED for key {k}")
    return table, collisions, probes, fails

def linear(k, i):    return (k % 10 + i) % 10
def quadratic(k, i): return (k % 10 + i * i) % 10
def double(k, i):    return (k % 11 + i * (8 - k % 8)) % 11

TECHNIQUES = {
    "1": ("Chaining",          lambda: run_chaining(KEYS, 10), "Yes"),
    "2": ("Linear Probing",    lambda: run_open(KEYS, 10, linear), "No"),
    "3": ("Quadratic Probing", lambda: run_open(KEYS, 10, quadratic), "No"),
    "4": ("Double Hashing",    lambda: run_open(KEYS, 11, double), "No"),
}

def display(table):
    for i, v in enumerate(table):
        if isinstance(v, list):
            items = "".join(f"{x} -> " for x in v)
            print(f"{i}: {items}None")
        else:
            print(f"{i}: {'-' if v == EMPTY else 'X' if v == DELETED else v}")

def run_one(choice):
    name, runner, _ = TECHNIQUES[choice]
    print(f"\n=== {name} ===")
    table, c, p, f = runner()
    display(table)
    print(f"Collisions: {c} | Total probes: {p} | Insert failures: {f}")

def compare_all():
    print(f"\n{'Technique':<18}{'Collisions':<12}{'Total Probes':<14}"
          f"{'Failures':<10}{'Extra Space?'}")
    for choice, (name, runner, extra) in TECHNIQUES.items():
        _, c, p, f = runner()
        print(f"{name:<18}{c:<12}{p:<14}{f:<10}{extra}")

def menu():
    while True:
        print("\n1) Chaining  2) Linear  3) Quadratic  4) Double Hashing"
              "  5) Compare all  6) Exit")
        choice = input("Choice: ")
        if choice in TECHNIQUES:
            run_one(choice)
        elif choice == "5":
            compare_all()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

menu()