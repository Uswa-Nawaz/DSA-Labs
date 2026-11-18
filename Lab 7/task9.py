import random

SIZE = 101
EMPTY = -1

def linear(k, i):
    return (k % SIZE + i) % SIZE

def quadratic(k, i):
    return (k % SIZE + i * i) % SIZE

def double(k, i):
    return (k % SIZE + i * (8 - k % 8)) % SIZE

TECHNIQUES = {"Linear": linear, "Quadratic": quadratic, "Double": double}

def insert(table, k, probe):
    """Insert k and return (probes_used, success). Counts every index checked."""
    probes = 0
    for i in range(SIZE):
        idx = probe(k, i)
        probes += 1
        if table[idx] == EMPTY:
            table[idx] = k
            return probes, True
    return probes, False              # gave up after SIZE probes

def experiment(n, probe):
    keys = random.sample(range(1, 1000), n)
    table = [EMPTY] * SIZE
    total = fails = 0
    for k in keys:
        p, ok = insert(table, k, probe)
        total += p
        if not ok:
            fails += 1
    return total / n, fails

RUNS = 5
results = {name: [] for name in TECHNIQUES}
failures = {name: 0 for name in TECHNIQUES}

print(f"{'N':<5}{'Load':<8}{'Linear':<10}{'Quadratic':<12}{'Double':<10}")
for n in (20, 40, 60, 80):
    row = {}
    for name, probe in TECHNIQUES.items():
        avgs = []
        for _ in range(RUNS):
            avg, fails = experiment(n, probe)
            avgs.append(avg)
            failures[name] += fails
        row[name] = sum(avgs) / RUNS
        results[name].append(row[name])
    print(f"{n:<5}{n / SIZE:<8.2f}{row['Linear']:<10.2f}"
          f"{row['Quadratic']:<12.2f}{row['Double']:<10.2f}")

print("Total insert failures:", failures)

# ---- Bonus: matplotlib plot ----
try:
    import matplotlib.pyplot as plt
    loads = [n / SIZE for n in (20, 40, 60, 80)]
    for name, vals in results.items():
        plt.plot(loads, vals, marker="o", label=name)
    plt.xlabel("Load factor")
    plt.ylabel("Average probes per insert")
    plt.title("Open addressing: probes vs load factor")
    plt.legend()
    plt.grid(True)
    plt.show()
except ImportError:
    print("matplotlib not installed: pip install matplotlib")