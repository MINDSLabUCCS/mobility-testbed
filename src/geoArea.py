from haversine import inverse_haversine, Direction
from math import pi
import config

def calc(latlong):
	
	point = tuple(map(float, latlong.strip("\"").split(",")))

	rightPoint = inverse_haversine(point, config.osm["geoSideLen"]/2, Direction.EAST)
	leftPoint = inverse_haversine(point, config.osm["geoSideLen"]/2, Direction.WEST)

	bottomRight = inverse_haversine(rightPoint, config.osm["geoSideLen"]/2, Direction.NORTH)
	topLeft = inverse_haversine(leftPoint, config.osm["geoSideLen"]/2, Direction.SOUTH)

	bottomRight = tuple([float("{0:.4f}".format(n)) for n in bottomRight])
	topLeft = tuple([float("{0:.4f}".format(n)) for n in topLeft])

	bottomRight=(bottomRight[1], bottomRight[0])	

	topLeft=(topLeft[1], topLeft[0])	
	
	geoBounds = topLeft + bottomRight

	geoBounds = ','.join(map(str, geoBounds))
	
	return geoBounds
