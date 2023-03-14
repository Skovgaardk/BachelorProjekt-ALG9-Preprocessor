import unittest

import Util
from ShortestPathAlgos import Dijkstra



class DijkstraTest(unittest.TestCase):

    def test_dijkstra(self):

        #The test case can be found on https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

        # Create some test nodes and edges to test the Dijkstra algorithm
        Graph = Util.Graph()
        # create 9 nodes
        for i in range(9):
            Graph.addNode(i, 0, 0)

        # create a directed graph
        DiGraph = Util.DiGraph(Graph)

        # create 14 edges, every edge is added twice, once for each direction, exept for the edges from node 0 to 1 and 7
        DiGraph.nodeList[0].addNeighbor(DiGraph.nodeList[1], 4)
        DiGraph.nodeList[0].addNeighbor(DiGraph.nodeList[7], 8)
        DiGraph.nodeList[1].addNeighbor(DiGraph.nodeList[2], 8)
        DiGraph.nodeList[1].addNeighbor(DiGraph.nodeList[7], 11)
        DiGraph.nodeList[2].addNeighbor(DiGraph.nodeList[3], 7)
        DiGraph.nodeList[2].addNeighbor(DiGraph.nodeList[8], 2)
        DiGraph.nodeList[2].addNeighbor(DiGraph.nodeList[5], 4)
        DiGraph.nodeList[3].addNeighbor(DiGraph.nodeList[4], 9)
        DiGraph.nodeList[3].addNeighbor(DiGraph.nodeList[5], 14)
        DiGraph.nodeList[5].addNeighbor(DiGraph.nodeList[6], 2)
        DiGraph.nodeList[6].addNeighbor(DiGraph.nodeList[7], 1)
        DiGraph.nodeList[6].addNeighbor(DiGraph.nodeList[8], 6)
        DiGraph.nodeList[7].addNeighbor(DiGraph.nodeList[8], 7)
        DiGraph.nodeList[7].addNeighbor(DiGraph.nodeList[1], 11)
        DiGraph.nodeList[2].addNeighbor(DiGraph.nodeList[1], 8)
        DiGraph.nodeList[8].addNeighbor(DiGraph.nodeList[2], 2)
        DiGraph.nodeList[8].addNeighbor(DiGraph.nodeList[6], 6)
        DiGraph.nodeList[7].addNeighbor(DiGraph.nodeList[6], 1)
        DiGraph.nodeList[6].addNeighbor(DiGraph.nodeList[5], 2)
        DiGraph.nodeList[5].addNeighbor(DiGraph.nodeList[4], 10)
        DiGraph.nodeList[8].addNeighbor(DiGraph.nodeList[7], 7)
        DiGraph.nodeList[5].addNeighbor(DiGraph.nodeList[2], 4)
        DiGraph.nodeList[5].addNeighbor(DiGraph.nodeList[3], 14)
        DiGraph.nodeList[3].addNeighbor(DiGraph.nodeList[2], 7)

        # test the Dijkstra algorithm
        path = Dijkstra.dijkstra(DiGraph, DiGraph.nodeList[0], DiGraph.nodeList[4])

        pathWeight = 0
        for i in range(len(path) - 1):
            pathWeight += DiGraph.getWeight(path[i].id, path[i + 1].id)

        # check if the path is correct
        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 7)
        self.assertEqual(path[2].id, 6)
        self.assertEqual(path[3].id, 5)
        self.assertEqual(path[4].id, 4)
        self.assertEqual(pathWeight, 21)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
