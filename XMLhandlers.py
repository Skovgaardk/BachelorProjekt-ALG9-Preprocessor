import osmium as osm

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

class BoxHandler(osm.SimpleHandler):
    def __init__(self):
        super(BoxHandler, self).__init__()

    def box(self, b: osm.osm.Box):
        print("Found bounding box: " + str(b) )
        bounds.append(b)

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






