
import sys

import heapq as hq
import time
import line_profiler

import Util.Graphs

from collections import defaultdict



def biDiDijkstra(graph, transPosedGraph, source, target):
    sourceNode = graph.nodeList[source.id]
    targetNode = transPosedGraph.nodeList[target.id]

    visitedForward = set()
    visitedBackward = set()

    openForward = [(0, sourceNode.id, sourceNode)]
    forwardDist = {sourceNode.id: 0}
    openBackward = [(0, targetNode.id, targetNode)]
    backwardDist = {targetNode.id: 0}

    prevDictForward = dict()
    prevDictBackward = dict()

    intercept = None
    while openForward and openBackward:
    ## forward search
        _, min_node_id, min_node = hq.heappop(openForward)
        if min_node_id in visitedForward:
            continue
        visitedForward.add(min_node_id)
        for adj, weight in min_node.adjacent.items():
            new_dist = forwardDist[min_node_id] + weight
            if adj.id not in forwardDist or new_dist < forwardDist[adj.id]:
                forwardDist[adj.id] = new_dist
                prevDictForward[adj.id] = min_node
                hq.heappush(openForward, (new_dist, adj.id, adj))

        # backward search
        _, min_node_id, min_node = hq.heappop(openBackward)
        if min_node_id in visitedBackward:
            continue
        visitedBackward.add(min_node_id)
        for adj, weight in min_node.adjacent.items():
            new_dist = backwardDist[min_node_id] + weight
            if adj.id not in backwardDist or new_dist < backwardDist[adj.id]:
                backwardDist[adj.id] = new_dist
                prevDictBackward[adj.id] = min_node
                hq.heappush(openBackward, (new_dist, adj.id, adj))

        # the queue is empty, there is no path
        if not openForward or not openBackward:
            return None, None, None

        if openForward[0][2].id in visitedBackward:
            intercept = openForward[0][2]
            break

        if openBackward[0][2].id in visitedForward:
            intercept = openBackward[0][2]
            break

    best_dist = forwardDist[intercept.id] + backwardDist[intercept.id]

    while openForward:
        dist, min_node_id, min_node = hq.heappop(openForward)
        if min_node.id in backwardDist:
            new_dist = dist + backwardDist[min_node.id]
            if new_dist < best_dist:
                intercept = min_node
                best_dist = new_dist
                forwardDist[intercept.id] = dist


    weight = forwardDist[intercept.id] + backwardDist[intercept.id]

    path = calculatePath(intercept, transPosedGraph, prevDictForward, prevDictBackward)

    return path, weight, len(visitedForward) + len(visitedBackward)



def calculatePath(node, transPosedgraph, prevDictForward, prevDictBackward):
    path = []

    forwardNode = node
    while forwardNode is not None:
        path.append(forwardNode)
        forwardNode = prevDictForward.get(forwardNode.id, None)

    backwardPath = []
    backwardNode = transPosedgraph.nodeList[node.id]
    while backwardNode is not None:
        backwardPath.append(backwardNode)
        backwardNode = prevDictBackward.get(backwardNode.id, None)

    completePath = path[::-1] + backwardPath[1:]
    return completePath
