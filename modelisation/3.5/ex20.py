L = list(map(int, input("Importer une liste d'entiers: ").split()))

def est_monotone(L):
    if not L:
        return True  
    est_croissant = True
    est_decroissant = True
    for i in range(1, len(L)):
        if L[i] < L[i - 1]:
            est_croissant = False
        if L[i] > L[i - 1]:
            est_decroissant = False
    return est_croissant or est_decroissant

print(est_monotone(L))