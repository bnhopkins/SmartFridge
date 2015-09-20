#!/usr/bin/python2.4

import cherrypy
import cgi
import tempfile
import os
from clarifai.client import ClarifaiApi
from PIL import Image
import serial # must install serial lib: $pip install pyserial
import time
#serArduino = serial.Serial('/dev/tty.usbmodem1421', 9600)

__author__ = "Ex Vito"




cherrypy.config.update({
                        'server.socket_port': 8000,
                       })

foodInTheFridge = [['','banana'],['',''],['','']]
tags=[]

# def dState(device,row,col,state): # Changes device states
#     serArduino.write("*"+device+row+col+state+"#")

def defineFood(fooditem):
	"""Send picture to clarafai, return tags"""
	tags=[]
	clarifai_api = ClarifaiApi(app_id='tbndTvx-Mv_OGD4CKeOhPap1gfAFSSWDUzPT2X6x', app_secret='JQNnSLBftBwJLMkNtIsdhUdU7OQ0a5HZDKLdPTtR') # assumes environment variables are set.
	result = clarifai_api.tag_images(fooditem)
	#parse result
	i=0
	while (i<len(result[u'results'][0][u'result'][u'tag'][u'classes'])):
		tags.append(result[u'results'][0][u'result'][u'tag'][u'classes'][i])
		i=i+1
	return tags



def setCoord():
	"""find empty item bin number to store food item, return coordinates """
	row=0
	for rows in foodInTheFridge:
		column=1
		for items in rows:
			if items == '':
				#return coordinates of first empty bin
				return [row,column]
			column= column+1
		row= row +1



def addFood(foodname):
	"""add the food tags and number to the fridge dictionary"""
	#set coordinates of food
	itemCoord=setCoord() #item coordinates in fridge table
	print(itemCoord)
	print(itemCoord)
	row=itemCoord[0]
	column=itemCoord[1] #column for serialCom
	#store item in list
	foodInTheFridge[row][column] = foodname # store string of food name chosen by user in the fridge inventory
	# rowLetter= char(row+97) #convert row into alphabet for serialCom
	#send food item to hardware to light up place in fridge
	# dState('L', rowLetter, column, 1)
	# #turn light off
	# time.sleep(10)
	# dState('L', rowLetter, column, 0)


def fridgeFoodList():
	"""return list of food available in fridge"""
	foodList=[]
	bin=1 #bin identifier
	for rows in foodInTheFridge:
		for items in rows:
			foodList.append([bin, items])
			bin= bin+1
	return foodList

def getCoord(requestedItem):
	row=0
	for rows in foodInTheFridge:
		column=0
		for items in rows:
			if items == requestedItem:
				return [row,column]
			column= column+1
		row= row +1

def removeFood(requestedItem):
	""""search for the food in the fridge and return bin number"""
	itemCoord = getCoord(requestedItem)
	row = itemCoord[0]
	column = itemCoord[1]
	foodInTheFridge[row][column] = ''
	# rowLetter = char(row+97)
	# dState('S',rowLetter, column,'1')
	# #turn light off
	# time.sleep(10)
	# dState('s', rowLetter, column, 0)

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
              <button type="submit" name="answer" value="'''+tags[1]+'''">'''+tags[1]+'''</button>
              <button type="submit" name="answer" value="'''+tags[2]+'''">'''+tags[2]+'''</button>
              <button type="submit" name="answer" value="'''+tags[3]+'''">'''+tags[3]+'''</button>
              <button type="submit" name="answer" value="'''+tags[4]+'''">'''+tags[4]+'''</button>
              <button type="submit" name="answer" value="'''+tags[5]+'''">'''+tags[5]+'''</button>
              <input type="text" name="answer">
              <input type="submit" value="Add custom tag.">
        </form>


        </body>
        </html>
        '''
    @cherrypy.expose
    def generate(self, answer):
        if type(answer) is list:
            answer = answer[0]
        addFood(answer)
        return '''
        <!doctype html>
        <html lang="en">
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

        </head>
        <body>
        <p>You added '''+str(answer[0])+''' to the inventory!</p>
        <a href="http://localhost:8000">Add Additional Items</a>
        <a href="http://localhost:8000/retrieve">Retrieve Items</a>
        </body>
        </html>
        '''


    @cherrypy.expose
    def retrieve(self):
        cont = fridgeFoodList()
        print(str(cont))
        return '''
        <!doctype html>
        <html lang="en">
        <head>
        </head>
        <body>
        <form method="get" action="getfromfridge">
              <button type="submit" name="answer" value="'''+cont[0][1]+'''">'''+cont[0][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[1][1]+'''">'''+cont[1][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[2][1]+'''">'''+cont[2][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[3][1]+'''">'''+cont[3][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[4][1]+'''">'''+cont[4][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[5][1]+'''">'''+cont[5][1]+'''</button>
        </form>

        </body>
        </html>
        '''
    @cherrypy.expose
    def getfromfridge(self, answer):
        removeFood(answer)
        cont = fridgeFoodList()
        return '''
        <!doctype html>
        <html lang="en">
        <head>
        </head>
        <body>
        <form method="get" action="getfromfridge">
              <button type="submit" name="answer" value="'''+cont[0][1]+'''">'''+cont[0][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[1][1]+'''">'''+cont[1][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[2][1]+'''">'''+cont[2][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[3][1]+'''">'''+cont[3][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[4][1]+'''">'''+cont[4][1]+'''</button>
              <button type="submit" name="answer" value="'''+cont[5][1]+'''">'''+cont[5][1]+'''</button>
        </form>

        </body>
        </html>
        '''

# remove any limit on the request body size; cherrypy's default is 100MB
# (maybe we should just increase it ?)
cherrypy.server.max_request_body_size = 0

# increase server socket timeout to 60s; we are more tolerant of bad
# quality client-server connections (cherrypy's defult is 10s)
cherrypy.server.socket_timeout = 60

cherrypy.quickstart(fileUpload())
