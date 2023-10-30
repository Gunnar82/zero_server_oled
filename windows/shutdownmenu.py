""" Shutdown menu """
from ui.menubase import MenuBase
from luma.core.render import canvas
from PIL import ImageFont
import settings, colors
import os

import asyncio

from integrations.functions import restart_oled, get_timeouts

class Shutdownmenu(MenuBase):

    def __init__(self, windowmanager,loop,title):
        super().__init__(windowmanager,loop,title)
        self.descr.append(["Shutdown","\uf011"])
        self.descr.append(["Reboot","\uf0e2"])

    async def push_handler(self):
        if self.counter == 1:
            settings.shutdown_reason = settings.SR2
            self.loop.stop()
        elif self.counter == 2:
            settings.shutdown_reason = settings.SR3
            self.loop.stop()
