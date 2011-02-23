import sys

from locations import findLocations
from animals import findAnimalsByLocation
from movies import findMoviesByAnimal

def findAnimalVideos(locationName, limit=2):
    locations = findLocations(locationName)
    animals = [animal
        for loc in locations
            for animal in findAnimalsByLocation(loc)]
    
    result = {}
    moviesCount = 0
    
    for animal in animals:
        movies = findMoviesByAnimal(animal)
        if len(movies) > 0:
            moviesCount += len(movies)
            result[animal] = findMoviesByAnimal(animal)
        
        if moviesCount > limit:
            return result
    
    return result

#NOT FOR STUDENTS
if __name__ == '__main__':
    locationName = sys.argv[1]
    result = findAnimalVideos(locationName)
    for (animal, videos) in result.items():
        print "For animal %s found videos:" % (animal)
        for video in videos:
            print '-> %s' % (video)