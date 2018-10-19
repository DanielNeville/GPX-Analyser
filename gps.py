# XML -> gpx -> trk -> trkseg -> trkpt (s)

file_ = 'C:\\Users\\Dan\\Downloads\\16_Oct_2018_09_21_55.gpx'
import dateutil.parser, math
import xmltodict
# , ciso8601

# Specifically for 52 degrees (UK), need to add equation for generalised distances.
degree_lat = 111267.892222
degree_long = 68678

class GPX:
    def __init__(self, list_of_nodes):
        self.track = list_of_nodes
        self.totalDistance = None

    def calculateTotalDistance(self, smoothing = 1):
        if self.totalDistance is not None:
            return self.totalDistance
        distance, elevation, time = 0, 0, 0
        first = True
        for node in self.track:
            if first:
                last = node
                first = False
                continue
            distance += node.distance(last)
            elevation += node.elevation(last)
            time += node.calculateTime(last)
            last = node

        # print(distance/time)
        print(distance, elevation, time)


class GPXNode:
    def __init__(self, gpx_long, gpx_lat, gpx_alt, gpx_time):
        self.long = float(gpx_long)
        self.lat = float(gpx_lat)
        self.alt = float(gpx_alt)
        # print(self.long, self.lat, self.alt)
        self.time = gpx_time

    def __lt__(self, other):
         return self.time < other.time

    def distance(self, other, flat = True):
        def long_degree_to_metres(self, latitude):
            return degree_long
        def lat_degree_to_metres(self, latitude):
            return degree_lat
        average_lat = (other.lat + self.lat) * 0.5


        long_m = long_degree_to_metres(average_lat) * (other.long-self.long)
        lat_m = lat_degree_to_metres(average_lat) * (other.lat-self.lat)
        alt_m = (other.alt - self.alt)
        return math.sqrt(long_m ** 2 + lat_m ** 2)

    def elevation(self, other):
        return self.alt - other.alt

    def calculateTime(self, other):
        return self.time - other.time

def openFile(file):
    locs = list()
    with open(file_) as fd:
        x = xmltodict.parse(fd.read())
        points = x['gpx']['trk']['trkseg']['trkpt']
        c = 0
        for point in points:
            required = ['@lat', '@lon', 'ele', 'time']
            if not all(req in point.keys() for req in required):
                continue
            time = point['time']
            ms = dateutil.parser.parse(time).timestamp()
            locs.append(GPXNode(point['@lon'], point['@lat'], point['ele'], ms))
    locs.sort()
    return locs

if __name__ == '__main__':
    locs = openFile(file_)
    track = GPX(locs)
    track.calculateTotalDistance()
