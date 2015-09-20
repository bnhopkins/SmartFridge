from SimpleCV import Camera
from clarifai.client import ClarifaiApi
from PIL import Image

print "Welcome to Sub Terrestrial"
 
foodInTheFridge = [[0,0],[0,0],[0,0]]
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
	clarifai_api = ClarifaiApi(app_id='tbndTvx-Mv_OGD4CKeOhPap1gfAFSSWDUzPT2X6x', app_secret='JQNnSLBftBwJLMkNtIsdhUdU7OQ0a5HZDKLdPTtR') # assumes environment variables are set.
	result = clarifai_api.tag_images(newfood)
	return result

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


thisFood = open('banana.jpg')
im = Image.open(thisFood)
im.rotate(45).show()

print(defineFood(thisFood))

takePicture()
