#!/usr/bin/python3

import os
import random
import socket
import sys
import threading

from PIL import Image

port = os.getenv('PORT') if os.getenv('PORT') is not None else '1234'
server = os.getenv('SERVER')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server, int(port)))

def offset(x, y):
  sock.send(b'OFFSET %d %d\n' % (x, y))

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
offset_x = int(os.getenv('OFFSET_X')) if os.getenv('OFFSET_X') is not None else 0
offset_y = int(os.getenv('OFFSET_Y')) if os.getenv('OFFSET_Y') is not None else 0
offset(offset_x, offset_y)

try:
  while True:
    for x in range(w):
      pos_x = x + offset_x
      for y in range(h):
        pos_y = y + offset_y
        if pos_x <= max_x and pos_y <= max_y:
          r, g, b, a = image.getpixel((x, y))
          rgb(x, y, r, g, b)
except KeyboardInterrupt:
  exit(0)
