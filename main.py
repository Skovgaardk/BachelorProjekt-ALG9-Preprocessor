import xml.etree.ElementTree as ET

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


def printDiGraph(graph):
    diGraph = Util.DiGraph(graph)

    for node in diGraph.nodeList:
        neighbors = diGraph.getNode(node).getNeighbors()
        # Prints the id of the node and the id of the adjacent nodes with its corresponding weight
        for neighbor in neighbors:
            neighborIds = []
            neighborIds.append(neighbor.getId())
            print("Node id", node, "has adjacent nodes with ID: ", neighborIds, "and weight: ", diGraph.getNode(node).adjacent[neighbor])


if __name__ == '__main__':
    tree = ET.parse('Data/map_2.osm')
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

    printDiGraph(graph)
