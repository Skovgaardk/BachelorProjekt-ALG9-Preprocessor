

class Node:
    def __init__(self, node):
        self.id = node.attrib['id']
        self.lat = node.attrib['lat']
        self.lon = node.attrib['lon']
        self.adjacent = {}
        self.distance = 0
        self.visited = False
        self.previous = None
        self.priority = 0
        self.heuristic = 0

    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def getNeighbors(self):
        return self.adjacent.keys()

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.nodeList = {}
        self.numNodes = 0

    def addNode(self, node):
        self.numNodes = self.numNodes + 1
        newNode = Node(node)
        self.nodeList[node.attrib['id']] = newNode
        return newNode

    def getNode(self, n):
        if n in self.nodeList:
            return self.nodeList[n]
        else:
            return None

    def addEdge(self, frm, to, cost=0):
        if frm not in self.nodeList:
            self.addNode(frm)
        if to not in self.nodeList:
            self.addNode(to)

        self.nodeList[frm].addNeighbor(self.nodeList[to], cost)

    def getNodes(self):
        return self.nodeList.keys()

    def __iter__(self):
        return iter(self.nodeList.values())

    def __str__(self):
        return str(self.nodeList)