"""
    A* algorithm som beskrevet i bogen:
    A classic goal-directed shortest path algorithm is A* search. It
    uses a potential function π : V → R on the vertices, which is a lower bound on
    the distance dist(u, t) from u to t. It then runs a modified version of Dijkstra’s
    algorithm in which the priority of a vertex u is set to dist(s, u) + π(u). This
    causes vertices that are closer to the target t to be scanned earlier during the
    algorithm.

"""

import heapq as hq
from math import sin, cos, sqrt, atan2, radians


def aStar(graph, source, target, heuristic = "euclidean"):
    initSingleSource(graph.nodeList.values(), source)

    # Calculate f value for start vertex(f = g + h) hvor g = 0. f = 16
    source.heuristicDist = calculateHeuristicDist(source, target, heuristic)

    openList = [(source.heuristicDist, 0, source)]
    openListSetId = {source.id}
    closedListSetId = set()

    visited = set()

    # While current vertex is not the destination vertex
    iteration = 0
    while True:

        # If openList is empty, then there is no path from source to target
        if not openList:
            return None, None, None

        _, _,  min_node = hq.heappop(openList)
        visited.add(min_node)
        openListSetId.remove(min_node.id)

        closedListSetId.add(min_node.id)
        iteration += 1

        if min_node == target:
            break

        for adj, weight in min_node.adjacent.items():
            if adj.id in closedListSetId:
                continue

            # Calculate g value for current vertex(g = min_node.distance + weight)
            g = min_node.distance + weight

            if adj.id not in openListSetId:
                adj.heuristicDist = calculateHeuristicDist(adj, target, heuristic)
                adj._distance = g
                adj._previous = min_node
                f = g + adj.heuristicDist
                hq.heappush(openList, (f, adj.id, adj))
                openListSetId.add(adj.id)

            else:
                if g < adj.distance:
                    adj.distance = g
                    adj.previous = min_node
                    f = g + adj.heuristicDist
                    for i, (fValue, id, node) in enumerate(openList):
                        if id == adj.id:
                            openList[i] = (f, adj.id, adj)
                            hq.heapify(openList)
                            break

            # if adj.id == target.id:
            #     adj._distance = min_node._distance + weight
            #     adj._previous = min_node
            #     path = calculatePath(target)
            #     return path, len(closedListSetId)

    weight = target.distance

    return calculatePath(target), weight, len(visited)


def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node.heuristicDist = 0
        node._previous = None
    source._distance = 0

def calculateHeuristicDist(source, target, heuristic):
    # Calculate heuristic distance of vertex to destination vertex as grid
    if heuristic == "grid":
        HeuristicDist = abs(source.lat - target.lat) + abs(source.lon - target.lon)
        return HeuristicDist
    elif heuristic == "euclidean":
        lat1, lon1 = source.lat, source.lon
        lat2, lon2 = target.lat, target.lon

        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c
    elif heuristic == "greedy":
        dx = abs(source.lat - target.lat)
        dy = abs(source.lon - target.lon)
        return sqrt(dx * dx + dy * dy)



def calculatePath(target):
    path = []
    while target is not None:
        path.append(target)
        target = target.previous
    return path[::-1]
