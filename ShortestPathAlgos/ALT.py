import math


import Util.Graphs as Graph
import heapq as hq
import random


def quadrantLandmarks(graph, amountOfLandmarks):
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
    quadrants = [[] for _ in range(amountOfLandmarks)]

    angles = 360 / amountOfLandmarks

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

    # Find node closest to the mean Latitude overall
    minDistance = 100000000
    minNode = None
    for node in graph.nodeList.values():
       distance = math.sqrt((node.lat - meanLatitude)**2 + (node.lon - meanLongitude)**2)
       if distance < minDistance:
           minDistance = distance
           minNode = node

    # Calculate the distance from the middle node to every other node
    distances = DijkstraNoTarget(graph, minNode)

    # Find the node furthest away from the middle node
    maxNode = None
    for quadrant in quadrants:
        maxDistance = 0
        for node in quadrant:
            distance = distances[node.id]
            #Need to ignore nodes where distance is infinity or 0
            if distance > maxDistance and distance != 0 and distance != float('inf'):
                maxDistance = distance
                maxNode = node
        if maxNode is not None:
            landmarks.append(maxNode)
            maxNode = None

    transPosedGraph = Graph.transposeDiGraph(graph)

    for landmark in landmarks:
        distancesFromLandmarkToNodes = DijkstraNoTarget(graph, landmark)
        distancesFromNodesToLandmark = DijkstraNoTarget(transPosedGraph, landmark)

        landmark.fromLandmark = distancesFromLandmarkToNodes
        landmark.toLandmark = distancesFromNodesToLandmark

    return landmarks


def randomLandmarks(graph, amountOfLandmarks):
    landmarks = []
    for i in range(amountOfLandmarks):
        randomNode = random.choice(list(graph.nodeList.values()))
        landmarks.append(randomNode)

    transPosedGraph = Graph.transposeDiGraph(graph)
    for landmark in landmarks:
        distancesFromLandmarkToNodes = DijkstraNoTarget(graph, landmark)
        distancesFromNodesToLandmark = DijkstraNoTarget(transPosedGraph, landmark)

        landmark.fromLandmark = distancesFromLandmarkToNodes
        landmark.toLandmark = distancesFromNodesToLandmark

    return landmarks


def farthestLandmarks(graph, amountOfLandmarks):

    transPosedGraph = Graph.transposeDiGraph(graph)

    startLandMark = random.choice(list(graph.nodeList.values()))

    landmarks = set()
    landmarks.add(startLandMark)

    startLandMark.toLandmark = DijkstraNoTarget(transPosedGraph, startLandMark)
    startLandMark.fromLandmark = DijkstraNoTarget(graph, startLandMark)

    for i in range(amountOfLandmarks):

        maxDist = 0
        maxNode = None

        for landmark in landmarks:
            toLandMarkDist = landmark.toLandmark
            for dist in toLandMarkDist.values():
                if dist > maxDist:
                    maxDist = dist
                    maxNode = landmark

        maxNode.fromLandmark = DijkstraNoTarget(graph, maxNode)
        maxNode.toLandmark = DijkstraNoTarget(transPosedGraph, maxNode)
        landmarks.add(maxNode)

    return landmarks

def findLandmarks(graph, amountOfLandmarks, heuristic="quadrants"):

    if heuristic == "quadrants":
        landmarks = quadrantLandmarks(graph, amountOfLandmarks)
        return landmarks
    elif heuristic == "random":
        landmarks = randomLandmarks(graph, amountOfLandmarks)
        return landmarks
    elif heuristic == "farthest":
        landmarks = farthestLandmarks(graph, amountOfLandmarks)
        print("landmarks returned:")
        for landmark in landmarks:
            print(landmark.id)
        return landmarks


def findBestLowerBound(node, target, landmarks):
    #max(d(l,u) - d(l,v), d(v,l) - d(u,l) for all l in landmarks

    bestLandmark = None
    maxLowerBound = float('-inf')

    for landmark in landmarks:
        lowerBound = max(
            abs(landmark.toLandmark[node.id] - landmark.toLandmark[target.id]),
            abs(landmark.fromLandmark[node.id] - landmark.fromLandmark[target.id]))
        if lowerBound > maxLowerBound:
            maxLowerBound = lowerBound
            bestLandmark = landmark

    return bestLandmark


def findThreeBestLandmarks(startNode, endNode, landmarks):

    bestLandmarks = []

    for landmark in landmarks:

        lowerBound = max(
            abs(landmark.toLandmark[startNode.id] - landmark.toLandmark[endNode.id]),
            abs(landmark.fromLandmark[endNode.id] - landmark.fromLandmark[startNode.id]))

        bestLandmarks.append((lowerBound, landmark))

    bestLandmarks.sort(key=lambda x: x[0], reverse=True)

    return [landmark[1] for landmark in bestLandmarks[:3]]


def calculateFHeuristicDistance(current, neighbor, landmarks):
    #h(u) = d(u,l) - d(s,l) for l in landmarks

    #Find the best landmark for the neighbor
    heuristicDist = float('inf')
    landmarkUsed = None
    for landmark in landmarks:
        dist = abs(landmark.toLandmark[current.id] - landmark.toLandmark[neighbor.id])
        #If the distance found is less than the current heuristic distance, update the heuristic distance
        if dist < heuristicDist:
            heuristicDist = dist
            landmarkUsed = landmark

    return heuristicDist



def ALT(graph, start, end, landmarks):

    startNode = graph.nodeList[start.id]
    endNode = graph.nodeList[end.id]

    startNode.distance = 0

    closedSet = set()

    openSet = [(0, startNode.id, startNode)]
    openSetIds = set()
    openSetIds.add(startNode.id)

    fromSet = {}
    fromSet[startNode.id] = None

    gScore = {node.id: float('inf') for node in graph.nodeList.values()}
    gScore[startNode.id] = 0

    landmarks = findThreeBestLandmarks(startNode, endNode, landmarks)

    while openSet:

        if not openSet:
            return None, None, None

        current = hq.heappop(openSet)[2]
        closedSet.add(current)

        if current.id == endNode.id:
            break

        for neighbor, weight in current.adjacent.items():

            if neighbor in closedSet:
                continue

            GScore = gScore[current.id] + weight

            if neighbor.id not in openSetIds:
                # W'(u,v) = w(u,v) + h(u) - h(v)
                heuristicDist = calculateFHeuristicDistance(current, neighbor, landmarks)
                f = GScore + heuristicDist
                gScore[neighbor.id] = GScore
                fromSet[neighbor.id] = current
                openSetIds.add(neighbor.id)
                hq.heappush(openSet, (f, neighbor.id, neighbor))

            else:
                if GScore < gScore[neighbor.id]:
                    heuristicDist = calculateFHeuristicDistance(current, neighbor, landmarks)
                    f = GScore + heuristicDist
                    gScore[neighbor.id] = GScore
                    fromSet[neighbor.id] = current
                    for i, (fValue, id, node) in enumerate(openSet):
                        if id == neighbor.id:
                            openSet[i] = (f, neighbor.id, neighbor)
                            hq.heapify(openSet)
                            break


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





