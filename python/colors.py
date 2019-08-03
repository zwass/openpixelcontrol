from __future__ import division
import time
import math
import sys
from copy import deepcopy

import opc
from color_utils import create_palette, schemes


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

palette = create_palette(n_pixels, schemes['pineapple'])


def create_color(i):
    return palette[int(i) % len(palette)]


start_time = time.time()
while True:
    t = (time.time() - start_time)
    for s in range(n_strips):
        pixels = [(0, 0, 0)] * n_pixels
        for i in range(n_pixels):
            # pixels[i] = create_color((i + t*37 + (17*s)))
            # pixels[i] = create_color(
            #     i +
            #     t * 37 +
            #     t_factor * math.cos(t) * math.sin(t) +
            #     (17*s) +
            #     t_factor * -15 * math.cos(s + t/13)
            # )
            pixels[i] = create_color((3*i + 23*math.cos(t)*math.sin(t)) - (150*math.cos(3.3*s + t/13)) + 47*t)
            # pixels[i].scale_luminance(-.3 * math.sin(s/n_strips*math.pi))
            # pixels[i] = create_color(((37*math.sin(i) +
            # 23*math.cos(t)*math.sin(t)) - (150*math.cos(s + t/13)) + 47*t))
        client.put_pixels([p.rgb_255 for p in pixels], channel=s+1)
    time.sleep(1 / fps)
