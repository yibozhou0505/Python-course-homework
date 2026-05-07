import collections as clt

### Construction de la classe Graphe
class Graphe:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def ajouter_arc(self, u, v):
        self.adj[u].append(v)

    def __str__(self):
        """ permet d'afficher avec print, affichage rudimentaire """
        return "\n".join(f"{i} → {self.adj[i]}" for i in range(self.n))

    # --- Exercice 1 ---
    def est_non_oriente(self):
        print(f"Adjacency lists: {self.adj}")
        adj_sets = [set(voisins) for voisins in self.adj]
        print(adj_sets)

        for u in range(self.n):
            for v in self.adj[u]:
                if u not in adj_sets[v]:
                    return False
        return True

    # --- Exercice 2 ---
    def affichage_profondeur(self, s):
        # s是起始顶点
        pile = [s]
        traites = [False for _ in range(self.n)] # bool列表：标记顶点是否处理
        vus = [False for _ in range(self.n)] # bool列表：标记顶点是否被发现
        vus[s] = True
        while pile != [] :
            e = pile.pop()
            print(e)
            traites[e] = True
            for x in self.adj[e] : # 遍历e的所有邻居
                if not traites[x] and not vus[x]:
                    pile.append(x)
                    vus[x] = True

    def parcours_profondeur(self, s):
        '''
        DFS:每次取出栈顶，如果没有访问过就访问，再把没有访问过的邻居入栈，如果栈不空就继续
        '''
        pile = [s]
        vus = [False for _ in range(self.n)]
        ordre = []

        while pile:
            u = pile.pop()

            if not vus[u]:
                vus[u] = True
                ordre.append(u)

                for v in self.adj[u]:
                    if not vus[v]:
                        pile.append(v)

        return ordre

    def affichage_largeur(self, s):
        file = clt.deque([s])  # 双端队列
        traites = [False for _ in range(self.n)]
        vus = [False for _ in range(self.n)]
        vus[s] = True
        while len(file) != 0:
            e = file.popleft() # 弹出左端点标记为处理
            print(e)
            traites[e] = True
            for x in self.adj[e]: # 遍历e的所有邻居, 如果没有发现没有处理就加到右端
                if not traites[x] and not vus[x]:
                    file.append(x)
                    vus[x] = True

    def parcours_largeur(self, s):
        '''
        BFS:每次取出队首，没有访问过就访问，再把没有访问过的邻居入队，队不空就继续
        '''
        file = clt.deque([s])
        vus = [False for _ in range(self.n)]
        ordre = []
        vus[s] = True

        while file:
            u = file.popleft()
            ordre.append(u)

            for v in self.adj[u]:
                if not vus[v]:
                    file.append(v)
                    vus[v] = True
        return ordre
    


    def affichage_profondeur_rec(self, s):
        vus = [False for _ in range(self.n)]
        def rec_aux(sommet):
            if not vus[sommet]:
                vus[sommet] = True
                print(sommet)
                for x in self.adj[sommet]:
                    rec_aux(x)
        rec_aux(s)


    def parcours_profondeur_rec(self, s):
        vus = [False for _ in range(self.n)]
        ordre = []

        def dfs(u):
            vus[u] = True
            ordre.append(u)

            for v in self.adj[u]:
                if not vus[v]:
                    dfs(v)
        dfs(s)
        return ordre
    

    # ex2.5
    # 非递归DFS使用显示栈pile，访问顺序受到邻居压栈(先进后出)顺序影响；递归则使用python的函数调用栈，通常按照邻接表从左到右访问邻居

    # --- Exercice 3 ---
    # 不连通：至少存在两个顶点之间没有路径；如果从一个顶点出发能够访问所有顶点则任意两个顶点之间都存在路径->连通
    def est_connexe_par_largeur(self):
        '''用BFS判断图是否连通'''
        if not self.est_non_oriente():
            return False
        
        if self.n == 0:
            return True
        
        return len(self.parcours_largeur(0)) == self.n


    def est_connexe_par_profondeur(self):
        '''用DFS判断图是否连通'''
        if not self.est_non_oriente():
            return False
        
        if self.n == 0:
            return True
        
        return len(self.parcours_profondeur(0)) == self.n


    # --- Exercice 4 ---
    def distance(self, s):
        dist = [float('inf') for _ in range(self.n)]
        dist[s] = 0
        file = clt.deque([s])

        while file:
            u = file.popleft()

            for v in self.adj[u]:
                if dist[v] == float('inf'):
                    dist[v] = dist[u] + 1
                    file.append(v)
        return dist
    
    def parents_largeur(self, s):
        '''
        从起点s到每个顶点的最短路径上的父节点(从哪条最短路径访问到这个节点的，这个节点的前一个节点)
        '''
        parents = [None for _ in range(self.n)]
        parents[s] = s
        file = clt.deque([s])

        while file:
            u = file.popleft()

            for v in self.adj[u]:
                if parents[v] is None:
                    parents[v] = u
                    file.append(v)
        return parents


    def chemins_optimaux(self, s):
        '''
        返回从起点s出发的所有最短路径
        '''
        parents = self.parents_largeur(s) # 获取父节点数组
        chemins = []

        for v in range(self.n):
            if parents[v] is None:
                chemins.append(None)
            else:
                chemin = []
                courant = v

                while courant != s:
                    chemin.append(courant)
                    courant = parents[courant]

                chemin.append(s)
                chemin.reverse()
                chemins.append(chemin)
        return chemins


    # --- Exercice 5 ---
    def contient_cycle(self):
        # à compléter
        pass

    # --- Bonus ---
    def composantes_connexes(self):
        # à compléter
        pass
    def tri_topo(self):
        # à compléter
        pass

### Fonction d'affichage de graphes (optionnel)

def afficher_graphique(graphe, titre="Graphe"):
    """
    Affichage graphique avec networkx et matplotlib.
    Si les bibliothèques ne sont pas installées, affiche un message.
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️ Affichage graphique impossible.")
        print("Installe networkx et matplotlib avec :")
        print("    pip install networkx matplotlib")
        return

    # Création
    G = nx.DiGraph()

    # Ajout des sommets
    for u in range(graphe.n):
        G.add_node(u)

    # Ajout des arcs
    for u in range(graphe.n):
        for v in graphe.adj[u]:
            G.add_edge(u, v)

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # Dessin
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=500,
            font_size=12,
            edge_color='gray',
            font_weight='bold')
    plt.title(titre)
    plt.show()


### Exemples de graphes pour des tests
# Exercice 1 - Non orienté (symétrique)
G1_non_oriente = Graphe(4)
G1_non_oriente.adj = [[1, 2], [0, 3], [0], [1]]

# Exercice 1 - Orienté (non symétrique)
G1_oriente = Graphe(3)
G1_oriente.adj = [[1], [2], []]

# Exercice 2 - Graphe en étoile (sommet 0 au centre)
G2_etoile = Graphe(4)
G2_etoile.adj = [[1, 2, 3], [0], [0], [0]]

# Exercice 2 - Graphe pour différencier BFS et DFS
G2_difference = Graphe(6)
G2_difference.adj = [[1, 2], [3, 4], [5], [], [], []]

# Exercice 2 - Graphe en chaîne
G2_chaine = Graphe(4)
G2_chaine.adj = [[1], [0, 2], [1, 3], [2]]

# Exercice 3 - Graphe connexe (chaîne de 5 sommets)
G3_connexe = Graphe(5)
G3_connexe.adj = [[1], [0, 2], [1, 3], [2, 4], [3]]

# Exercice 3 - Graphe non connexe (deux composantes)
G3_non_connexe = Graphe(5)
G3_non_connexe.adj = [[1], [0, 2], [1], [4], [3]]

# Exercice 3 - Graphe avec sommet isolé (sommet 4)
G3_avec_isolet = Graphe(5)
G3_avec_isolet.adj = [[1], [0, 2], [1, 3], [2], []]

# Exercice 4 - Graphe pour calculer les distances
G4_distances = Graphe(6)
G4_distances.adj = [[1, 2], [3, 4], [5], [], [], []]

# Exercice 4 - Graphe plus complet (7 sommets)
G4_complet = Graphe(7)
G4_complet.adj = [[1, 2], [3, 4], [4, 5], [6], [6], [], []]

# Exercice 5 - Graphe orienté sans cycle (DAG)
G5_sans_cycle = Graphe(4)
G5_sans_cycle.oriente = True
G5_sans_cycle.adj = [[1, 2], [3], [3], []]

# Exercice 5 - Graphe orienté avec cycle (triangle)
G5_avec_cycle = Graphe(3)
G5_avec_cycle.adj = [[1], [2], [0]]

# Exercice 5 - Cycle long (5 sommets)
G5_cycle_long = Graphe(5)
G5_cycle_long.adj = [[1], [2], [3], [4], [1]]

# Exercice 5 - graphe sans cycle
G5_pas_cycle = Graphe(4)
G5_pas_cycle.adj = [[1], [2, 3], [3], []]

# Exercice 6 - Trois composantes connexes
G6_composantes = Graphe(7)
G6_composantes.adj = [[1], [0, 2], [1], [4], [3], [6], [5]]

# Exercice 7 - graphe sans cycle pour tri topologique
G7_tri_topo = Graphe(4)
G7_tri_topo.adj = [[1, 2], [3], [3], []]

# Exercice 7 - Graphe avec cycle (doit lever une exception)
G7_avec_cycle = Graphe(3)
G7_avec_cycle.adj = [[1], [2], [0]]

# Graphe vide (0 sommet)
G_vide = Graphe(0)
G_vide.adj = []

# Graphe à 1 sommet
G_1_sommet = Graphe(1)
G_1_sommet.adj = [[]]

# Graphe complet à 4 sommets (K4)
G_K4 = Graphe(4)
G_K4.adj = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]

# Graphe complet à 5 sommets (K5)
G_K5 = Graphe(5)
G_K5.adj = [
    [1, 2, 3, 4],
    [0, 2, 3, 4],
    [0, 1, 3, 4],
    [0, 1, 2, 4],
    [0, 1, 2, 3]
]

### Tests
if __name__ == "__main__":
    print("=== Exercice 1 ===")
    print("Non orienté (True attendu):", G1_non_oriente.est_non_oriente())
    print("Orienté (False attendu):", G1_oriente.est_non_oriente())

    print("\n=== Exercice 2 ===")
    print("BFS:", G2_difference.parcours_largeur(0))
    print("DFS:", G2_difference.parcours_profondeur(0))

    print("\n=== Exercice 3 ===")
    print("Connexe (True):", G3_connexe.est_connexe_par_largeur())
    print("Non connexe (False):", G3_non_connexe.est_connexe_par_largeur())

    print("\n=== Exercice 4 ===")
    print("Distances:", G4_distances.distance(0))

    print("\n=== Exercice 5 ===")
    print("Sans cycle (False):", G5_sans_cycle.contient_cycle())
    print("Avec cycle (True):", G5_avec_cycle.contient_cycle())

    print("\n=== Cas limites ===")
    print("Graphe vide - connexe:", G_vide.est_connexe_par_largeur())
    print("1 sommet - connexe:", G_1_sommet.est_connexe_par_largeur())