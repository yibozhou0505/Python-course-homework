import heapq
import math
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()


### Manipulation des files de priorité en Python : 
"""
Une file de priorité en Python est représenté par une liste de couples, 
la première composante représente la priorité, la seconde l'objet. 
- pour initialiser une file de priorité FP, il suffit 
d'écrire :
FP = []
- Pour vérifier si une file priorité FP est vide, il suffit d'écrire :
FP == []. La valeur est True si elle est vide et False sinon.
- Pour extraire l'élément avec la priorité la plus petite de FP, 
on écrit : 
p,v = heapq.heappop(FP) 
p contient la priorité, v la valeur. 
- Pour ajouter un élément v avec la priorité p dans FP, on écrit : 
heapq.heappush(FP,(p,v)) 

"""

def lire_matrice_csv(nom_fichier,conv=int):
    """
    Lit un CSV contenant une matrice de nombres.
    Retourne une liste de listes d'int ou de float. On 
    peut choisir la fonction de conversion
    """
    matrice = []

    with open(nom_fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:  # ignorer lignes vides
                continue

            # Découper aux virgules et convertir en float
            ligne_valeurs = [conv(v.strip()) for v in ligne.split(',')]
            matrice.append(ligne_valeurs)

    return matrice


def read_csv(file, conv=int):
    matrix = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() # 去掉两端空白字符
            if not line:  # 忽略空行
                continue
            line_valus = [conv(v.strip()) for v in line.split(',')]
            matrix.append(line_valus)
    return matrix


### Exercice 1 Q1
M = lire_matrice_csv(CURRENT_DIR / "matrice.csv",int)

### Exercice 1 Q2
def conversion_matrice_liste(M):
    G = []
    for i in range(len(M)):
        voisins = []
        for j in range(len(M[i])):
            poids = M[i][j]
            if poids != -1:
                voisins.append((j, poids))
        G.append(voisins)
    return G

G = conversion_matrice_liste(M)

def matrix2table(M):
    T = []
    for i in range(len(M)):
        neighber = []
        for j in range(len(M[i])):
            weight = M[i][j]
            if weight != -1:
                neighber.append((j, weight))
        T.append(neighber)
    return T

### Exercice 1 Q3
def dijkstra(G, s):
    n = len(G)
    d = [math.inf] * n
    d[s] = 0

    FP = []
    heapq.heappush(FP, (0, s))

    while FP:
        a, u = heapq.heappop(FP)

        if a == d[u]:
            for v, poids in G[u]:
                nouvelle_distance = d[u] + poids

                if nouvelle_distance < d[v]:
                    d[v] = nouvelle_distance
                    heapq.heappush(FP, (nouvelle_distance, v))

    return d

### Exercice 1 Q4
def verifier_dijkstra(G, nom_fichier_distances=CURRENT_DIR.joinpath("distances.csv")):
    distances_ref = lire_matrice_csv(nom_fichier_distances, int)
    n = len(G)

    for i in range(n):
        distances_calc = dijkstra(G, i)

        for j in range(n):
            ref = distances_ref[i][j]
            calc = distances_calc[j]

            if ref == -1:
                ok = math.isinf(calc)
            else:
                ok = (calc == ref)

            if not ok:
                print("Erreur : source", i, "destination", j)
                print("  calculé =", calc)
                print("  attendu =", ref)
                return False

    print("Vérification Dijkstra réussie.")
    return True
### Exercice 2 Q1
def a_star(G, s, d, H):
    n = len(G)
    distance = [math.inf] * n
    distance[s] = 0

    FP = []
    heapq.heappush(FP, (distance[s] + H[s][d], s))

    while FP:
        priorite, u = heapq.heappop(FP)

        if priorite != distance[u] + H[u][d]:
            continue

        if u == d:
            return distance[d]

        for v, poids in G[u]:
            nouvelle_distance = distance[u] + poids

            if nouvelle_distance < distance[v]:
                distance[v] = nouvelle_distance
                nouvelle_priorite = nouvelle_distance + H[v][d]
                heapq.heappush(FP, (nouvelle_priorite, v))

    return math.inf

### Exercice 2 Q2.a
coordonnees = lire_matrice_csv(CURRENT_DIR.joinpath("localisation.csv"),float)

### Exercice 2 Q2.b
def temps_estime(pos1,pos2):
    lat1,lon1 = pos1
    lat2,lon2 = pos2
    R = 6371  # km rayon considéré pour la Terre
    lat_moy = (lat1 + lat2) / 2
    cos_lat = math.cos(lat_moy * math.pi / 180)

    # km par degré
    km_par_deg_lat = 111.32  # ≈ R * π/180 
    km_par_deg_lon = 111.32 * cos_lat
    """
    on peut prendre comme approximation la distance euclidienne entre pos1 
    et pos2. On suppose que les trains du réseaux roulent à 30km/h. 

    """
    dy = (lat2 - lat1) * km_par_deg_lat
    dx = (lon2 - lon1) * km_par_deg_lon
    distance = math.sqrt(dy**2 + dx**2)
    temps = distance / 30  # en heures
    return temps

### Exercice 2 Q2.c
def construire_H(coordonnees):
    n = len(coordonnees)
    H = []

    for u in range(n):
        ligne = []
        for v in range(n):
            ligne.append(temps_estime(coordonnees[u], coordonnees[v]))
        H.append(ligne)

    return H
H = construire_H(coordonnees)

### Exercice 2 Q2.d
def verifier_a_star(G, H, nom_fichier_distances="distances.csv"):
    distances_ref = lire_matrice_csv(nom_fichier_distances, int)
    n = len(G)

    for s in range(n):
        for d in range(n):
            calc = a_star(G, s, d, H)
            ref = distances_ref[s][d]

            if ref == -1:
                ok = math.isinf(calc)
            else:
                ok = (calc == ref)

            if not ok:
                print("Erreur A* : source", s, "destination", d)
                print("  calculé =", calc)
                print("  attendu =", ref)
                return False

    print("Vérification A* réussie.")
    return True

verifier_a_star(G, H, CURRENT_DIR.joinpath("distances.csv"))