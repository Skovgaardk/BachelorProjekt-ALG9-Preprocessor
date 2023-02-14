import pickle
import xml.etree.ElementTree as ET
import networkx as nx
from matplotlib import pyplot as plt
import Util


def findNode(ref, root):
    for child in root:
        if child.tag == 'node':
            if child.attrib['id'] == ref:
                return child.attrib['id'], float(child.attrib['lat']), float(child.attrib['lon'])


def printGraph(graph):
    for node in graph.nodeList:
        neighbors = graph.getNode(node).getNeighbors()
        neighborIds = []
        for neighbor in neighbors:
            neighborIds.append(neighbor.getId())
        print("Node id", node, "has adjacent nodes with ID: ", neighborIds)


def printDiGraph(diGraph):
    for node in diGraph.nodeList:
        neighbors = diGraph.getNode(node).getNeighbors()
        # Prints the id of the node and the id of the adjacent nodes with its corresponding weight
        lat, lon = diGraph.getNode(node).getLatLon()
        print("Node id", node, "with latlon: ", lat, lon,  " and has adjacent nodes with ID: ")
        for neighbor in neighbors:
            neighborIds = [neighbor.getId()]
            print(neighborIds, "with weight: ", diGraph.getWeight(node, neighbor.getId()))

def parseXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    graph = Util.Graph()

    # Her går vi ind og finder alle noder som ligger på en way med tag highway
    for child in root:
        if child.tag == 'way':
            if child.find('./tag[@k="highway"]') is not None:
                # print("Number of references: " + str(len(child.find('/tag[@k="highway"]'))))
                refCount = 0
                numOfRefs = len(child.findall('./nd'))
                prevId = prevLat = prevLon = None
                for index, ng in enumerate(child.findall('./nd')):
                    # check of road is has k="oneway" v="no"
                    isOneway = child.find('./tag[@k="oneway"]') is not None and child.find('./tag[@k="oneway"]').attrib['v'] == 'yes'
                    isMotorWay = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'motorway'
                    isRoundAbout = child.find('./tag[@k="junction"]') is not None and child.find('./tag[@k="junction"]').attrib['v'] == 'roundabout'
                    isDriveWay = child.find('./tag[@k="service"]') is not None and child.find('./tag[@k="service"]').attrib['v'] == 'driveway'
                    if isDriveWay:
                        continue
                    if isOneway or isMotorWay or isRoundAbout or isDriveWay:
                        id, lat, lon = findNode(ng.attrib['ref'], root)
                        graph.addNode(id, lat, lon)
                        if 0 < index < numOfRefs:
                            graph.addEdge(prevId, prevLat, prevLon, ng.attrib['ref'], lat, lon)
                        prevId = ng.attrib['ref']
                        prevLat = lat
                        prevLon = lon
                        refCount += 1
                    else:
                        id, lat, lon = findNode(ng.attrib['ref'], root)
                        graph.addNode(id, lat, lon)
                        # Alt større end nul og mindre end numOfRefs tilføjer sig selv til listen af noder og sætter
                        # sig selv ind i prev, og sætter prev til sig selv
                        if 0 < index < numOfRefs:
                            graph.addEdge(prevId, prevLat, prevLon, ng.attrib['ref'], lat, lon)
                            graph.addEdge(ng.attrib['ref'], lat, lon, prevId, prevLat, prevLon)
                        prevId = ng.attrib['ref']
                        prevLat = lat
                        prevLon = lon
                        refCount += 1
    return graph

def saveGraph(graph, filename):
    f = open(filename, 'wb')
    pickle.dump(graph, f)
    f.close()
    print("Graph saved to file: " + filename)

def loadGraph(filename):
    f = open(filename, 'rb')
    graph = pickle.load(f)
    f.close()
    print("Graph loaded from file: " + filename)
    return graph



if __name__ == '__main__':
    #graph = parseXml('data/map_2.osm')

    #DiGraph = Util.DiGraph(graph)

    #saveGraph(DiGraph, 'data/graph_2.pickle')

    DiGraph = loadGraph('data/graph_2.pickle')

    printDiGraph(DiGraph)

    ## Converter vores DiGraph til en networkx DiGraph
    G = nx.DiGraph()
    for node in DiGraph.nodeList:
        G.add_node(node, pos=(DiGraph.getNode(node).getLatLon()))
        neighbors = DiGraph.getNode(node).getNeighbors()
        for neighbor in neighbors:
            G.add_edge(node, neighbor.getId(), weight=DiGraph.getWeight(node, neighbor.getId()))

    ## Plotter vores DiGraph
    nx.draw_networkx(G, pos=nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=1, width=0.5, arrowsize=0.5, edge_color='black')
    plt.show()






