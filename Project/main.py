import webapp2
import jinja2

import urllib, urllib2, json, os, webbrowser
import logging

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request." 
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server"
        print "Reason: ", e.reason
    return None

def petfinderREST(baseurl = 'http://api.petfinder.com/',
    method = 'pet.find',
    format = 'format=json',
    key = 'key=b77c1b5d856fabf33e950557bda56381',
    params={},
    printurl = False
    ):
    url = baseurl + method + "?" + format + "&" + key + "&" + urllib.urlencode(params)
    if printurl:
        print url
    else:
        return safeGet(url)

def getPetIDs(location, type, age, gender, size, n=25):
    result = petfinderREST(params={"location":location, "count":n, "animal":type, "age":age, "sex":gender, "size":size})
    d = json.load(result)
    pets = d['petfinder']['pets']['pet']
    petIDs = [pets[x]['id']['$t'] for x in range(n)]
    return petIDs

def getPetInfo(petID):
    result = petfinderREST(params={"id":petID},method='pet.get')
    jsonresult = result.read()
    d = json.loads(jsonresult)
    return d

class Pet():
    def __init__(self, petInfo):
        d = petInfo['petfinder']['pet']
        self.name = d['name']['$t']
        self.gender = d['sex']['$t']
        self.age = d['age']['$t']
        if type(d['breeds']['breed']) is list:
            self.breed = d['breeds']['breed'][0]['$t'] + " and " + d['breeds']['breed'][1]['$t']
        else:
            self.breed = d['breeds']['breed']['$t']
        self.size = d['size']['$t']
        self.city = d['contact']['city']['$t']
        self.id = d['id']['$t']
        if 'photos' in d['media']:
            self.photoURL = d['media']['photos']['photo'][3]['$t']
        else:
            self.photoURL = "No photo available"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #print statements don't work well
        #print "In MainHandler"
        logging.info("In MainHandler")
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

class ResponseHandler(webapp2.RequestHandler):
    def post(self):
        vals = {}
        vals['page_title']="Adoptable Pets"
        location = self.request.get('location')
        type = self.request.get('type')
        age = self.request.get('age')
        gender = self.request.get('gender')
        size = self.request.get('size')
        go = self.request.get('gobtn') 
        logging.info(location)
        logging.info(type)
        logging.info(age)
        logging.info(gender)
        logging.info(size)        
        logging.info(go)
        if location:
            # if form is filled in, display the results
            listOfIDs = getPetIDs(self.request.get('location'), self.request.get('type'), self.request.get('age'), self.request.get('gender'), self.request.get('size'), n=25)
            pets = [Pet(getPetInfo(x)) for x in listOfIDs]
            vals['urls'] = [x.photoURL for x in pets]
            vals['name'] = [x.name for x in pets]
            vals['gender'] = [x.gender for x in pets]
            vals['age'] = [x.age for x in pets]
            vals['breed'] = [x.breed for x in pets]
            vals['size'] = [x.size for x in pets]
            vals['city'] = [x.city for x in pets]
            vals['location'] = location
            vals['id'] = [x.id for x in pets]
            template = JINJA_ENVIRONMENT.get_template('results.html')
            self.response.write(template.render(vals))
            logging.info('location= '+location)
            logging.info('animal= '+type)
            logging.info('age= '+age)
            logging.info('gender= '+gender)
            logging.info('size= '+size)
            logging.info(vals['urls'])
        else:
            #if not, then show the form again with a correction to the user
            vals['prompt'] = "Please enter a zipcode."
            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(vals))
    

# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/results', ResponseHandler),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)
