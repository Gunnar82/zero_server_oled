""" Start screen """
from ui.windowbase import WindowBase
from luma.core.render import canvas
from PIL import ImageFont
import settings, colors

from datetime import datetime

class Ende(WindowBase):

    def __init__(self,windowmanager,title):
        super().__init__(windowmanager)
        self.font = ImageFont.truetype(settings.FONT_TEXT, size=settings.FONT_SIZE_L)
        self.fontawesome = ImageFont.truetype(settings.FONT_ICONS, size=settings.FONT_SIZE_XXL)

    def activate(self):
        self.set_busy("wird getestet","\uf011",settings.shutdown_reason)
        self.renderbusy()