import sys
from urllib import quote_plus
from urllib2 import Request, urlopen
from json import loads

HOST = 'localhost'
REPOSITORY = 'master'

SESAME = 'http://%s:8080/sesame/' % (HOST)
HEADERS = {"Accept": "application/sparql-results+json"}

class Connection:
    def __init__(self,url):
        self.baseurl=url
        self.sparql_prefix=""
    
    def addnamespace(self,id,ns):
        self.sparql_prefix+='PREFIX %s:<%s>\n' % (id,ns)
    
    def __getsparql__(self,method):
        url = self.baseurl+method
        req = Request(url, headers=HEADERS)
        data= urlopen(req).read()
        try:
            result=loads(data)['results']['bindings']
            return result
        except:
            return [{'error':data}];
    
    def repositories(self):
        return self.__getsparql__('repositories')
        
    def use_repository(self,r):
        self.repository=r
    
    def query(self,q):
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        return self.__getsparql__(q)

connection = Connection('http://localhost:8080/sesame/')
connection.use_repository(REPOSITORY)
connection.addnamespace('gso','http://rdf.geospecies.org/ont/geospecies#')
connection.addnamespace('skos','http://www.w3.org/2004/02/skos/core#')
connection.addnamespace('owl','http://www.w3.org/2002/07/owl#')

#NOT FOR STUDENTS
if __name__=='__main__':
    locationId = sys.argv[1]
    
    res = connection.query(
        'SELECT ?specie WHERE { ?specie gso:isExpectedIn <http://sws.geonames.org/5001836/> . }')
    print res
