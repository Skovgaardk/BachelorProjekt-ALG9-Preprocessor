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
        graph.nodeList[0].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[0].addNeighbor(graph.nodeList[4], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[5], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[0], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[3].addNeighbor(graph.nodeList[7], 1)
        graph.nodeList[3].addNeighbor(graph.nodeList[2], 1)
        graph.nodeList[4].addNeighbor(graph.nodeList[5], 1)
        graph.nodeList[4].addNeighbor(graph.nodeList[0], 1)
        graph.nodeList[4].addNeighbor(graph.nodeList[8], 1)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[5].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[5].addNeighbor(graph.nodeList[4], 1)
        graph.nodeList[5].addNeighbor(graph.nodeList[9], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[7], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[2], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 1)
        graph.nodeList[6].addNeighbor(graph.nodeList[10], 1)
        graph.nodeList[7].addNeighbor(graph.nodeList[3], 1)
        graph.nodeList[7].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[7].addNeighbor(graph.nodeList[11], 1)
        graph.nodeList[8].addNeighbor(graph.nodeList[9], 1)
        graph.nodeList[8].addNeighbor(graph.nodeList[4], 1)
        graph.nodeList[8].addNeighbor(graph.nodeList[12], 1)
        graph.nodeList[9].addNeighbor(graph.nodeList[10], 1)
        graph.nodeList[9].addNeighbor(graph.nodeList[5], 1)
        graph.nodeList[9].addNeighbor(graph.nodeList[8], 1)
        graph.nodeList[9].addNeighbor(graph.nodeList[13], 1)
        graph.nodeList[10].addNeighbor(graph.nodeList[11], 1)
        graph.nodeList[10].addNeighbor(graph.nodeList[6], 1)
        graph.nodeList[10].addNeighbor(graph.nodeList[9], 1)
        graph.nodeList[10].addNeighbor(graph.nodeList[14], 1)
        graph.nodeList[11].addNeighbor(graph.nodeList[7], 1)
        graph.nodeList[11].addNeighbor(graph.nodeList[10], 1)
        graph.nodeList[11].addNeighbor(graph.nodeList[15], 1)
        graph.nodeList[12].addNeighbor(graph.nodeList[13], 1)
        graph.nodeList[12].addNeighbor(graph.nodeList[8], 1)
        graph.nodeList[13].addNeighbor(graph.nodeList[14], 1)
        graph.nodeList[13].addNeighbor(graph.nodeList[9], 1)
        graph.nodeList[13].addNeighbor(graph.nodeList[12], 1)
        graph.nodeList[14].addNeighbor(graph.nodeList[15], 1)
        graph.nodeList[14].addNeighbor(graph.nodeList[10], 1)
        graph.nodeList[14].addNeighbor(graph.nodeList[13], 1)
        graph.nodeList[15].addNeighbor(graph.nodeList[11], 1)
        graph.nodeList[15].addNeighbor(graph.nodeList[14], 1)


        landmarks = ALT.findLandmarks(graph, 16)

        print("Landmarks:")
        for node in landmarks:
            print(node.id)

        landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)

        print("Landmark Distances:")
        print(landmarkDistances)
        for landmark in landmarkDistances.keys():
            print("Landmark: " + str(landmark))
            print("To distances", landmarkDistances[landmark][0])
            print("From distances", landmarkDistances[landmark][1])



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
        graph.nodeList[1].addNeighbor(graph.nodeList[0], 4)

        graph.nodeList[2].addNeighbor(graph.nodeList[5], 3)

        graph.nodeList[3].addNeighbor(graph.nodeList[5], 4)
        graph.nodeList[3].addNeighbor(graph.nodeList[6], 6)
        graph.nodeList[3].addNeighbor(graph.nodeList[0], 7)

        graph.nodeList[4].addNeighbor(graph.nodeList[8], 13)
        graph.nodeList[4].addNeighbor(graph.nodeList[1], 9)
        graph.nodeList[4].addNeighbor(graph.nodeList[5], 12)

        graph.nodeList[5].addNeighbor(graph.nodeList[4], 12)
        graph.nodeList[5].addNeighbor(graph.nodeList[2], 3)
        graph.nodeList[5].addNeighbor(graph.nodeList[3], 4)
        graph.nodeList[5].addNeighbor(graph.nodeList[6], 2)
        graph.nodeList[5].addNeighbor(graph.nodeList[7], 5)

        graph.nodeList[6].addNeighbor(graph.nodeList[8], 9)
        graph.nodeList[6].addNeighbor(graph.nodeList[5], 2)
        graph.nodeList[6].addNeighbor(graph.nodeList[3], 6)

        graph.nodeList[7].addNeighbor(graph.nodeList[8], 3)
        graph.nodeList[7].addNeighbor(graph.nodeList[5], 5)

        graph.nodeList[8].addNeighbor(graph.nodeList[7], 3)
        graph.nodeList[8].addNeighbor(graph.nodeList[6], 9)
        graph.nodeList[8].addNeighbor(graph.nodeList[4], 13)

        landmarks = [graph.nodeList[5]]

        landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)

        print("Landmark Distances:")
        print(landmarkDistances)
        for landmark in landmarkDistances.keys():
            print("Landmark: " + str(landmark))
            print("To distances", landmarkDistances[landmark][0])
            print("From distances", landmarkDistances[landmark][1])


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

    def test_landMarkMakesRightTuples(self):
        graph = Graphs.DiGraph()

        # add 9 nodes
        for i in range(5):
            graph.addNode(i, 0, 0)


        graph.nodeList[0].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[0].addNeighbor(graph.nodeList[2], 1)
        graph.nodeList[0].addNeighbor(graph.nodeList[3], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[0], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[2], 1)
        graph.nodeList[1].addNeighbor(graph.nodeList[3], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[0], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[2].addNeighbor(graph.nodeList[3], 1)
        graph.nodeList[3].addNeighbor(graph.nodeList[0], 1)
        graph.nodeList[3].addNeighbor(graph.nodeList[1], 1)
        graph.nodeList[3].addNeighbor(graph.nodeList[2], 1)


        landmarks = [graph.nodeList[2]]

        landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)

        print("Landmark Distances:")
        print(landmarkDistances)
        for landmark in landmarkDistances.keys():
            print("Landmark: " + str(landmark))
            print("To distances", landmarkDistances[landmark][0])
            print("From distances", landmarkDistances[landmark][1])


        anyIsNotExistant = False
        for landmark in landmarkDistances.keys():
            for node in graph.nodeList:
                print("Checking if node " + str(node))
                print("landmark to distances: ", landmarkDistances[landmark][0].keys())
                print("landmark from distances: ", landmarkDistances[landmark][1].keys())
                if node not in landmarkDistances[landmark][0].keys():
                    anyIsNotExistant = True
                if node not in landmarkDistances[landmark][1].keys():
                    anyIsNotExistant = True

        self.assertFalse(anyIsNotExistant)

    def Main(self):
        unittest.main()


if __name__ == '__main__':
    unittest.main()