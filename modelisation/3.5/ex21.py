n, m = map(int, input("Importer entier n >= 1 et m >= 0: ").split())
def bezout(n, m):
    if m == 0:
        return (1, 0)
    u0, v0 = 1, 0
    u1, v1 = 0, 1
    while m != 0:
        q, r = divmod(n, m)
        n, m = m, r
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return (u0, v0)
print(f"u = {bezout(n, m)[0]}, v = {bezout(n, m)[1]}")