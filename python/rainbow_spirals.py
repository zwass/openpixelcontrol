from __future__ import division
import time
import math
import sys

from colour import Color

import opc
import color_utils


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

print('    sending pixels forever (control-c to exit)...')
print('')

n_pixels = 150
n_strips = 16
fps = 60         # frames per second


def map_color(c):
    return tuple(255 * x for x in c.rgb)


def create_color(i):
    return Color(hsl=(float(i) / n_pixels, 1.0, 0.5))


start_time = time.time()
while True:
    t = (time.time() - start_time)
    for s in range(n_strips):
        pixels = [(0, 0, 0)] * n_pixels
        for i in range(n_pixels):
            pixels[i] = map_color(create_color((i + t*37 + 17*s) % n_pixels))
        client.put_pixels(pixels, channel=s+1)
    time.sleep(1 / fps)
