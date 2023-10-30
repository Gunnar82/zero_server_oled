""" Playlist menu """
import settings, colors
import time
import asyncio

from ui.listbase import ListBase

class Hostapd(ListBase):
    def __init__(self, windowmanager):
        super().__init__(windowmanager, "hostapd.conf")


    def activate(self):
        self.window_on_back = "idle"
        text_file = open("/etc/hostapd/hostapd.conf", "r")
        self.menu = text_file.readlines()


    def push_callback(self,lp=False):
        self.windowmanager.set_window("mainmenu")

    def on_key_left(self):
        self.windowmanager.set_window("playbackmenu")
