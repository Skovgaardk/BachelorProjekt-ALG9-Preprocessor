import webbrowser

import folium


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

def visualize_path(path):

    pathLatLon = []
    for node in path:
        pathLatLon.append([node.lat, node.lon])

    map = visualize_shortest_path(pathLatLon)
    map.render()
    map.save("latestPath.html")
    webbrowser.open("latestPath.html")


