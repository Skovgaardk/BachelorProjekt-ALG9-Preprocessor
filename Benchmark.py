

'''
Benchmark test til vores forskellige algorithms
'''
import argparse
import random
import timeit

import Util.Graphs
from ShortestPathAlgos import Dijkstra, AStar, BiDiDijstra, ALT
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
    ALTTimes = list()

    dijkstraVisitedList = list()
    aStarVisitedList = list()
    biDiDijkstraVisitedList = list()
    ALTVistedList = list()

    invalidTimes = 0

    transPosedGraph = Util.Graphs.transposeDiGraph(diGraph)

    landmarks = ALT.findLandmarks(diGraph, 3)

    landmarkDistances = ALT.calculateLandmarkDistances(diGraph, landmarks)

    wrongWays = 0

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
        dijkstraVisitedList.append(dijkstraVisited)

        aStarStartTime = timeit.default_timer()
        aStarPath, aStarWeight, aStarVisited = AStar.aStar(diGraph, start, end)
        aStarTimes.append(timeit.default_timer()-aStarStartTime)
        aStarVisitedList.append(aStarVisited)

        biDiDijkstraStartTime = timeit.default_timer()
        biDiDijkstraPath, biDiDijkstraWeight, biDiDijkstraVisited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, start, end)
        biDiDijkstraTimes.append(timeit.default_timer()-biDiDijkstraStartTime)
        biDiDijkstraVisitedList.append(biDiDijkstraVisited)

        ALTStartTime = timeit.default_timer()
        ALTPath, ALTWeight, ALTVisited = ALT.ALT(diGraph, start, end, landmarkDistances)
        ALTTimes.append(timeit.default_timer()-ALTStartTime)
        ALTVistedList.append(ALTVisited)

        allWeights = [dijkstraWeight, aStarWeight, biDiDijkstraWeight, ALTWeight]

        ##Check if the length of the paths are within 2 meters of each other
        if max(allWeights) - min(allWeights) > 0.002:
            print("Wrong path lengths")
            print(f"Dijkstra: {dijkstraWeight}")
            print(f"A*: {aStarWeight}")
            print(f"BiDiDijkstra: {biDiDijkstraWeight}")
            print(f"ALT: {ALTWeight}")
            print(f"Start: {start}")
            print(f"End: {end}")
            print("--------------------------------------------------")
            wrongWays += 1
            i += 1
        else:
            i += 1

    dijkstraInfo = [dijkstraTimes, dijkstraVisitedList]
    aStarInfo = [aStarTimes, aStarVisitedList]
    biDiDijkstraInfo = [biDiDijkstraTimes, biDiDijkstraVisitedList]
    ALTInfo = [ALTTimes, ALTVistedList]

    return dijkstraInfo, aStarInfo, biDiDijkstraInfo, ALTInfo, invalidTimes, wrongWays


if __name__ == '__main__':

    # graph = DataManager.read_DiGrapgh_from_Parquet("ProcessedGraphs/malta-latest.parquet")
    #
    # transPosedGraph = Util.Graphs.transposeDiGraph(graph)
    #
    # landmarks = ALT.findLandmarks(graph, 16)
    #
    # landmarkDistances = ALT.calculateLandmarkDistances(graph, landmarks)
    #
    # lp = LineProfiler()
    # lp.add_function(ALT.ALT)
    # lp.add_function(ALT.findBestLowerBound)
    # lp_wrapper = lp(ALT.ALT)
    # lp_wrapper(graph, graph.nodeList["9067296420"], graph.nodeList["382980629"], landmarkDistances)
    # lp_wrapper = lp(ALT.findBestLowerBound)
    # lp_wrapper(graph.nodeList["10028683375"], graph.nodeList["382980629"], landmarks)
    # lp.print_stats()

    parser = argparse.ArgumentParser(description='argparser for shortest path program')
    parser.add_argument('graph', metavar='map', type=str, help='enter a map to use')
    parser.add_argument('algorithm', metavar='algorithm', type=str, help='enter a algorithm to use')
    parser.add_argument('amount', metavar='amount', type=int, help='enter a amount of tests to run')

    args = parser.parse_args()

    algorithms = {"dijkstra", "astar", "bididijkstra", "ALT"}

    if args.algorithm not in algorithms and args.algorithm != "all":
        print("Invalid algorithm")
        exit()

    print("Reading graph from file...")
    diGraph = DataManager.read_DiGrapgh_from_Parquet(args.graph)
    print("Graph loaded from file")

    print(f"Running benchmark for {args.algorithm}")

    if args.algorithm == "all":
        dijstraInfo, aStarInfo, biDiDijkstraInfo, ALTinfo, invalidPaths, wrongWays = benchMarkAllAlgos(diGraph, args.amount)
        print(f"Average time for Dijkstra: {sum(dijstraInfo[0])/len(dijstraInfo[0])}")
        print(f"Average nodes visited for Dijkstra: {sum(dijstraInfo[1])/len(dijstraInfo[1])}")
        print(f"Average time for A*: {sum(aStarInfo[0])/len(aStarInfo[0])}")
        print(f"Average nodes visited for A*: {sum(aStarInfo[1])/len(aStarInfo[1])}")
        print(f"Average time for BiDiDijkstra: {sum(biDiDijkstraInfo[0])/len(biDiDijkstraInfo[0])}")
        print(f"Average nodes visited for BiDiDijkstra: {sum(biDiDijkstraInfo[1])/len(biDiDijkstraInfo[1])}")
        print(f"Average time for ALT: {sum(ALTinfo[0])/len(ALTinfo[0])}")
        print(f"Average nodes visited for ALT: {sum(ALTinfo[1])/len(ALTinfo[1])}")
        print(f"Amount of invalid paths found: {invalidPaths}")
        print(f"Amount of wrong ways found: {wrongWays}")
        print(f"Percent of wrong ways: {wrongWays/args.amount*100}%")

    else:
        times, invalidTimes = benchMarkSingleAlgo(diGraph, args.algorithm, args.amount)
        print(f"Average time for {args.algorithm}: {sum(times)/len(times)}")
        print(f"Invalid times: {invalidTimes}")

        
    
    
