n = int(input("Importer un entier naturel: "))
def suite(n)->int:
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    u_i = 3
    u_i_plus_1 = 3

    for i in range(1, n + 1):
        u_i_plus_1 = u_i ** 2 + 3 * u_i + (i-1)
        u_i = u_i_plus_1

    return u_i_plus_1

print(suite(n))

n = int(input("Importer un entier naturel: "))
def somme(n)->int:
    sum = 3
    for i in range(1, n + 1):
        sum += suite(i)
    return sum

print(somme(n))