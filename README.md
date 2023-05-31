# Project Name

A brief description or introduction to your project.

## Table of Contents

- [Dependencies](#dependencies)
- [Main](#main-file)
- [OSMPreprocessor](#preprocessor-file)
- [Benchmark](#benchmark-file)


## Dependencies

You can use a `requirements.txt` file to manage the required dependencies. 

To install the dependencies, first navigate to the project directory, and then run the following command in your terminal:

```
pip install -r requirements.txt
```

## Main

The main file allows to load a processed graph into memory, such that you can run multible shortest paths algorithms in sequence.

To run the main file, run:

```
python3 Main.py
```

Your terminal will show a list of preprocessed graphs to select from, after this you chose an algorithm, as well as a start and end node.

## OSMPreprocessor

The OSMPreprocessor file allows for preprocessing and storage of OSM files. 

To use the OSMPreprocessor run:

```
python3 OSMPreprocessor.py OSMData/your-osm-file.osm
```

OSM files can be downloaded as osm.Bz2 at: https://download.geofabrik.de/

## Benchmark

The benchmark file allows for running an algorithm on a chosen graph, for a arbitrary amount of random start and stop nodes.

The command will output information about average notes visited, time to run, etc.

To use the Benchmark file, run the following:

```
python Benchmark.py ProcessedGraphs/your-processed-graph.parquet algorithm NumOfIterations
```

algorithms currently include:
* dijkstra
* Astar
* bididijkstra (bidirectional dijkstra)
* ALT
* all (runs benchmark on all algorithms)
