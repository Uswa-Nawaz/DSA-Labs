# Calculating power function through iteration

n=int(input("Enter a number: "))
p=int(input("Enter a power: "))
result=1
for i in range(p):
    result=result*n

print(f"{n} raised to power {p} : {result}")