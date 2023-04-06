

'''
Benchmark test til vores forskellige algorithms
'''
import argparse
import random
import timeit

import Util.Graphs
from ShortestPathAlgos import Dijkstra, AStar, BiDiDijstra
from Util import DataManager

from line_profiler import LineProfiler


def benchMarkSingleAlgorithm(diGraph, param, amount):
    '''
    :param diGraph:
    :param param:
    :param amount:
    :return:
    '''

    times = list()
    invalidTimes = 0

    transPosedGraph = Util.Graphs.transposeDiGraph(diGraph)

    i = 0
    while i < amount:

        start = random.choice(list(diGraph.nodeList.values()))
        end = random.choice(list(diGraph.nodeList.values()))

        # print every 10% progress
        if i % (amount // 10) == 0:
            print(f"{i / amount * 100:.2f}%", "of", param, "done")

        if param == "dijkstra":
            startTime2 = timeit.default_timer()
            path, weight, visited = Dijkstra.dijkstra(diGraph, start, end)
            # if the path is none, there exists no path between the two nodes, and we should not add the time to the set
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-startTime2)
            i += 1
        elif param == "astar":
            startTime3 = timeit.default_timer()
            path, weight, visited = AStar.aStar(diGraph, start, end)
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-startTime3)
            i += 1
        elif param == "bididijkstra":
            startTime4 = timeit.default_timer()
            path, weight, visited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, start, end)
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-startTime4)
            i += 1
        else:
            print("How did you even get here?!")

    return times, invalidTimes



if __name__ == '__main__':

    # graph = DataManager.read_DiGrapgh_from_Parquet("ProcessedGraphs/malta-latest.parquet")
    #
    # transPosedGraph = Util.Graphs.transposeDiGraph(graph)
    #
    # lp = LineProfiler()
    # lp.add_function(BiDiDijstra.biDiDijkstra)
    # lp_wrapper = lp(BiDiDijstra.biDiDijkstra)
    # lp_wrapper(graph, transPosedGraph, graph.nodeList["9067296420"], graph.nodeList["382980629"])
    # lp.print_stats()

    parser = argparse.ArgumentParser(description='argparser for shortest path program')
    parser.add_argument('graph', metavar='map', type=str, help='enter a map to use')
    parser.add_argument('algorithm', metavar='algorithm', type=str, help='enter a algorithm to use')
    parser.add_argument('amount', metavar='amount', type=int, help='enter a amount of tests to run')

    args = parser.parse_args()

    algorithms = {"dijkstra", "astar", "bididijkstra"}

    if args.algorithm not in algorithms and args.algorithm != "all":
        print("Invalid algorithm")
        exit()

    print("Reading graph from file...")
    diGraph = DataManager.read_DiGrapgh_from_Parquet(args.graph)
    print("Graph loaded from file")

    print(f"Running benchmark for {args.algorithm}")

    if args.algorithm == "all":
        for algorithm in algorithms:
            times, invalidTimes = benchMarkSingleAlgorithm(diGraph, algorithm, args.amount)
            print(f"Average time for {algorithm}: {sum(times)/len(times)}")
            print(f"Total amount of times recorded: {len(times)}")
            print(f"Total amount of invalid times: {invalidTimes}")
            print("--------------------------------------------------")

    else:
        times = benchMarkSingleAlgorithm(diGraph, args.algorithm, args.amount)
        print(f"Average time for {args.algorithm}: {sum(times)/len(times)}")

        
    
    
