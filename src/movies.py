import rdflib
from rdflib import URIRef, Namespace, Graph
import pysesame

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')

#NOT FOR STUDENTS
WILDLIFE_DOC = 'http://www.bbc.co.uk/nature/species/%s.rdf'
#NOT FOR STUDENTS
CLIPS_QUERY = 'PREFIX po: <http://purl.org/ontology/po/> SELECT ?clip WHERE { ?clip a po:Clip. }'
#NOT FOR STUDENTS
GET_DBPEDIA_URI = 'SELECT ?dbp WHERE { <%s> skos:closeMatch ?dbp. }'

def findMoviesByAnimal(animal):
    """
    @return: list of movies about a given animal
    """
#    print 'Looking for movies about animal: %s' % (animal)
    graph = getWildlifeData(animal)
    if graph != None:
        result = graph.query(CLIPS_QUERY)
        resultList = [x for x in result]
#        print 'Next movies have been found: %s' % (resultList)
        return resultList
    else:
#        print 'No movies have been found'
        return []

def getWildlifeData(animal):
    """
    @return: graph with data about an an animal or None
    """
    graph = Graph()
    try:
        graph.parse( getWlDocUrl(animal) )
    except:
        return None
    return graph

def getWlDocUrl(animal):
    """
    @return: URL of a document, describing a given animal
    """
    dbpId = getDbpediaId(animal) 
    return WILDLIFE_DOC % (dbpId)

def getDbpediaId(animal):
    """
    @return: dbpedia id for a given animal
    """
    dbpUri = getDbpediaUri(animal)
    sIndex = dbpUri.rfind('/')
    return dbpUri[sIndex+1:]

def getDbpediaUri(animal):
    """
    @return: dbpedia uri for a given animal
    """
    res = pysesame.connection.query(
        GET_DBPEDIA_URI % (animal))
    
    uris = ( URIRef(x['dbp']['value']) for x in res)
    for uri in uris:
        if str(uri).startswith('http://dbpedia.org/resource/'):
            return uri
    
    raise "No Dbpedia uri found"

#NOT FOR STUDENTS
if __name__ == '__main__':
    for clip in findMoviesByAnimal('http://lod.geospecies.org/ses/diuwP'):
        print clip
