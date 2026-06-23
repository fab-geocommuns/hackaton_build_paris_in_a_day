from data.voirie import get_voirie
from data.filter import filter_impasses
from data.connectors import tag_connectors


def main():
    G = get_voirie()
    G_propre = filter_impasses(G)
    G_tagged, nodes_gdf, edges_gdf = tag_connectors(
        G_propre,
        connector_length_m=12,
        min_degree=3,
    )


if __name__ == "__main__":
    main()
