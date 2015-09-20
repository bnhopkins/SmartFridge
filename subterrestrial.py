#from SimpleCV import Camera
from clarifai.client import ClarifaiApi
from PIL import Image
from serialCom import dState

print "Welcome to Sub Terrestrial"

#inventory list
foodInTheFridge = [[0,0],[0,0],[0,0]]


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

def setFoodName():
	## impliment get choice#####
	str choice ='banana'
	#############################

def setCoord():
	"""find empty item bin number to store food item, return coordinates """
	row=0
	for rows in foodInTheFridge:
		column=1
		for items in rows:
			if items == 0:
				return [row,column]
			column= column+1
		row= row +1


def addFood():
	"""add the food tags and number to the fridge dictionary"""
	#set coordinates of food
	itemCoord=foodItemNum() #item coordinates in fridge table
	row=itemCoord[0]
	column=itemCoord[1] #column for serialCom
	#store item in list
	foodInTheFridge[itemCoord[0], column] = getChoice() # store string of food name chosen by user in the fridge inventory
	rowLetter= char(row+97) #convert row into alphabet for serialCom
	#send food item to hardware to light up place in fridge
	dState('L', rowLetter, column, 1)


def returnFridgeFoodList():
	"""return list of food available in fridge"""
	foodList=[]
	box=1
	for rows in foodInTheFridge:
		for items in rows:
			if (items!=0):
				foodList.append(item)
	return foodList

def getChoice():
	##impliment ################
	return str "banana"
	############################

def getCoord(requestedItem):
	row=0
	for rows in foodInTheFridge:
		column=1
		for items in rows:
			if items == getChoice():
				return [row,column]
			column= column+1
		row= row +1		

def removeFood(requestedItem):
	""""search for the food in the fridge and return bin number"""
	itemCoord = getCoord(requestedItem)
	row = itemCoord[0]
	column = itemCoord[1]
	foodInTheFridge[row, column] = 0
	rowLetter = char(row+97)
	dState('S',rowLetter, column,'1')


##run code- get item and remove item from fridge
addFood()
removeFood()
