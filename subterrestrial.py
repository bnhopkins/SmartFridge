#from SimpleCV import Camera
from clarifai.client import ClarifaiApi
from PIL import Image
from serialCom import dState
import time



print "Welcome to Sub Terrestrial"

#inventory list
foodInTheFridge = [['',''],['','',['','']]

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
	foodInTheFridge[itemCoord[0], column] = foodname # store string of food name chosen by user in the fridge inventory
	rowLetter= char(row+97) #convert row into alphabet for serialCom
	#send add food item call to hardware to light up place in fridge
	dState('L', rowLetter, column, 1)
	#turn light off
	time.sleep(10)
	dState('L', rowLetter, column, 0)


def fridgeFoodList():
	"""return list of food available in fridge"""
	foodList=[]
	bin=1 #bin identifier
	for rows in foodInTheFridge:
		for items in rows:
			foodList.append([bin, item])
			bin= bin+1
	return foodList

def getCoord(requestedItem):
	row=0
	for rows in foodInTheFridge:
		column=1
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
	foodInTheFridge[row, column] = ''
	rowLetter = char(row+97)
	#send remove call to hardware
	dState('S',rowLetter, column,'1')
	#turn light off
	time.sleep(10)
	dState('s', rowLetter, column, 0)


##run code- get item and remove item from fridge
addFood("banana")
removeFood("banana")
