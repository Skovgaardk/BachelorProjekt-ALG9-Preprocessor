

class Node:
    def __init__(self, id, lat, lon):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.adjacent = {}
        self.distance = 0
        self.visited = False
        self.previous = None
        self.priority = 0
        self.heuristic = 0

    def addNeighbor(self, id, weight=0):
        self.adjacent[id] = weight

    def getNeighbors(self):
        return self.adjacent.keys()

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

    def __str__(self):
        return str(self.nodeList)