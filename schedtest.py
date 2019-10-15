import sched
import time
import dbus
import random

scheduler = sched.scheduler(time.time, time.sleep)


def print_event(filepath, plugin = 'org.kde.image'):
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
IMAGE = WALLPAPER_PATH + "N" + str(random.randint(0,5)) + ".png"

now = time.time()
print('START:', time.ctime(now))

scheduler.enterabs(now + 5, 2, print_event, (IMAGE,))
scheduler.run()