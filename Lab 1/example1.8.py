#  Read data from File

given_file=open(file="test.txt", mode="r")
lines=given_file.read()
arr=lines.split()
numbers=[]

for s in arr:
    num=int(s)
    numbers.append(num)

print(numbers)
