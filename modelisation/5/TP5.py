# ========== Ex1 ============
# 1.1
def polEgaux(L, M):
    if len(L)== len(M):
        for i in range(len(L)):
            if L[i] != M[i]:
                return False
        return True
    else:
        rear = min(len(L), len(M))
        for i in range(rear):
            if L[i] != M[i]:
                return False
        if len(L) > len(M):
            L[rear:] = []
            return True
        else:
            M[rear:] = []
            return True

# 1.2
def reduire(L):
    rear = len(L) - 1
    for _ in range(rear):
        if L[rear] == 0:
            L.pop()
            rear -= 1
        else:
            break

# 1.3
def degre(P):
    P = reduire(P)
    return len(P) - 1

# ========== Ex2 ============
def derive(P):
    dP = []
    for i in range(1, len(P)):
        dP.append(i * P[i])
    return dP

# ========== Ex3 ============
def somme(P, Q):
    S = []
    for i in range(max(len(P), len(Q))):
        if i < len(P) and i < len(Q):
            S.append(P[i] + Q[i])
        elif i < len(P):    
            S.append(P[i])
        else:
            S.append(Q[i])
    return S

# ========== Ex4 ============
# 4.1
def evaluations(P, a):
    res = 0
    for i in range(len(P)):
        res += P[i] * a ** i
    return res

# 4.3
def Horner(P, a, res=0):
    if P == []:
        return res
    res += P[-1] * a ** len(P)
    P.pop()
    return Horner(P, a, res)


# ========== Ex5 ============
def produit(P, Q):
    res = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            res[i + j] += P[i] * Q[j]
    return res

# ========== Ex6 ============
def deg(P):
    i = len(P) - 1
    while i > 0 and P[i] == 0:
        i -= 1
    return i

def division(P, Q):
    P = P[:]  
    n = deg(P)
    m = deg(Q)

    while n >= m:
        coef = P[n] / Q[m]   
        power = n - m        

        for i in range(m + 1):
            P[i + power] -= coef * Q[i]

        n = deg(P)

    return P[:n+1]

# ========== Ex7 ============

def produit_rapide(P,Q):
    return 


    