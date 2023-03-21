import os.path

import Util.Graphs
from Util import XMLParser, XMLhandlers, Graphs, DataManager
import Visualize
import timeit
from ShortestPathAlgos import AStar, Dijkstra

VejleMapPath = 'data/map_2.osm'
Vejle2MapPath = 'data/Vejlev2.osm'
MaltaMapPath = 'data/malta-latest.osm'

if __name__ == '__main__':
    mapToUse = MaltaMapPath
    testPath = 'data/map_2_TEST.osm'

    XMLhandlers.handleXML(mapToUse, testPath)

    print("Starting to parse new XML file")
    diGraph = XMLParser.parseXML(testPath)
    diGraph.calculateWeights()

    print("Starting to write graph to csv")
    Util.DataManager.write_DiGraph_to_csv(diGraph, 'malta_graph')

    # printVisitedOrNot = True
    #
    # dijkstraTimes = set()
    # for i in range(10):
    #     start_time = timeit.default_timer()
    #     path, visited = Dijkstra.dijkstra(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'], returnVisited=printVisitedOrNot)
    #     end_time = timeit.default_timer() - start_time
    #     dijkstraTimes.add(end_time)
    #
    # averageTime = sum(dijkstraTimes) / len(dijkstraTimes)
    #
    # aStarTimes = set()
    # for i in range(10):
    #     start_time = timeit.default_timer()
    #     path, visited = AStar.aStar(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'], returnVisited=printVisitedOrNot)
    #     end_time = timeit.default_timer() - start_time
    #     aStarTimes.add(end_time)
    #
    # averageAstarTime = sum(aStarTimes) / len(aStarTimes)
    #
    # print("Average time for Dijkstra: ", averageTime)
    # print("Average time for A*: ", averageAstarTime)


    # start_time = timeit.default_timer()
    # path, visited = AStar.aStar(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'], returnVisited=printVisitedOrNot)
    # #print("Shortest path: ")
    # pathLatLon = []
    # for node in path:
    #     #print("Node: ", node.id, " with latlon: ", node.lat, node.lon, " and distance: ", node._distance)
    #     pathLatLon.append([node.lat, node.lon])
    #
    # dist = path[-1]._distance
    # end_time = timeit.default_timer() - start_time
    #
    # print("The algorithm took: --- %s seconds ---" % end_time)
    #
    # print("Weight of path: ", dist)
    # if printVisitedOrNot:
    #     print("Visited nodes: ")
    #     print(visited)
    #
    # map = Visualize.visualize_shortest_path(pathLatLon)
    # map.render()
    # map.show_in_browser()








