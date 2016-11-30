#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2

import urllib, urllib2, json, os, webbrowser
import logging

import flickr_key

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

def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.search',
    api_key = flickr_key.key,
    format = 'json',
    params={},
    printurl = False
    ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"]=True
    url = baseurl + "?" + urllib.urlencode(params)
    if printurl:
        print url
    else:
        return safeGet(url)

def getPhotoIDs(tag, n = 100):
    result = flickrREST(params={"tags":tag,"per_page":n})
    d = json.load(result)
    photos = d['photos']['photo']
    photoIDs = [photos[x]['id'] for x in range(n)]
    return photoIDs

def getPhotoInfo(photoID):
    result = flickrREST(params={"photo_id":photoID},method='flickr.photos.getInfo')
    jsonresult = result.read()
    d = json.loads(jsonresult)
    return d

class Photo():
    def __init__(self, photoInfo):
        d = photoInfo['photo']
        self.title = d['title']['_content']
        self.author = d['owner']['username']
        self.userid = d['owner']['nsid']
        self.tags = [d['tags']['tag'][x]['_content'] for x in range(len(d['tags']['tag']))]
        self.commentcount = int(d['comments']['_content'])
        self.numViews = int(d['views'])
        self.url = d['urls']['url'][0]['_content']
        self.thumbnailURL = "https://farm" + str(d['farm']) + ".staticflickr.com/" + d['server'] + "/" + d['id'] + "_" + d['secret'] + "_q.jpg"
        
    def __str__(self):
        s = '~~~ %s~~~\n' % self.title.encode('utf-8')
        s += 'author: %s\n' % self.author.encode('utf-8')
        s += 'number of tags: %s\n' % len(self.tags)  
        s += 'views: %s\n' % self.numViews
        s += 'comments: %s\n' % self.commentcount
        return s
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        #print statements don't work well
        #print "In MainHandler"
        logging.info("In MainHandler")
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(template_values))

class ResponseHandler(webapp2.RequestHandler):
    def post(self):
        vals = {}
        vals['page_title']="Flickr Results"
        name = self.request.get('username')
        go = self.request.get('gobtn') 
        logging.info(name)
        logging.info(go)
        if name:
            # if form is filled in, display the results
            listOfIDs = getPhotoIDs(self.request.get('username'), n=18)
            photos = [Photo(getPhotoInfo(x)) for x in listOfIDs]
            vals['urls'] = [x.thumbnailURL for x in photos]
            template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
            self.response.write(template.render(vals))
            logging.info('name= '+name)
            logging.info(vals['urls'])
        else:
            #if not, then show the form again with a correction to the user
            vals['prompt'] = "No keyword was entered. Please enter a search keyword."
            template = JINJA_ENVIRONMENT.get_template('greetform.html')
            self.response.write(template.render(vals))
    

# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/results', ResponseHandler),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)
