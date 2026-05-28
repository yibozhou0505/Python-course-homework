# ex2.1
def suite(n):
    u = 5
    for i in range(1, n+1):
        u = i*u + 2
    return u

def calcul_liste(n):
    L = []
    for i in range(n+1):
        L.append(suite(i))
    return L


def calcul_liste_opt(n):
    L = [5]
    for i in range(1, n+1):
        u = i*L[i-1] + 2
        L.append(u)
    return L
# ex2.2
def catalan_naif(n):
    if n == 0:
        return 1
    else:
        S = 0
        for i in range(n):
            S = S + catalan_naif(i) * catalan_naif(n-1-i)
        return S
    
def catalan_iter(n):
    C = [1]
    for k in range(1, n+1):
        S = 0
        for i in range(k):
            S = S + C[i] * C[k-1-i]
        C.append(S)
    return C[n]


dico_cat = {0: 1}

def catalan(n):
    if n in dico_cat:
        return dico_cat[n]
    else:
        S = 0
        for i in range(n):
            S = S + catalan(i) * catalan(n-1-i)
        dico_cat[n] = S  # 非常重要：将结果存入字典
        return S
    
# ex2.3
def optimale(P):
    N = len(P)
    L = [[P[i][j] for i in range(j+1)] for j in range(N)]
    for i in range(1, N):
        for j in range(0, i+1):
            M = [0]
            for k in range(j-1, j+2):
                if (k >= 0) and (k < i):
                    M.append(L[i-1][k])
            L[i][j] = max(M) + P[i][j]
    return max(L[N-1])

# ======= ex3 ========
# ex3.1
def valeur(s):
    results = 0
    for i in s:
        results += i
    return results

# ex3.2
# (a) prove: pour any entier n ,on peut trouver une composition utilisant les entier dans [500, 200, 100, 50, 20, 10, 5, 2, 1]
EURO = [500, 200, 100, 50, 20, 10, 5, 2, 1]
def  culcule(x):
    '''input x is a integer'''
    cost = [0]*9
    i = 0
    while True:
        if x >= EURO[i]:
            cost[i] += 1
            x -= EURO[i]
        else:
            i += 1
            if i == 9:
                break

    return cost

# x = int(input("Enter a number: "))
# print(culcule(x))

# (b)
def glouton(D,p):
    cost = [0]*9
    i = 0
    while True:
        if p >= D[i]:
            cost[i] += 1
            p -= D[i]
        else:
            i += 1
            if i == len(D)+1:
                break

    return cost

# ex3.3
# (a): Pf = [50,20,20,20] p = 60
# (b)
def paye_glouton(Pf, p):
    reste = p
    paiement = []

    for piece in sorted(Pf, reverse=True):
        if piece <= reste:
            paiement.append(piece)
            reste -= piece

        if reste == 0:
            return paiement

    return []

# ex3.4
# (a)
def compte_paiements(Pf, p):
    """
    Pf: list[int]
    p: int

    返回从 Pf 中选出若干元素，使总和为 p 的方法数量。
    相同面值但位置不同的钱，视为不同选择。
    """

    # 成功凑出 p
    if p == 0:
        return 1

    # p 变成负数，说明这条路不行
    if p < 0:
        return 0

    # 没钱了，但 p 还没凑出来
    if len(Pf) == 0:
        return 0

    # 情况 1：不用第一张/枚钱
    sans_premiere = compte_paiements(Pf[1:], p)

    # 情况 2：使用第一张/枚钱
    avec_premiere = compte_paiements(Pf[1:], p - Pf[0])

    return sans_premiere + avec_premiere


# (b)::
def compte_paiements_opt(Pf, p):
    """
    Pf: tuple[int]
    p: int

    返回从 Pf 中选出若干元素，使总和为 p 的方法数量。
    使用字典记忆化优化。
    """

    memo = {}

    def aux(i, reste):
        # 成功凑出目标
        if reste == 0:
            return 1

        # 超过目标，不可能
        if reste < 0:
            return 0

        # 没有钱可选了，但还没凑出来
        if i == len(Pf):
            return 0

        key = (i, reste)

        if key in memo:
            return memo[key]

        # 不选 Pf[i]
        sans = aux(i + 1, reste)

        # 选 Pf[i]
        avec = aux(i + 1, reste - Pf[i])

        memo[key] = sans + avec
        return memo[key]

    return aux(0, p)