""" Shutdown menu """
from ui.menubase import MenuBase
from luma.core.render import canvas
from PIL import ImageFont
import settings, colors
import os

from integrations.logging import *
import time
import asyncio

 
class Mountmenu(MenuBase):


    def __init__(self, windowmanager,loop,title):
        super().__init__(windowmanager,loop,title)
        self.loop = loop
        self.descr.append(["mount NAS", "\uf07b"])
        self.descr.append(["umount nas", "\uf114"])
        self.descr.append(["link NAS", "\uf115"])
        self.descr.append(["link USB", "\uf115"])
        self.descr.append(["start hostapd", "\uf115"])
        self.descr.append(["stop hostapd", "\uf115"])


    def deactivate(self):
        print ("ende")

    async def push_handler(self):
        await asyncio.sleep(1)
        if self.counter == 1:
            os.system ("sudo mount 192.168.8.21:/nfs/Audio /media/nas/")
            os.system ("sudo rm /media/gunnar/")

        elif self.counter == 2:
            os.system ("sudo umount /media/nas/")
        elif self.counter == 3:
            os.system ("sudo rm /media/gunnar")
            os.system ("sudo ln -s /media/nas /media/gunnar")
        elif self.counter == 4:
            os.system ("sudo rm /media/gunnar")
            os.system ("sudo ln -s /media/usb /media/gunnar")
        elif self.counter == 5:
            os.system ("sudo /usr/bin/autohotspotN startap")
        elif self.counter == 6:
            os.system ("sudo /usr/bin/autohotspotN stopap")
        time.sleep(2)


