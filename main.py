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



if __name__ == '__main__':
    tree = ET.parse('Data/malta-latest.osm')
    root = tree.getroot()

    graph = Util.Graph()

    # for node in root.findall('./node'):
    #     if node.find('tag[@k="highway"]') is not None:
    #         graph.addNode(node)
    #
    # for way in root.findall('./way'):
    #     if way.find('tag[@k="highway"]') is not None:
    #         for nd in way.findall('./nd'):
    #             graph.addEdge(way[0].attrib['ref'], nd.attrib['ref'])

    for child in root:
        if child.tag == 'node':
            for tag in child:
                if tag.attrib['k'] == 'highway':
                    graph.addNode(child)
                    break
        if child.tag == 'way':
            for tag in child:
                try:
                    if tag.attrib['k'] == 'highway':
                        for child2 in child.findall('./nd'):
                            print("Found way with highway tag, printing refs")
                            print("Child id: " + child.attrib['id'])
                            childId = child.attrib['id']
                            refcount = 0
                            ## Iterate over attributes of refs
                            for etELlerAndet in child.findall('./nd'):
                                print("Reference number: " + str(refcount) + " ref: " + etELlerAndet.attrib['ref'])
                                print("Adding edge from " + child.attrib['id'] + " to " + etELlerAndet.attrib['ref'])
                                graph.addEdge(child, etELlerAndet)
                                refcount += 1


                            # for etELlerAndet in child:
                            #     print("Reference number: " + str(refcount) + " ref: " + etELlerAndet.attrib['ref'])
                            #     print("Adding edge from " + child.attrib['id'] + " to " + etELlerAndet.attrib['ref'])
                            #     graph.addEdge(child, etELlerAndet)
                            #     refcount += 1

                        break
                except KeyError:
                    pass

    for node in graph.getNodes():
        print(node, graph.getNode(node).adjacent)











