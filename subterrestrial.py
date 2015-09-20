#from SimpleCV import Camera
from clarifai.client import ClarifaiApi
from PIL import Image
from serialCom import dState

print "Welcome to Sub Terrestrial"
 
foodInTheFridge = [[0,0],[0,0],[0,0]]
tags=[]

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

def setFoodName():
	## impliment get choice#####
	str choice ='banana'
	#############################

def setCoord():
	"""find empty item bin number"""
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
	itemCoord=foodItemNum() #item coordinates in fridge table
	foodInTheFridge[row, column] = getChoice() # store string of food name chosen by user in the fridge inventory
	row= char(itemCoord[0]+97) #convert row into alphabet for serialCom
	column=itemCoord[1] #column for serialCom
	dState('L', row, column, 1)

def returnFridgeFoodList():
	"""return list of food available in fridge"""
	return foodInTheFridge

def getChoice():
	##impliment ################
	return str "banana"
	############################

#def removeItem();
#	"""remove item from the inventory of foodInTheFridge"""
def getCoord(requestedItem):
	row=0
	for rows in foodInTheFridge:
		column=1
		for items in rows:
			if items == getChoice():
				return [row,column]
			column= column+1
		row= row +1		

def getFood(requestedItem):
	""""search for the food in the fridge and return bin number"""
	itemCoord=
	dState('S',row,colum,)



#thisFood = open('banana.jpg')
#print(defineFood(thisFood))

foodItemNum()


#takePicture()
