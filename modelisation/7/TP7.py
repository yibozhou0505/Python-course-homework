"""
TP7 - informatique et probabilites

这份文件按题目顺序给出一份可运行解答。
题目核心是利用 random 库模拟若干离散随机实验。
"""

import math
import random as rd


# ============================================================
# Exercice 1
# ============================================================
def experience1(N1, N2, n):
    """
    有放回抽样。

    每次抽取时，红球概率始终是 N1 / (N1 + N2)。
    返回 n 次抽样中红球的个数。
    """

    nb_rouges = 0
    proba_rouge = N1 / (N1 + N2)

    for _ in range(n):
        if rd.random() < proba_rouge:
            nb_rouges += 1

    return nb_rouges


def experience2(N1, N2, n):
    """
    无放回抽样。

    直接维护当前 urne 中红球和绿球的数量。
    每抽一次，就把对应颜色的球数减 1。
    """

    rouges = N1
    vertes = N2
    nb_rouges = 0

    for _ in range(n):
        total = rouges + vertes
        if total == 0:
            break

        if rd.random() < rouges / total:
            nb_rouges += 1
            rouges -= 1
        else:
            vertes -= 1

    return nb_rouges


# 理论题结果：
# 1.3 
#
#
#
#

# 对任意第 i 次抽取，“第 i 个球是红球”的概率在两种情形下都等于
# P(R_i) = N1 / (N1 + N2)
#
# 因而 X = 1_{R1} + ... + 1_{Rn}
# 所以在两种情形下
# E(X) = n * N1 / (N1 + N2)


# ============================================================
# Exercice 2
# ============================================================
def esperance(L):
    """
    L 的元素形如 (a, p)，表示 P(X = a) = p。
    于是 E(X) = somme a * p。
    """
    e = 0.0
    for a, p in L:
        e += a * p
    return e


def variance(L):
    """
    利用公式 Var(X) = E(X^2) - E(X)^2。
    """
    ex = esperance(L)
    ex2 = 0.0
    for a, p in L:
        ex2 += (a ** 2) * p
    return ex2 - ex ** 2


# ============================================================
# Exercice 3
# ============================================================
def premier_rang(p):
    """
    模拟“第一个 1 出现的位置”。

    每次以概率 p 得到 1，以概率 1-p 得到 0。
    一旦第一次出现 1，就返回当前序号。
    """

    rang = 1
    while True:
        if rd.random() < p:
            return rang
        rang += 1


# 理论题结果：
# P(X = k) = (1-p)^(k-1) * p,  k >= 1
# 这就是参数 p 的几何分布。


# ============================================================
# Exercice 4
# ============================================================
def poisson(l):
    term = 1
    u = rd.random()
    k = 0
    p_k = math.exp(-l)
    accum = p_k
    while u > accum:
        k += 1
        p_k = p_k * l / k 
        accum += p_k

        term += 1
        print(term)
    return k



def poisson_ai(l):
    """
    生成参数 lambda = l 的 Poisson 随机变量。

    思路：
    - 先算 P(X=0) = e^{-l}
    - 再用递推关系
      P(X=k+1) = P(X=k) * l / (k+1)
    - 把 [0,1] 按这些概率切成若干段，用一个 uniforme U 落点决定返回值。
    """

    u = rd.random()
    k = 0
    pk = math.exp(-l)
    cumul = pk

    while u > cumul:
        k += 1
        pk = pk * l / k
        cumul += pk

    return k


# ============================================================
# Exercice 5
# ============================================================
def entier_aleatoire(L):
    """
    给定概率列表 L = [p0, ..., pk]，返回 j，使得 P(j) = pj。

    做法是把 [0,1] 划分成长度分别为 p0, ..., pk 的若干子区间。
    """

    u = rd.random()
    accum = 0.0

    for j, p in enumerate(L):
        accum += p
        if u <= accum:
            return j

    return len(L) - 1


# ============================================================
# Exercice 6
# ============================================================
def approx(n):
    """
    Monte Carlo pour approximer pi/4.

    在 [0,1]^2 中均匀取 n 个点，统计落在四分之一圆
    x^2 + y^2 <= 1 内的比例。
    """

    compteur = 0
    for _ in range(n):
        x = rd.random()
        y = rd.random()
        if x * x + y * y <= 1:
            compteur += 1

    return compteur / n


# ============================================================
# Exercice 7
# ============================================================
def permutation_aleatoire(n):
    """
    返回 {0, ..., n-1} 的一个均匀随机排列。

    使用 Fisher-Yates 洗牌。
    """
    if n <= 0:
        raise ValueError("On doit avoir n >= 1.")

    L = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rd.randrange(i + 1)
        L[i], L[j] = L[j], L[i]
    return L


def nb_points_fixes(L):
    """
    统计固定点个数：满足 L[i] == i 的下标个数。
    """
    compteur = 0
    for i in range(len(L)):
        if L[i] == i:
            compteur += 1
    return compteur


def moyenne_empirique(n, m):
    """
    生成 m 个随机排列，返回固定点个数的经验平均值。
    """
    if n <= 0 or m <= 0:
        raise ValueError("On doit avoir n >= 1 et m >= 1.")

    total = 0.0
    for _ in range(m):
        perm = permutation_aleatoire(n)
        total += nb_points_fixes(perm)
    return total / m


# 理论题结果：
# 若 X_n 是大小为 n 的随机排列的固定点个数，则 E(X_n) = 1。
# 证明思路是把 X_n 写成若干指示变量之和：
# X_n = I_0 + ... + I_(n-1)
# 且每个位置成为固定点的概率都是 1/n，
# 所以 E(X_n) = n * (1/n) = 1。


# ============================================================
# Quelques tests simples
# ============================================================
def demo():
    print("Exercice 1")
    print("experience1(3,2,10) =", experience1(3, 2, 10))
    print("experience2(3,2,4)  =", experience2(3, 2, 4))
    print()

    print("Exercice 2")
    loi = [(0, 0.2), (1, 0.5), (3, 0.3)]
    print("esperance =", esperance(loi))
    print("variance  =", variance(loi))
    print()

    print("Exercice 3")
    print("premier_rang(0.3) =", premier_rang(0.3))
    print()

    print("Exercice 4")
    print("poisson(2) =", poisson(2))
    print()

    print("Exercice 5")
    print("entier_aleatoire([0.1, 0.2, 0.7]) =", entier_aleatoire([0.1, 0.2, 0.7]))
    print()

    print("Exercice 6")
    print("approx(10000) =", approx(10000))
    print("4 * approx(10000) ~ pi =", 4 * approx(10000))
    print()

    print("Exercice 7")
    perm = permutation_aleatoire(10)
    print("permutation_aleatoire(10) =", perm)
    print("nb_points_fixes(perm) =", nb_points_fixes(perm))
    print("moyenne_empirique(50, 2000) =", moyenne_empirique(50, 2000))


if __name__ == "__main__":
    demo()
