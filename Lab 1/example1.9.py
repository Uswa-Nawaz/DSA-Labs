# Write data to File

arr = ['Hello world', 'UET']

with open("Test.txt", "w") as f:
    for i in arr:
        f.write(i + "\n")