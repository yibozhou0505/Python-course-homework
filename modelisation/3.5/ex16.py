n, m = map(int, input("deux entiers: ").split())
def is_premier(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
def si_premier_entre(n, m):
    if n < 2 or m < 2:
        return False
    for i in range(min(n,m)+1,max(n,m)):
        if is_premier(i):
            return True
    return False
print(si_premier_entre(n, m))
        