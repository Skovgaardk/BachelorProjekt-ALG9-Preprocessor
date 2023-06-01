import webbrowser
import folium
import matplotlib.pyplot as plt
import mpl_toolkits.basemap as bm



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

def plot_points(path, visited):

    lats = []
    lons = []
    for node in visited:
        lats.append(node.lat)
        lons.append(node.lon)

    pathLats = []
    pathLons = []
    for node in path:
        pathLats.append(node.lat)
        pathLons.append(node.lon)


    centerLat = sum(lats) / len(lats)
    centerLon = sum(lons) / len(lons)

    m = bm.Basemap(projection='merc', llcrnrlon=13.375, llcrnrlat=34.5, urcrnrlon=15.25, urcrnrlat=36.5, resolution='h', lat_0=centerLat, lon_0=centerLon)

    malta_lat, malta_lon = 35.9375, 14.3754
    malta_x, malta_y = m(malta_lon, malta_lat)

    m.plot(malta_x, malta_y, 'ro', markersize=6)

    m.drawcoastlines(linewidth=0.5)
    m.drawcounties(linewidth=0.5)
    m.drawrivers(linewidth=0.5)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='white',lake_color='#68b1ed')

    m.scatter(lons, lats, latlon=True, s=1, c='red', marker='o', alpha=1)

    m.scatter(pathLons, pathLats, latlon=True, s=1, c='blue', marker='o', alpha=1)

    #Kan også scatter ens path med en anden farve

    plt.show()
