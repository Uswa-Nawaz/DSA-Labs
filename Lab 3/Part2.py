import math
import time
from itertools import combinations

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# Task 1: load the data using pandas
# ---------------------------------------------------------------
train = pd.read_csv('part2data/Train.csv')   # main data (with labels)
test = pd.read_csv('part2data/Test.csv')     # test data (no labels)

symptoms = [c for c in train.columns if c != 'TYPE']

train_symptoms = train[symptoms].values.tolist()
train_labels = train['TYPE'].values.tolist()
test_symptoms = test[symptoms].values.tolist()

# ---------------------------------------------------------------
# Task 2: scatter graph between each symptom and the label
# For each disease, the % of its patients that have each symptom
# ---------------------------------------------------------------
rates = train.groupby('TYPE')[symptoms].mean() * 100
print(rates.round(1).T)

x_positions = range(len(symptoms))

plt.figure(figsize=(14, 7))
for i, disease in enumerate(rates.index):
    shift = (i - 1.5) * 0.18   # small shift so overlapping dots stay visible
    plt.scatter([x + shift for x in x_positions], rates.loc[disease], label=disease, s=70)

plt.xticks(x_positions, symptoms, rotation=90)
plt.xlabel('Symptom')
plt.ylabel('% of patients with this symptom')
plt.title('How often each disease shows each symptom')
plt.legend(title='Disease')
plt.tight_layout()
# plt.show() is called once at the very end of the file,
# so the chart window does not stop the rest of the program.

# ---------------------------------------------------------------
# Tasks 3 and 4: Euclidean distance, then give each test patient
# the label of the closest patient in the main data
# ---------------------------------------------------------------
def euclidean(x, y):
    total = 0
    for i in range(len(x)):
        total = total + (x[i] - y[i]) ** 2
    return math.sqrt(total)


def classify(patient, cabinet_symptoms, cabinet_labels):
    # compare with every record, keep the label of the closest one
    best_distance = None
    best_label = None
    for i in range(len(cabinet_symptoms)):
        d = euclidean(patient, cabinet_symptoms[i])
        if best_distance is None or d < best_distance:
            best_distance = d
            best_label = cabinet_labels[i]
    return best_label


print()
print("Predicted labels for the patients in Test.csv:")
test_predictions = []
for t in test_symptoms:
    test_predictions.append(classify(t, train_symptoms, train_labels))
print(test_predictions)


# ---------------------------------------------------------------
# Task 5: time complexity (written answer is in Lab4.docx)
# m = patients in Test.csv, n = patients in Train.csv, k = symptoms
# For each of m patients we compare with all n records, and each
# comparison checks k symptoms  ->  O(m * n * k)
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Task 6: split the main data into Part 1 and Part 2
# Part 1 = reference data (labels kept)
# Part 2 = 200 patients taken out of the data, labels hidden
# (shuffled first, because the file is sorted by disease)
# ---------------------------------------------------------------
shuffled = train.sample(frac=1, random_state=42).reset_index(drop=True)

part2_df = shuffled.iloc[:200]
part1_df = shuffled.iloc[200:]

part1_symptoms = part1_df[symptoms].values.tolist()
part1_labels = part1_df['TYPE'].values.tolist()

part2_symptoms = part2_df[symptoms].values.tolist()
part2_answers = part2_df['TYPE'].values.tolist()   # kept aside for marking only

print()
print("Part 1 (reference) size:", len(part1_symptoms))
print("Part 2 (hidden labels) size:", len(part2_symptoms))


def report(name, guesses, seconds):
    correct = 0
    for i in range(len(guesses)):
        if guesses[i] == part2_answers[i]:
            correct = correct + 1
    print()
    print(name)
    print("Correct:", correct, "out of", len(guesses))
    print("Accuracy:", correct / len(guesses) * 100, "%")
    print("Time taken:", round(seconds, 3), "seconds")


# ---------------------------------------------------------------
# Task 7: run the algorithm on Part 2, with Part 1 as reference
# ---------------------------------------------------------------
t0 = time.time()
guesses = []
for p in part2_symptoms:
    guesses.append(classify(p, part1_symptoms, part1_labels))
t1 = time.time()
report("TASK 7: simple loop (first closest record wins)", guesses, t1 - t0)


# Improvement: when several records are equally close, let them vote
def classify_vote(patient, cabinet_symptoms, cabinet_labels):
    best_distance = None
    best_labels = []
    for i in range(len(cabinet_symptoms)):
        d = euclidean(patient, cabinet_symptoms[i])
        if best_distance is None or d < best_distance:
            best_distance = d
            best_labels = [cabinet_labels[i]]
        elif d == best_distance:
            best_labels.append(cabinet_labels[i])

    counts = {}
    for label in best_labels:
        if label in counts:
            counts[label] = counts[label] + 1
        else:
            counts[label] = 1

    winner = None
    winner_count = 0
    for label in counts:
        if counts[label] > winner_count:
            winner = label
            winner_count = counts[label]
    return winner


t0 = time.time()
vote_guesses = []
for p in part2_symptoms:
    vote_guesses.append(classify_vote(p, part1_symptoms, part1_labels))
t1 = time.time()
report("TASK 7 improvement: voting among equally close records", vote_guesses, t1 - t0)


# ---------------------------------------------------------------
# Task 8: recursive algorithm (cut the reference data in half)
# ---------------------------------------------------------------
def closest_recursive(patient, cabinet_symptoms, cabinet_labels, start, end):
    # stopping rule: only one record left in this piece
    if end - start == 1:
        return (euclidean(patient, cabinet_symptoms[start]), cabinet_labels[start])

    # otherwise cut the piece in half and solve each half
    middle = (start + end) // 2
    left = closest_recursive(patient, cabinet_symptoms, cabinet_labels, start, middle)
    right = closest_recursive(patient, cabinet_symptoms, cabinet_labels, middle, end)

    # keep whichever half found the closer record
    if left[0] <= right[0]:
        return left
    else:
        return right


def classify_recursive(patient, cabinet_symptoms, cabinet_labels):
    result = closest_recursive(patient, cabinet_symptoms, cabinet_labels, 0, len(cabinet_symptoms))
    return result[1]


t0 = time.time()
rec_guesses = []
for p in part2_symptoms:
    rec_guesses.append(classify_recursive(p, part1_symptoms, part1_labels))
t1 = time.time()
report("TASK 8: recursive version", rec_guesses, t1 - t0)


# ---------------------------------------------------------------
# Task 9: efficient algorithm - change how the data is stored
# Store the reference data in a dictionary:
#   key = symptom pattern, value = how many times each disease had it
# ---------------------------------------------------------------
build_start = time.time()
pattern_counts = {}

for i in range(len(part1_symptoms)):
    key = tuple(part1_symptoms[i])
    label = part1_labels[i]

    if key not in pattern_counts:
        pattern_counts[key] = {}

    if label in pattern_counts[key]:
        pattern_counts[key][label] = pattern_counts[key][label] + 1
    else:
        pattern_counts[key][label] = 1
build_end = time.time()

print()
print("Unique symptom patterns in Part 1:", len(pattern_counts))
print("Time to build the dictionary:", round(build_end - build_start, 3), "seconds")


def classify_neighbors(patient, table):
    # look up patterns that differ in 0 symptoms, then 1, then 2, ...
    # stop at the first level that finds something (those are the closest)
    key = tuple(patient)

    for dist in range(0, len(key) + 1):
        tally = {}
        for positions in combinations(range(len(key)), dist):
            candidate = list(key)
            for p in positions:
                candidate[p] = 1 - candidate[p]   # flip 0 <-> 1
            candidate = tuple(candidate)

            if candidate in table:
                for label in table[candidate]:
                    tally[label] = tally.get(label, 0) + table[candidate][label]

        if tally:
            winner = None
            winner_count = 0
            for label in tally:
                if tally[label] > winner_count:
                    winner = label
                    winner_count = tally[label]
            return winner


t0 = time.time()
nb_guesses = []
for p in part2_symptoms:
    nb_guesses.append(classify_neighbors(p, pattern_counts))
t1 = time.time()
report("TASK 9: dictionary + neighbour search", nb_guesses, t1 - t0)


# Show the scatter graph from Task 2 (close the window to finish)
plt.show()
