import osmium as osm
import os.path

ways = set()
refs = set()
nodes = set()

def handleXML(mapToUse: str, newXMLPath):
    wayHandler = StreetHandler()
    nodeHandler = NodeHandler()
    wayHandler.apply_file(mapToUse)
    nodeHandler.apply_file(mapToUse)

    if os.path.exists(newXMLPath):
        os.remove(newXMLPath)

    writer = wayWriter(newXMLPath)
    writer.apply_file(mapToUse)
    writer.close()

class Handler(osm.SimpleHandler):
    def __init__(self):
        super(Handler, self).__init__()

class StreetHandler(osm.SimpleHandler):
    def __init__(self):
        super(StreetHandler, self).__init__()


    # This method finds every highway in the map and adds it to the list of streets
    def way(self, w):
        if 'highway' not in w.tags:
            return

        highway_set = {
            'service', 'pedestrian', 'busway', 'bus_guideway', 'footway',
            'bridleway', 'corridor', 'via_ferrata', 'cycleway', 'proposed',
            'construction', 'steps', 'escape', 'raceway', 'bus_stop', 'crossing',
            'elevator', 'emergency_bay', 'emergency_access_point', 'give_way',
            'phone', 'milestone', 'passing_place', 'platform', 'rest_area',
            'services', 'speed_camera', 'stop', 'street_lamp', 'toll_gantry',
            'traffic_mirror', 'traffic_signals', 'trailhead', 'turning_circle',
            'turningloop', 'path'
        }

        if w.tags['highway'] in highway_set:
            return

        ways.add(w.id)
        # add refs id's to list
        refs.update(ref.ref for ref in w.nodes)

class NodeHandler(osm.SimpleHandler):
    def __init__(self):
        super(NodeHandler, self).__init__()

    def node(self, n):
        if n.id in refs:
            nodes.add(n.id)

class wayWriter(osm.SimpleHandler):
    # Takes params: filename to write to, list of streets
    def __init__(self, filename):
        super(wayWriter, self).__init__()
        self.writer = osm.SimpleWriter(filename)

    # Adds streets to the output file
    def way(self, w):
        if w.id in ways:

            #Remove tags such as 'name' and 'surface' from the street
            self.writer.add_way(w)

    def node(self, n):
        if n.id in refs:
            self.writer.add_node(n)

    def close(self):
        self.writer.close()



