import os.path
import pickle
import time
import xml.etree.ElementTree
import xml.etree.ElementTree as ET

import mplleaflet
import networkx as nx
import osmium
from matplotlib import pyplot as plt
import osmnx as ox
import Util
import XMLhandlers


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
                    # check of road only have one direction or is a way not for vehicles
                    isOneway = child.find('./tag[@k="oneway"]') is not None and child.find('./tag[@k="oneway"]').attrib['v'] == 'yes'
                    isMotorWay = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'motorway'
                    isRoundAbout = child.find('./tag[@k="junction"]') is not None and child.find('./tag[@k="junction"]').attrib['v'] == 'roundabout'
                    isDriveWay = child.find('./tag[@k="service"]') is not None and child.find('./tag[@k="service"]').attrib['v'] == 'driveway'
                    isPedestrian = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'pedestrian'
                    isBusway = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'busway'
                    isBusguideway = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'bus_guideway'
                    isFootway = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'footway'
                    isBridleway = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'bridleway'
                    isCorridor = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'corridor'
                    isViaferrata = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'via_ferrata'
                    isCycleway = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'cycleway'
                    isProposed = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'proposed'
                    isConstruction = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'construction'
                    if isDriveWay or isPedestrian or isBusway or isBusguideway or isFootway or isBridleway or isCorridor or isViaferrata or isCycleway or isProposed or isConstruction:
                        continue
                    if isOneway or isMotorWay or isRoundAbout:
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

def createAndPrintNetworkxGraph(graph):
    G = nx.Graph()

    for node in graph.nodeList:
        G.add_node(node, pos=(graph.getNode(node).getLatLon()))
        neighbors = graph.getNode(node).getNeighbors()
        for neighbor in neighbors:
            G.add_edge(node, neighbor.getId(), weight=graph.getWeight(node, neighbor.getId()))

    #Make the networkx graph into a matplotlib plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nx.draw(G, ax=ax, with_labels=True, node_size=10, node_color='b', edge_color='r', width=0.5)

    #Make a leaflet map from the matplotlib plot
    mplleaflet.show(fig=fig)


def newParseXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    graph = Util.Graph()

    for child in root:
        if child.tag == 'way':
            refCount = 0
            numOfRefs = len(child.findall('./nd'))
            prevId, prevLat, prevLon = None, None, None

            for index, ng in enumerate(child.findall('./nd')):
                isOneway = child.find('./tag[@k="oneway"]') is not None and child.find('./tag[@k="oneway"]').attrib['v'] == 'yes'
                isMotorWay = child.find('./tag[@k="highway"]') is not None and child.find('./tag[@k="highway"]').attrib['v'] == 'motorway'
                isRoundAbout = child.find('./tag[@k="junction"]') is not None and child.find('./tag[@k="junction"]').attrib['v'] == 'roundabout'

                if isOneway or isMotorWay or isRoundAbout:
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





if __name__ == '__main__':

    print("Starting program")

    wayHandler = XMLhandlers.StreetHandler()
    nodeHandler = XMLhandlers.NodeHandler()
    boundsHandler = XMLhandlers.BoxHandler()
    boundsHandler.apply_file('data/map_2.osm')
    wayHandler.apply_file('data/map_2.osm')
    nodeHandler.apply_file('data/map_2.osm')

    if os.path.exists('data/map_2_TEST.osm'):
        os.remove('data/map_2_TEST.osm')


    writer = XMLhandlers.wayWriter('data/map_2_TEST.osm')
    writer.apply_file('data/map_2.osm')
    writer.close()

    graph = newParseXml('data/map_2_TEST.osm')

    DiGraph = Util.DiGraph(graph)

    printDiGraph(DiGraph)








    #graph = parseXml('data/map_2.osm')

    #DiGraph = Util.DiGraph(graph)

    #saveGraph(DiGraph, 'data/graph_2.pickle')

    ##graph = loadGraph('dat    for street in h.streets:

    ## Converter vores DiGraph til en networkx DiGraph

    #createAndPrintNetworkxGraph(graph)

    # Convert Digraph to networkx graph
    #G = nx.MultiDiGraph()
    ##G = ox.graph_from_xml('data/map_2.osm')


    #for node in graph.nodeList:
    #    G.add_node(node, pos=(graph.getNode(node).getLatLon()))
    #    neighbors = graph.getNode(node).getNeighbors()
    #    for neighbor in neighbors:
    #        G.add_edge(node, neighbor.getId(), weight=graph.getWeight(node, neighbor.getId()))


    # Convert networkx graph to GeoPandas GeoDataFrame

    ##gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    ##G = ox.graph_from_gdfs(gdf_nodes, gdf_edges, graph_attrs=G.graph)

    ##fig, ax = ox.plot_graph(G, node_size=1, node_zorder=3, edge_linewidth=0.5, edge_color='white', show=False, close=False)
    ##fig.show()

    # Plot the GeoDataFrame
    #fig, ax = ox.plot_graph(gdf, node_size=0, edge_linewidth=0.5, edge_color='black', show=False, close=False)
    #plt.show()





