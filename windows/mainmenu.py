""" Main menu """
from ui.menubase import MenuBase
from luma.core.render import canvas
from PIL import ImageFont
import settings, colors, symbols

from integrations.functions import mountusb, get_folder_from_file
import asyncio

class Mainmenu(MenuBase):

    def __init__(self, windowmanager,loop,title):
        super().__init__(windowmanager,loop,title)
        self.counter = 0
        self.descr.append([ "Ausschaltmenü", "\uf011"])
        self.window_on_back = "idle"

    async def push_handler(self):
        if self.counter == 1:
            self.windowmanager.set_window("shutdownmenu")
