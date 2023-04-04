import sys

import heapq as hq





def dijkstra(graph, source, target):


    initSingleSource(graph.nodeList.values(), source)

    visited = set()

    queue = [(0, source)]
    while True:

        # the queue is empty, there is no path
        if not queue:
            return None, None, None

        min_dist, min_node = hq.heappop(queue)
        if min_node in visited:
            continue
        visited.add(min_node)
        if min_node == target:
            break
        for adj, weight in min_node.adjacent.items():
            if adj in visited:
                continue
            relax(min_node, adj, weight, queue)

    weight = target.distance

    return calculatePath(target), weight, len(visited)


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


def calculatePath(target):
    path = []
    while target is not None:
        path.append(target)
        target = target.previous
    return path[::-1]


