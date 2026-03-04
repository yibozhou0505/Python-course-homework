def power_of_two(n):
    return 2 ** n

def list_powers(m):
    return [power_of_two(i) for i in range(m)]

def product(Ist):
    result = 1
    for num in Ist:
        result *= num
    return result

final = product(list_powers(4))
print(final)
