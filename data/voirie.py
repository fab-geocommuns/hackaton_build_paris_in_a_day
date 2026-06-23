import osmnx as ox
from shapely.ops import unary_union


def get_paris_poly():
    # Récupérer les limites de Paris
    paris_avec_bois = ox.geocode_to_gdf(
        "Paris, France"
    )
    boulogne = ox.geocode_to_gdf("Bois de Boulogne, Paris, France")
    vincennes = ox.geocode_to_gdf("Bois de Vincennes, Paris, France")

    woods = unary_union([
        boulogne.geometry.iloc[0],
        vincennes.geometry.iloc[0],
    ])

    paris = paris_avec_bois.geometry.iloc[0].difference(woods)
    if paris.geom_type == "MultiPolygon":
        paris = max(
            paris.geoms,
            key=lambda g: g.area
        )
    return paris


def get_voirie(paris):
    G = ox.graph_from_polygon(
        paris,
        network_type="bike",
        truncate_by_edge=True
    )

    nodes, edges = ox.graph_to_gdfs(G)
    return nodes, edges
