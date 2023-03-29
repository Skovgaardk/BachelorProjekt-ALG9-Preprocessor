import time

import pandas as pd
import os.path
import ast

from collections import defaultdict
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

        super.to_parquet(file_path, index=False)


def read_DiGrapgh_from_Parquet(filename):
    df = pd.read_parquet(filename)

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


    return graph

# def write_DiGraph_to_csv(graph, filename):
#     super = []
#
#     for i, node in enumerate(graph.nodeList):
#         [lat, lon] = graph.nodeList[node].lat, graph.nodeList[node].lon
#         adjacent = {}
#         weights = []
#         for neighbor, weight in graph.nodeList[node].adjacent.items():
#             adjacent[neighbor.id] = [neighbor.lat, neighbor.lon]
#             weights.append(weight)
#         super.append([node, lat, lon, adjacent, weights])
#
#     super = pd.DataFrame(super, columns=["Node", "lat", "lon", "adjacent", "weights"])
#
#     parent_dir = "ProcessedGraphs"
#
#     if not os.path.exists(parent_dir):
#         os.mkdir(filename)
#
#     file_path = os.path.join(parent_dir, filename + ".csv")
#
#     super.to_csv(file_path, index=False)
#
#
# def read_data_to_DiGraph(file_path):
#     df = pd.read_csv(file_path, sep=",", header=0)
#
#     graph = Graphs.DiGraph()
#
#     amountOfNeighbors = 0
#     amountOfRows = 0
#     for i, row in df.iterrows():
#         nodeId, lat, lon = row["Node"], row["lat"], row["lon"]
#         graph.addNode(nodeId, lat, lon)
#         adjacent = ast.literal_eval(row["adjacent"])
#         weights = ast.literal_eval(row["weights"])
#         amountOfNeighbors += len(adjacent)
#         for j, neighbor in enumerate(adjacent):
#             neighborId, neighborLat, neighborLon = neighbor, adjacent[neighbor][0], adjacent[neighbor][1]
#             weight = weights[j]
#             graph.addEdge(nodeId, lat, lon, neighborId, neighborLat, neighborLon, weight)
#         amountOfRows += 1
#     print("Amount of Neighbors from CSV: ", amountOfNeighbors)
#     print("Amount of rows in CSV: ", amountOfRows)
#     time.sleep(10)
#
#     return graph





