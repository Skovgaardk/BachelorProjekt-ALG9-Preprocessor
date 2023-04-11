import os
import timeit

import Util.Graphs
from ShortestPathAlgos import Dijkstra, AStar, BiDiDijstra
from Util import DataManager
from Visualize import visualize_path


def runAlgorithm(algorithm, diGraph, startNode, endNode):
    if algorithm == "Dijkstra":
        startTime2 = timeit.default_timer()
        path, weight, visited = Dijkstra.dijkstra(diGraph, diGraph.nodeList[startNode], diGraph.nodeList[endNode])
        print("Time to run Dijkstra: ", timeit.default_timer() - startTime2)
    elif algorithm == "A*":
        startTime3 = timeit.default_timer()
        path, weight, visited = AStar.aStar(diGraph, diGraph.nodeList[startNode], diGraph.nodeList[endNode])
        print("Time to run A*: ", timeit.default_timer() - startTime3)
    elif algorithm == "Bidirectional Dijkstra":
        transPosedGraph = Util.Graphs.transposeDiGraph(diGraph)
        startTime4 = timeit.default_timer()
        path, weight, visited = BiDiDijstra.biDiDijkstra(diGraph, transPosedGraph, diGraph.nodeList[startNode],
                                                         diGraph.nodeList[endNode])
        print("Time to run Bidirectional Dijkstra: ", timeit.default_timer() - startTime4)

    if path is None:
        print("No path found between the two nodes")
        return

    print("Weight of path: ", weight)
    print("Amount of visited notes:", visited)
    print("Visualizing path in browser...")
    visualize_path(path)


def RunAfterGraphLoaded():
    print("Please select a algorithm to use from the list below:")

    ListOfAlgorithms = ["Dijkstra", "A*", "Bidirectional Dijkstra"]

    lenOfAlgorithms = len(ListOfAlgorithms)
    for i in range(len(ListOfAlgorithms)):
        print(i, ": ", ListOfAlgorithms[i])
    print("Or enter ", lenOfAlgorithms, " to exit the program.")

    # Get the user's input
    userInput = input("Enter the number of the algorithm you want to use: ")

    print("You selected: ", ListOfAlgorithms[int(userInput)])


    print("please enter the start node")
    startNode = input("Enter the start node: ")
    print("please enter the end node")
    endNode = input("Enter the end node: ")

    print("Running algorithm...")
    runAlgorithm(ListOfAlgorithms[int(userInput)], diGraph, startNode, endNode)

    print("Done")

    RunAfterGraphLoaded()


if __name__ == '__main__':

    # Get the list of all files in the ProcessedGraphs folder
    listOfProcessedGraphs = os.listdir("ProcessedGraphs")

    #Remove the .parquet extension from the file names and the gitIgnore file
    listOfProcessedGraphs.remove(".gitignore")
    for i in range(len(listOfProcessedGraphs)):
        listOfProcessedGraphs[i] = listOfProcessedGraphs[i][:-8]

    print("Please select a graph to load from the list below:")
    for i in range(len(listOfProcessedGraphs)):
        print(i, ": ", listOfProcessedGraphs[i])

    # Get the user's input
    userInput = input("Enter the number of the graph you want to load: ")
    print("You selected: ", listOfProcessedGraphs[int(userInput)])

    # Load the graph
    diGraph = DataManager.read_DiGrapgh_from_Parquet("ProcessedGraphs/" + listOfProcessedGraphs[int(userInput)] + ".parquet")

    print("Graph loaded successfully")

    RunAfterGraphLoaded()










