from __future__ import division
import time
import math
import random
import sys

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

r_jit, g_jit, b_jit = 13.0, 7.0, 9.0
start_time = time.time()
while True:
    r_jit += random.gauss(0, 1)
    g_jit += random.gauss(0, 1)
    b_jit += random.gauss(0, 1)
    t = (time.time() - start_time)
    for s in range(n_strips):
        pixels = []
        for i in range(n_pixels):
            r_idx = (i + 7*s + 13*t) / n_pixels * math.pi * 2
            g_idx = (i + 5*s - 7*t) / n_pixels * math.pi * 2 + (math.pi / 2)
            b_idx = (i + 13*s + 9*t) / n_pixels * math.pi * 2 + (math.pi)
            color = (math.sin(r_idx)*255, math.sin(g_idx)*255, math.sin(b_idx) * 255)
            #color = color_utils.contrast(color, 128, math.sin(((s / n_strips) + t / 2) * math.pi * 2))
            pixels.append(color)
        client.put_pixels(pixels, channel=s+1)
    time.sleep(1 / fps)
