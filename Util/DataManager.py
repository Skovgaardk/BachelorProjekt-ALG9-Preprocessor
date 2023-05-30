import pandas as pd
import os.path
import timeit

from Util import Graphs, Nodes


def write_DiGraph_to_file_Parquet(graph, filename):
        super = []

        for i, node in enumerate(graph.nodeList):
            [lat, lon] = graph.nodeList[node].lat, graph.nodeList[node].lon
            adjacent = {}
            weights = []
            for neighbor, weight in graph.nodeList[node].adjacent.items():
                adjacent[neighbor.id] = [neighbor.lat, neighbor.lon]
                weights.append(weight)
            super.append([node, lat, lon, adjacent, weights])

        super = pd.DataFrame(super, columns=["Node", "lat", "lon", "adjacent", "weights"])

        parent_dir = "ProcessedGraphs"

        if not os.path.exists(parent_dir):
            os.mkdir(filename)


        file_path = os.path.join(parent_dir, filename + ".parquet")

        super.to_parquet(file_path,engine="fastparquet")



def read_DiGrapgh_from_Parquet(filename):
    start = timeit.default_timer()
    print("got here")
    df = pd.read_parquet(filename, engine="fastparquet")
    print("Time to read graph: ", timeit.default_timer() - start)

    print("Converting to graph...")
    graph = Graphs.DiGraph()

    amountOfRows = df.shape[0]
    iterator = 0
    for i, row in df.iterrows():
        nodeId, lat, lon = row["Node"], row["lat"], row["lon"]
        graph.addNode(nodeId, lat, lon)
        adjacent = row["adjacent"]
        weights = row["weights"]
        for neighbor, weight in zip(adjacent, weights):
            graph.addEdge(nodeId, lat, lon, neighbor, adjacent[neighbor][0], adjacent[neighbor][1], weight)
        # Every 10% of the data, print the progress
        if iterator % (amountOfRows // 10) == 0:
            print(f"{iterator / amountOfRows * 100:.2f}%")
        iterator += 1

    del df

    return graph





