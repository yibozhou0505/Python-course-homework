
import math

import numpy as np
import matplotlib.pyplot as plt



# ============ Probleme 1 ============
a_vl = 3.0
b_vl = 2.0
c_vl = 2.0
d_vl = 3.0
x0 = 1.5
y0 = 0.75



# ------- ex1 -------
def FVL(X):
    return np.array([
        a_vl * X[0] - b_vl * X[0] * X[1],
        -c_vl * X[1] + d_vl * X[0] * X[1],
    ], dtype=float)

def DFVL(X):
    x, y = X[0], X[1]
    return np.array([
        [a_vl - b_vl * y, -b_vl * x],
        [d_vl * y, -c_vl + d_vl * x],
    ], dtype=float)

# ------- ex2 -------
def Euler(F,X0,T,N):
    h=T/N
    n=np.size(X0)
    S=np.zeros((n,N+1))
    S[:,0]=X0
    Xn=X0
    for i in range(N):
        Xn+=h*F(Xn)
        S[:,i+1]=Xn
    return S

T = 3
N = 100
X0 = np.array([x0, y0], dtype=float)

S = Euler(FVL,X0,T,N)

# ------- ex3 -------

t = np.linspace(0.0, T, N + 1)

# 1. x(t), y(t) 随时间变化
plt.figure()
plt.plot(t, S[0, :], label="x(t)")
plt.plot(t, S[1, :], label="y(t)")
plt.xlabel("t")
plt.legend()
plt.grid(True)
plt.show()

# 2. 相平面 (x, y)
plt.figure()
plt.plot(S[0, :], S[1, :])
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
plt.show()


# ------- ex4 -------

def RK2(F,X0,T,N):
    h = T / N  # 步长，总时间T/份数N
    n = np.size(X0)  # 维数--状态变量有几个分量
    S = np.zeros((n, N + 1))  # solve
    S[:, 0] = X0
    Xn = X0.copy()
    for i in range(N):
        K1 = F(Xn)
        Xn = Xn + h * F(Xn + 0.5 * h * K1)
        S[:, i + 1] = Xn
    return S


# ------- ex5 -------

def AB2(F,X0,T,N):
    h = T / N  
    n = np.size(X0)  
    S = np.zeros((n, N + 1))  
    S[:, 0] = X0
    
    X1 = X0 + h * F(X0 + 0.5 * h * F(X0))
    S[:, 1] = X1

    Xn_m_1 = X0.copy()
    Xn = X1.copy()

    for i in range(1,N):
        X_n_a_1 = Xn + 0.5 * h * (3 * F(Xn) - F(Xn_m_1))
        S[:, i + 1] = X_n_a_1
        Xn_m_1 = Xn
        Xn = X_n_a_1
    return S

# ------- ex6 -------

def RK4(F,X0,T,N):
    h = T / N  
    n = np.size(X0)  
    S = np.zeros((n, N + 1))  
    S[:, 0] = X0
    Xn = X0.copy()
    for i in range(N):
        K0 = F(Xn)
        K1 = F(Xn + 0.5 * h * K0)
        K2 = F(Xn + 0.5 * h * K1)
        K3 = F(Xn + h * K2)

        K = (K0 + 2 * K1 + 2 * K2 + K3) / 6.0
        Xn = Xn + h * K
        S[:, i + 1] = Xn
    return S


# ------- ex7 -------
def IEuler(F,DF,X0,T,N):
    h = T / N  
    n = np.size(X0)  
    S = np.zeros((n, N + 1))  
    S[:, 0] = X0

    Xn = X0.copy()
    I = np.eye(n)
    for i in range(N):
        def G(Z):
            return Z - Xn - h * F(Z)

        def DG(Z):
            return I - h * DF(Z)

        Z = Xn + h * F(Xn)

        for _ in range(20):
            delta = np.linalg.solve(DG(Z), G(Z))
            Z = Z - delta
            if np.linalg.norm(delta) < 1e-12:
                break
        
        Xn = Z
        S[:, i + 1] = Xn
    return S


# ------- ex8 -------
def CN(F,DF,X0,T,N):
    h = T / N  
    n = np.size(X0)  
    S = np.zeros((n, N + 1))  
    S[:, 0] = X0

    Xn = X0.copy()
    I = np.eye(n)
    for i in range(N):
        def G(Z):
            return Z - Xn - 0.5 * h * (F(Xn) +F(Z))

        def DG(Z):
            return I - 0.5 *h * DF(Z)

        Z = Xn + h * F(Xn)

        for _ in range(20):
            delta = np.linalg.solve(DG(Z), G(Z))
            Z = Z - delta
            if np.linalg.norm(delta) < 1e-12:
                break
        
        Xn = Z
        S[:, i + 1] = Xn
    return S


# ------- ex9 -------
def H(X):
    x = X[0]
    y = X[1]
    return d_vl * x - c_vl * np.log(x) + b_vl * y - a_vl * np.log(y)

methods = {
    "Euler": Euler(FVL, X0, T, N),
    "RK2": RK2(FVL, X0, T, N),
    "AB2": AB2(FVL, X0, T, N),
    "RK4": RK4(FVL, X0, T, N),
    "IEuler": IEuler(FVL, DFVL, X0, T, N),
    "CN": CN(FVL, DFVL, X0, T, N),
}

t = np.linspace(0.0, T, N + 1)

plt.figure()
for name, S in methods.items():
    plt.plot(t, H(S), label=name)

plt.xlabel("t")
plt.ylabel("H(x, y)")
plt.title("Premiere integrale")
plt.grid(True)
plt.legend()
plt.show()


# ======= Probleme 2 =======


























# # ============================================================
# # Outils generiques
# # ============================================================
# def time_grid(T, N):
#     return np.linspace(0.0, T, N + 1)


# def as_float_array(X):
#     return np.array(X, dtype=float)


# def plot_solution_2d(t, S, title="", labels=None):
#     """
#     Trace les composantes d'une solution 2D en fonction du temps.
#     S est un tableau de forme (2, N+1).
#     """
#     if labels is None:
#         labels = ("x", "y")

#     plt.figure(figsize=(9, 4))
#     plt.plot(t, S[0], label=labels[0])
#     plt.plot(t, S[1], label=labels[1])
#     plt.xlabel("t")
#     plt.ylabel("solution")
#     plt.title(title)
#     plt.grid(True, alpha=0.3)
#     plt.legend()


# def plot_phase_2d(S, title="", labels=None):
#     """
#     Trace le portrait de phase pour un systeme a 2 variables.
#     """
#     if labels is None:
#         labels = ("x", "y")

#     plt.figure(figsize=(5, 5))
#     plt.plot(S[0], S[1])
#     plt.xlabel(labels[0])
#     plt.ylabel(labels[1])
#     plt.title(title)
#     plt.grid(True, alpha=0.3)
#     plt.axis("equal")


# def plot_solution_3d(t, S, title="", labels=None):
#     """
#     Trace les composantes d'une solution 3D en fonction du temps.
#     """
#     if labels is None:
#         labels = ("y1", "y2", "y3")

#     plt.figure(figsize=(10, 4))
#     for i, lab in enumerate(labels):
#         plt.plot(t, S[i], label=lab)
#     plt.xlabel("t")
#     plt.ylabel("solution")
#     plt.title(title)
#     plt.grid(True, alpha=0.3)
#     plt.legend()


# def plot_phase_3d_y1_y3(S, title="", labels=("y1", "y3")):
#     """
#     Trace le portrait de phase (y1, y3).
#     """
#     plt.figure(figsize=(5, 5))
#     plt.plot(S[0], S[2], lw=0.8)
#     plt.xlabel(labels[0])
#     plt.ylabel(labels[1])
#     plt.title(title)
#     plt.grid(True, alpha=0.3)


# # ============================================================
# # Probleme 1 - Volterra-Lotka
# # ============================================================
# a_vl = 3.0
# b_vl = 2.0
# c_vl = 2.0
# d_vl = 3.0


# def FVL(X):
#     """
#     Systeme proies-predateurs de Volterra-Lotka.
#     X = array([x, y]).
#     """
#     x, y = X
#     return np.array([
#         a_vl * x - b_vl * x * y,
#         -c_vl * y + d_vl * x * y,
#     ], dtype=float)


# def DFVL(X):
#     """
#     Jacobi de FVL.
#     """
#     x, y = X
#     return np.array([
#         [a_vl - b_vl * y, -b_vl * x],
#         [d_vl * y, -c_vl + d_vl * x],
#     ], dtype=float)


# def Euler(F, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0
#     Xn = X0.copy()
#     for i in range(N):
#         Xn = Xn + h * F(Xn)
#         S[:, i + 1] = Xn
#     return S


# def RK2(F, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0
#     Xn = X0.copy()
#     for i in range(N):
#         K1 = F(Xn)
#         Xn = Xn + h * F(Xn + 0.5 * h * K1)
#         S[:, i + 1] = Xn
#     return S


# def AB2(F, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0

#     if N == 0:
#         return S

#     # Premier pas avec RK2.
#     X1 = X0 + h * F(X0 + 0.5 * h * F(X0))
#     S[:, 1] = X1

#     Xnm1 = X0.copy()
#     Xn = X1.copy()
#     for i in range(1, N):
#         Xnp1 = Xn + 0.5 * h * (3.0 * F(Xn) - F(Xnm1))
#         S[:, i + 1] = Xnp1
#         Xnm1, Xn = Xn, Xnp1

#     return S


# def RK4(F, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0
#     Xn = X0.copy()
#     for i in range(N):
#         k0 = F(Xn)
#         k1 = F(Xn + 0.5 * h * k0)
#         k2 = F(Xn + 0.5 * h * k1)
#         k3 = F(Xn + h * k2)
#         Xn = Xn + (h / 6.0) * (k0 + 2.0 * k1 + 2.0 * k2 + k3)
#         S[:, i + 1] = Xn
#     return S


# def newton_solve_step(G, DG, X_init, tol=1e-12, max_iter=30):
#     """
#     Newton pour resoudre G(X)=0 avec matrice jacobienne DG(X).
#     """
#     X = X_init.copy()
#     for _ in range(max_iter):
#         GX = G(X)
#         J = DG(X)
#         delta = np.linalg.solve(J, GX)
#         X_new = X - delta
#         if np.linalg.norm(delta, ord=np.inf) <= tol * (1.0 + np.linalg.norm(X_new, ord=np.inf)):
#             return X_new
#         X = X_new
#     return X


# def IEuler(F, DF, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0
#     Xn = X0.copy()
#     I = np.eye(n)

#     for i in range(N):
#         def G(Z):
#             return Z - Xn - h * F(Z)

#         def DG(Z):
#             return I - h * DF(Z)

#         X_guess = Xn + h * F(Xn)
#         Xn = newton_solve_step(G, DG, X_guess)
#         S[:, i + 1] = Xn
#     return S


# def CN(F, DF, X0, T, N):
#     h = T / N
#     X0 = as_float_array(X0)
#     n = np.size(X0)
#     S = np.zeros((n, N + 1), dtype=float)
#     S[:, 0] = X0
#     Xn = X0.copy()
#     I = np.eye(n)

#     for i in range(N):
#         Fn = F(Xn)

#         def G(Z):
#             return Z - Xn - 0.5 * h * (Fn + F(Z))

#         def DG(Z):
#             return I - 0.5 * h * DF(Z)

#         X_guess = Xn + h * Fn
#         Xn = newton_solve_step(G, DG, X_guess)
#         S[:, i + 1] = Xn
#     return S


# def H_vl(S):
#     """
#     Premiere integrale du systeme Volterra-Lotka.
#     """
#     x = S[0]
#     y = S[1]
#     return d_vl * x - c_vl * np.log(x) + b_vl * y - a_vl * np.log(y)


# def demo_volterra_lotka(T=3.0, N=100):
#     X0 = np.array([1.5, 0.75], dtype=float)
#     t = time_grid(T, N)

#     S_e = Euler(FVL, X0, T, N)
#     S_rk2 = RK2(FVL, X0, T, N)
#     S_ab2 = AB2(FVL, X0, T, N)
#     S_rk4 = RK4(FVL, X0, T, N)
#     S_ie = IEuler(FVL, DFVL, X0, T, N)
#     S_cn = CN(FVL, DFVL, X0, T, N)

#     return {
#         "t": t,
#         "Euler": S_e,
#         "RK2": S_rk2,
#         "AB2": S_ab2,
#         "RK4": S_rk4,
#         "IEuler": S_ie,
#         "CN": S_cn,
#     }


# def plot_volterra_lotka_results(results):
#     t = results["t"]
#     for name in ["Euler", "RK2", "AB2", "RK4", "IEuler", "CN"]:
#         S = results[name]
#         plot_solution_2d(t, S, title=f"Volterra-Lotka - {name}", labels=("x", "y"))
#         plot_phase_2d(S, title=f"Phase portrait - {name}", labels=("x", "y"))

#     # Evolution de l'integrale premiere pour comparer les schemas.
#     plt.figure(figsize=(9, 4))
#     for name in ["Euler", "RK2", "AB2", "RK4", "IEuler", "CN"]:
#         S = results[name]
#         plt.plot(t, H_vl(S), label=name)
#     plt.xlabel("t")
#     plt.ylabel("H(x,y)")
#     plt.title("Premiere integrale du systeme Volterra-Lotka")
#     plt.grid(True, alpha=0.3)
#     plt.legend()


# # ============================================================
# # Probleme 2 - Lorenz
# # ============================================================
# sigma_l = 10.0
# b_l = 8.0 / 3.0
# r_l = 28.0


# def FLorenz(X):
#     y1, y2, y3 = X
#     return np.array([
#         sigma_l * (y2 - y1),
#         r_l * y1 - y2 - y1 * y3,
#         y1 * y2 - b_l * y3,
#     ], dtype=float)


# def DFLorenz(X):
#     y1, y2, y3 = X
#     return np.array([
#         [-sigma_l, sigma_l, 0.0],
#         [r_l - y3, -1.0, -y1],
#         [y2, y1, -b_l],
#     ], dtype=float)


# def demo_lorenz(T=100.0, N=20000):
#     X0 = np.array([1.0, 0.0, 0.0], dtype=float)
#     t = time_grid(T, N)

#     S_e = Euler(FLorenz, X0, T, N)
#     S_rk2 = RK2(FLorenz, X0, T, N)
#     S_rk4 = RK4(FLorenz, X0, T, N)

#     return {
#         "t": t,
#         "Euler": S_e,
#         "RK2": S_rk2,
#         "RK4": S_rk4,
#     }


# def plot_lorenz_results(results):
#     t = results["t"]
#     for name in ["Euler", "RK2", "RK4"]:
#         S = results[name]
#         plot_solution_3d(t, S, title=f"Lorenz - {name}", labels=("y1", "y2", "y3"))
#         plot_phase_3d_y1_y3(S, title=f"Phase portrait (y1,y3) - {name}")


# def compare_small_perturbations(base_X0=np.array([1.0, 0.0, 0.0]), base_sigma=10.0, base_h=0.005):
#     """
#     Petite fonction pour explorer la sensibilite du systeme de Lorenz.
#     """
#     global sigma_l

#     cases = []

#     # Perturbation initiale
#     cases.append(("X0 + 1e-8", base_X0 + np.array([1e-8, 0.0, 0.0]), base_sigma, base_h))

#     # Perturbation de sigma
#     cases.append(("sigma + 1e-8", base_X0, base_sigma + 1e-8, base_h))

#     # Perturbation du pas
#     cases.append(("h + 1e-8", base_X0, base_sigma, base_h + 1e-8))

#     original_sigma = sigma_l
#     outputs = {}
#     for label, X0, sigma_val, h in cases:
#         sigma_l = sigma_val
#         T = 10.0
#         N = int(round(T / h))
#         outputs[label] = RK4(FLorenz, X0, T, N)
#     sigma_l = original_sigma
#     return outputs


# # ============================================================
# # Quelques demos
# # ============================================================
# def main():
#     print("TP8: test preliminaire")
#     x = np.linspace(0, 2 * np.pi, 1000)
#     y = np.sin(x)
#     plt.figure(figsize=(6, 3))
#     plt.plot(x, y)
#     plt.title("Test preliminaire - sin(x)")
#     plt.grid(True, alpha=0.3)

#     print("Probleme Volterra-Lotka")
#     vl = demo_volterra_lotka()
#     print("Euler final:", vl["Euler"][:, -1])
#     print("RK4 final:", vl["RK4"][:, -1])
#     print("H(Euler) final:", H_vl(vl["Euler"])[:3])

#     print("Probleme Lorenz")
#     lo = demo_lorenz(T=5.0, N=5000)
#     print("Euler final:", lo["Euler"][:, -1])
#     print("RK4 final:", lo["RK4"][:, -1])

#     plot_volterra_lotka_results(vl)
#     plot_lorenz_results(lo)

#     # En environnement terminal, on enregistre les figures plutôt que
#     # d'ouvrir une fenetre interactive.
#     plt.savefig("TP8_plots.png", dpi=150, bbox_inches="tight")
#     plt.close("all")


# if __name__ == "__main__":
#     main()
