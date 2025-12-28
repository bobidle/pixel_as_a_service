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

def pixel(x, y, r, g, b, a=255):
  if a == 255:
    sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
  else:
    sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

image = Image.open('image.png').convert('RGBA')
_, _, w, h = image.getbbox()

while True:
  for x in range(w):
    for y in range(h):
      r, g, b, a = image.getpixel((x, y))
      pixel(x, y, r, g, b, a)
