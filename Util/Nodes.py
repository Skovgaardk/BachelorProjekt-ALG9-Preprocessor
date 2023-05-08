
class Node:
    def __init__(self, id, lat, lon):
        self._id = id
        self._lat = lat
        self._lon = lon
        self.adjacent = {}
        self._distance = 0
        self.visited = False
        self._previous = None
        self.priority = 0
        self.heuristicDist = 0
        self.toLandmark = {}
        self.fromLandmark = {}

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, lat):
        self._lat = lat

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, lon):
        self._lon = lon

    def addNeighbor(self, id, weight):
        self.adjacent[id] = weight

    def getNeighbors(self):
        return self.adjacent.keys()

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        self._distance = distance

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, previous):
        self._previous = previous

    @property
    def heuristicDist(self):
        return self._heuristicDist

    @heuristicDist.setter
    def heuristicDist(self, heuristicDist):
        self._heuristicDist = heuristicDist

    def addToLandmark(self, landmark, distance):
        self.toLandmark[landmark] = distance

    def addFromLandmark(self, landmark, distance):
        self.fromLandmark[landmark] = distance

    def getToLandmark(self, landmark):
        return self.toLandmark[landmark]

    def getFromLandmark(self, landmark):
        return self.fromLandmark[landmark]
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])























