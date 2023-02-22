import folium
import osmnx as ox
import Util


def visualize_map():
    m = folium.Map(location=[55.71629, 9.5319778], zoom_start=17)
    return m


def visualize_shortest_path(path):
    middleOfList = path[int(len(path) / 2)]

    sw = max(path, key=lambda x: x[0])
    ne = min(path, key=lambda x: x[0])

    map = folium.Map(location=middleOfList)
    map.fit_bounds([sw, ne])

    folium.PolyLine(path, color="red", weight=2.5, opacity=1).add_to(map)




    return map

  #  G = ox.graph_from_xml(testPath)
  #
  #  gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
  #
  #  G = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)
  # fig, ax = ox.plot_graph(G, node_size=10, node_zorder=0, edge_linewidth=0.5, edge_color='white', show=False, close=False)
  # fig.show()