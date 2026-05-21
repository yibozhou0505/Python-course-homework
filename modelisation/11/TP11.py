import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Exercice 1
# Prise en main de la transformee de Fourier discrete
# ============================================================


def exercice1():
    x = np.linspace(0.0001, 2 * np.pi, 1000)  # 从0.0001 到 2pi的1000个等间距数组成数组
    # print(x)
    y = np.sin(100 / x)

    plt.figure()
    plt.plot(x, y)
    plt.title("sin(100/x)")

    z = np.fft.fft(y)  # 得到频域表示
    n = z.size
    fq = np.arange(-np.floor(n / 2), n - np.floor(n / 2))
    # print(z)
    # print(n)
    # print(fq)

    plt.figure()
    plt.plot(fq, np.abs(np.fft.fftshift(z)))  # fftshift(z)把0频率分量移动到数组中心
    plt.title("Module de la transformee de Fourier")
    plt.show()


# exercice1()


# ============================================================
# Exercice 2
# Une fonction dynamique
# ============================================================

def exercice2():
    def fonction_dynamique(t, epsilon=1e-2):
        return np.sin(10 * np.pi / (np.abs(t) + epsilon))
    # 2.1
    N = 1000
    t = np.linspace(-np.pi, np.pi, N, endpoint=False)
    y = fonction_dynamique(t)
    plt.figure()
    plt.plot(t, y)

    # 2.2
    z = np.fft.fft(y)
    n = z.size
    fq = np.arange(-np.floor(n / 2), n - np.floor(n / 2))
    flat = z/N


    plt.figure()
    plt.plot(fq,np.abs(np.fft.fftshift(flat)))
    plt.show()
    
    # 2.3

    modes = np.fft.fftfreq(N, d=1/N).astype(int)

    def filtre_condition(z, masque):
        z_filtre = np.zeros_like(z)
        z_filtre[masque] = z[masque]
        g = np.fft.ifft(z_filtre).real
        return g
    s1 = (-N/20 <= modes) & (modes <= N/20)
    s2 = (N/20 <= abs(modes)) & (abs(modes) <= N/10)
    s3 = (N/4 <= abs(modes)) & (abs(modes) <= N/2)

    S1 = filtre_condition(z, s1)
    S2 = filtre_condition(z, s2)
    S3 = filtre_condition(z, s3)

    plt.figure()
    plt.plot(t,S1)
    plt.plot(t,S2)
    plt.plot(t,S3)
    plt.title("Reconstructions par bandes de frequences")
    plt.show()

# exercice2()

# ============================================================
# Exercice 3
# Equation de la chaleur
# ============================================================

# 3.1
def temperature(f0, t, n):
    x = np.arange(n) / n
    valeurs_initiales = f0(x)
    coeffs = np.fft.fft(valeurs_initiales)
    frequences = np.fft.fftfreq(n, d=1.0 / n)
    facteur = np.exp(-((2 * np.pi * frequences) ** 2) * t)
    return np.fft.ifft(coeffs * facteur).real


def condition_initiale_barre(x):
    return ((7 / 16 <= x) & (x <= 9 / 16)).astype(float)


def exercice3(n=1000):
    x = np.arange(n) / n
    temps = np.arange(0, 11) * 1e-3

    plt.figure()
    for t in temps:
        plt.plot(x, temperature(condition_initiale_barre, t, n), label=f"t={t:.3f}")
    plt.legend()
    plt.title("Evolution de la temperature")
    plt.show()

exercice3()

# ============================================================
# Exercice 4
# Interpolation de fonctions periodiques
# ============================================================


# def filtre(phi, n, m):
#     h = np.zeros(n, dtype=float)
#     for k in range(n):
#         total = 0.0
#         for j in range(-m, m + 1):
#             total += phi(k + n * j)
#         h[k] = total
#     return h


# def interpole(f, phi, n, m=0, seuil=1e-14):
#     x = np.arange(n) / n
#     valeurs = f(x)
#     h = filtre(phi, n, m)

#     fh = np.fft.fft(h)
#     ff = np.fft.fft(valeurs)

#     if np.any(np.abs(fh) < seuil):
#         raise ZeroDivisionError("Le filtre a un coefficient de Fourier trop proche de zero.")

#     ck = np.fft.ifft(ff / fh)
#     return ck.real


# def somme(ck, phi, n, m=0):
#     h = filtre(phi, n, m)
#     valeurs = np.fft.ifft(np.fft.fft(h) * np.fft.fft(ck))
#     return valeurs.real


# def phi_gaussienne(t, sigma=1.0):
#     return np.exp(-(t ** 2) / (sigma ** 2)) / (sigma * np.sqrt(np.pi))


# def fonction_interpolation(t, epsilon=1e-2):
#     return np.sin(10 * np.pi / (np.abs(t - 0.5) + epsilon))


# def exercice4(n=1000, m=0, sigma=1.0, epsilon=1e-2):
#     phi = lambda t: phi_gaussienne(t, sigma)
#     f = lambda t: fonction_interpolation(t, epsilon)

#     x = np.arange(n) / n
#     valeurs = f(x)
#     ck = interpole(f, phi, n, m)
#     interpolees = somme(ck, phi, n, m)

#     plt.figure()
#     plt.plot(x, valeurs, label="f")
#     plt.plot(x, interpolees, "--", label="S_N")
#     plt.legend()
#     plt.title("Interpolation periodique")
#     plt.show()

#     return x, valeurs, ck, interpolees


# # if __name__ == "__main__":
# #     # Decommenter les lignes voulues pour afficher les figures.
# #     # exercice1()
#     # exercice2()
#     # exercice3()
#     # exercice4()
#     pass
