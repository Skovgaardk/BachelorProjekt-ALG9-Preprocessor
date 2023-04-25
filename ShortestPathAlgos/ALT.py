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

    print("meanLatitude: ", meanLatitude)
    print("meanLongitude: ", meanLongitude)

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
        print("index: ", index)
        quadrants[index].append(node)


    landmarks = []
    #Iterate through the quardrants and find the node with the largest distance from the center node

    print("quadrants: ")
    i = 0
    for quadrant in quadrants:
        print("Quadrant: ", i)
        for node in quadrant:
            print(node.id)
        i += 1  # for quardrant in [quadrants]:


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
    for landmark in landmarks:
        landmarkDistance = {}
        for node in graph.nodeList.values():
            distance = Dijkstra.dijkstra(graph, graph.nodeList[landmark.id], graph.nodeList[node.id])[1]
            if distance is None:
                distance = float('inf')
            landmarkDistance[node.id] = distance

        listOfLandmarkDistances[landmark.id] = landmarkDistance

    return listOfLandmarkDistances

def greedyHeuristic(node1, node2):
    '''
    Heuristic function for the A* algorithm
    :param node1:
    :param node2:
    :return:
    '''
    return math.sqrt((node1.lat - node2.lat)**2 + (node1.lon - node2.lon)**2)



def ALT(graph, start, end, landmarks):


    startNode = graph.nodeList[start.id]
    endNode = graph.nodeList[end.id]

    closedSet = set()

    openSet = [(0, startNode)]

    fromSet = {}

    gScore = {}
    gScore[startNode.id] = 0

    #Map every node to infinite distance
    fScore = {node.id: float('inf') for node in graph.nodeList.values()}
    fScore[startNode.id] = greedyHeuristic(startNode, endNode)


    while openSet:

        current = hq.heappop(openSet)[1]

        if current == endNode:
            break

        closedSet.add(current)

        for neighbor, weight in current.adjacent.items():

            if neighbor in closedSet:
                continue

            tentativeGScore = gScore[current.id] + weight + getLandMarkDist(current, neighbor, landmarks, weight)

            if neighbor not in openSet:
                openSet.append((tentativeGScore + greedyHeuristic(neighbor, endNode), neighbor))
            elif tentativeGScore >= gScore[neighbor.id]:
                continue

            fromSet[neighbor.id] = current
            gScore[neighbor.id] = tentativeGScore
            fScore[neighbor.id] = gScore[neighbor.id] + greedyHeuristic(neighbor, endNode)



    return calculatePath(fromSet, endNode), gScore[endNode.id], len(closedSet)



def getLandMarkDist(node1, node2, landmarks, weight):
    '''
    Calculate the distance between two nodes using the landmarks and triangle inequality
    :param node1:
    :param node2:
    :param landmarks:
    :return:
    '''

    bestFscore = float('inf')
    for landmark in landmarks.values():
        print("landmark: ", landmark)
        fScore = landmark[node1.id] + landmark[node2.id] - weight
        if fScore < bestFscore:
            bestFscore = fScore

    return bestFscore

def calculatePath(fromSet, current):
    totalPath = [current]
    while fromSet[current.id] is not None:
        current = fromSet[current.id]
        totalPath.append(current)

    return totalPath[::-1]







