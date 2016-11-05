import urllib2, json

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        elif hasattr(e,'reason'):
            print "We failed to reach a server"
            print "Reason: ", e.reason
        return None

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# Finds pets based on zipcode, the type of animal (barnyard, bird, cat, dog, horse, pig, reptile, smallfurry),
# and the age of the animal (Baby, Young, Adult, Senior). Asks for a number of results to display 
# and the description type (basic or full) for each result. Returns a dictionary of the results.
def findPet(zipcode, animal, age, numResults, description):
    baseurl = "http://api.petfinder.com/"
    method = "pet.find"
    f = "format=json"
    key = "key=b77c1b5d856fabf33e950557bda56381"
    arguments = "location=" + str(zipcode) + "&animal=" + animal + "&count=" + str(numResults) + "&output=" + description
    url = baseurl + method + "?" + f + "&" + key + "&" + arguments
    r = safeGet(url)
    data = json.load(r)
    return data

# Prints information about a pet (name, age, description) and shelter (phone, email, location).
def printPetInfo(result):
    nameString = result['name']['$t'].split()
    name = nameString[0].upper()
    if "-IS" in name:
        name = name.replace("-IS", "")
    print "---Pet Information---"
    print "    Name: " + name
    print "    Age: " + result['age']['$t']
    print "    Description: " + result['description']['$t']
    print "---Shelter Information---"
    print "    Phone: " + result['contact']['phone']['$t']
    print "    Email: " + result['contact']['email']['$t']
    print "    Location: " + result['contact']['city']['$t'] + ", " + result['contact']['state']['$t']
    print "\n" 
    
d = findPet(98109, "dog", "Young", 5, "basic")
pet = d['petfinder']['pets']['pet']
for i in range(len(pet)):
    print "-----RESULT " + str(i + 1) + "-----"
    printPetInfo(pet[i])
 





