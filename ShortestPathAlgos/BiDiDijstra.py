import sys

import heapq as hq
import time

import Util.Graphs


def biDiDijkstra(graph, source, target):

    transposedGraph = Util.Graphs.transposeDiGraph(graph)

    targetNode = transposedGraph.nodeList[target.id]

    initSingleSource(graph.nodeList.values(), source)
    initSingleSource(transposedGraph.nodeList.values(), targetNode)

    visited = set()

    if type(source) == str:
        source = graph.nodeList[source]

    if type(target) == str:
        target = targetNode

    openForward = [(0, source.id, source)]
    forwardDist = {source.id: 0}
    openBackward = [(0, target.id, target)]
    backwardDist = {target.id: 0}


    intercept = None
    while True:
        if openForward[0][1] in backwardDist:
            intercept = openForward[0][2]
            break

        if openBackward[0][1] in forwardDist:
            intercept = openBackward[0][2]
            break

        # forward search
        _, _,  min_node = hq.heappop(openForward)
        visited.add(min_node)
        for adj, weight in graph.nodeList[min_node.id].adjacent.items():
            new_dist = forwardDist[min_node.id] + weight
            if adj.id not in forwardDist or new_dist < forwardDist[adj.id]:
                forwardDist[adj.id] = new_dist
                adj.previous = min_node
                hq.heappush(openForward, (new_dist, adj.id, adj))

        # backward search
        _, _,  min_node = hq.heappop(openBackward)
        visited.add(min_node)
        for adj, weight in transposedGraph.nodeList[min_node.id].adjacent.items():
            new_dist = backwardDist[min_node.id] + weight
            if adj.id not in backwardDist or new_dist < backwardDist[adj.id]:
                backwardDist[adj.id] = new_dist
                adj.previous = min_node
                hq.heappush(openBackward, (new_dist, adj.id, adj))


    while openForward:
        dist, _, min_node = hq.heappop(openForward)
        if min_node.id in backwardDist:
            new_dist = dist + backwardDist[min_node.id]
            if min_node.id not in forwardDist or new_dist < forwardDist[min_node.id]:
                forwardDist[min_node.id] = new_dist
                min_node.previous = min_node
                intercept = min_node

    weight = forwardDist[intercept.id] + backwardDist[intercept.id]

    path = calculatePath(intercept, transposedGraph)

    return path, weight, len(visited)

def calculatePath(node, transPosedgraph):
    path = []

    forwardNode = node
    while forwardNode is not None:
        path.append(forwardNode)
        forwardNode = forwardNode.previous

    backwardPath = []
    backwardNode = transPosedgraph.nodeList[node.id]
    while backwardNode is not None:
        backwardPath.append(backwardNode)
        backwardNode = backwardNode.previous

    completePath = path[::-1] + backwardPath[1:]
    return completePath


def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node._previous = None
    source._distance = 0

