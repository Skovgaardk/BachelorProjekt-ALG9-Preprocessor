

import Util.Nodes as Node
import Util.Graphs as Graph

def ALT(graph, start, end):


    startNode = graph.nodeList[start]

    openSet = [(startNode, 0)]
    closedSet = {}

    landmarks = findLandmarks(graph)

    return landmarks




def findLandmarks(graph):
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
    quadrants = [[] for _ in range(16)]

    #Iterate through the nodes and add them to the correct quadrant
    for node in graph.nodeList.values():
        latitude_difference = node.lat - meanLatitude
        longitude_difference = node.lon - meanLongitude




    landmarks = []
    #Iterate through the quardrants and find the node with the largest distance from the center node

    print(quadrants)

    for quardrant in [quadrants]:
        maxNode = None
        for node in quardrant:
            print("node", node)
            distance = graph.calculateDistance(meanLatitude, meanLongitude, node.lat, node.lon)
            if distance > maxDistance:
                maxDistance = distance
                maxNode = node
        landmarks.append(maxNode)


    return landmarks




