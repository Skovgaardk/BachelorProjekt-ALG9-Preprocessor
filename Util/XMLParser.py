import xml.etree.ElementTree as ET

import Util.Graphs


def parseXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    graph = Util.Graphs.DiGraph()

    nodes = {}
    for node in root.findall('./node'):
        id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[id] = (lat, lon)


    for child in root:
        if child.tag == 'way':
            refCount = 0
            refs = [ng.attrib['ref'] for ng in child.findall('./nd')]
            numOfRefs = len(refs)
            prevId, prevLat, prevLon = None, None, None


            for index, ref in enumerate(refs):
                onewayTag = child.find('./tag[@k="oneway"]')
                isOneway = onewayTag is not None and onewayTag.attrib['v'] == 'yes'

                highwayTag = child.find('./tag[@k="highway"]')
                isMotorWay = highwayTag is not None and highwayTag.attrib['v'] == 'motorway'

                junctionTag = child.find('./tag[@k="junction"]')
                isRoundAbout = junctionTag is not None and junctionTag.attrib['v'] == 'roundabout'

                if isOneway or isMotorWay or isRoundAbout:
                    lat, lon = nodes[ref]
                    graph.addNode(ref, lat, lon)
                    if 0 < index < numOfRefs:
                        graph.addEdge(prevId, prevLat, prevLon, ref, lat, lon)
                    prevId = ref
                    prevLat = lat
                    prevLon = lon
                    refCount += 1
                else:
                    lat, lon = nodes[ref]
                    graph.addNode(ref, lat, lon)
                    # Alt større end nul og mindre end numOfRefs tilføjer sig selv til listen af noder og sætter
                    # sig selv ind i prev, og sætter prev til sig selv
                    if 0 < index < numOfRefs:
                        graph.addEdge(prevId, prevLat, prevLon, ref, lat, lon)
                        graph.addEdge(ref, lat, lon, prevId, prevLat, prevLon)
                    prevId = ref
                    prevLat = lat
                    prevLon = lon
                    refCount += 1

    return graph