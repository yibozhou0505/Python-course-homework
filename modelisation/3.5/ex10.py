n = int(input("importer un entier n: "))
def est_somme_de_carres(n)->bool:
    for i in range(1, int(n**0.5) + 1):
        for j in range(1, int(n**0.5) + 1):
            if i**2 + j**2 == n:
                return True
    return False
print(est_somme_de_carres(n))