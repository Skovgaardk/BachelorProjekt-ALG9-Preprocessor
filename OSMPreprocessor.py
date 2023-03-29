import argparse

from Util import XMLParser, XMLhandlers, Graphs, DataManager

VejleMapPath = 'OSMData/Vejle.osm'
Vejle2MapPath = 'OSMData/Vejlev2.osm'
MaltaMapPath = 'OSMData/malta-latest.osm'

VejleProcessedGraphPath = 'ProcessedGraphs/Vejle'
Vejle2ProcessedGraphPath = 'ProcessedGraphs/Vejle2'
MaltaProcessedGraphPath = 'ProcessedGraphs/Malta'

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='argparser for shortest path program')
    parser.add_argument('map', metavar='map', type=str, help='enter a map to use')

    args = parser.parse_args()

    mapToUse = args.map

    print("Map to use: ", mapToUse)
    print("Processing map to new XML file...")
    mapname = mapToUse[10:]
    mapname = mapname[:-4]
    print("Map name: ", mapname)
    XMLhandlers.handleXML(mapToUse, "ProcessedXML/" + mapname + ".xml")

    print("Parsing XML file to DiGraph...")
    diGraph = XMLParser.parseXML("ProcessedXML/" + mapname + ".xml")
    diGraph.calculateWeights()

    print("Writing DiGraph to file...")
    DataManager.write_DiGraph_to_file_Parquet(diGraph, mapname)























