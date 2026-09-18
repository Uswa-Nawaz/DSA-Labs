def power(n, k):
    if k==1:
        return n
    else:
        return n*power(n, k-1)

n=int(input("Enter a number: "))
k=int(input("Enter a power: "))

result=power(n, k)
print(f"{n} raised to power {k} : {result}")