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
import random as rand
from math import sin, cos, sqrt, atan2, radians

import Util


def aStar(graph, source, target):
    # Initialiserer alle nodene i grafen
    copyOfGraphList = list(graph.nodeList.values())

    initSingleSource(copyOfGraphList, source)

    # Calculate heuristic distance of start vertex to destination vertex
    heuristicDist = calculateHeristicDistAsGrid(source, target)

    # Calculate f value for start vertex(f = g + h) hvor g = 0. f = 167

    openList = [(heuristicDist, 0, source)]
    openListSetId = set()
    openListSetId.add(source.id)
    closedList = [(0, 0, target)]
    closedListSetId = set()
    closedListSetId.add(target.id)

    # While current vertex is not the destination vertex
    iteration = 0
    while True:

        print("openList", openList, "at iteration", iteration)
        print("closedList", closedList, "at iteration", iteration)
        if len(openList) == 0:
            print("openList is None, don't think it ever come here though, cuz while stops")
            path = calculatePath(target)
            for node in path:
                print(node.id)
            return path

        length, _,  min_node = hq.heappop(openList)
        openListSetId.remove(min_node.id)
        print("length: ", length, "min_node: ", min_node)

        for adj, weight in min_node.adjacent.items():
            print("going into for loop for adjacent nodes")
            # Calculate heuristic distance of current vertex to destination vertex
            heuristicDist = calculateHeristicDistAsGrid(adj, target)
            # Calculate f value for current vertex(f = g + h)
            f = min_node.distance + weight + heuristicDist
            print("g is:", min_node.distance, "h is:", heuristicDist, "weight is", weight, "f is:", f, "adj is:", adj)

            if adj.id not in closedListSetId and adj.id not in openListSetId:
                print("adj is not in closedList or openList, push to openList")
                adj._distance = min_node.distance + weight
                adj._previous = min_node
                hq.heappush(openList, (f, adj.id, adj))
                openListSetId.add(adj.id)

            elif adj.id in openListSetId:
                    print("adj is in openList")
                    #Get the node from openList's heruistic value
                    for nodes in openList:
                        if adj in nodes:
                            print("adj is in nodes")
                            if f < nodes[0]:
                                print("f is less than nodes[0], update distance and previous and push top openList")
                                adj._distance = min_node._distance + weight
                                adj._previous = min_node
                                openList.remove((nodes[0], adj.id, adj))
                                openListSetId.remove(adj.id)
                                hq.heappush(openList, (f, adj.id, adj))
                                openListSetId.add(adj.id)
                                break

            if adj.id == target.id:
                adj._distance = min_node._distance + weight
                adj._previous = min_node
                path = calculatePath(target)
                for node in path:
                    print(node.id)
                return path
        print("last case heappush")
        hq.heappush(closedList, (length, min_node.id, min_node))
        closedListSetId.add(min_node.id)
        iteration += 1

def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node._previous = None
    source._distance = 0


def calculateHeristicDistAsGrid(source, target):
    # Calculate heuristic distance of start vertex to destination vertex
    HeuristicDist = abs(source.lat - target.lat) + abs(source.lon - target.lon)
    return HeuristicDist


def calcHeuristicDist(source, target):

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

def calculatePath(target):
    path = []
    print("calculatePath")
    print("target is:", target)
    while target is not None:
        path.append(target)
        target = target.previous
        print("new target is:", target)
    return path[::-1]
