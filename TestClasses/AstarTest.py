import unittest
from ShortestPathAlgos import AStar
import Util.Graphs as Graphs


class AstarTest(unittest.TestCase):

    def test_astar(self):
        # Test that the A* implementation returns the expected path
        # for a simple graph

        graph = Graphs.DiGraph()

        graph.addNode(0, 0, 8)
        graph.addNode(1, 2, 11)
        graph.addNode(2, 3, 8)
        graph.addNode(3, 4, 12)
        graph.addNode(4, 4, 4)
        graph.addNode(5, 1, 3)
        graph.addNode(6, 6, 1)
        graph.addNode(7, 7, 6)
        graph.addNode(8, 9, 5)
        graph.addNode(9, 12, 4)
        graph.addNode(10, 12, 8)
        graph.addNode(11, 12, 11)
        graph.addNode(12, 12, 14)
        graph.addNode(13, 14, 13)
        graph.addNode(14, 15, 12)
        graph.addNode(15, 16, 8)

        # Add edges
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 5)
        graph.nodeList[0].addNeighbor(graph.nodeList[2], 5)
        graph.nodeList[1].addNeighbor(graph.nodeList[0], 5)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 4)
        graph.nodeList[1].addNeighbor(graph.nodeList[3], 3)
        graph.nodeList[2].addNeighbor(graph.nodeList[0], 5)
        graph.nodeList[2].addNeighbor(graph.nodeList[1], 4)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 7)
        graph.nodeList[2].addNeighbor(graph.nodeList[4], 7)
        graph.nodeList[2].addNeighbor(graph.nodeList[7], 8)
        graph.nodeList[3].addNeighbor(graph.nodeList[1], 3)
        graph.nodeList[3].addNeighbor(graph.nodeList[2], 7)
        graph.nodeList[3].addNeighbor(graph.nodeList[7], 11)
        graph.nodeList[3].addNeighbor(graph.nodeList[10], 16)
        graph.nodeList[3].addNeighbor(graph.nodeList[11], 13)
        graph.nodeList[3].addNeighbor(graph.nodeList[12], 14)
        graph.nodeList[4].addNeighbor(graph.nodeList[2], 7)
        graph.nodeList[4].addNeighbor(graph.nodeList[5], 5)
        graph.nodeList[4].addNeighbor(graph.nodeList[7], 5)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 4)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 9)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 9)
        graph.nodeList[6].addNeighbor(graph.nodeList[13], 12)
        graph.nodeList[7].addNeighbor(graph.nodeList[2], 8)
        graph.nodeList[7].addNeighbor(graph.nodeList[3], 11)
        graph.nodeList[7].addNeighbor(graph.nodeList[4], 5)
        graph.nodeList[7].addNeighbor(graph.nodeList[8], 3)
        graph.nodeList[8].addNeighbor(graph.nodeList[7], 3)
        graph.nodeList[8].addNeighbor(graph.nodeList[9], 4)
        graph.nodeList[9].addNeighbor(graph.nodeList[8], 4)
        graph.nodeList[9].addNeighbor(graph.nodeList[13], 3)
        graph.nodeList[9].addNeighbor(graph.nodeList[15], 8)
        graph.nodeList[10].addNeighbor(graph.nodeList[3], 16)
        graph.nodeList[10].addNeighbor(graph.nodeList[11], 5)
        graph.nodeList[10].addNeighbor(graph.nodeList[13], 7)
        graph.nodeList[10].addNeighbor(graph.nodeList[15], 4)
        graph.nodeList[11].addNeighbor(graph.nodeList[3], 13)
        graph.nodeList[11].addNeighbor(graph.nodeList[10], 5)
        graph.nodeList[11].addNeighbor(graph.nodeList[12], 9)
        graph.nodeList[11].addNeighbor(graph.nodeList[14], 4)
        graph.nodeList[12].addNeighbor(graph.nodeList[3], 14)
        graph.nodeList[12].addNeighbor(graph.nodeList[11], 9)
        graph.nodeList[12].addNeighbor(graph.nodeList[14], 5)
        graph.nodeList[13].addNeighbor(graph.nodeList[6], 12)
        graph.nodeList[13].addNeighbor(graph.nodeList[9], 3)
        graph.nodeList[13].addNeighbor(graph.nodeList[10], 7)
        graph.nodeList[13].addNeighbor(graph.nodeList[15], 7)
        graph.nodeList[14].addNeighbor(graph.nodeList[11], 4)
        graph.nodeList[14].addNeighbor(graph.nodeList[12], 5)
        graph.nodeList[15].addNeighbor(graph.nodeList[9], 8)
        graph.nodeList[15].addNeighbor(graph.nodeList[10], 4)
        graph.nodeList[15].addNeighbor(graph.nodeList[13], 7)

        path = AStar.aStar(graph, graph.nodeList[0], graph.nodeList[15], "grid")

        pathWeight = 0
        for i in range(len(path) - 1):
            pathWeight += graph.getWeight(path[i].id, path[i + 1].id)

        #Check if the path mathces: 0, 5, 9, 12, 13, 17, 18, 19
        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 2)
        self.assertEqual(path[2].id, 7)
        self.assertEqual(path[3].id, 8)
        self.assertEqual(path[4].id, 9)
        self.assertEqual(path[5].id, 15)

        #Check if the path weight is correct
        self.assertEqual(pathWeight, 28)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
