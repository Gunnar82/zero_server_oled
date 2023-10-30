""" Display hardware or emulator """
import settings

def get_display():
    settings.CONTRAST_HANDLE = True

    from luma.core.interface.serial import spi

    from luma.oled.device import sh1106

    serial = spi(port=0,device=0, gpio_SCLK=11,gpio_SDA=10, gpio_DC = 24, gpio_CS = 8, gpio_RST=25, bus_speed_hz=8000000)
    device = sh1106(serial_interface=serial,rotate=2,bgf=True,active_low=False)


    device.contrast(settings.CONTRAST_FULL)
    device.cleanup = do_nothing

    print("Using real display hardware")
    return device

def do_nothing(obj):
    pass



def set_fonts():
    settings.FONT_SIZE_XXXL = 40
    settings.FONT_SIZE_XXL = 20
    settings.FONT_SIZE_XL = 18
    settings.FONT_SIZE_L = 16
    settings.FONT_SIZE_NORMAL = 12
    settings.FONT_SIZE_SMALL = 10

    settings.FONT_HEIGHT_XXL = 20
    settings.FONT_HEIGHT_XL = 18
    settings.FONT_HEIGHT_NORMAL = 14
    settings.FONT_HEIGHT_SMALL = 12

    settings.DISPLAY_WIDTH = 128
    settings.DISPLAY_HEIGHT = 128 # or 64
    settings.DISPLAY_RGB = False

    settings.DISPLAY_HEIGHT = 64
    settings.DISPLAY_WIDTH = 128