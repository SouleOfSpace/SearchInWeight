from ctypes import *

WIDTH = windll.user32.GetSystemMetrics(0) - 200
HEIGHT = windll.user32.GetSystemMetrics(1) - 200
FPS = 60