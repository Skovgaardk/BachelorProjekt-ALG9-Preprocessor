import unittest

import Util.Graphs
from ShortestPathAlgos import BiDiDijstra
import Util.Graphs as Graphs
import timeit



class DijkstraTest(unittest.TestCase):

    def test_dijkstra(self):

        #The test case can be found on https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

        # Create some test nodes and edges to test the Dijkstra algorithm
        graph = Graphs.DiGraph()
        # create 9 nodes
        for i in range(9):
            graph.addNode(i, 0, 0)

        # Create the 14 edges, only going from left to right
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 4)
        graph.nodeList[0].addNeighbor(graph.nodeList[7], 8)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 8)
        graph.nodeList[1].addNeighbor(graph.nodeList[7], 11)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 7)
        graph.nodeList[2].addNeighbor(graph.nodeList[8], 2)
        graph.nodeList[2].addNeighbor(graph.nodeList[5], 4)
        graph.nodeList[3].addNeighbor(graph.nodeList[4], 9)
        graph.nodeList[3].addNeighbor(graph.nodeList[5], 14)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 2)
        graph.nodeList[7].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[7].addNeighbor(graph.nodeList[8], 7)
        graph.nodeList[8].addNeighbor(graph.nodeList[6], 6)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 10)

        transposedGraph = Util.Graphs.transposeDiGraph(graph)

        # test the Dijkstra algorithm
        start = timeit.default_timer()
        path, weight, len = BiDiDijstra.biDiDijkstra(graph, transposedGraph, graph.nodeList[0], graph.nodeList[4])
        print("Time: ", (timeit.default_timer() - start)*1000)

        print("Path: ")
        for i in path:
            print(i.id)


        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 7)
        self.assertEqual(path[2].id, 6)
        self.assertEqual(path[3].id, 5)
        self.assertEqual(path[4].id, 4)
        self.assertEqual(weight, 21)

    def test_edgeCase(self):
        graph = Graphs.DiGraph()

        for i in range(3):
            graph.addNode(i, 0, 0)

        graph.nodeList[0].addNeighbor(graph.nodeList[1], 2)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 2)
        graph.nodeList[0].addNeighbor(graph.nodeList[2], 3)


        transposedGraph = Util.Graphs.transposeDiGraph(graph)

        start = timeit.default_timer()
        path, weight, len = BiDiDijstra.biDiDijkstra(graph, transposedGraph, graph.nodeList[0], graph.nodeList[2])
        print("Time: ", (timeit.default_timer() - start)*1000)

        print("Path: ")
        for i in path:
            print(i.id)

        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 2)
        self.assertEqual(weight, 3)

    def test_edgeCase2(self):
        graph = Graphs.DiGraph()

        for i in range(6):
            graph.addNode(i, 0, 0)


        graph.nodeList[0].addNeighbor(graph.nodeList[1], 2)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 2)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 2)
        graph.nodeList[3].addNeighbor(graph.nodeList[4], 2)
        graph.nodeList[0].addNeighbor(graph.nodeList[5], 3)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 3)

        transPosedGraph = Util.Graphs.transposeDiGraph(graph)

        start = timeit.default_timer()
        path, weight, len = BiDiDijstra.biDiDijkstra(graph, transPosedGraph, graph.nodeList[0], graph.nodeList[4])
        print("Time: ", (timeit.default_timer() - start)*1000)

        print("Path: ")
        for i in path:
            print(i.id)

        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 5)
        self.assertEqual(path[2].id, 4)
        self.assertEqual(weight, 6)



def main():
    unittest.main()


if __name__ == '__main__':
    main()
