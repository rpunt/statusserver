#!/usr/bin/env python

import json
#import threading
from flask import Flask, render_template, jsonify, make_response
from time import sleep
import colorsys
import math
import time
from unicornhatmini import UnicornHATMini
from jsmin import jsmin

app = Flask(__name__)

globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0.1

# initialize the hat
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(globalBrightness)
unicornhatmini.set_rotation(0)
u_width, u_height = unicornhatmini.get_shape()

## Generate a lookup table for 8-bit hue to RGB conversion
#hue_to_rgb = []
#for i in range(0, 360):
#  hue_to_rgb.append(colorsys.hsv_to_rgb(i / 359.0, 1, 1))

def setColor(r, g, b):
  setPixels(r, g, b, globalBrightness)
  unicornhatmini.show()

def setPixels(r, g, b, brightness=0.1):
  global globalBrightness, globalBlue, globalGreen, globalRed

  globalRed = r
  globalGreen = g
  globalBlue = b

  if brightness is not None:
    globalBrightness = brightness
    unicornhatmini.set_brightness(brightness)

  unicornhatmini.clear()
  for x in range(u_width):
    for y in range(u_height):
      unicornhatmini.set_pixel(x, y, r, g, b)


@app.route("/")
def index():
  templateData = {
    'title'  : 'Current Status',
    'status' : globalStatus
  }
  return render_template('index.html', **templateData)

@app.route("/api/<status>")
def action(status):
  global globalStatus
  if status == 'busy':
    globalStatus = status
    setColor(255, 0, 0)
  if status == 'free': 
    globalStatus = status
    setColor(0, 255, 0)
  if status == 'away': 
    globalStatus = status
    setColor(255, 191, 0)
  if status == 'off': 
    globalStatus = status
    unicornhatmini.clear()
    unicornhatmini.show()
  if status == 'status': 
    next
  return make_response(jsonify({'status': globalStatus}))

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=False)
