#!/usr/bin/env python3

from unicornhatmini import UnicornHATMini
import numpy as np
import time
import datetime

globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0.0
globalStatus = 'free'

# initialize the hat
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(globalBrightness)
unicornhatmini.set_rotation(0)
u_width, u_height = unicornhatmini.get_shape()

unicornhatmini.set_all(0,255,0)
unicornhatmini.show()

brightness = np.arange(0.0, 0.35, 1/60)

while True:
  for x in brightness:
    # print("brightness: ", x)
    unicornhatmini.set_brightness(x)
    time.sleep(1/15)
  for x in brightness[::-1]:
    # print("brightness: ", x)
    unicornhatmini.set_brightness(x)
    time.sleep(1/15)
