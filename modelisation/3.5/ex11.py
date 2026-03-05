x = int(input("Importer un entier positif n: "))

def somme(n:int)->int:
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum  # e.g., n=3 sum = 1+2+3 = 6

def calcul(x)->int:
    if x < 0:
        raise ValueError("n must be a positive integer.")
    k =0
    while True:
        if somme(k) < x:
            k += 1 
        else:
            k -= 1
            break
    return k #

print(calcul(x))