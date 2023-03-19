import unittest
from ShortestPathAlgos import AStar

import Util


class AstarTest(unittest.TestCase):

    def test_astar(self):
        # Test that the A* implementation returns the expected path
        # for a simple graph

        graph = Util.Graph()

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


        # Create a directed graph
        digraph = Util.DiGraph(graph)

        # Create edges

        digraph.nodeList[0].addNeighbor(digraph.nodeList[1], 5)
        digraph.nodeList[0].addNeighbor(digraph.nodeList[2], 5)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[0], 5)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[2], 4)
        digraph.nodeList[1].addNeighbor(digraph.nodeList[3], 3)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[0], 5)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[1], 4)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[3], 7)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[4], 7)
        digraph.nodeList[2].addNeighbor(digraph.nodeList[7], 8)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[1], 3)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[2], 7)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[7], 11)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[10], 16)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[11], 13)
        digraph.nodeList[3].addNeighbor(digraph.nodeList[12], 14)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[2], 7)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[5], 5)
        digraph.nodeList[4].addNeighbor(digraph.nodeList[7], 5)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[4], 4)
        digraph.nodeList[5].addNeighbor(digraph.nodeList[6], 9)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[5], 9)
        digraph.nodeList[6].addNeighbor(digraph.nodeList[13], 12)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[2], 8)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[3], 11)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[4], 5)
        digraph.nodeList[7].addNeighbor(digraph.nodeList[8], 3)
        digraph.nodeList[8].addNeighbor(digraph.nodeList[7], 3)
        digraph.nodeList[8].addNeighbor(digraph.nodeList[9], 4)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[8], 4)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[13], 3)
        digraph.nodeList[9].addNeighbor(digraph.nodeList[15], 8)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[3], 16)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[11], 5)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[13], 7)
        digraph.nodeList[10].addNeighbor(digraph.nodeList[15], 4)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[3], 13)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[10], 5)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[12], 9)
        digraph.nodeList[11].addNeighbor(digraph.nodeList[14], 4)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[3], 14)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[11], 9)
        digraph.nodeList[12].addNeighbor(digraph.nodeList[14], 5)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[6], 12)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[9], 3)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[10], 7)
        digraph.nodeList[13].addNeighbor(digraph.nodeList[15], 7)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[11], 4)
        digraph.nodeList[14].addNeighbor(digraph.nodeList[12], 5)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[9], 8)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[10], 4)
        digraph.nodeList[15].addNeighbor(digraph.nodeList[13], 7)


        # digraph.nodeList[0].addNeighbor(digraph.nodeList[1], 1)
        # digraph.nodeList[0].addNeighbor(digraph.nodeList[2], 2)
        # digraph.nodeList[0].addNeighbor(digraph.nodeList[4], 3)
        # digraph.nodeList[1].addNeighbor(digraph.nodeList[2], 4)
        # digraph.nodeList[1].addNeighbor(digraph.nodeList[6], 5)
        # digraph.nodeList[1].addNeighbor(digraph.nodeList[5], 6)
        # digraph.nodeList[1].addNeighbor(digraph.nodeList[4], 7)
        # digraph.nodeList[1].addNeighbor(digraph.nodeList[1], 8)
        # digraph.nodeList[2].addNeighbor(digraph.nodeList[3], 9)
        # digraph.nodeList[2].addNeighbor(digraph.nodeList[7], 10)
        # digraph.nodeList[2].addNeighbor(digraph.nodeList[6], 11)
        # digraph.nodeList[2].addNeighbor(digraph.nodeList[5], 12)
        # digraph.nodeList[2].addNeighbor(digraph.nodeList[1], 13)
        # digraph.nodeList[3].addNeighbor(digraph.nodeList[8], 14)
        # digraph.nodeList[3].addNeighbor(digraph.nodeList[7], 15)
        # digraph.nodeList[3].addNeighbor(digraph.nodeList[6], 16)
        # digraph.nodeList[3].addNeighbor(digraph.nodeList[2], 17)
        # digraph.nodeList[4].addNeighbor(digraph.nodeList[5], 18)
        # digraph.nodeList[4].addNeighbor(digraph.nodeList[0], 19)
        # digraph.nodeList[4].addNeighbor(digraph.nodeList[1], 20)
        # digraph.nodeList[5].addNeighbor(digraph.nodeList[6], 21)
        # digraph.nodeList[5].addNeighbor(digraph.nodeList[1], 22)
        # digraph.nodeList[5].addNeighbor(digraph.nodeList[2], 23)
        # digraph.nodeList[5].addNeighbor(digraph.nodeList[0], 24)
        # digraph.nodeList[5].addNeighbor(digraph.nodeList[4], 25)
        # digraph.nodeList[6].addNeighbor(digraph.nodeList[7], 26)
        # digraph.nodeList[6].addNeighbor(digraph.nodeList[3], 27)
        # digraph.nodeList[6].addNeighbor(digraph.nodeList[2], 28)
        # digraph.nodeList[6].addNeighbor(digraph.nodeList[1], 29)
        # digraph.nodeList[6].addNeighbor(digraph.nodeList[5], 30)
        # digraph.nodeList[7].addNeighbor(digraph.nodeList[8], 31)
        # digraph.nodeList[7].addNeighbor(digraph.nodeList[3], 32)
        # digraph.nodeList[7].addNeighbor(digraph.nodeList[2], 33)
        # digraph.nodeList[7].addNeighbor(digraph.nodeList[6], 34)
        # digraph.nodeList[8].addNeighbor(digraph.nodeList[7], 35)
        # digraph.nodeList[8].addNeighbor(digraph.nodeList[3], 36)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[5], 37)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[6], 38)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[7], 39)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[10], 40)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[11], 41)
        # digraph.nodeList[9].addNeighbor(digraph.nodeList[12], 42)
        # digraph.nodeList[10].addNeighbor(digraph.nodeList[9], 43)
        # digraph.nodeList[10].addNeighbor(digraph.nodeList[11], 44)
        # digraph.nodeList[11].addNeighbor(digraph.nodeList[12], 45)
        # digraph.nodeList[11].addNeighbor(digraph.nodeList[9], 46)
        # digraph.nodeList[11].addNeighbor(digraph.nodeList[10], 47)
        # digraph.nodeList[12].addNeighbor(digraph.nodeList[13], 48)
        # digraph.nodeList[12].addNeighbor(digraph.nodeList[9], 49)
        # digraph.nodeList[12].addNeighbor(digraph.nodeList[11], 50)
        # digraph.nodeList[13].addNeighbor(digraph.nodeList[14], 51)
        # digraph.nodeList[13].addNeighbor(digraph.nodeList[12], 52)
        # digraph.nodeList[13].addNeighbor(digraph.nodeList[17], 53)
        # digraph.nodeList[14].addNeighbor(digraph.nodeList[15], 54)
        # digraph.nodeList[14].addNeighbor(digraph.nodeList[13], 55)
        # digraph.nodeList[14].addNeighbor(digraph.nodeList[18], 56)
        # digraph.nodeList[14].addNeighbor(digraph.nodeList[17], 57)
        # digraph.nodeList[15].addNeighbor(digraph.nodeList[16], 58)
        # digraph.nodeList[15].addNeighbor(digraph.nodeList[14], 59)
        # digraph.nodeList[15].addNeighbor(digraph.nodeList[19], 60)
        # digraph.nodeList[15].addNeighbor(digraph.nodeList[18], 61)
        # digraph.nodeList[15].addNeighbor(digraph.nodeList[17], 62)
        # digraph.nodeList[16].addNeighbor(digraph.nodeList[15], 63)
        # digraph.nodeList[16].addNeighbor(digraph.nodeList[19], 64)
        # digraph.nodeList[16].addNeighbor(digraph.nodeList[18], 65)
        # digraph.nodeList[17].addNeighbor(digraph.nodeList[18], 66)
        # digraph.nodeList[17].addNeighbor(digraph.nodeList[13], 67)
        # digraph.nodeList[17].addNeighbor(digraph.nodeList[14], 68)
        # digraph.nodeList[17].addNeighbor(digraph.nodeList[15], 69)
        # digraph.nodeList[18].addNeighbor(digraph.nodeList[19], 70)
        # digraph.nodeList[18].addNeighbor(digraph.nodeList[17], 71)
        # digraph.nodeList[18].addNeighbor(digraph.nodeList[14], 72)
        # digraph.nodeList[18].addNeighbor(digraph.nodeList[15], 73)
        # digraph.nodeList[18].addNeighbor(digraph.nodeList[16], 74)
        # digraph.nodeList[19].addNeighbor(digraph.nodeList[18], 75)
        # digraph.nodeList[19].addNeighbor(digraph.nodeList[15], 76)
        # digraph.nodeList[19].addNeighbor(digraph.nodeList[16], 77)


        path = AStar.aStar(digraph, digraph.nodeList[0], digraph.nodeList[15])

        pathWeight = 0
        for i in range(len(path) - 1):
            pathWeight += digraph.getWeight(path[i].id, path[i + 1].id)

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
