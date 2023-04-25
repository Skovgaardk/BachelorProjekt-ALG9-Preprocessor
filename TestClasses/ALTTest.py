import unittest
from ShortestPathAlgos import AStar
import Util.Graphs as Graphs
from ShortestPathAlgos import ALT
import timeit


class ALTTest(unittest.TestCase):

    def test_Landmark(self):
        # Test that the ALT algorithm correctly finds the landmarks

        graph = Graphs.DiGraph()

        idNum = 0
        for i in range(4):
            for j in range(4):
                graph.addNode(idNum, i, j)
                idNum += 1


        # add edges
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 1.01)
        graph.nodeList[0].addNeighbor(graph.nodeList[4], 1.02)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 1.03)
        graph.nodeList[1].addNeighbor(graph.nodeList[5], 1.04)
        graph.nodeList[1].addNeighbor(graph.nodeList[0], 1.05)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 1.06)
        graph.nodeList[2].addNeighbor(graph.nodeList[6], 1.07)
        graph.nodeList[2].addNeighbor(graph.nodeList[1], 1.08)
        graph.nodeList[3].addNeighbor(graph.nodeList[7], 1.09)
        graph.nodeList[3].addNeighbor(graph.nodeList[2], 1.10)
        graph.nodeList[4].addNeighbor(graph.nodeList[5], 1.11)
        graph.nodeList[4].addNeighbor(graph.nodeList[0], 1.12)
        graph.nodeList[4].addNeighbor(graph.nodeList[8], 1.13)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 1.14)
        graph.nodeList[5].addNeighbor(graph.nodeList[1], 1.15)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 1.16)
        graph.nodeList[5].addNeighbor(graph.nodeList[9], 1.17)
        graph.nodeList[6].addNeighbor(graph.nodeList[7], 1.18)
        graph.nodeList[6].addNeighbor(graph.nodeList[2], 1.19)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 1.20)
        graph.nodeList[6].addNeighbor(graph.nodeList[10], 1.21)
        graph.nodeList[7].addNeighbor(graph.nodeList[3], 1.22)
        graph.nodeList[7].addNeighbor(graph.nodeList[6], 1.23)
        graph.nodeList[7].addNeighbor(graph.nodeList[11], 1.24)
        graph.nodeList[8].addNeighbor(graph.nodeList[9], 1.25)
        graph.nodeList[8].addNeighbor(graph.nodeList[4], 1.26)
        graph.nodeList[8].addNeighbor(graph.nodeList[12], 1.27)
        graph.nodeList[9].addNeighbor(graph.nodeList[10], 1.28)
        graph.nodeList[9].addNeighbor(graph.nodeList[5], 1.29)
        graph.nodeList[9].addNeighbor(graph.nodeList[8], 1.30)
        graph.nodeList[9].addNeighbor(graph.nodeList[13], 1.31)
        graph.nodeList[10].addNeighbor(graph.nodeList[11], 1.32)
        graph.nodeList[10].addNeighbor(graph.nodeList[6], 1.33)
        graph.nodeList[10].addNeighbor(graph.nodeList[9], 1.34)
        graph.nodeList[10].addNeighbor(graph.nodeList[14], 1.35)
        graph.nodeList[11].addNeighbor(graph.nodeList[7], 1.36)
        graph.nodeList[11].addNeighbor(graph.nodeList[10], 1.37)
        graph.nodeList[11].addNeighbor(graph.nodeList[15], 1.38)
        graph.nodeList[12].addNeighbor(graph.nodeList[13], 1.39)
        graph.nodeList[12].addNeighbor(graph.nodeList[8], 1.40)
        graph.nodeList[13].addNeighbor(graph.nodeList[14], 1.41)
        graph.nodeList[13].addNeighbor(graph.nodeList[9], 1.42)
        graph.nodeList[13].addNeighbor(graph.nodeList[12], 1.43)
        graph.nodeList[14].addNeighbor(graph.nodeList[15], 1.44)
        graph.nodeList[14].addNeighbor(graph.nodeList[10], 1.45)
        graph.nodeList[14].addNeighbor(graph.nodeList[13], 1.46)
        graph.nodeList[15].addNeighbor(graph.nodeList[11], 1.47)
        graph.nodeList[15].addNeighbor(graph.nodeList[14], 1.48)


        landmarks = ALT.findLandmarks(graph, 16)

        print("Landmarks:")
        for node in landmarks:
            print(node.id)

        landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)

        print("Landmark Distances:")
        print(landmarkDistances)
        for landmark in landmarkDistances.items():
            print("Landmark: ", landmark[0])
            for node in landmark[1].items():
                print("Node: ", node[0], " Distance: ", node[1])




    def test_ALT(self):
        graph = Graphs.DiGraph()

        # add 9 nodes
        for i in range(9):
            graph.addNode(i, 0, 0)

        # add edges
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 4)
        graph.nodeList[0].addNeighbor(graph.nodeList[2], 5)
        graph.nodeList[0].addNeighbor(graph.nodeList[3], 7)
        graph.nodeList[1].addNeighbor(graph.nodeList[4], 9)
        graph.nodeList[2].addNeighbor(graph.nodeList[5], 3)
        graph.nodeList[3].addNeighbor(graph.nodeList[5], 4)
        graph.nodeList[3].addNeighbor(graph.nodeList[6], 6)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 12)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 2)
        graph.nodeList[5].addNeighbor(graph.nodeList[7], 5)
        graph.nodeList[4].addNeighbor(graph.nodeList[8], 13)
        graph.nodeList[6].addNeighbor(graph.nodeList[8], 9)
        graph.nodeList[7].addNeighbor(graph.nodeList[8], 3)

        landmarks = [graph.nodeList[5]]

        landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)


        start = timeit.default_timer()
        path, weight, len = ALT.ALT(graph, graph.nodeList[0], graph.nodeList[8], landmarkDistances)
        print("Time: ", (timeit.default_timer() - start)*1000)

        print("Path: ")
        for i in path:
            print(i.id)

        #Correct path is: s, b, e, g, t
        self.assertEqual(path[0].id, 0)
        self.assertEqual(path[1].id, 2)
        self.assertEqual(path[2].id, 5)
        self.assertEqual(path[3].id, 7)
        self.assertEqual(path[4].id, 8)
        self.assertEqual(weight, 16)

    def Main(self):
        unittest.main()


if __name__ == '__main__':
    unittest.main()