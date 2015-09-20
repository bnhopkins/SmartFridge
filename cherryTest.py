#!/usr/bin/python2.4

import cherrypy
import cgi
import tempfile
import os
from clarifai.client import ClarifaiApi
from PIL import Image


__author__ = "Ex Vito"




cherrypy.config.update({
                        'server.socket_port': 8000,
                       })

foodInTheFridge = [[0,0],[0,0],[0,0]]
tags=[]
# jpgdata = newFood.read()
# newFood.close()
# ##figure out gui

# # ## AddFood item
# def takePicture():
# 	"""take picture of the food to add to inventory"""
# 	cam = Camera()
# 	newFood = cam.getImage()
# 	newFood.save("newFood.png")
# 	return newFood

def defineFood(newfood):
	"""Send picture to clarafai, return tags"""
	tags=[]
	clarifai_api = ClarifaiApi(app_id='tbndTvx-Mv_OGD4CKeOhPap1gfAFSSWDUzPT2X6x', app_secret='JQNnSLBftBwJLMkNtIsdhUdU7OQ0a5HZDKLdPTtR') # assumes environment variables are set.
	result = clarifai_api.tag_images(newfood)
	#parse result
	i=0
	while (i<len(result[u'results'][0][u'result'][u'tag'][u'classes'])):
		tags.append(result[u'results'][0][u'result'][u'tag'][u'classes'][i])
		i=i+1
	return tags

# def foodItemNum():
# 	"""find empty item bin number"""
# 	row=0
# 	for rows in foodInTheFridge:
# 		column=1
# 		for items in rows:
# 			if items == 0;
# 				return [column,row]
# 			column++
# 		row++


# def addFood():
# 	"""add the food tags and number to the fridge dictionary"""
# 	foodNum = foodItemNum()
# 	foodTags = defineFood()
# 	foodInTheFridge[foodNum] = foodTags #adds the list of food to the array of items in fridge at the foodNum index

def returnFridgeFoodList():
	"""return list of food available in fridge"""

#def getFood():
#	""""search for the food in the fridge and return bin number"""

class myFieldStorage(cgi.FieldStorage):
    """Our version uses a named temporary file instead of the default
    non-named file; keeping it visibile (named), allows us to create a
    2nd link after the upload is done, thus avoiding the overhead of
    making a copy to the destination filename."""

    def make_file(self, binary=None):
        return tempfile.NamedTemporaryFile()


def noBodyProcess():
    """Sets cherrypy.request.process_request_body = False, giving
    us direct control of the file upload destination. By default
    cherrypy loads it to memory, we are directing it to disk."""
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)


class fileUpload:
    """fileUpload cherrypy application"""

    @cherrypy.expose
    def index(self):
        """Simplest possible HTML file upload form. Note that the encoding
        type must be multipart/form-data."""

        return """
            <html>
            <body>
                <form action="upload" method="post" enctype="multipart/form-data">
                    File: <input type="file" name="theFile"/> <br/>
                    <input type="submit"/>
                </form>
            </body>
            </html>
            """

    @cherrypy.expose
    @cherrypy.tools.noBodyProcess()
    def upload(self, theFile=None):
        """upload action

        We use our variation of cgi.FieldStorage to parse the MIME
        encoded HTML form data containing the file."""

        # the file transfer can take a long time; by default cherrypy
        # limits responses to 300s; we increase it to 1h
        cherrypy.response.timeout = 3600

        # convert the header keys to lower case
        lcHDRS = {}
        for key, val in cherrypy.request.headers.iteritems():
            lcHDRS[key.lower()] = val

        # at this point we could limit the upload on content-length...
        # incomingBytes = int(lcHDRS['content-length'])

        # create our version of cgi.FieldStorage to parse the MIME encoded
        # form data where the file is contained
        formFields = myFieldStorage(fp=cherrypy.request.rfile,
                                    headers=lcHDRS,
                                    environ={'REQUEST_METHOD':'POST'},
                                    keep_blank_values=True)

        # we now create a 2nd link to the file, using the submitted
        # filename; if we renamed, there would be a failure because
        # the NamedTemporaryFile, used by our version of cgi.FieldStorage,
        # explicitly deletes the original filename
        theFile = formFields['theFile'] #/Users/brookehopkins/Desktop/SubFridge/
        os.link(theFile.file.name, '/Users/maslo/Desktop/SubFridge/'+theFile.filename)
        thisFood = open(theFile.filename)
        im = Image.open(thisFood)
        im.rotate(45).show()

        tags = defineFood(thisFood)

        return '''
        <!doctype html>
        <html lang="en">
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

        </head>
        <body>
        <form method="get" action="generate">
              <button type="submit" name="answer" value="'''+tags[0]+'''">'''+tags[0]+'''</button>
              <button type="submit" name="answer" value="'''+tags[1]+'''">'''+tags[0]+'''</button>
              <button type="submit" name="answer" value="'''+tags[2]+'''">'''+tags[0]+'''</button>
              <button type="submit" name="answer" value="'''+tags[3]+'''">'''+tags[0]+'''</button>
              <button type="submit" name="answer" value="'''+tags[4]+'''">'''+tags[0]+'''</button>
              <button type="submit" name="answer" value="'''+tags[5]+'''">'''+tags[0]+'''</button>
              <input type="text" name="answer">
              <input type="submit" value="Add custom tag.">
        </form>


        </body>
        </html>
        '''
    @cherrypy.expose
    def generate(self, answer):
        return '''
        <!doctype html>
        <html lang="en">
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

        </head>
        <body>
        <p>You added'''+str(answer[0])+'''to the inventory</p>
        <div href="http://localhost:8000">Add Additional Items</div>
        <div href="http://localhost:8000/retrieve">Retrieve Items</div>
        </body>
        </html>
        '''
        ### HERE WE NEED TO ADD ANSWER TO FRIDGE

    # def retrieve(self):
    #     return '''

# remove any limit on the request body size; cherrypy's default is 100MB
# (maybe we should just increase it ?)
cherrypy.server.max_request_body_size = 0

# increase server socket timeout to 60s; we are more tolerant of bad
# quality client-server connections (cherrypy's defult is 10s)
cherrypy.server.socket_timeout = 60

cherrypy.quickstart(fileUpload())
