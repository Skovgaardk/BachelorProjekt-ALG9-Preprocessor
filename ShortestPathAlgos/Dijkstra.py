import sys

import Util


def dijkstra(graph, source, target):
    copyOfGraphList = list(graph.nodeList.values())
    initSingleSource(copyOfGraphList, source)

    visited = set()
    while copyOfGraphList:
        min_node = None
        for node in copyOfGraphList:
            if min_node is None:
                min_node = node
            elif node.distance < min_node.distance:
                min_node = node
        copyOfGraphList.remove(min_node)
        visited.add(min_node)

        for adj, weight in min_node.adjacent.items():
            if adj not in visited:
                print("Relaxing node: ", adj.id, " with weight: ", weight)
                relax(min_node, adj, weight)

    path = []
    while target is not None:
        path.append(target)
        target = target.previous
    return path[::-1]


def initSingleSource(graph, source):
    for node in graph:
        node._distance = sys.maxsize
        node._previous = None
    source._distance = 0

def relax(min_node, adj, weight):
    new_dist = min_node.distance + weight
    if new_dist < adj.distance:
        adj.distance = new_dist
        adj.previous = min_node
