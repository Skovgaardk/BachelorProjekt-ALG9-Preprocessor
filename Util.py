import numpy as np
from math import sin, cos, sqrt, atan2, radians


class Node:
    def __init__(self, id, lat, lon):
        self._id = id
        self._lat = lat
        self._lon = lon
        self.adjacent = {}
        self._distance = 0
        self.visited = False
        self._previous = None
        self.priority = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, lat):
        self._lat = lat

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, lon):
        self._lon = lon

    def addNeighbor(self, id, weight):
        self.adjacent[id] = weight

    def getNeighbors(self):
        return self.adjacent.keys()

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        self._distance = distance

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, previous):
        self._previous = previous

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])



class Graph:
    def __init__(self):
        self.nodeList = {}
        self.numNodes = 0

    def addNode(self, id, lat, lon):
        if id in self.nodeList:
            return self.nodeList[id]
        self.numNodes = self.numNodes + 1
        newNode = Node(id, lat, lon)
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
    def __init__(self, graph):
        self.nodeList = graph.nodeList
        self.numNodes = graph.numNodes
        self.calculateWeights()

    def getNodes(self):
        return self.nodeList.keys()

    def getNode(self, n):
        if n in self.nodeList:
            return self.nodeList[n]
        else:
            return None

    def getWeight(self, fromId, toId):
        return self.nodeList[fromId].adjacent[self.nodeList[toId]]

    def calculateDistance(self, lat1, lon1, lat2, lon2):
        # Here we use the Haversine formula to calculate the distance between two points
        R = 6373.0

        print("Calculating distance between: ", lat1, lon1, lat2, lon2)

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



















