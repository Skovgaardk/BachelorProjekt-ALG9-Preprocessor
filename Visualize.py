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

def plot_points(path, visited, landmarks = None):

    maxLat = float('-inf')
    minLat = float('inf')
    maxLon = float('-inf')
    minLon = float('inf')

    landmarkLat = []
    landmarkLon = []

    lats = []
    lons = []
    for node in visited:
        lats.append(node.lat)
        lons.append(node.lon)

        if node.lat > maxLat:
            maxLat = node.lat
        if node.lat < minLat:
            minLat = node.lat
        if node.lon > maxLon:
            maxLon = node.lon
        if node.lon < minLon:
            minLon = node.lon

    pathLats = []
    pathLons = []
    for node in path:
        pathLats.append(node.lat)
        pathLons.append(node.lon)

    maxLat += 1
    minLat -= 1
    maxLon += 1
    minLon -= 1



    m = bm.Basemap(projection='merc', llcrnrlon=minLon, llcrnrlat=minLat, urcrnrlon=maxLon, urcrnrlat=maxLat, resolution='h',)



    m.drawcoastlines(linewidth=0.5)
    m.drawcounties(linewidth=0.5)
    m.drawrivers(linewidth=0.5)
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='white',lake_color='#68b1ed')

    if landmarks != None:
        print("Plotting landmarks")
        for landmark in landmarks:
            landmarkLat.append(landmark.lat)
            landmarkLon.append(landmark.lon)

        m.scatter(landmarkLon, landmarkLat, latlon=True, s=25, c='purple', marker='o', alpha=1)

    m.scatter(lons, lats, latlon=True, s=1, c='red', marker='o', alpha=1)

    m.scatter(pathLons, pathLats, latlon=True, s=1, c='blue', marker='o', alpha=1)

    #Kan også scatter ens path med en anden farve

    plt.show()
