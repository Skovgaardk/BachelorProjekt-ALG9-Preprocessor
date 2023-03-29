import sys

import heapq as hq
import time

import Util.Graphs


def biDiDijkstra(graph, source, target, returnVisited=False):

    transposedGraph = Util.Graphs.transposeDiGraph(graph)
    targetNode = transposedGraph.nodeList[target.id]
    copyOfGraphList = list(graph.nodeList.values())
    transposedGraph = list(transposedGraph.nodeList.values())

    initSingleSource(copyOfGraphList, source)
    initSingleSource(transposedGraph, target)

    target = transposedGraph[transposedGraph.index(targetNode)]

    visited = set()

    openForward = [(0, source.id, source)]
    forwardDist = {source.id: 0}
    openBackward = [(0, target.id, target)]
    backwardDist = {target.id: 0}

    while True:
        if openForward[0][1] in backwardDist:
            return calculatePath(openForward[0][2], openBackward) if not returnVisited else (calculatePath(openForward[0][2], openBackward), len(visited))

        if openBackward[0][1] in forwardDist:
            return calculatePath(openBackward[0][2], openForward) if not returnVisited else (calculatePath(openBackward[0][2], openForward), len(visited))

        # forward search
        min_dist, _,  min_node = hq.heappop(openForward)
        visited.add(min_node)
        for adj, weight in min_node.adjacent.items():
            relax(min_node, adj, weight, openForward, forwardDist)

        # backward search
        min_dist, _,  min_node = hq.heappop(openBackward)
        visited.add(min_node)
        for adj, weight in min_node.adjacent.items():
            relax(min_node, adj, weight, openBackward, backwardDist)

def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node._previous = None
    source._distance = 0


def relax(min_node, adj, weight, openList, distDict):
    new_dist = distDict[min_node.id] + weight
    if adj.id not in distDict or new_dist < distDict[adj.id]:
        distDict[adj.id] = new_dist
        adj.previous = min_node
        hq.heappush(openList, (new_dist, adj.id, adj))


def calculatePath(node, openList):
    path = []
    while node is not None:
        path.append(node)
        node = node.previous

    backwardPath = []
    node = hq.heappop(openList)[2]
    while node is not None:
        backwardPath.append(node)
        node = node.previous

    return path[::-1] + backwardPath[1:]



