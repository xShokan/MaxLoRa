import pandas as pd
import numpy as np
import math
import random


# N = 100
# Range = [0, 200]


def Generate(Num, Range):
    sf7 = np.array([7, -126.5, -124.25, -120.75])
    sf8 = np.array([8, -127.25, -126.75, -124.0])
    sf9 = np.array([9, -131.25, -128.25, -127.5])
    sf10 = np.array([10, -132.75, -130.25, -128.75])
    sf11 = np.array([11, -134.5, -132.75, -128.75])
    sf12 = np.array([12, -133.25, -132.25, -132.25])
    sensi = np.array([sf7, sf8, sf9, sf10, sf11, sf12])
    Ptx = 14
    gamma = 2.08
    d0 = 40.0
    var = 0  # variance ignored for now
    Lpld0 = 127.41
    GL = 0
    minsensi = np.amin(sensi)
    Lpl = Ptx - minsensi
    maxDist = d0 * (math.e ** ((Lpl - Lpld0) / (10.0 * gamma)))
    bsx = maxDist + 10
    bsy = maxDist + 10
    maxX = 2 * maxDist * math.sin(60 * (math.pi / 180))  # == sqrt(3) * maxDist
    maxY = 2 * maxDist * math.sin(30 * (math.pi / 180))  # == maxdist

    df = pd.DataFrame(columns=['x', 'y', 'RSSI'])

    for i in range(Num):
        dict0 = {}
        for h in range(len(Range)):
            lambda0 = random.randint(Range[h][0], Range[h][1])
            dict0['lambda' + str(h)] = lambda0
        posx = random.randint(0, int(maxX))
        posy = random.randint(0, int(maxY))
        dist = np.sqrt(((abs(bsx - posx)) ** 2) + ((abs(bsy - posy)) ** 2))
        Lpl = Lpld0 + 10 * gamma * math.log10(dist / d0)
        Prx = Ptx - GL - Lpl

        dict0['x'] = posx
        dict0['y'] = posy
        dict0['RSSI'] = Prx

        df = df.append(dict0, ignore_index=True)

    df.to_csv("./data/OneGateway_" + str(Num) + ".csv", index=False)
