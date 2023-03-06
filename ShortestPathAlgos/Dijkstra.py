import sys

import heapq as hq


def dijkstra(graph, source, target):
    copyOfGraphList = list(graph.nodeList.values())
    initSingleSource(copyOfGraphList, source)

    visited = set()

    que = [(0, source)]
    while que:
        min_dist, min_node = hq.heappop(que)
        if min_node in visited:
            continue
        visited.add(min_node)
        if min_node == target:
            break
        for adj, weight in min_node.adjacent.items():
            if adj in visited:
                continue
            relax(min_node, adj, weight, que)

    path = []
    while target is not None:
        path.append(target)
        target = target.previous
    return path[::-1]


def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node._previous = None
    source._distance = 0

def relax(min_node, adj, weight, not_visited):
    new_dist = min_node.distance + weight
    if new_dist < adj.distance:
        adj.distance = new_dist
        adj.previous = min_node
        hq.heappush(not_visited, (new_dist, adj))



