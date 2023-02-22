import os.path
import pickle
import xml.etree.ElementTree as ET

import osmnx as ox
import Util
import XMLhandlers
from ShortestPathAlgos import Dijkstra


VejleMapPath = 'data/map_2.osm'
Vejle2MapPath = 'data/Vejlev2.osm'
MaltaMapPath = 'data/malta-latest.osm'

def printGraph(graph):
    for node in graph.nodeList:
        neighbors = graph.getNode(node).getNeighbors()
        neighborIds = []
        for neighbor in neighbors:
            neighborIds.append(neighbor.id)
        print("Node id", node, "has adjacent nodes with ID: ", neighborIds)


def printDiGraph(diGraph):
    for node in diGraph.nodeList:
        neighbors = diGraph.getNode(node).getNeighbors()
        # Prints the id of the node and the id of the adjacent nodes with its corresponding weight
        lat, lon = diGraph.getNode(node).lat, diGraph.getNode(node).lon
        print("Node id", node, "with latlon: ", lat, lon,  " and has adjacent nodes with ID: ")
        for neighbor in neighbors:
            neighborIds = [neighbor.id]
            print(neighborIds, "with weight: ", diGraph.getWeight(node, neighbor.id))

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

def newParseXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    graph = Util.Graph()

    nodes = {}
    for node in root.findall('./node'):
        id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[id] = (lat, lon)


    for child in root:
        if child.tag == 'way':
            refCount = 0
            refs = [ng.attrib['ref'] for ng in child.findall('./nd')]
            numOfRefs = len(refs)
            prevId, prevLat, prevLon = None, None, None


            for index, ref in enumerate(refs):
                onewayTag = child.find('./tag[@k="oneway"]')
                isOneway = onewayTag is not None and onewayTag.attrib['v'] == 'yes'

                highwayTag = child.find('./tag[@k="highway"]')
                isMotorWay = highwayTag is not None and highwayTag.attrib['v'] == 'motorway'

                junctionTag = child.find('./tag[@k="junction"]')
                isRoundAbout = junctionTag is not None and junctionTag.attrib['v'] == 'roundabout'

                if isOneway or isMotorWay or isRoundAbout:
                    lat, lon = nodes[ref]
                    print("Added node " + ref)
                    graph.addNode(ref, lat, lon)
                    if 0 < index < numOfRefs:
                        graph.addEdge(prevId, prevLat, prevLon, ref, lat, lon)
                    prevId = ref
                    prevLat = lat
                    prevLon = lon
                    refCount += 1
                else:
                    lat, lon = nodes[ref]
                    print("Added node " + ref)
                    graph.addNode(ref, lat, lon)
                    # Alt større end nul og mindre end numOfRefs tilføjer sig selv til listen af noder og sætter
                    # sig selv ind i prev, og sætter prev til sig selv
                    if 0 < index < numOfRefs:
                        graph.addEdge(prevId, prevLat, prevLon, ref, lat, lon)
                        graph.addEdge(ref, lat, lon, prevId, prevLat, prevLon)
                    prevId = ref
                    prevLat = lat
                    prevLon = lon
                    refCount += 1

    return graph


if __name__ == '__main__':

    print("Starting program")

    mapToUse = MaltaMapPath
    testPath = 'data/map_2_TEST.osm'

    print("Starting to handle streets")
    wayHandler = XMLhandlers.StreetHandler()
    print("Starting to handle nodes")
    nodeHandler = XMLhandlers.NodeHandler()
    print("Starting to apply ways")
    wayHandler.apply_file(mapToUse)
    print("Starting to apply nodes")
    nodeHandler.apply_file(mapToUse)

    print("Creating new XML file")
    if os.path.exists(testPath):
        os.remove(testPath)

    print("Starting to write to new XML file")
    writer = XMLhandlers.wayWriter(testPath)
    print("Starting to apply new XML file")
    writer.apply_file(mapToUse)
    print("Closing writer")
    writer.close()

    print("Starting to parse new XML file")
    graph1 = newParseXml(testPath)

    print("Starting to create DIgraph")
    diGraph = Util.DiGraph(graph1)

    printDiGraph(diGraph)

    # path = Dijkstra.dijkstra(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'])
    # print("Shortest path: ")
    # pathLatLon = []
    # for node in path:
    #     print("Node: ", node.id, " with latlon: ", node.lat, node.lon, " and distance: ", node._distance)
    #     pathLatLon.append([node.lat, node.lon])
    #
    # dist = path[-1]._distance
    #
    # print("Weight of path: ", dist)
    #
    #
    # map = Visualize.visualize_shortest_path(pathLatLon)
    # map.show_in_browser()








