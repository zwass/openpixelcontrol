from __future__ import division
import time
import math
import random
import sys

import opc
from color_utils import Color


#-------------------------------------------------------------------------------
# handle command line

if len(sys.argv) == 1:
    IP_PORT = '127.0.0.1:7890'
elif len(sys.argv) == 2 and ':' in sys.argv[1] and not sys.argv[1].startswith('-'):
    IP_PORT = sys.argv[1]
else:
    print('''
Usage: raver_plaid.py [ip:port]

If not set, ip:port defauls to 127.0.0.1:7890
''')
    sys.exit(0)


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(IP_PORT)
if client.can_connect():
    print('    connected to %s' % IP_PORT)
else:
    # can't connect, but keep running in case the server appears later
    print('    WARNING: could not connect to %s' % IP_PORT)
print('')


#-------------------------------------------------------------------------------
# send pixels

n_pixels = 150


palette = create_palette(n_pixels)

class Line:
    def __init__(self):
        self.x = random.randrange(0, n_pixels)
        self.speed = random.randrange(0, 55) + 30
        self.tick = 0
        self.color = random.choice(palette)
        self.direction = random.choice([-1, 1])

    def update(self, t_delta):
        self.tick += 1000 * t_delta
        if self.tick > self.speed:
            self.x = (self.x + self.direction) % n_pixels
            self.tick = 0

    def render(self, pixels):
        for s in range(n_strips):
            pixels[s][self.x] = self.color.rgb_255

print('    sending pixels forever (control-c to exit)...')
print('')

n_pixels = 150
n_strips = 16
fps = 60         # frames per second

r_jit, g_jit, b_jit = 13.0, 7.0, 9.0
start_time = time.time()
t_last = start_time
pixels = []
for _ in range(n_strips):
    pixels.append(n_pixels * [(0, 0, 0)])

lines = []
for i in range(32):
    lines.append(Line())

while True:
    lines.append(Line())
    for s in range(n_strips):
        pixels[s] = n_pixels * [(0, 0, 0)]
    t = (time.time() - start_time)
    t_delta = time.time() - t_last
    t_last = time.time()
    for l in lines:
        l.update(t_delta)
        l.render(pixels)
    for p, i in zip(pixels, range(n_strips)):
        client.put_pixels(p, channel=i+1)
    time.sleep(1 / fps)
