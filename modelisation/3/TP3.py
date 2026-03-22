# ========== Ex1 ==========
# 1.1
def fibo_rec(n) :
    if n == 0 or n == 1 :
        return 1
    return fibo_rec(n-1) + fibo_rec(n-2)

# print(fibo_rec(37))

# ========== Ex2 ==========
# 2.1
# print("1"+"0")

# 2.2
def list_mots_binaires(n) :
    if n == 0 :
        return [""]
    elif n == 1 :
        return ["0", "1"]
    L = list_mots_binaires(n-1)
    M = []
    for mot in L :
        M.append(mot + "0")
        M.append(mot + "1")
    return M
# print(list_mots_binaires(4))

# ========== Ex3 ==========
# 3.1
def exponentiation_rapide(x,n):
    if n == 0 :
        return 1
    elif n % 2 == 0 :
        return exponentiation_rapide(x * x,n//2)
    else :
        return x * exponentiation_rapide(x * x, (n-1)//2)
# print(exponentiation_rapide(2,10))

# ========== Ex4 ==========
# 4.1
def u(a,b,c,n):

    if n == 0:
        return a
    elif n == 1:
        return b
    elif n == 2:
        return c
    prev3, prev2, prev1 = a, b, c
    
    for i in range(3, n + 1):
        current = 2 * prev1 - prev2 + 4 * prev3
        prev3, prev2, prev1 = prev2, prev1, current
    
    return prev1
    
# 4.2
# print(u(2,0,3,2000))

# ========== Ex5 ==========
# 5.1
# L = []
# for i in range(1,10):
#     L.append(i)

# print(L)
