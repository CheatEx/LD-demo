import sys
from urllib import urlopen
from json import load

from rdflib import Namespace

GEONAMES = Namespace('http://sws.geonames.org/')

#NOT FOR STUDENTS
LOCATION_REQUEST = 'http://ws.geonames.org/search?name_equals=%s&maxRows=1&type=json&style=short'
#NOT FOR STUDENTS
CHILDREN_REQUEST = 'http://ws.geonames.org/childrenJSON?geonameId=%d'

def findLocations(locationName):
    """
    @return: location with a given name and all its children
    """
#    print 'Looking for location: %s' % (locationName)
    geonameId = findGeoname(locationName)
    if geonameId != None:
        result = getChildren(geonameId)
        result.append(geonameId)
        uris = map(toURI, result)
#        print 'Next locations have been found: %s' % (str(uris))
        return uris
    else:
        return None

def findGeoname(locationName):
    """
    @return: geoname id for location with a given name
    """
    request = LOCATION_REQUEST % (locationName)
    response = urlopen(request)
    data = load(response)
    resultsCount = data['totalResultsCount']
    if resultsCount == 0 :
        return None
    else:
        return data['geonames'][0]['geonameId']

def getChildren(geonameId):
    """
    @return: list of children locations ids for a given parent location
    """
    request = CHILDREN_REQUEST % (geonameId)
    response = urlopen(request)
    data = load(response)
    return [x['geonameId'] for x in data['geonames']]

def toURI(geonameId):
    """
    @return: URI for a given geoname id
    """
    return GEONAMES[str(geonameId) + '/']

#NOT FOR STUDENTS
if __name__ == '__main__':
    locationName = sys.argv[1]
    res = findLocations(locationName)
    for r in res:
        print r