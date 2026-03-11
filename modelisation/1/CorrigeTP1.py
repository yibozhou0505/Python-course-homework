# Exemples sequances

 def apparait(sequence) :
    N = len(sequence)
    for i in range(N-2) :
        c = sequence[i]+sequence[i+1]+sequence[i+2]
        if c=="AUG" :
            print(i)
            return
    print(-1)
    return

# Exercice 1
#1. n et m valent respectivement 13 et 78
#2. n et m valent toutes les deux 13. La troisième ligne
# écrase l'ancienne valeur de n.

# Exercice 2
def saisie () :
    chaine = input()
    print(len(chaine)%2 == 0)
    return 

# Exercice 3
def conversion () :
    secondes = int(input())
    initial = secondes
    heures = secondes // 3600
    secondes = secondes % 3600
    minutes = secondes // 60
    secondes = secondes % 60
    print(initial," correspond à ",heures," heures ", minutes, "minutes", secondes," secondes")
    return

# Exercice 4
def affichage () :
    chaine = input()
    print(chaine[-5:])
    return

# Exercice 5
def absolue (x) :
    if x>=0 :
        return x
    return -x

# Exercice 6
def somme_p(n,p) :
    S = 0
    for i in range(n+1) :
        S = S + i**p
    return S

# Exercice 7
def est_premier(n) :
    for i in range(2,n) :
        if i**2 > n :
            return True 
        if (n%i) == 0 :
            return False
    return True

# Exercice 8
def factorielle(n) :
    P = 1
    for i in range(1,n+1) :
        P = P*i
    return P

def binome(n,p) :
    if (p>n) or (p<0) :
        return 0
    else :
        return (factorielle(n))//(factorielle(p)*factorielle(n-p))

# Exercice 9
def fibo(n) :
    f0 = 1
    f1 = 1
    for _ in range(n) :
        f2 = f0 + f1
        f0 = f1
        f1 = f2
    return f0

# Exercice 10
def est_somme_de_carre(n) :
    for a in range(n) :
        for b in range(n) :
            if (a*a + b*b)==n :
                return True
    return False
# Il est possible de améliorer les bornes...

# Exercice 11
def calcul(x) :
    n = 0
    S = 0
    while S <= x :
        n = n + 1
        S = S + n
    return n-1

# Exercice 12
def u(n) :
    u0 = 3
    for i in range(n) :
        u0 = u0**2 + 3*u0 + i
    return u0

def somme_u(n) :
    S = 0
    for i in range(n+1) :
        S = S + u(i)
    return S

# Exercice 13
def distance(a,b) :
    if len(a) == len(b) :
        d = 0
        for i in range(len(a)) :
            if a[i] != b[i] :
                d = d + 1
        return d
    else :
        print("pas de la même longueur")
        return

# Exercice 14
def nb_voyelles(s) :
    nb = 0
    voyelles = "aeiouy"
    for i in range(len(s)) :
        if s[i] in voyelles :
            nb = nb + 1
    return nb

# Exercice 15
def dans_le_disque(a,b,r,x,y) :
    S = (x-a)**2 + (y-b)**2
    return (S < r*r)

# Exercice 16
def nourrir_pigeon(nbre_portions) :
    pigeons = 0
    minutes = 0
    while nbre_portions > 0 :
        minutes = minutes + 1
        if pigeons >= nbre_portions :
            return pigeons
        elif pigeons + minutes >= nbre_portions :
            return nbre_portions
        else :
            pigeons = pigeons + minutes
            nbre_portions = nbre_portions - pigeons
    return pigeons

# Exercice 17 
def premiers_entre_eux(n,m) :
    if (n == 0) or (m == 0) :
        return max(n,m)
    else : 
        while (n % m != 0) :
            reste = n % m
            n = m
            m = reste
        return m

# Exercice 18
def lettres_consecutives_id(texte) :
    for i in range(len(texte)-1) :
        if texte[i] == texte[i+1] :
            return True
    return False


# Exercice 19
def est_suffixe(s,m) : 
    if len(m)<len(s) :
        return False
    for i in range(len(m)-1,len(m)-1-len(s),-1) :
        if s[i-len(m)]!=m[i] :
            return False
    return True

# Exercice 20
def est_croissante(L) :
    if len(L) <= 1 :
        return True
    for i in range(len(L)-1) :
        if L[i] > L[i+1] :
            return False
    return True 
def est_decroissante(L) :
    if len(L) <= 1 :
        return True
    for i in range(len(L)-1) :
        if L[i] < L[i+1] :
            return False
    return True
    
    
def est_monotone(L)  :
    return est_croissante(L) or est_decroissante(L)

# Exercice 21

def bezout(n,m) :
    if m==0 :
        return (1,0) # cas où n est le pgcd
    (a,b) = bezout(m,n%m) # on trouve de façon récursive un couple u,v pour (m,n modulo m)
    return (b,a-(n//m)*b) # on retrouve le couple u,v pour (n,m) 

