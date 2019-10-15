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
	for image in imagelist:
		if(time.hour <= image.time.hour):
			if(time.hour == image.time.hour):
				current_image = image
			break
		current_image = image
	return current_image



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


scheduler = sched.scheduler(time.time, time.sleep)
WALLPAPER_PATH = "/home/navis/Pictures/Wallpapers/Firewatch\ Dynamic/"
imagelist = loadXML('images.xml')

#now = datetime.datetime.now()
now = datetime.time(8)
print("NOW: " + str(now.hour) + ":" + str(now.minute))

for i in range(0, 24):
	time.sleep(1)
	now = datetime.time(i)
	print(getCurrentImage(imagelist, now))
	current_image = getCurrentImage(imagelist, now)
	setWallpaper(WALLPAPER_PATH + current_image.name)


