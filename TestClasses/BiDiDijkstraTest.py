import unittest

from ShortestPathAlgos import BiDiDijstra
import Util.Graphs as Graphs



class DijkstraTest(unittest.TestCase):

    def test_dijkstra(self):

        #The test case can be found on https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

        # Create some test nodes and edges to test the Dijkstra algorithm
        graph = Graphs.DiGraph()
        # create 9 nodes
        for i in range(9):
            graph.addNode(i, 0, 0)


        # create 14 edges, every edge is added twice, once for each direction, exept for the edges from node 0 to 1 and 7
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 4)
        graph.nodeList[0].addNeighbor(graph.nodeList[7], 8)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 8)
        graph.nodeList[1].addNeighbor(graph.nodeList[7], 11)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 7)
        graph.nodeList[2].addNeighbor(graph.nodeList[8], 2)
        graph.nodeList[2].addNeighbor(graph.nodeList[5], 4)
        graph.nodeList[3].addNeighbor(graph.nodeList[4], 9)
        graph.nodeList[3].addNeighbor(graph.nodeList[5], 14)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 2)
        graph.nodeList[6].addNeighbor(graph.nodeList[7], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[8], 6)
        graph.nodeList[7].addNeighbor(graph.nodeList[8], 7)
        graph.nodeList[7].addNeighbor(graph.nodeList[1], 11)
        graph.nodeList[2].addNeighbor(graph.nodeList[1], 8)
        graph.nodeList[8].addNeighbor(graph.nodeList[2], 2)
        graph.nodeList[8].addNeighbor(graph.nodeList[6], 6)
        graph.nodeList[7].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 2)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 10)
        graph.nodeList[8].addNeighbor(graph.nodeList[7], 7)
        graph.nodeList[5].addNeighbor(graph.nodeList[2], 4)
        graph.nodeList[5].addNeighbor(graph.nodeList[3], 14)
        graph.nodeList[3].addNeighbor(graph.nodeList[2], 7)

        # test the Dijkstra algorithm
        path = BiDiDijstra.biDiDijkstra(graph, graph.nodeList[0], graph.nodeList[4])

        print("Path: ", path)
        for node in path:
            print(node.id)

        pathWeight = 0
        for i in range(len(path) - 1):
            pathWeight += graph.getWeight(path[i].id, path[i + 1].id)

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
