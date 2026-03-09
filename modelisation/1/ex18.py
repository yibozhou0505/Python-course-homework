n, m =map(int, input("Importer deux entiers n et m: ").split())
def PGCD(n, m)->int:
    while m != 0:
        n, m = m, n % m
    return n

print("Le PGCD de", n, "et", m, "est", PGCD(n, m))
