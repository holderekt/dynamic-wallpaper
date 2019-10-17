import time
import dbus
import random
import xml.etree.ElementTree as ET
import datetime
import sys

class Image:
	def __init__(self, name, times):
		self.name = name
		self.time = datetime.datetime.strptime(times, '%H:%M')

	def __str__(self):
		return self.name + " " + str(self.time.hour)

def loadXML(filename):
	tree = ET.parse(filename)
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

def setWallpaper(filepath):
    script = """
    var allDesktops = desktops();
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(script % (filepath))


PATH = sys.argv[1] + "/"
imagelist = loadXML(PATH + "images.xml")

while(True):
	now = datetime.datetime.now()

	current_image, current_image_index = getCurrentImage(imagelist, now)
	setWallpaper(PATH + current_image.name)

	if(current_image_index == len(imagelist) - 1):
		timenext = getTimeToNextImage(imagelist[0], now)
	else:
		timenext = getTimeToNextImage(imagelist[current_image_index + 1], now)

	secondsWait = hoursToSeconds(timenext)
	intervals = secondsWait / 60
	time.sleep(3)
	'''
	for interval in range(0, int(intervals)):
		time.sleep(60)
		time_passed = datetime.timedelta(seconds = 60)
		new_now = datetime.datetime.now()
		now_delta = datetime.timedelta(hours = now.hour, minutes = now.minute, seconds = now.second)
		new_time_delta = datetime.timedelta(hours = new_now.hour, minutes = new_now.minute, seconds = new_now.second - 5)

		if((now_delta + time_passed) < new_time_delta):
			break
	'''
		



	

