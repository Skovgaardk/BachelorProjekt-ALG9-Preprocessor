
import sys

import heapq as hq
import time
import line_profiler

import Util.Graphs





def biDiDijkstra(graph, transPosedGraph, source, target):
    sourceNode = graph.nodeList[source.id]
    targetNode = transPosedGraph.nodeList[target.id]

    visited = set()

    openForward = [(0, source)]
    forwardDist = {source.id: 0}
    openBackward = [(0, targetNode)]
    backwardDist = {target.id: 0}

    prevDictForward = dict()
    prevDictBackward = dict()

    intercept = None
    while True:

        # the queue is empty, there is no path
        if not openForward or not openBackward:
            return None, None, None

        if openForward[0][1].id in backwardDist:
            intercept = openForward[0][1]
            break

        if openBackward[0][1].id in forwardDist:
            intercept = openBackward[0][1]
            break

        # forward search
        _, min_node = hq.heappop(openForward)
        min_node_id = min_node.id
        if min_node_id in visited:
            continue
        visited.add(min_node_id)
        for adj, weight in min_node.adjacent.items():
            new_dist = forwardDist[min_node_id] + weight
            if adj.id not in forwardDist or new_dist < forwardDist[adj.id]:
                forwardDist[adj.id] = new_dist
                prevDictForward[adj.id] = min_node
                hq.heappush(openForward, (new_dist, adj))

        # backward search
        _, min_node = hq.heappop(openBackward)
        min_node_id = min_node.id
        if min_node_id in visited:
            continue
        visited.add(min_node_id)
        for adj, weight in min_node.adjacent.items():
            new_dist = backwardDist[min_node_id] + weight
            if adj.id not in backwardDist or new_dist < backwardDist[adj.id]:
                backwardDist[adj.id] = new_dist
                prevDictBackward[adj.id] = min_node
                hq.heappush(openBackward, (new_dist, adj))

    while openForward:
        dist, min_node = hq.heappop(openForward)
        if min_node.id in backwardDist:
            new_dist = dist + backwardDist[min_node.id]
            if min_node.id not in forwardDist or new_dist < forwardDist[min_node.id] + backwardDist[min_node.id]:
                forwardDist[min_node.id] = new_dist
                min_node.previous = min_node
                intercept = min_node

    weight = forwardDist[intercept.id] + backwardDist[intercept.id]

    path = calculatePath(intercept, transPosedGraph, prevDictForward, prevDictBackward)

    return path, weight, len(visited)


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

def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node._previous = None
    source._distance = 0
