import osmium as osm
import xml.etree.ElementTree as ET

import osmium.io

ways = []
refs = []
nodes = []
bounds = []

class Handler(osm.SimpleHandler):
    def __init__(self):
        super(Handler, self).__init__()

class StreetHandler(osm.SimpleHandler):
    def __init__(self):
        super(StreetHandler, self).__init__()


    # This method finds every highway in the map and adds it to the list of streets
    def way(self, w):
        if 'highway' in w.tags:

            #Check if the street is a driveway
            isDriveway = w.tags.get('highway') == 'service' and w.tags.get('service') == 'driveway'
            isPedestrian = w.tags.get('highway') == 'pedestrian'
            isBusWay = w.tags.get('highway') == 'busway'
            isBusGuideway = w.tags.get('highway') == 'bus_guideway'
            isFootway = w.tags.get('highway') == 'footway'
            isBridleway = w.tags.get('highway') == 'bridleway'
            isCorridor = w.tags.get('highway') == 'corridor'
            isViaFerrata = w.tags.get('highway') == 'via_ferrata'
            isCycleway = w.tags.get('highway') == 'cycleway'
            isProposed = w.tags.get('highway') == 'proposed'
            isConstruction = w.tags.get('highway') == 'construction'
            notInterested = [isDriveway, isPedestrian, isBusWay, isBusGuideway, isFootway, isBridleway, isCorridor, isViaFerrata, isCycleway, isProposed, isConstruction]
            if any(notInterested):
                return

            ways.append(w.id)
            # add refs id's to list
            for ref in w.nodes:
                refs.append(ref.ref)

class NodeHandler(osm.SimpleHandler):
    def __init__(self):
        super(NodeHandler, self).__init__()

    def node(self, n):
        if n.id in refs:
            nodes.append(n.id)

class ChangeSetHandler(osm.SimpleHandler):
    def __init__(self):
        super(ChangeSetHandler, self).__init__()

    def changeset(self, c):
        print(c.bounds)
        bounds.append(c.bounds)

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









        # root = ET.Element('osm')
        # root.set('version', '0.6')
        # root.set('generator', 'osmium')
        # for street in self.streets:
        #     way_elem = ET.SubElement(root, 'way')
        #     way_elem.set('id', str(street['id']))
        #
        #     # tags is of type osmium.osm.TagList
        #     # convert to list of tuples
        #     tags = [(tag.k, tag.v) for tag in street['tags']]
        #
        #     for key, value in tags:
        #         tag_elem = ET.SubElement(way_elem, 'tag')
        #         tag_elem.set('k', key)
        #         tag_elem.set('v', value)
        #     for node in street['nodes']:
        #         nd_elem = ET.SubElement(way_elem, 'nd')
        #         nd_elem.set('ref', str(node))
        #
        # tree = ET.ElementTree(root)
        # tree.write(self.output_filename)








