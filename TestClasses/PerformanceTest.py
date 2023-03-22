from ShortestPathAlgos import Dijkstra, AStar
import timeit

from Util import XMLhandlers, XMLParser

MaltaMapPath = 'data/malta-latest.osm'
def test_performance():

    mapToUse = MaltaMapPath
    testPath = 'data/map_2_TEST.osm'

    XMLhandlers.handleXML(mapToUse, testPath)

    printVisitedOrNot = True

    print("Starting to parse new XML file")
    diGraph = XMLParser.parseXML(testPath)
    diGraph.calculateWeights()
    dijkstraTimes = set()
    for i in range(10):
        start_time = timeit.default_timer()
        path, visited = Dijkstra.dijkstra(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'], returnVisited=printVisitedOrNot)
        end_time = timeit.default_timer() - start_time
        dijkstraTimes.add(end_time)

    averageTime = sum(dijkstraTimes) / len(dijkstraTimes)

    aStarTimes = set()
    for i in range(10):
        start_time = timeit.default_timer()
        path, visited = AStar.aStar(diGraph, diGraph.nodeList['9067296420'], diGraph.nodeList['382980629'], returnVisited=printVisitedOrNot)
        end_time = timeit.default_timer() - start_time
        aStarTimes.add(end_time)

    averageAstarTime = sum(aStarTimes) / len(aStarTimes)

    print("Average time for Dijkstra: ", averageTime)
    print("Average time for A*: ", averageAstarTime)

def main():
    test_performance()

if __name__ == "__main__":
    main()