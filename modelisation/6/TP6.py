import math


# ============================================================
# Exercice 1
# Implementation des methodes composites
# ============================================================


# 题目先给了一个函数 cos(x)
def f(x):
    return math.cos(x)


# 1.1 Methode des rectangles a gauche
#
# 区间 [a,b] 被分成 N 个小区间，步长 h = (b-a)/N。
# 在每个小区间上，用左端点的函数值来近似积分。
#
# 注意：
# 第 i 个小区间的左端点是 a + i*h，其中 i 从 0 到 N-1。
# 所以这里只需要加 N 项，而不是 N+1 项。
def integraleG(f, a, b, N):
    h = (b - a) / N
    t = [a + i * h for i in range(N)]
    IN = 0.0
    for i in range(N):
        IN += h * f(t[i])
    return IN


# 为了验证阶数，写一个误差函数。
# 对 cos 在 [0, pi/2] 上的积分，精确值是 1。
def erreur_rectangle_gauche(N):
    exacte = 1.0
    approx = integraleG(f, 0.0, math.pi / 2, N)
    return abs(approx - exacte)


# 1.2 Methode des trapezes
#
# 梯形法公式：
# ∫[a,b] f(x) dx ≈ h * ( f(a)/2 + f(a+h) + ... + f(b-h) + f(b)/2 )
#
# 端点只算半次，中间点算一次。
def integraleT(f, a, b, N):
    h = (b - a) / N
    IN = 0.5 * (f(a) + f(b))
    for i in range(1, N):
        IN += f(a + i * h)
    return h * IN


def integraleT_ai(f, a, b, N):
    h = (b - a) / N
    IN = 0.5 * (f(a) + f(b))
    for i in range(1, N):
        IN += f(a + i * h)
    return h * IN


def erreur_trapezes(N):
    exacte = 1.0
    approx = integraleT(f, 0.0, math.pi / 2, N)
    return abs(approx - exacte)


# 1.3 Methode du point milieu
#
# 每个小区间 [x_i, x_(i+1)] 上，取中点
# x_i + h/2
# 然后用这个点的函数值乘以 h。
def integraleM(f,a,b,N):
    h = (b - a) / N
    IN = 0.0
    for i in range(N):
        M = (a+i*h + (a+(i+1)*h))/2 
        IN += h * f(M)
    return IN


def integraleM_ai(f, a, b, N):
    h = (b - a) / N
    IN = 0.0
    for i in range(N):
        milieu = a + (i + 0.5) * h
        IN += h * f(milieu)
    return IN


def erreur_milieu(N):
    exacte = 1.0
    approx = integraleM(f, 0.0, math.pi / 2, N)
    return abs(approx - exacte)


# 比较梯形法和中点法时，可以直接比较它们的误差。
def comparaison_trapezes_milieu(liste_N):
    for N in liste_N:
        errT = erreur_trapezes(N)
        errM = erreur_milieu(N)
        print("N =", N, " erreur trapezes =", errT, " erreur milieu =", errM)


# 1.4 Methode de Simpson
#
# 在每个小区间 [x_i, x_(i+1)] 上使用一次 Simpson 公式：
# h/6 * (f(x_i) + 4f((x_i+x_(i+1))/2) + f(x_(i+1))):抛物线面积公式
#
# 这样写成复合公式后，不需要特别要求 N 是偶数。
def integraleS(f,a,b,N):
    h = (b - a) / N
    IN = 0.0
    for i in range(N):
        M = (a+i*h + (a+(i+1)*h))/2
        IN += h/6 * (f(a+i*h) + 4*f(M) + f(a+(i+1)*h))
    return IN


def integraleS_ai(f, a, b, N):
    h = (b - a) / N
    IN = 0.0
    for i in range(N):
        xg = a + i * h
        xd = xg + h
        xm = (xg + xd) / 2
        IN += (h / 6) * (f(xg) + 4 * f(xm) + f(xd))
    return IN


def erreur_simpson(N):
    exacte = 1.0
    approx = integraleS(f, 0.0, math.pi / 2, N)
    return abs(approx - exacte)


# 如果误差大约像 C / N^p，
# 那么当 N 变成 2N 时，误差会差不多除以 2^p。
# 所以可以用这个公式估计数值实验里观察到的阶数。
def ordre_observe(eN, e2N):
    return math.log(eN / e2N, 2)


def affiche_convergence(nom, erreur):
    print(nom)
    liste_N = [10, 20, 40, 80, 160]
    for i in range(len(liste_N)):
        N = liste_N[i]
        e = erreur(N)
        if i == 0:
            print("N =", N, " erreur =", e)
        else:
            e_prec = erreur(liste_N[i - 1])
            p = ordre_observe(e_prec, e)
            print("N =", N, " erreur =", e, " ordre observe =", p)
    print()


# 1.5 Cas de sqrt(x) sur [0,1]
#
# 积分精确值：
# ∫_0^1 sqrt(x) dx = 2/3
#
# 这里继续用 Simpson 方法做实验。
def g(x):
    return math.sqrt(x)


def erreur_simpson_sqrt(N):
    exacte = 2.0 / 3.0
    approx = integraleS(g, 0.0, 1.0, N)
    return abs(approx - exacte)


# 对这一问的解释：
# Simpson 方法通常是四阶，但这需要函数足够光滑。
# 对 sqrt(x)，在 x=0 附近导数会发散，所以经典四阶误差估计不再成立。
# 数值实验会看到收敛速度明显慢下来，大约接近 3/2 阶。


# ============================================================
# Exercice 2
# Integrale exacte de polynomes
# ============================================================
#
# 这里把多项式写成列表：
# P = [a0, a1, a2, ..., an]
# 表示
# P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
#
# 例如 [2, -3, 0, 5] 表示 2 - 3x + 5x^3


def eval_poly_ai(P, x):
    val = 0
    for i in range(len(P)):
        val += P[i] * (x ** i)
    return val


# 2.1 primitivePoly(P)
#
# 如果 P(x) = a0 + a1*x + ... + an*x^n
# 那么它的一个原函数可以取
# F(x) = a0*x + a1*x^2/2 + ... + an*x^(n+1)/(n+1)
#
# 这里把积分常数取成 0。
def primitivePoly(P):
    F = [0]
    for i in range(len(P)):
        F.append(P[i]/(i+1))
    return F


def primitivePoly_ai(P):
    F = [0]
    for i in range(len(P)):
        F.append(P[i] / (i + 1))
    return F


# 2.2 integrerPoly(P, a, b)
#
# 直接使用牛顿-莱布尼茨公式：
# ∫[a,b] P(x) dx = F(b) - F(a)

def integrerPoly(P,a,b):
    term = 0.0
    F = primitivePoly(P)
    for i in range(len(F)):
        term += F[i] * b ** i - F[i] * a ** i
    return term


def integrerPoly_ai(P, a, b):
    F = primitivePoly_ai(P)
    return eval_poly_ai(F, b) - eval_poly_ai(F, a)


def test_exercice2():
    print()
    print("Exercice 2")
    P = [1, -2, 3]
    print("P =", P)
    print("primitivePoly_ai(P) =", primitivePoly_ai(P))
    print("integrerPoly_ai(P, 0, 1) =", integrerPoly_ai(P, 0, 1))


# ============================================================
# Exercice 3
# Polynomes de Legendre
# ============================================================
#
# 递推公式是：
# (n + 1) P_(n+1) = (2n + 1) X P_n - n P_(n-1)
#
# 并且
# P0 = 1
# P1 = X
#
# 这里仍然用列表表示多项式：
# [a0, a1, ..., an] 表示 a0 + a1*x + ... + an*x^n

def somme_poly_ai(P, Q):
    n = max(len(P), len(Q))
    R = [0] * n
    for i in range(n):
        if i < len(P):
            R[i] += P[i]
        if i < len(Q):
            R[i] += Q[i]
    return R


def produit_scalaire_poly_ai(lam, P):
    return [lam * x for x in P]


def produit_X_poly_ai(P):
    return [0] + P


def difference_poly_ai(P, Q):
    n = max(len(P), len(Q))
    R = [0] * n
    for i in range(n):
        if i < len(P):
            R[i] += P[i]
        if i < len(Q):
            R[i] -= Q[i]
    return R


def nettoyer_poly_ai(P):
    Q = P[:]
    while len(Q) > 1 and abs(Q[-1]) < 1e-14:
        Q.pop()
    return Q


def polyLegendre(n):
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]
    P_n_1 = polyLegendre(n - 1)
    P_n_2 = polyLegendre(n - 2)
    
    X_P_n_1 = [0] + P_n_1
    M = max(len(X_P_n_1), len(P_n_2))
    X_P_n_1 = X_P_n_1 + [0] * (M - len(X_P_n_1))
    P_n_2 = P_n_2 + [0] * (M - len(P_n_2))

    P_n = []
    for i in range(M):
        coeff = ((2*n - 1)*X_P_n_1[i] - (n - 1)*P_n_2[i])/n
        P_n.append(coeff)

    while len(P_n) > 1 and abs(P_n[-1]) == 0:
        P_n.pop()

    return P_n



def polyLegendre_ai(n):
    # 题目给的初值
    if n == 0:
        return [1]
    if n == 1:
        return [0, 1]

    # 递归得到 P_(n-1) 和 P_(n-2)
    Pn_1 = polyLegendre_ai(n - 1)
    Pn_2 = polyLegendre_ai(n - 2)

    # 按题目公式：
    # n*P_n = (2n-1) X P_(n-1) - (n-1) P_(n-2)
    #
    # 这里先算 X*P_(n-1)
    XPn_1 = [0] + Pn_1

    # 为了做减法，先把两个列表补到一样长
    m = max(len(XPn_1), len(Pn_2))
    XPn_1 = XPn_1 + [0] * (m - len(XPn_1))
    Pn_2 = Pn_2 + [0] * (m - len(Pn_2))

    Pn = []
    for i in range(m):
        coeff = ((2 * n - 1) * XPn_1[i] - (n - 1) * Pn_2[i]) / n
        Pn.append(coeff)

    while len(Pn) > 1 and abs(Pn[-1]) < 1e-14:
        Pn.pop()

    return Pn


def test_exercice3():
    print()
    print("Exercice 3")
    print("P6 =", polyLegendre_ai(6))


if __name__ == "__main__":
    print("Verification de l'ordre pour cos sur [0, pi/2]")
    print()

    affiche_convergence("Rectangles a gauche", erreur_rectangle_gauche)
    affiche_convergence("Trapezes", erreur_trapezes)
    affiche_convergence("Point milieu", erreur_milieu)
    affiche_convergence("Simpson", erreur_simpson)

    print("Comparaison trapezes / point milieu")
    comparaison_trapezes_milieu([10, 20, 40, 80])
    print()

    print("Simpson applique a sqrt(x) sur [0,1]")
    affiche_convergence("Simpson pour sqrt(x)", erreur_simpson_sqrt)

    test_exercice2()
    test_exercice3()
