import unittest
from ShortestPathAlgos import AStar

import Util


class AstarTest(unittest.TestCase):

    def test_astar(self):
        # Test that the A* implementation returns the expected path
        # for a simple graph

        graph = Util.Graph()

        # Create 32 nodes, resemples a 4x8 grid
        for i in range(20):
            graph.addNode(i, 0, 0)


        # Create a directed graph
        digraph = Util.DiGraph(graph)

        # Create edges
        digraph.nodeList[0].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[0].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[0].addNeighbor(digraph.nodeList[4], 1)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[5], 1)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[4], 1)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[3], 1)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[7], 1)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[5], 1)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[8], 1)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[7], 1)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[5], 1)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[0], 1)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[0], 1)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[4], 1)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[7], 1)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[3], 1)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[1], 1)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[5], 1)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[8], 1)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[3], 1)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[2], 1)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[8].addNeighbor(digraph.nodeList[7], 1)
        digraph.nodeList[8].addNeighbor(digraph.nodeList[3], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[5], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[6], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[7], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[10], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[11], 1)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[12], 1)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[9], 1)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[11], 1)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[12], 1)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[9], 1)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[10], 1)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[13], 1)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[9], 1)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[11], 1)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[14], 1)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[12], 1)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[17], 1)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[15], 1)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[13], 1)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[18], 1)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[17], 1)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[16], 1)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[14], 1)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[19], 1)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[18], 1)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[17], 1)
        digraph.nodeList[16].addNeighbor(digraph.nodeList[15], 1)
        digraph.nodeList[16].addNeighbor(digraph.nodeList[19], 1)
        digraph.nodeList[16].addNeighbor(digraph.nodeList[18], 1)
        digraph.nodeList[17].addNeighbor(digraph.nodeList[18], 1)
        digraph.nodeList[17].addNeighbor(digraph.nodeList[13], 1)
        digraph.nodeList[17].addNeighbor(digraph.nodeList[14], 1)
        digraph.nodeList[17].addNeighbor(digraph.nodeList[15], 1)
        digraph.nodeList[18].addNeighbor(digraph.nodeList[19], 1)
        digraph.nodeList[18].addNeighbor(digraph.nodeList[17], 1)
        digraph.nodeList[18].addNeighbor(digraph.nodeList[14], 1)
        digraph.nodeList[18].addNeighbor(digraph.nodeList[15], 1)
        digraph.nodeList[18].addNeighbor(digraph.nodeList[16], 1)
        digraph.nodeList[19].addNeighbor(digraph.nodeList[18], 1)
        digraph.nodeList[19].addNeighbor(digraph.nodeList[15], 1)
        digraph.nodeList[19].addNeighbor(digraph.nodeList[16], 1)


        path = AStar.astar(digraph.nodeList[0], digraph.nodeList[19])

        pathWeight = 0
        for i in range(len(path) - 1):
            pathWeight += digraph.getWeight(path[i].id, path[i + 1].id)

        #Check if the path mathces: 0, 5, 9, 12, 13, 17, 18, 19
        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 5)
        self.assertEqual(path[2].id, 9)
        self.assertEqual(path[3].id, 12)
        self.assertEqual(path[4].id, 13)
        self.assertEqual(path[5].id, 17)
        self.assertEqual(path[6].id, 18)
        self.assertEqual(path[7].id, 19)

        #Check if the path weight is correct
        self.assertEqual(pathWeight, 8)






def main():
    unittest.main()

if __name__ == '__main__':
    main()
