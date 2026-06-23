import osmnx as ox
from shapely.ops import unary_union
import geopandas as gpd
from shapely.geometry import Point


def get_voirie_buffer(
    place="Paris, France",
    radius_m=1000,
    network_type="bike",
    crs_proj=2154
):

    """
    Graphe OSM sur intersection :
    (buffer autour du centroid du polygone) ∩ polygone
    """

    # 1. polygone de référence
    poly = get_poly(place)
    # 2. centroid du polygone
    centroid = poly.centroid

    gdf_centroid = gpd.GeoDataFrame(
        geometry=[centroid],
        crs="EPSG:4326"
    )

    # 3. projection métrique
    gdf_proj = gdf_centroid.to_crs(epsg=crs_proj)

    # 4. buffer en mètres
    buffer_proj = gdf_proj.buffer(radius_m).iloc[0]

    # 5. reprojection buffer en WGS84
    buffer = gpd.GeoSeries([buffer_proj], crs=crs_proj).to_crs(epsg=4326).iloc[0]

    # 6. intersection buffer ∩ polygone
    clipped_region = poly.intersection(buffer)

    # sécurité géométrique
    if clipped_region.is_empty:
        raise ValueError("Intersection vide : augmenter le rayon du buffer.")

    # 7. graphe OSM sur zone réduite
    G = ox.graph_from_polygon(
        clipped_region,
        network_type=network_type,
        simplify=True,
        truncate_by_edge=True
    )
    return G
    
def get_poly(place="Paris, France"):
    poly = ox.geocode_to_gdf(place)

    if place == "Paris, France":
        paris_avec_bois = poly.copy()
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

    else:
        return poly.geometry.iloc[0]


def get_voirie(place="Paris, France"):
    poly = get_poly(place)

    G = ox.graph_from_polygon(
        poly,
        network_type="bike",
        truncate_by_edge=True
    )

    # nodes, edges = ox.graph_to_gdfs(G)
    return G
