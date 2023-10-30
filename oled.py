#!/usr/bin/python3
"""Start file for Werkstattradio OLED controller"""
import asyncio
import signal
import sys
import os
import time

from subprocess import call

import integrations.functions as fn


import settings

######
from datetime import datetime
###########################
settings.screenpower = True
settings.shutdown_reason = "changeme"
settings.lastinput = datetime.now()


from integrations.logging import *

if settings.DISPLAY_DRIVER == "ST7789":
    import integrations.display.st7789 as idisplay
elif settings.DISPLAY_DRIVER == "ssd1351":
    import integrations.display.ssd1351 as idisplay
elif settings.DISPLAY_DRIVER == "sh1106":
    import integrations.display.sh1106 as idisplay
elif settings.DISPLAY_DRIVER == "emulated":
    import integrations.display.emulated as idisplay
else:
    raise Exception("no DISPLAY")

idisplay.set_fonts()


from ui.windowmanager import WindowManager
import windows.idle
import windows.mainmenu
import windows.shutdownmenu
import windows.start
import windows.ende
import windows.hostapd

#Systemd exit
def gracefulexit(signum, frame):
    sys.exit(0)
signal.signal(signal.SIGTERM, gracefulexit)

def main():
    loop = asyncio.get_event_loop()

    #shutdown reason default
    settings.shutdown_reason = settings.SR1

    #Display = real hardware or emulator (depending on settings)
    display = idisplay.get_display()

    #screen = windowmanager
    windowmanager = WindowManager(loop, display)

    #Software integrations
    #Rotary encoder setup
    def turn_callback(direction,_key=False):
        windowmanager.turn_callback(direction, key=_key)

    def push_callback(_lp=False):
        windowmanager.push_callback(lp=_lp)


    ###GPICase
    if "gpicase" in settings.INPUTS:
        from integrations.inputs.gpicase import pygameInput

        print ("Using pyGameInput")
        mypygame = pygameInput(loop, turn_callback, push_callback,windowmanager)

    #Import all window classes and generate objects of them
    loadedwins = []
    idlescreen = windows.idle.Idle(windowmanager,loop)
    shutdownscreen = windows.shutdownmenu.Shutdownmenu(windowmanager, loop, "Powermenü")
    loadedwins.append(idlescreen)
    loadedwins.append(windows.mainmenu.Mainmenu(windowmanager,loop,"Hauptmenü"))
    loadedwins.append(windows.ende.Ende(windowmanager,"ende"))
    loadedwins.append(windows.hostapd.Hostapd(windowmanager))
    loadedwins.append(shutdownscreen)

    loadedwins.append(windows.start.Start(windowmanager))
    for window in loadedwins:
        windowmanager.add_window(window.__class__.__name__.lower(), window)

    #Load start window

    windowmanager.set_window("start")


    #init Inputs


    #### pirateaudio init
    if "waveshare" in settings.INPUTS:
        from integrations.inputs.waveshare import WaveShare
        waveshare = WaveShare(loop, turn_callback, push_callback)

# end init inputs

    ######Status LED

    ###main
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        log(lERROR,"Exiting")
    finally:
        loop.close()

    windowmanager.set_window("ende")

    if settings.shutdown_reason == settings.SR2:
        os.system("sudo poweroff")

    if settings.shutdown_reason == settings.SR3:
        os.system("sudo reboot")



if __name__ == '__main__':
    main()

    sys.exit(0)
