import unittest
from ShortestPathAlgos import AStar
import Util.Graphs as Graphs
from ShortestPathAlgos import ALT
import timeit


class ALTTest(unittest.TestCase):

    def test_Landmark(self):
        # Test that the ALT algorithm correctly finds the landmarks

        graph = Graphs.DiGraph()

        for i in range(4):
            for j in range(4):
                graph.addNode(i+j, i, j)

        landmarks = ALT.ALT(graph, 4, 6)
        print(landmarks)

    def Main(self):
        unittest.main()


if __name__ == '__main__':
    unittest.main()