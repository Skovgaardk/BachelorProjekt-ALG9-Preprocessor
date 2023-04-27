import math

import Util.Nodes as Node
import Util.Graphs as Graph
import heapq as hq

from ShortestPathAlgos import Dijkstra


def findLandmarks(graph, quadrantSize=16):
    latitudes = []
    longitudes = []
    for node in graph.nodeList.values():
        latitudes.append(node.lat)
        longitudes.append(node.lon)


    sumOfLatitudes = sum(latitudes)
    sumOfLongitudes = sum(longitudes)

    meanLatitude = sumOfLatitudes / len(latitudes)
    meanLongitude = sumOfLongitudes / len(longitudes)

    #Create 16 quardrants
    quadrants = [[] for _ in range(quadrantSize)]

    angles = 360 / quadrantSize

    #Iterate through the nodes and add them to the correct quadrant
    for node in graph.nodeList.values():

        dx = node.lon - meanLongitude
        dy = node.lat - meanLatitude

        angle = math.atan2(dy, dx)

        angle = math.degrees(angle)

        if angle < 0:
            angle += 360

        index = int(angle / angles)
        quadrants[index].append(node)


    landmarks = []
    #Iterate through the quardrants and find the node with the largest distance from the center node

    maxNode = None
    for quadrant in quadrants:
        maxDistance = 0
        for node in quadrant:
            distance = math.sqrt((node.lat - meanLatitude)**2 + (node.lon - meanLongitude)**2)
            if distance > maxDistance:
                maxDistance = distance
                maxNode = node
        if maxNode is not None:
            landmarks.append(maxNode)
            maxNode = None

    return landmarks


def calculateLandmarkDistances(graph, landmarks):
    '''
    Calculate the distance from each node to each landmark
    :param graph:
    :param landmarks:
    :return:
    '''

    listOfLandmarkDistances = {landmark.id: {} for landmark in landmarks}

    transPosedGraph = Graph.transposeDiGraph(graph)

    for landmark in landmarks:
        distancesTo = DijkstraNoTarget(graph, landmark)
        distancesFrom = DijkstraNoTarget(transPosedGraph, landmark)

        landmarkDistances = (distancesTo, distancesFrom)

        listOfLandmarkDistances[landmark.id] = landmarkDistances

    return listOfLandmarkDistances

def findBestLowerBound(neighbor, landmarks, node):
    #max(d(l,u) - d(l,v), d(v,l) - d(u,l) for all l in landmarks

    bestLowerbound = -1000000
    bestLandmark = None
    for landmark in landmarks.values():
        lowerBound = max(abs(landmark[0][node.id] - landmark[0][neighbor.id]), abs(landmark[1][neighbor.id] - landmark[1][node.id]))
        if lowerBound > bestLowerbound:
            bestLowerbound = lowerBound
            bestLandmark = landmark

    return bestLandmark


def ALT(graph, start, end, landmarks):

    startNode = graph.nodeList[start.id]
    endNode = graph.nodeList[end.id]

    startNode.distance = 0

    closedSet = set()

    openSet = [(0, startNode.id, startNode)]

    fromSet = {}
    fromSet[startNode.id] = None

    gScore = {node.id: float('inf') for node in graph.nodeList.values()}
    gScore[startNode.id] = 0

    #Map every node to infinite distance
    fScoreList = {node.id: float('inf') for node in graph.nodeList.values()}
    fScoreList[startNode.id] = 0


    iteration = 0
    while openSet:

        current = hq.heappop(openSet)[2]

        if current == endNode:
            break

        closedSet.add(current)

        for neighbor, weight in current.adjacent.items():

            if neighbor in closedSet:
                continue

            landmark = findBestLowerBound(neighbor, landmarks, current)

            tentativeGScore = gScore[current.id] + weight

            ## wægt + abs(d(l,u) - d(t, l))

            fscore = tentativeGScore + abs(landmark[0][neighbor.id] - landmark[1][endNode.id])

            if not openSet or neighbor not in [node[2] for node in openSet]:
                hq.heappush(openSet, (fscore, neighbor.id, neighbor))
            elif tentativeGScore > gScore[neighbor.id]:
                continue

            fromSet[neighbor.id] = current
            gScore[neighbor.id] = tentativeGScore
            fScoreList[neighbor.id] = fscore

    return calculatePath(fromSet, endNode), gScore[endNode.id], len(closedSet)
def calculatePath(fromSet, endNode):
    path = []
    node = endNode
    while node is not None:
        path.append(node)
        node = fromSet[node.id]
    return path[::-1]

def DijkstraNoTarget(graph, startNode):
    '''
    Dijkstra without a target node, instead just calculates the distance to all nodes
    :param node:
    :return:
    '''

    startNode = graph.nodeList[startNode.id]

    queue = [(0, startNode.id, startNode)]
    visited = set()

    distanceDist = {node.id: float('inf') for node in graph.nodeList.values()}
    distanceDist[startNode.id] = 0

    while queue:
        if not queue:
            break

        min_dist, id, min_node = hq.heappop(queue)
        if min_node in visited:
            continue
        visited.add(min_node)

        for neighbor, weight in min_node.adjacent.items():
            if neighbor in visited:
                continue
            new_dist = min_dist + weight
            if new_dist < distanceDist[neighbor.id]:
                distanceDist[neighbor.id] = new_dist
                hq.heappush(queue, (new_dist, neighbor.id, neighbor))

    ## In the case where a distance is still infinity, set it to 0
    for node in graph.nodeList.values():
        if distanceDist[node.id] == float('inf'):
            distanceDist[node.id] = 0

    return distanceDist





