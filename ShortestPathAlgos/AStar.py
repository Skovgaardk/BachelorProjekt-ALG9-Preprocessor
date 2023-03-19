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

def aStar(graph, source, target):
    # Initialiserer alle nodene i grafen
    copyOfGraphList = list(graph.nodeList.values())

    initSingleSource(copyOfGraphList, source)




    # Calculate heuristic distance of start vertex to destination vertex
    HeuristicDist = calculateHeristicDistAsGrid(source, target)

    # Calculate f value for start vertex(f = g + h) hvor g = 0. f = 167

    openList = [(0, source)]
    closedList = [(0, target)]

    # While current vertex is not the destination vertex
    while openList:
        print("openList: ", openList)
        smallestF, current = hq.heappop(openList)

        if current == target:
            print("current is target")
            break

        for adj, weight in current.adjacent.items():
            print("going through adjacents")
            if adj == target:
                print("adj is target")
                adj.previous = current
                adj.distance = current.distance + weight
                break
            else:
                newF = current.distance + weight + calculateHeristicDistAsGrid(adj, target)
                print("calculating newF", newF)

            if adj not in openList and adj not in closedList:
                print("adj not in openList or closedList, therefore adding to openList")
                hq.heappush(openList, (newF, adj))
                adj.previous = current
                adj.distance = current.distance + weight

            if adj in openList:
                print("adj in openList")
                # find the node in openList which has the same id as adj, and check if the f value is smaller than the new f value
                for i in range(len(openList)):
                    print("i:", i)
                    if openList[i][1] == adj:
                        print(i, "in openList is adj")
                        if openList[i][0] > newF:
                            print("newf is smaller than openList[i][0], therefore replacing with newF:", newF)
                            openList[i] = (newF, adj)
                            adj.previous = current
                            adj.distance = current.distance + weight
                        break

            elif adj in closedList:
                print("adj in closedList")
                for i in range(len(closedList)):
                    print("i:", i)
                    if closedList[i][1] == adj:
                        print(i, "in closedlist is adj")
                        if closedList[i][0] < newF:
                            print("newF is bigger therefore skipping, newF:", newF)
                            break
                        else:
                            print("newF is smaller therefore replacing, newF:", newF)
                            hq.heappush(openList, (newF, adj))
                            adj.previous = current
                            adj.distance = current.distance + weight

        hq.heappush(closedList, (smallestF, current))

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
