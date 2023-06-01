

'''
Benchmark test til vores forskellige algorithms
'''
import argparse
import math
import random
import timeit

import Util.Graphs
import Visualize
from ShortestPathAlgos import Dijkstra, AStar, BiDiDijstra, ALT
from Util import DataManager

from line_profiler import LineProfiler


def benchMarkSingleAlgo(diGraph, algorithm, amount):
    times = list()
    invalidTimes = 0
    efficiencyList = []

    algorithm = algorithm.lower()

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
                continue
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
                continue
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
                continue
            times.append(timeit.default_timer()-starTime)
            i += 1

    elif algorithm == "alt":
        i = 0
        #quadrants, farthest, random
        landmarks = ALT.findLandmarks(diGraph, 16, "farthest")
        while i < amount:

            start = random.choice(list(diGraph.nodeList.values()))
            end = random.choice(list(diGraph.nodeList.values()))
            starTime = timeit.default_timer()
            path, weight, visited = ALT.ALT(diGraph, start, end, landmarks)
            if path is None:
                invalidTimes += 1
                continue
            times.append((timeit.default_timer()-starTime)*1000)
            efficiencyList.append(len(path)/len(visited))

            # print every 10% progress

            if i % (amount // 10) == 0:
                print(f"{i / amount * 100:.2f}%", "of", amount, "done")


            i += 1
    else:
        print("Invalid algorithm")
        exit()

    return times, invalidTimes, efficiencyList


def benchMarkAllAlgos(diGraph, amount):
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

    landmarks = ALT.findLandmarks(diGraph, 32, "farthest")

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
        dijkstraVisitedList.append(len(dijkstraVisited))

        aStarStartTime = timeit.default_timer()
        aStarPath, aStarWeight, aStarVisited = AStar.aStar(diGraph, start, end)
        aStarTimes.append(timeit.default_timer()-aStarStartTime)
        aStarVisitedList.append(len(aStarVisited))

        biDiDijkstraStartTime = timeit.default_timer()
        biDiDijkstraPath, biDiDijkstraWeight, biDiDijkstraVisited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, start, end)
        biDiDijkstraTimes.append(timeit.default_timer()-biDiDijkstraStartTime)
        biDiDijkstraVisitedList.append(len(biDiDijkstraVisited))

        ALTStartTime = timeit.default_timer()
        ALTPath, ALTWeight, ALTVisited = ALT.ALT(diGraph, start, end, landmarks)
        ALTTimes.append(timeit.default_timer()-ALTStartTime)
        ALTVistedList.append(len(ALTVisited))

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


def astarHeuristicsTest(diGraph, amount):
    eucleudianTimes = []
    greedyTimes = []


    eucleudianVisitedList = []
    greedyVisitedList = []

    print("Starting test")
    print("Graph has ", diGraph.countNodes(), " nodes")
    print("Graph has ", diGraph.countEdges(), " edges")

    for i in range(amount):
        startNode = random.choice(list(diGraph.nodeList.values()))
        endNode = random.choice(list(diGraph.nodeList.values()))

        testPath, testWeight, testVisited = AStar.aStar(diGraph, startNode, endNode)
        if testPath is None:
            continue

        greedyTimeStart = timeit.default_timer()
        greedyPath, greedyWeight, greedyVisited = AStar.aStar(diGraph, startNode, endNode, "greedy")
        greedyTimes.append((timeit.default_timer() - greedyTimeStart)*1000)
        greedyVisitedList.append(len(greedyVisited))

        eucleudianTimeStart = timeit.default_timer()
        eucleudianPath, eucleudianWeight, eucleudianVisited = AStar.aStar(diGraph, startNode, endNode)
        eucleudianTimes.append((timeit.default_timer() - eucleudianTimeStart)*1000)
        eucleudianVisitedList.append(len(eucleudianVisited))

        if i % (amount // 10) == 0:
            print(f"{i / amount * 100:.2f}%", "of", "all", "done")



    print("Greedy average time: ", sum(greedyTimes)/len(greedyTimes))
    print("Eucleudian average time: ", sum(eucleudianTimes)/len(eucleudianTimes))

    print("Greedy average visited: ", sum(greedyVisitedList)/len(greedyVisitedList))
    print("Eucleudian average visited: ", sum(eucleudianVisitedList)/len(eucleudianVisitedList))


def searchSpaceGraph(diGraph, algorithm):

    averageLat = 0
    averageLon = 0
    for node in diGraph.nodeList.values():
        averageLat += node.lat
        averageLon += node.lon

    averageLat = averageLat / len(diGraph.nodeList)
    averageLon = averageLon / len(diGraph.nodeList)

    # Find the closest node to the middle of the graph
    minDistance = float("inf")
    minNode = None
    for node in diGraph.nodeList.values():
       distance = math.sqrt((node.lat - averageLat)**2 + (node.lon - averageLon)**2)
       if distance < minDistance:
           minDistance = distance
           minNode = node

    # Find node longest distance from the middle of the graph
    minNode.fromLandmark = ALT.DijkstraNoTarget(diGraph, minNode)

    maxDistance = 0
    maxNode = None
    for (key, dist) in minNode.fromLandmark.items():
        if dist > maxDistance:
            maxDistance = dist
            maxNode = diGraph.nodeList[key]




    # call algorithm with the two nodes

    if algorithm == "dijkstra":

        print("min node: ", minNode)
        print("max node: ", maxNode)

        path, weight, visited = Dijkstra.dijkstra(diGraph, minNode, maxNode)

        print("Rendering searchspace")

        Visualize.plot_points(path, visited)

    else:
        print("Algorithm not found")







if __name__ == '__main__':

    # graph = DataManager.read_DiGrapgh_from_Parquet("ProcessedGraphs/malta-latest.parquet")
    #
    # transPosedGraph = Util.Graphs.transposeDiGraph(graph)
    #
    # landmarks = ALT.findLandmarks(graph, 10)
    #
    # lp = LineProfiler()
    # lp.add_function(ALT.ALT)
    # lp.add_function(ALT.findBestLowerBound)
    # lp_wrapper = lp(ALT.ALT)
    # lp_wrapper(graph, graph.nodeList["9067296420"], graph.nodeList["382980629"], landmarks)
    # lp_wrapper = lp(ALT.findBestLowerBound)
    # lp_wrapper(graph.nodeList["10028683375"], graph.nodeList["382980629"], landmarks)
    # lp.print_stats()

    parser = argparse.ArgumentParser(description='argparser for shortest path program')
    parser.add_argument('graph', metavar='map', type=str, help='enter a map to use')
    parser.add_argument('algorithm', metavar='algorithm', type=str, help='enter a algorithm to use')
    parser.add_argument('amount', metavar='amount', type=int, help='enter a amount of tests to run')

    args = parser.parse_args()

    algorithms = {"dijkstra", "astar", "bididijkstra", "ALT"}

    if args.algorithm not in algorithms and args.algorithm != "all" and args.algorithm != "astarheuristics" and not args.algorithm.startswith("searchspace"):
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

    if args.algorithm == "astarheuristics":
        astarHeuristicsTest(diGraph, args.amount)

    if args.algorithm.startswith("searchspace"):
        algorithm = args.algorithm[len("searchspace"):]
        if algorithm in algorithms:
            searchSpaceGraph(diGraph, algorithm)

    if args.algorithm != "all" and args.algorithm != "astarheuristics" and not args.algorithm.startswith("searchspace"):
        times, invalidTimes, efficiencyList = benchMarkSingleAlgo(diGraph, args.algorithm, args.amount)
        print(f"Average time for {args.algorithm}: {sum(times)/len(times)}")
        print(f"Average efficiency for {args.algorithm}: {(sum(efficiencyList)/len(efficiencyList))*100}%")
        print(f"Invalid times: {invalidTimes}")
