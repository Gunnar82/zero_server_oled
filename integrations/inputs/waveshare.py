""" Rotary encoder setup """
import asyncio
import threading
import settings # pylint: disable=import-error
import time
import integrations.functions as fn

from integrations.logging import *

try:
    #Only avaiable on Raspberry
    import RPi.GPIO as GPIO # pylint: disable=import-error
except ImportError:
    pass

class WaveShare():
    PIN_UP = 6
    PIN_DOWN = 19
    PIN_LEFT = 5
    PIN_RIGHT = 26
    PIN_KEY_1 = 21
    PIN_KEY_2 = 20
    PIN_KEY_3 = 16

    def __init__(self, loop, turn_callback, push_callback):
        self.loop = loop
        self.turn_callback = turn_callback
        self.push_callback = push_callback

        GPIO.setmode(GPIO.BCM)

        #Config for pins!
        self.lockrotary = threading.Lock() #create lock for rotary switch
        self._setup_gpio(self.PIN_UP)
        self._setup_gpio(self.PIN_DOWN)
        self._setup_gpio(self.PIN_LEFT)
        self._setup_gpio(self.PIN_RIGHT)
        self._setup_gpio(self.PIN_KEY_1)
        self._setup_gpio(self.PIN_KEY_2)
        self._setup_gpio(self.PIN_KEY_3)

        log(lINFO,"using gpiocontrol")

    def _button_press(self, *args):
        try:
            time.sleep (0.1)
            if not settings.callback_active:
                settings.callback_active = True
                key = args[0]
                log(lDEBUG,"gpiocontrol args %s"%(format(args)))

                if key == self.PIN_KEY_2:
                    self.turn_callback(0,'#')
                elif key == self.PIN_KEY_1:
                    self.push_callback()
                elif key == self.PIN_LEFT:
                    self.turn_callback(0,'left')
                elif key == self.PIN_RIGHT:
                    self.turn_callback(0,'right')
                elif key == self.PIN_DOWN:
                    self.turn_callback(0,'down')
                elif key == self.PIN_UP:
                    self.turn_callback(0,'up')
        finally:
            log(lDEBUG,"gpiocontrol: ende")
            time.sleep(0.1)
            settings.callback_active = False



    def _setup_gpio(self, pin):

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #Push Button
        GPIO.add_event_detect(pin,GPIO.RISING, callback=self._button_press, bouncetime=300)


    @staticmethod
    def cleanup():
        print("Cleaning up GPIO")
        if not settings.EMULATED:
            GPIO.cleanup()
