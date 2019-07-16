import math

n = 150
radius = 0.477
strands = 16
spacing = 0.2


for s in range(strands):
    result = ['[']
    strandtheta = s / 16 * math.pi * 2
    for i in range(n):
        theta = i / n * math.pi * 2
        x = math.sin(theta) * radius
        y = math.cos(theta) * radius
        z = s * spacing

        result.append('  {"point": [%.4f, %.4f, %.4f]},' % (x, y, z))

    # trim off last comma
    result[-1] = result[-1][:-1]

    result.append(']')

    f = open("layout" + str(s) + ".json", "w")
    f.write('\n'.join(result))
    f.close()
