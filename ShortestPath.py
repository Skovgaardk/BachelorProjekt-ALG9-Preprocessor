import argparse
import timeit

import Visualize
from Visualize import visualize_path
from Util import DataManager
from ShortestPathAlgos import Dijkstra, AStar

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='argparser for shortest path program')
    parser.add_argument('graph', metavar='map', type=str, help='enter a map to use')
    parser.add_argument('algorithm', metavar='algorithm', type=str, help='enter a algorithm to use')
    parser.add_argument('start', metavar='start', type=str, help='enter a start node')
    parser.add_argument('end', metavar='end', type=str, help='enter a end node')
    parser.add_argument('visited', metavar='visited', type=bool, help='show amount of visited nodes', nargs='?', default=False)

    args = parser.parse_args()

    graph = args.graph
    algorithm = args.algorithm
    start = args.start
    end = args.end
    visited = args.visited

    startTime1 = timeit.default_timer()

    if algorithm != "dijkstra" and algorithm != "astar":
        print("Invalid algorithm")
        exit()

    diGraph = DataManager.read_DiGrapgh_from_Parquet(graph)
    print("Time to read graph: ", timeit.default_timer()-startTime1)

    result = None
    if algorithm == "dijkstra":
        startTime2 = timeit.default_timer()
        result = Dijkstra.dijkstra(diGraph, diGraph.nodeList[start], diGraph.nodeList[end], returnVisited=visited)
        print("Time to run Dijkstra: ", timeit.default_timer()-startTime2)
    elif algorithm == "astar":
        startTime3 = timeit.default_timer()
        result = AStar.aStar(diGraph, diGraph.nodeList[start], diGraph.nodeList[end], returnVisited=visited)
        print("Time to run A*: ", timeit.default_timer()-startTime3)
    else:
        print("Invalid algorithm")

    if visited:
        pathWeight = 0
        actualPath = result[0]
        for i in range(len(actualPath) - 1):
            pathWeight += diGraph.getWeight(actualPath[i].id, actualPath[i + 1].id)
        print("Path weight: ", pathWeight)
        print("Amount of visited nodes: ", result[1])

        print("Visualizing path in browser...")
        visualize_path(result[0])
    else:
        pathWeight = 0
        for i in range(len(result) - 1):
            pathWeight += diGraph.getWeight(result[i].id, result[i + 1].id)
        print("Path weight: ", pathWeight)

        print("Visualizing path in browser...")
        visualize_path(result)








