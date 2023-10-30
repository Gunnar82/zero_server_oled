""" Start screen """
from ui.windowbase import WindowBase
from luma.core.render import canvas
from PIL import ImageFont
from datetime import datetime

import settings, colors, symbols

from integrations.logging import *


class Start(WindowBase):
    font = ImageFont.truetype(settings.FONT_TEXT, size=settings.FONT_SIZE_NORMAL)
    fontawesome = ImageFont.truetype(settings.FONT_ICONS, size=settings.FONT_SIZE_XXL)

    def __init__(self, windowmanager):
        super().__init__(windowmanager)
        self.timeout = False
        self.startup = datetime.now()
        self.conrasthandle = False


    def render(self):
        self.set_busy("Wird gestartet...")

        color = colors.COLOR_WHITE

        self.renderbusy(symbolcolor=color, textcolor2=color)


        self.windowmanager.set_window("idle")




    def push_callback(self,lp=False):
        pass

    def turn_callback(self, direction, ud=False):
        pass
