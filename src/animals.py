import sys
from rdflib import URIRef

import locations
import pysesame

#NOT FOR STUDENTS
EXPECTED_QUERY = 'SELECT ?specie WHERE { ?specie gso:isExpectedIn <%s> . }'

def findAnimalsByLocation(location):
    """
    @return: list of animals, expected in a given location
    """
#    print 'Looking for animal in location: %s' % (location)
    res=pysesame.connection.query(EXPECTED_QUERY % (location))
    
    animals = [ URIRef(x['specie']['value'])
            for x in res]
#    print 'Next animals have been found: %s' % (str(animals))
    return animals

#NOT FOR STUDENTS
if __name__ == '__main__':
    location = sys.argv[1]
    for a in findAnimalsByLocation(locations.GEONAMES[location+'/']):
        print a
