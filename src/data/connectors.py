import osmnx as ox
import networkx as nx


def tag_connectors(
    G,
    connector_length_m=12,
    min_degree=3,
):
    """
    Tag les petits tronçons de transit ("connecteurs").

    Paramètres
    ----------
    G : networkx.MultiDiGraph
        Graphe OSMnx orienté.

    connector_length_m : float
        Longueur maximale d'un connecteur.

    min_degree : int
        Degré minimal des deux extrémités.

    Retour
    -------
    G_tagged : MultiDiGraph
        Graphe avec les attributs :
            - is_connector
            - mandatory_cover
            - is_bridge

    nodes_gdf : GeoDataFrame

    edges_gdf : GeoDataFrame
    """

    G_tagged = G.copy()

    # --------------------------------------------------------
    # Graphe non orienté pour l'analyse topologique
    # --------------------------------------------------------

    G_und = ox.convert.to_undirected(G_tagged)

    degree = dict(G_und.degree())

    bridges = {
        tuple(sorted(edge))
        for edge in nx.bridges(G_und)
    }

    # --------------------------------------------------------
    # GeoDataFrame des arêtes
    # --------------------------------------------------------

    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G_tagged)

    edges = edges_gdf.reset_index().copy()

    edges["pair"] = edges.apply(
        lambda r: tuple(sorted((r["u"], r["v"]))),
        axis=1,
    )

    edges["deg_u"] = edges["u"].map(degree)
    edges["deg_v"] = edges["v"].map(degree)

    edges["is_bridge"] = (
        edges["pair"].isin(bridges)
    )

    # --------------------------------------------------------
    # Détection des connecteurs
    # --------------------------------------------------------

    edges["is_connector"] = (
        (edges["length"] < connector_length_m)
        & (edges["deg_u"] >= min_degree)
        & (edges["deg_v"] >= min_degree)
        & (~edges["is_bridge"])
    )

    edges["mandatory_cover"] = (
        ~edges["is_connector"]
    )

    # --------------------------------------------------------
    # Réinjection dans le graphe
    # --------------------------------------------------------

    for _, row in edges.iterrows():

        u = row["u"]
        v = row["v"]
        k = row["key"]

        G_tagged[u][v][k]["is_bridge"] = bool(
            row["is_bridge"]
        )

        G_tagged[u][v][k]["is_connector"] = bool(
            row["is_connector"]
        )

        G_tagged[u][v][k]["mandatory_cover"] = bool(
            row["mandatory_cover"]
        )

    # --------------------------------------------------------
    # Retour
    # --------------------------------------------------------

    edges_gdf = edges.set_index(
        ["u", "v", "key"]
    )

    return G_tagged, nodes_gdf, edges_gdf
