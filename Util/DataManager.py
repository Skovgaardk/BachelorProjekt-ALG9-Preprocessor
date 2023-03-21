import pandas as pd
import os.path

from Util import Graphs


def write_DiGraph_to_csv(graph, filename):
    super = []

    for i, node in enumerate(graph.nodeList):
        [lat, lon] = graph.nodeList[node].lat, graph.nodeList[node].lon
        adjacent = []
        weights = []
        for neighbor, weight in graph.nodeList[node].adjacent.items():
            adjacent.append(neighbor.id)
            weights.append(weight)
        super.append([node, lat, lon, adjacent, weights])

    super = pd.DataFrame(super, columns=["Node", "lat", "lon", "adjacent", "weights"])

    directory = filename
    parent_dir = "ProcessedData"

    if not os.path.exists(parent_dir):
        os.mkdir(directory)

    file_path = os.path.join(parent_dir, filename + ".csv")

    super.to_csv(file_path, index=False)

def read_data_to_DiGraph(file_path):
    df = pd.read_csv(file_path)

    graph = Graphs.DiGraph()





