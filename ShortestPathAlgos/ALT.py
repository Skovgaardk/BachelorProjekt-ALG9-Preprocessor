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

    landmarks = []
    unvisitedNodes = set(graph.nodeList.values())

    firstLandmark = random.choice(list(graph.nodeList.values()))
    landmarks.append(firstLandmark)
    unvisitedNodes.remove(firstLandmark)

    firstLandmark.fromLandmark = DijkstraNoTarget(graph, firstLandmark)
    firstLandmark.toLandmark = DijkstraNoTarget(transPosedGraph, firstLandmark)

    for i in range(amountOfLandmarks - 1):
        farthestNode = None
        maxDistance = 0

        for node in unvisitedNodes:
            minDistance = float('inf')
            for landmark in landmarks:
                distance = landmark.fromLandmark[node.id]
                if distance < minDistance:
                    minDistance = distance

            if minDistance > maxDistance:
                maxDistance = minDistance
                farthestNode = node


        # Edge case where there is no path to the node
        if farthestNode is None:
            farthestNode = random.choice(list(unvisitedNodes))


        farthestNode.fromLandmark = DijkstraNoTarget(graph, farthestNode)
        farthestNode.toLandmark = DijkstraNoTarget(transPosedGraph, farthestNode)
        landmarks.append(farthestNode)
        unvisitedNodes.remove(farthestNode)

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
        return landmarks
    else:
        print("No such heuristic, defaulting to quadrants")
        landmarks = quadrantLandmarks(graph, amountOfLandmarks)
        return landmarks


def findBestLowerBound(node, target, landmarks):
    #max(d(l,u) - d(l,v), d(v,l) - d(u,l) for all l in landmarks

    bestLandmark = None
    maxLowerBound = float('-inf')

    for landmark in landmarks:
        dist1 = abs(landmark.fromLandmark[node.id] - landmark.fromLandmark[target.id])
        dist2 = abs(landmark.toLandmark[target.id] - landmark.toLandmark[node.id])
        dist = max(dist1, dist2)
        if dist > maxLowerBound:
            maxLowerBound = dist
            bestLandmark = landmark

    return bestLandmark


def findThreeBestLandmarks(startNode, endNode, landmarks):

    #Check of there are more than 3 landmarks
    if len(landmarks) <= 3:
        return landmarks

    bestLandmarks = []

    for landmark in landmarks:

        lowerBound = max(
            abs(landmark.toLandmark[startNode.id] - landmark.toLandmark[endNode.id]),
            abs(landmark.fromLandmark[endNode.id] - landmark.fromLandmark[startNode.id]))

        bestLandmarks.append((lowerBound, landmark))

    bestLandmarks.sort(key=lambda x: x[0], reverse=True)

    return [landmark[1] for landmark in bestLandmarks[:3]]


def calculateFHeuristicDistance(neighbor, target, landmarks):
    #h(u) = d(u,l) - d(s,l) for l in landmarks

    #Find the best landmark for the neighbor
    heuristicDist = float('-inf')
    for landmark in landmarks:
        dist1 = landmark.toLandmark[neighbor.id] - landmark.toLandmark[target.id]
        dist2 = landmark.fromLandmark[target.id] - landmark.fromLandmark[neighbor.id]
        dist = max(dist1, dist2)
        #If the distance found is less than the current heuristic distance, update the heuristic distance
        if dist > heuristicDist:
            heuristicDist = dist

    return heuristicDist




def ALT(graph, start, end, landmarks):
    initSingleSource(graph.nodeList.values(), start)

    start.heuristic = calculateFHeuristicDistance(start, end, landmarks)

    openList = [(start.heuristic, 0, start)]
    openListSetId = {start.id}
    closedListSetId = set()

    visited = set()

    landmarks = findThreeBestLandmarks(start, end, landmarks)

    # While current vertex is not the destination vertex
    while True:

        # If openList is empty, then there is no path from source to target
        if not openList:
            return None, None, None

        _, _,  min_node = hq.heappop(openList)
        visited.add(min_node)
        openListSetId.remove(min_node.id)

        closedListSetId.add(min_node.id)

        if min_node == end:
            break

        for adj, weight in min_node.adjacent.items():
            if adj.id in closedListSetId:
                continue

            # Calculate g value for current vertex(g = min_node.distance + weight)
            g = min_node.distance + weight

            if adj.id not in openListSetId:
                adj.heuristicDist = calculateFHeuristicDistance(adj, end, landmarks)
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

    weight = end.distance

    return calculatePath(end), weight, visited


def initSingleSource(graph, source):
    for node in graph:
        node._distance = float('inf')
        node.heuristicDist = 0
        node._previous = None
    source._distance = 0

def calculatePath(target):
    path = []
    while target is not None:
        path.append(target)
        target = target.previous
    return path[::-1]

def DijkstraNoTarget(graph, startNode):
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





