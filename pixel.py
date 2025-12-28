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
sock.connect((server, port))
