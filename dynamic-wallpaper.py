import sched
import time
import dbus
import random
import xml.etree.ElementTree as ET
import datetime

class Image:
	def __init__(self, name, times):
		self.name = name
		self.time = datetime.datetime.strptime(times, '%H:%M')

	def __str__(self):
		return self.name + " " + str(self.time.hour)

def loadXML(filename):
	tree = ET.parse('images.xml')
	root = tree.getroot()
	images = []

	for image in root:
		images.append(Image(image[0].text, image[1].text))

	return images

def getCurrentImage(imagelist, time):

	current_image = imagelist[-1]
	current_image_index = len(imagelist) - 1

	for index in range(0, len(imagelist)):
		if(time.hour <= imagelist[index].time.hour):
			if(time.hour == imagelist[index].time.hour):
				current_image = imagelist[index]
				current_image_index = index
			break
		current_image = imagelist[index]
		current_image_index = index

	return current_image, current_image_index

def getTimeToNextImage(image, time):
	if(time.hour > image.time.hour):
		test = 24 - time.hour + image.time.hour
	else:
		test = image.time.hour - time.hour
	
	return test

def hoursToSeconds(hour):
	return hour * 60 * 60

def setWallpaper(filepath, plugin = 'org.kde.image'):
    jscript = """
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % (plugin, plugin, filepath))


WALLPAPER_PATH = "/home/navis/Pictures/Wallpapers/Firewatch\ Dynamic/"
imagelist = loadXML('images.xml')

#now = datetime.datetime.now()
now = datetime.time(16)
print("NOW: " + str(now.hour) + ":" + str(now.minute))


'''
for i in range(0, 24):
	time.sleep(1)
	now = datetime.time(i)
	current_image, index = getCurrentImage(imagelist, now)
	print(str(now.hour) + " " + str(current_image))
	setWallpaper(WALLPAPER_PATH + current_image.name)
'''


while(True):
	now = datetime.datetime.now()
	print("NOW: " + str(now.hour) + ":" + str(now.minute))

	current_image, current_image_index = getCurrentImage(imagelist, now)
	setWallpaper(WALLPAPER_PATH + current_image.name)
	print(current_image)

	if(current_image_index == len(imagelist) - 1):
		print(imagelist[0])
		timenext = getTimeToNextImage(imagelist[0], now)
	else:
		print(imagelist[current_image_index + 1])
		timenext = getTimeToNextImage(imagelist[current_image_index + 1], now)

	print("Aspetto: " + str(timenext) + " secondi")
	time.sleep(hoursToSeconds(timenext))

