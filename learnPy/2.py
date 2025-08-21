tup="helloWorld"
it=iter(tup)

print(next(it),end=" ")
print(next(it))
print(next(it))
print(next(it))

print("\n")

tup2=("a","b","x")

for x in tup2:
    print(x)
    