
#from SimpleCV import Camera
from clarifai.client import ClarifaiApi
from PIL import Image

print "Welcome to Sub Terrestrial"
 
foodInTheFridge = []
# jpgdata = newFood.read()
# newFood.close()
# ##figure out gui

# ## AddFood item
# def takePicture():
# 	"""take picture of the food to add to inventory"""
# 	cam = Camera()
# 	newFood = cam.getImage()
# 	newFood.save("newFood.png")
# 	return newFood

def defineFood(newFood):
	"""Send picture to clarafai, return tags"""
	clarifai_api = ClarifaiApi() # assumes environment variables are set.
	result = clarifai_api.tag_images(newfood)
	return result

# def foodItemNum():
# 	"""find empty item bin number"""

# def addFood():
# 	"""add the food tags and number to the fridge dictionary"""
# 	foodNum = foodItemNum()
# 	foodTags = defineFood()
# 	foodInTheFridge[foodNum] = foodTags #adds the list of food to the array of items in fridge at the foodNum index




thisFood = open('banana.jpg')
im = Image.open(thisFood)
im.rotate(45).show()

print(defineFood(im))
