import numpy as np
from math import sin, cos, sqrt, atan2, radians
import Util.Nodes as Nodes

class Graph:
    def __init__(self):
        self.nodeList = {}


    def addNode(self, id, lat, lon):
        if id in self.nodeList:
            return self.nodeList[id]
        newNode = Nodes.Node(id, lat, lon)
        self.nodeList[id] = newNode
        return newNode

    def getNode(self, n):
        if n in self.nodeList:
            return self.nodeList[n]
        else:
            return None

    def addEdge(self, fromId, fromlat, fromlon, toid, tolat, tolon, cost=0):
        if fromId not in self.nodeList:
            self.addNode(fromId, fromlat, fromlon)
        if toid not in self.nodeList:
            self.addNode(toid, tolat, tolon)

        self.nodeList[fromId].addNeighbor(self.nodeList[toid], cost)

    def getNodes(self):
        return self.nodeList.keys()

    def __iter__(self):
        return iter(self.nodeList.values())


class DiGraph:
    def __init__(self):
        self.nodeList = {}

    def getNodes(self):
        return self.nodeList.keys()

    def getNode(self, n):
        if n in self.nodeList:
            return self.nodeList[n]
        else:
            return None

    def addNode(self, id, lat, lon):
        if id in self.nodeList:
            return self.nodeList[id]
        newNode = Nodes.Node(id, lat, lon)
        self.nodeList[id] = newNode
        return newNode

    def addEdge(self, fromId, fromlat, fromlon, toid, tolat, tolon, cost=0):
        if fromId not in self.nodeList:
            self.addNode(fromId, fromlat, fromlon)
        if toid not in self.nodeList:
            self.addNode(toid, tolat, tolon)

        self.nodeList[fromId].addNeighbor(self.nodeList[toid], cost)

    def getWeight(self, fromId, toId):
        return self.nodeList[fromId].adjacent[self.nodeList[toId]]

    def calculateDistance(self, lat1, lon1, lat2, lon2):
        # Here we use the Haversine formula to calculate the distance between two points
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 *atan2(sqrt(a), sqrt(1-a))

        return R * c

    def calculateWeights(self):
        for node in self.nodeList:
            neighbors = self.nodeList[node].getNeighbors()
            # Updates node's adjacent dictionary with distance as weight
            for neighbor in neighbors:
                neighborLat, neighborLon = neighbor.lat, neighbor.lon
                nodeLat, nodeLon = self.nodeList[node].lat, self.nodeList[node].lon
                distance = self.calculateDistance(nodeLat, nodeLon, neighborLat, neighborLon)
                self.nodeList[node].adjacent[neighbor] = distance


def printDiGraph(diGraph):
    for node in diGraph.nodeList:
        neighbors = diGraph.getNode(node).getNeighbors()
        # Prints the id of the node and the id of the adjacent nodes with its corresponding weight
        lat, lon = diGraph.getNode(node).lat, diGraph.getNode(node).lon
        print("Node: ", node, "Lat: ", lat, "Lon: ", lon, "has neighbors: ")
        for neighbor in neighbors:
            neighborIds = [neighbor.id]
            neighborWeights = [diGraph.getNode(node).adjacent[neighbor]]
            print("Neighbor: ", neighborIds, "Weight: ", neighborWeights)