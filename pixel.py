#!/usr/bin/python3

import os
import random
import sys
import socket
import threading
from PIL import Image

port = os.getenv('PORT')
server = os.getenv('SERVER')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, int(port)))

def offset(x, y):
  sock.send(b'OFFSET %d %d' % (x, y))

def rgb(x, y, r, g, b):
  sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))

def rgba(x, y, r, g, b, a=255):
  if a == 255:
    rgb(x, y, r, g, b)
  else:
    sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

def screen_size():
  sock.send(b'SIZE')
  _, x, y = sock.recv(24).decode("utf-8").split()
  return int(x), int(y)

image = Image.open('image.png').convert('RGBA')
_, _, w, h = image.getbbox()

max_x, max_y = screen_size()
offset_x = 450
offset_y = 0
offset(offset_x, offset_y)

while True:
  for x in range(w):
    image_x = x + offset_x
    for y in range(h):
      image_y = y + offset_y
      if image_x <= max_x and image_y <= max_y:
        r, g, b, a = image.getpixel((x, y))
        rgb(x, y, r, g, b)
