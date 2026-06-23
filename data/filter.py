import osmnx as ox
import pandas as pd


def longueur_impasse(G_und, dead_end_node):
    """
    Remonte depuis un nœud terminal jusqu'au premier carrefour.

    Retourne :
        longueur_totale_m,
        liste_des_noeuds,
        noeud_carrefour
    """

    longueur = 0
    chemin = [dead_end_node]

    courant = dead_end_node
    precedent = None

    while True:

        voisins = [
            n
            for n in G_und.neighbors(courant)
            if n != precedent
        ]

        # Carrefour atteint
        if len(voisins) != 1:
            return longueur, chemin, courant

        suivant = voisins[0]

        edge_data = G_und.get_edge_data(
            courant,
            suivant
        )

        # MultiGraph -> premier segment
        data = next(iter(edge_data.values()))

        longueur += data.get("length", 0)

        chemin.append(suivant)

        precedent = courant
        courant = suivant


def filter_impasses(G, seuil=100):
    # Une rue à double sens ne doit pas compter deux fois
    G_und = ox.convert.to_undirected(G)

    dead_end_nodes = {
        node
        for node, degree in G_und.degree()
        if degree == 1
    }

    impasses = []

    for node in dead_end_nodes:

        longueur, chemin, entree = longueur_impasse(
            G_und,
            node
        )

        impasses.append({
            "dead_end_node": node,
            "entry_node": entree,
            "longueur_m": longueur,
            "nb_segments": len(chemin) - 1,
            "chemin_nodes": chemin,
        })

    df_impasses = pd.DataFrame(impasses)

    a_ignorer = df_impasses[
        df_impasses["longueur_m"] < seuil
    ]

    nodes_a_retirer = set()

    for chemin in a_ignorer["chemin_nodes"]:

        # dernier noeud = carrefour
        for n in chemin[:-1]:
            nodes_a_retirer.add(n)

    G_propre = G.copy()

    G_propre.remove_nodes_from(nodes_a_retirer)

    # nodes_propres, edges_propres = ox.graph_to_gdfs(G_propre)
    return G_propre
