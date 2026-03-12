# ======ex1========
# ...

# ======ex2=========
# 2.1
def dicho(a, b, A, n):
    for _ in range(n):
        mid = (a + b) / 2
        if mid ** 2 < A:
            a = mid
        else:
            b = mid
    return (a, b)

# 2.2
def return_limite(n, A, eps=1e-10):
    un = 1
    converged = False
    for _ in range(n):
        un1 = 0.5 * (un + A/un)
        if abs(un1 - un) < eps:  
            converged = True
            break
        un = un1
    if converged:
        print("Convergent vers", un)
        return un
    else:
        print("Warning: Non convergent")
        return un
return_limite(100, 10)

# 2.3
# ...

# 2.4
def newton(A, n):
    u = 1.0  
    for _ in range(n):
        u = 0.5 * (u + A / u)
    return u
A = 10
for n in range(6):
    approx = newton(A, n)
    print("n =", n, "approx =", approx)

# 2.5
# ...

# ========ex3========
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def cul_1_sur_pi(n):
    sum = 0
    for k in range(n):
        sum += factorial(4*k) * (1103 + 26390*k) / ((factorial(k)**4) * 396**(4*k))
    un_sur_pi = 2 * (2**0.5) / 9801 * sum
    print(un_sur_pi)
    return un_sur_pi

cul_1_sur_pi(100)


# ========ex4========
# 4.1
def dicho(f, a, b, e):
    while b - a > e:
        m = (a + b) / 2
        if f(m) == 0:
            return m
        elif f(a) * f(m) < 0:
            b = m
        else:
            a = m

    return (a + b) / 2

print(dicho(lambda x: x**2 - 2, 1, 2, 1e-10))

# 4.2
def newton(f, df, x0, n):
    x = x0
    for _ in range(n):
        if df(x) == 0:
            raise ValueError("derivation = 0, s'arrete")
        x = x - f(x) / df(x)
    return x

print(newton(lambda x: x**2 - 2, lambda x: 2*x, 1, 100))


# ========ex5========
# 5.1
# ...

# 5.2
def decomposition(p,q):
    L=[]
    while q != 0:
        L.append(p // q)   
        p,q = q, p % q
    return L

print(decomposition(22,7))

# 5.3
def fraction(L): 
    p, q = L[-1], 1
    for i in range(len(L)-2, -1, -1):
         a = L[i]
         p, q = a * p + q, p
    return p, q

print(fraction([3,7]))

# 5.4

    





