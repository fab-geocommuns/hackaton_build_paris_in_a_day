from data.voirie import get_voirie
from data.filter import filter_impasses
from data.connectors import tag_connectors


def main():
    print("Lancement de la pipeline des données")
    print("Récupérer les voies cyclables de Paris via OSM")
    G = get_voirie()
    print("Filtrer les petites impasses")
    G_propre = filter_impasses(G)
    print("Détecter les tronçons de connection de voies")
    G_tagged, nodes_gdf, edges_gdf = tag_connectors(
        G_propre,
        connector_length_m=12,
        min_degree=3,
    )


if __name__ == "__main__":
    main()
