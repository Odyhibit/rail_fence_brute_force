key = 13
possibilities = 0
for i in range(2, key):
    for j in range(2 * (key - 1)):
        possibilities += 1

print(f"There are {possibilities} possibilities")
