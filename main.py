import xml.etree.ElementTree as ET

import geopandas as gpd

import Util


def noteTest():
    tree = ET.parse('Data/malta-latest.osm')
    root = tree.getroot()
    nodeDict = {
    }


    ##Find nodes with tag = highway
    for child in root:
        if child.tag == 'node':
            for tag in child:
                if tag.attrib['k'] == 'highway':
                    nodeDict[child.attrib['id']] = child.attrib['lat'] + ',' + child.attrib['lon']
                    break

    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    print(f"{type(df_world)}, {df_world.geometry.name}")

def plotTest():
    df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    print(df_world.geometry.geom_type.value_counts())
    #df_world.plot(figsize=(10, 6))
    df_world.head()
    df_world.plot()


def findNode(ref, root):
    for child in root:
        if child.tag == 'node':
            if child.attrib['id'] == ref:
                return child.attrib['id'], child.attrib['lat'], child.attrib['lon']


if __name__ == '__main__':
    tree = ET.parse('Data/map_2.osm')
    root = tree.getroot()

    graph = Util.Graph()

    ##Her går vi ind og finder alle noder som ligger på en way med tag highway
    for child in root:
        if child.tag == 'way':
            if child.find('./tag[@k="highway"]') is not None:
                #print("Number of references: " + str(len(child.find('/tag[@k="highway"]'))))
                refCount = 0
                numOfRefs = len(child.findall('./nd'))
                prevId = prevLat = prevLon = None
                for index, ng in enumerate(child.findall('./nd')):
                    id, lat, lon = findNode(ng.attrib['ref'], root)
                    graph.addNode(id, lat, lon)
                    # Alt større end nul og mindre end numOfRefs tilføjer sig selv til listen af noder og sætter sig selv ind i prev, og sætter prev til sig selv
                    if 0 < index < numOfRefs:
                        graph.addEdge(prevId, prevLat, prevLon, ng.attrib['ref'], lat, lon)
                        graph.addEdge(ng.attrib['ref'], lat, lon, prevId, prevLat, prevLon)
                    prevId = ng.attrib['ref']
                    prevLat = lat
                    prevLon = lon
                    refCount += 1






    ##Print every node in graph and its adjacent nodes
    for node in graph.nodeList:
        print("Node id", node, "has adjacent nodes with ID: ", )

    print("test print: ", graph.getNode('6996546298'))








