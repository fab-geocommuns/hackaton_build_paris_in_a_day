import itertools
import networkx as nx

def calcul_trajet(G):
    G_undirected = nx.Graph(G)
    largest = max(nx.connected_components(G_undirected), key=len)

    G_c_principal = G_undirected.subgraph(largest).copy()

    for u, v, data in G_c_principal.edges(data=True):
        if "weight" not in data:
            data["weight"] = data.get("length", 1)

    # Un graphe possède un circuit eulérien si et seulement si tous ses sommets sont de degré pair.
    # Les sommets de degré impair constituent donc les "défauts" qu'il faut corriger pour eulériser le graphe.
    odd_nodes = [n for n in G_c_principal.nodes if G_c_principal.degree[n] % 2 == 1]
    
    # Nombre de sommets de degré impair (problème classique du "Chinese Postman Problem")
    print("impairs :", len(odd_nodes))
    
    # Calcul de toutes les distances minimales entre paires de sommets
    # (plus court chemin pondéré selon l'attribut "weight" des arêtes)
    lengths = dict(nx.all_pairs_dijkstra_path_length(G_c_principal, weight="weight"))
    
    # Construction d'un graphe auxiliaire complet entre les sommets impairs
    # Ce graphe servira à trouver les paires optimales à relier pour rendre tous les degrés pairs
    K = nx.Graph()
    
    # Pour chaque paire de sommets impairs (u, v), on ajoute une arête
    # dont le poids correspond à la distance minimale dans le graphe original
    for i, u in enumerate(odd_nodes):
        for v in odd_nodes[i+1:]:
            K.add_edge(u, v, weight=lengths[u][v])

    print("calcul matching")

    matching = nx.algorithms.matching.min_weight_matching(K, weight="weight")

    # Création d'un multigraphe à partir du graphe initial
    # (on autorise plusieurs arêtes entre deux mêmes nœuds)
    # Cela permet de "dupliquer" des chemins sans écraser les arêtes existantes
    G_aug = nx.MultiGraph(G_c_principal)
    
    # Pour chaque paire (u, v) du matching optimal :
    for u, v in matching:
    
        # On récupère le plus court chemin entre u et v dans le graphe original
        # Ce chemin représente la manière la moins coûteuse de "corriger" les degrés
        path = nx.shortest_path(G_c_principal, u, v, weight="weight")
    
        # On ajoute toutes les arêtes du chemin dans le multigraphe
        # Cela revient à dupliquer ces arêtes dans G_aug
    
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
    
            # Ajout d'une arête supplémentaire (duplication)
            # On conserve le poids d'origine de l'arête correspondante
            G_aug.add_edge(a, b, weight=G_c_principal[a][b]["weight"])
    
    # Vérification des sommets de degré impair après augmentation du graphe
    # (ils doivent idéalement être tous pairs si l'eulérisation est réussie)
    
    odd_after = [n for n in G_aug.nodes if G_aug.degree[n] % 2 == 1]

    circuit = list(nx.eulerian_circuit(G_aug))

    return G_c_principal, circuit