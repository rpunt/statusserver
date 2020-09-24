#!/usr/bin/env python

import json
import threading
import numpy as np
from flask import Flask, render_template, jsonify, make_response
from time import sleep
import colorsys
import math
import time
from gpiozero import CPUTemperature
from unicornhatmini import UnicornHATMini
from jsmin import jsmin

app = Flask(__name__)

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0.1
globalStatus = 'free'

# initialize the hat
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(globalBrightness)
unicornhatmini.set_rotation(0)
u_width, u_height = unicornhatmini.get_shape()

## Generate a lookup table for 8-bit hue to RGB conversion
#hue_to_rgb = []
#for i in range(0, 360):
#  hue_to_rgb.append(colorsys.hsv_to_rgb(i / 359.0, 1, 1))

#def setColor(r, g, b):
#  setPixels(r, g, b, globalBrightness)
#  unicornhatmini.show()

#def setPixels(r, g, b, brightness=0.1):
#  global globalBrightness, globalBlue, globalGreen, globalRed
#  globalRed = r
#  globalGreen = g
#  globalBlue = b
#
#  if brightness is not None:
#    globalBrightness = brightness
#    unicornhatmini.set_brightness(brightness)
#
#  unicornhatmini.clear()
#  for x in range(u_width):
#    for y in range(u_height):
#      unicornhatmini.set_pixel(x, y, r, g, b)

def switchOff():
  global blinkThread, globalBlue, globalGreen, globalRed
  globalRed = 0
  globalGreen = 0
  globalBlue = 0
  if blinkThread is not None:
    blinkThread.do_run = False
  unicornhatmini.clear()
  unicornhatmini.show()

def pulsar(r, g, b):
  global blinkThread, globalBlue, globalGreen, globalRed
  globalRed = r
  globalGreen = g
  globalBlue = b
  brightness_range = np.arange(0.0, 0.35, 1/60)
  # print(brightness_range)
  switchOff()
  unicornhatmini.set_all(r, g, b)
  unicornhatmini.show()
  # print("pulsar with ", r, ", ", g, ", ", b)
  while True:
    for x in brightness_range:
      unicornhatmini.set_brightness(x)
      time.sleep(1/15)
    for x in brightness_range[::-1]:
      unicornhatmini.set_brightness(x)
      time.sleep(1/15)

@app.route("/")
def index():
  templateData = {
    'title'  : 'Current Status',
    'status' : globalStatus
  }
  return render_template('index.html', **templateData)

@app.route("/api/<command>")
def action(command):
  global blinkThread, globalStatus

  if command == 'busy':
    globalStatus = command
    blinkThread = threading.Thread(target=pulsar, args=(255, 0, 0))
    blinkThread.do_run = True
    blinkThread.start()

  if command == 'free':
    globalStatus = command
    blinkThread = threading.Thread(target=pulsar, args=(0, 255, 0))
    blinkThread.do_run = True
    blinkThread.start()

  if command == 'away':
    globalStatus = command
    blinkThread = threading.Thread(target=pulsar, args=(255, 191, 0))
    blinkThread.do_run = True
    blinkThread.start()

  if command == 'off':
    globalStatus = command
    switchOff()

  if command == 'status':
    cpu = CPUTemperature()
    return jsonify({
      'status': globalStatus,
      'cpuTemp': cpu.temperature * 1.8 + 32,
      'height': u_height,
      'width': u_width
    })

  return make_response(jsonify({'status': globalStatus}))

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=False)
