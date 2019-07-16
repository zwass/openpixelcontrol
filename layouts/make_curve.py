import math

n = 150
radius = 10
strands = 16


# x' = x*cos q - y*sin q
# y' = x*sin q + y*cos q

for s in range(strands):
    result = ['[']
    strandtheta = s / 16 * math.pi * 2
    for i in range(n):
        theta = (i + 1) / 600 * math.pi * 2
        x = math.sin(theta) * radius
        z = math.cos(theta) * radius
        y = 0

        xprime = x * math.cos(strandtheta) - y * math.sin(strandtheta)
        yprime = x * math.sin(strandtheta) + y * math.cos(strandtheta)
        result.append('  {"point": [%.4f, %.4f, %.4f]},' % (xprime, yprime, z))

    # trim off last comma
    result[-1] = result[-1][:-1]

    result.append(']')

    f = open("layout" + str(s) + ".json", "w")
    f.write('\n'.join(result))
    f.close()
