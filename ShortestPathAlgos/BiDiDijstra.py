import sys

import heapq as hq
import time

import Util.Graphs


def biDiDijkstra(graph, source, target, returnVisited=False):

    transposedGraph = Util.Graphs.transposeDiGraph(graph)

    targetNode = transposedGraph.nodeList[target.id]

    copyOfGraphList = list(graph.nodeList.values())
    transposedGraphList = list(transposedGraph.nodeList.values())

    target = transposedGraphList[transposedGraphList.index(targetNode)]

    visited = set()

    if type(source) == str:
        source = graph.nodeList[source]

    if type(target) == str:
        target = graph.nodeList[target]

    openForward = [(0, source.id, source)]
    forwardDist = {source.id: 0}
    openBackward = [(0, target.id, target)]
    backwardDist = {target.id: 0}
    print("Source", source.id, "Target", target.id)

    while True:
        if openForward[0][1] in backwardDist:
            return calculatePath(openForward[0][2], openBackward, graph, False) if not returnVisited else \
                (calculatePath(openForward[0][2], openBackward, graph, False), len(visited))

        if openBackward[0][1] in forwardDist:
            return calculatePath(openBackward[0][2], openForward, graph, True) if not returnVisited else \
                (calculatePath(openBackward[0][2], openForward, graph, True), len(visited))

        # forward search
        _, _,  min_node = hq.heappop(openForward)
        visited.add(min_node)
        min_node_index = copyOfGraphList.index(min_node)
        for adj, weight in copyOfGraphList[min_node_index].adjacent.items():
            new_dist = forwardDist[min_node.id] + weight
            if adj.id not in forwardDist or new_dist < forwardDist[adj.id]:
                forwardDist[adj.id] = new_dist
                adj.previous = min_node
                hq.heappush(openForward, (new_dist, adj.id, adj))

        # backward search
        _, _,  min_node = hq.heappop(openBackward)
        visited.add(min_node)
        for adj, weight in min_node.adjacent.items():
            relax(min_node, adj, weight, openBackward, backwardDist)


def calculatePath(node, openList, graph, isBackward):
    path = []
    while node is not None:
        path.append(node)
        node = node.previous

    backwardPath = []
    if openList:
        _, _, node = hq.heappop(openList)
        while node is not None:
            backwardPath.append(node)
            node = node.previous

    ## if it is backwards path, translate the backward path to the original graph
    if isBackward:
        for i in range(len(backwardPath)):
            backwardPath[i] = graph.nodeList[backwardPath[i].id]
    ## If it is forward path, translate the forward path to the transposed graph
    else:
        for i in range(len(path)):
            path[i] = graph.nodeList[path[i].id]

    ## print node in both paths
    # for node in path:
    #     for node2 in backwardPath:
    #         if node.id == node2.id:
    #             print("Node in both paths: ", end=' ')
    #             print(node, end=' ')
    #     print()

    print("Path: ")
    for node in path:
        print(node)


    return path[::-1] + backwardPath[1:]


