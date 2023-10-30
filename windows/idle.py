""" IDLE screen """
import datetime
import asyncio
from ui.windowbase import WindowBase
import settings, colors, symbols

from luma.core.render import canvas
from PIL import ImageFont
import os,subprocess
import RPi.GPIO as GPIO
import locale
import time
import socket

from integrations.logging import *


class Idle(WindowBase):
    bigfont = ImageFont.truetype(settings.FONT_CLOCK, size=22)
    font = ImageFont.truetype(settings.FONT_TEXT, size=settings.FONT_SIZE_NORMAL)
    fontsmall = ImageFont.truetype(settings.FONT_TEXT, size=settings.FONT_SIZE_SMALL)
    faicons = ImageFont.truetype(settings.FONT_ICONS, size=settings.FONT_SIZE_SMALL)
    faiconsbig = ImageFont.truetype(settings.FONT_ICONS, size=12)
    faiconsxl = ImageFont.truetype(settings.FONT_ICONS, size=30)
    active = False

    def __init__(self, windowmanager,loop):
        super().__init__(windowmanager)
        self.loop = loop
        self.changerender = True
        self.window_on_back = "none"
        self.timeout = False
        self.line1 = ""


    def activate(self):
        self.active = True
        self.loop.create_task(self.get_infos())


    def deactivate(self):
        self.active = False

    def render(self):
        with canvas(self.device) as draw:

            now = datetime.datetime.now()

            #####IDLE RENDER
            draw.text((1, settings.DISPLAY_HEIGHT - 2*settings.FONT_HEIGHT_NORMAL ), self.line1, font=Idle.font, fill="white")
            draw.text((1, settings.DISPLAY_HEIGHT - 3*settings.FONT_HEIGHT_NORMAL ), self.line2, font=Idle.font, fill="white")
            draw.text((1, settings.DISPLAY_HEIGHT - 4*settings.FONT_HEIGHT_NORMAL ), self.line3, font=Idle.font, fill="white")



    def push_callback(self,lp=False):
            self.windowmanager.set_window("mainmenu")


    def turn_callback(self, direction, key=None):
        print (key)


    async def get_infos(self):
        while self.loop.is_running and self.active:
            ip_address = self.get_local_ip()
            wifi = self.get_wifiname()
            hostapd = self.get_hostapd_status()

            self.line3 = "Hotpot : %s " % (hostapd)
            self.line2 = "Wifi: %s" % (wifi)
            self.line1 = "IP: %s" % (ip_address)

            await asyncio.sleep(5)

    def get_hostapd_status(self):
        try:
            output = subprocess.check_output(['sudo', 'systemctl', 'is-active', 'hostapd'])
            return str(output).split("'")[1][:-2]
        except Exception as e:
            return "n/a"


    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('192.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
 
    def get_wifiname(self):
        try:
            output = subprocess.check_output(['sudo', 'iwgetid'])
            return str(output).split('"')[1]
        except Exception as e:
            return "n/a"
