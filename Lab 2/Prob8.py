import time
from funcs import InsertionSort, MergeSort, ShuffleArray

# Step 1: read words.txt into a list
with open("words.txt", "r") as f:
    words = [line.strip() for line in f if line.strip()]

print("Loaded", len(words), "words")

# Step 2: sort the words AS-IS with InsertionSort
words_copy = words.copy()
start_time = time.time()
InsertionSort(words_copy, 0, len(words_copy))
insertion_time = time.time() - start_time
print("InsertionSort on original words.txt:", insertion_time, "seconds")

# Step 2: sort the words AS-IS with MergeSort
words_copy = words.copy()
start_time = time.time()
MergeSort(words_copy, 0, len(words_copy))
merge_time = time.time() - start_time
print("MergeSort on original words.txt:", merge_time, "seconds")

# Step 3: shuffle the words
shuffled_words = words.copy()
ShuffleArray(shuffled_words, 0, len(shuffled_words))

# Step 4: sort the SHUFFLED words with InsertionSort
words_copy = shuffled_words.copy()
start_time = time.time()
InsertionSort(words_copy, 0, len(words_copy))
insertion_time_shuffled = time.time() - start_time
print("InsertionSort on shuffled words:", insertion_time_shuffled, "seconds")

# Step 4: sort the SHUFFLED words with MergeSort
words_copy = shuffled_words.copy()
start_time = time.time()
MergeSort(words_copy, 0, len(words_copy))
merge_time_shuffled = time.time() - start_time
print("MergeSort on shuffled words:", merge_time_shuffled, "seconds")

# InsertionSort is much faster on the ORIGINAL words.txt because it starts
# already sorted - it barely has to shift any elements per pass.
# On the SHUFFLED version, InsertionSort slows down noticeably, because
# now elements can be far from their correct position and need many shifts.
# MergeSort's runtime stays roughly the SAME either way, because it always
# performs the same splitting/merging work regardless of the input's
# original order.
