

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


def benchMarkSingleAlgo(diGraph, algorithm, amount):
    '''
    :param diGraph:
    :param algorithm:
    :param amount:
    :return:
    '''

    times = list()
    invalidTimes = 0

    if algorithm == "bididijkstra":
        transPosedGraph = Util.Graphs.transposeDiGraph(diGraph)

        i = 0
        while i < amount:

            start = random.choice(list(diGraph.nodeList.values()))
            end = random.choice(list(diGraph.nodeList.values()))

            starTime = timeit.default_timer()
            path, weight, visited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, start, end)
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-starTime)
            i += 1

    elif algorithm == "dijkstra":
        i = 0
        while i < amount:

            start = random.choice(list(diGraph.nodeList.values()))
            end = random.choice(list(diGraph.nodeList.values()))

            starTime = timeit.default_timer()
            path, weight, visited = Dijkstra.dijkstra(diGraph, start, end)
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-starTime)
            i += 1

    elif algorithm == "astar":
        i = 0
        while i < amount:

            start = random.choice(list(diGraph.nodeList.values()))
            end = random.choice(list(diGraph.nodeList.values()))

            starTime = timeit.default_timer()
            path, weight, visited = AStar.aStar(diGraph, start, end)
            if path is None:
                invalidTimes += 1
            times.append(timeit.default_timer()-starTime)
            i += 1

    else:
        print("Invalid algorithm")
        exit()

    return times, invalidTimes


def benchMarkAllAlgos(diGraph, amount):
    '''
    :param diGraph:
    :param amount:
    :return:
    '''

    i = 0

    dijkstraTimes = list()
    aStarTimes = list()
    biDiDijkstraTimes = list()

    invalidTimes = 0

    transPosedGraph = Util.Graphs.transposeDiGraph(diGraph)


    while i < amount:

        start = random.choice(list(diGraph.nodeList.values()))
        end = random.choice(list(diGraph.nodeList.values()))

        # print every 10% progress
        if i % (amount // 10) == 0:
            print(f"{i / amount * 100:.2f}%", "of", "all", "done")

        dijstraStartTime = timeit.default_timer()
        dijkstraPath, dijkstraWeight, dijkstraVisited = Dijkstra.dijkstra(diGraph, start, end)
        if dijkstraPath is None:
            invalidTimes += 1
            continue
        dijkstraTimes.append(timeit.default_timer()-dijstraStartTime)

        aStarStartTime = timeit.default_timer()
        aStarPath, aStarWeight, aStarVisited = AStar.aStar(diGraph, start, end)
        aStarTimes.append(timeit.default_timer()-aStarStartTime)

        biDiDijkstraStartTime = timeit.default_timer()
        biDiDijkstraPath, biDiDijkstraWeight, biDiDijkstraVisited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, start, end)
        biDiDijkstraTimes.append(timeit.default_timer()-biDiDijkstraStartTime)

        ##Check if the length of the paths are within 2 meters of each other
        if abs(dijkstraWeight - aStarWeight) > 0.002 or abs(dijkstraWeight - biDiDijkstraWeight) > 0.002 or abs(aStarWeight - biDiDijkstraWeight) > 0.002:
            print("Invalid path lengths")
            print(f"Dijkstra: {dijkstraWeight}")
            print(f"A*: {aStarWeight}")
            print(f"BiDiDijkstra: {biDiDijkstraWeight}")
            print("--------------------------------------------------")
            i += 1
        else:
            i += 1

    return dijkstraTimes, aStarTimes, biDiDijkstraTimes






if __name__ == '__main__':

    # graph = DataManager.read_DiGrapgh_from_Parquet("ProcessedGraphs/lta-latest.parquet")
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
        dijkstraTimes, aStarTimes, biDiDijkstraTimes = benchMarkAllAlgos(diGraph, args.amount)
        print(f"Average time for Dijkstra: {sum(dijkstraTimes)/len(dijkstraTimes)}")
        print(f"Average time for A*: {sum(aStarTimes)/len(aStarTimes)}")
        print(f"Average time for BiDiDijkstra: {sum(biDiDijkstraTimes)/len(biDiDijkstraTimes)}")

    else:
        times, invalidTimes = benchMarkSingleAlgo(diGraph, args.algorithm, args.amount)
        print(f"Average time for {args.algorithm}: {sum(times)/len(times)}")
        print(f"Invalid times: {invalidTimes}")

        
    
    
