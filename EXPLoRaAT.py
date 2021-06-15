import numpy as np
import pandas as pd

def local_peaks_indexes(P):
    P_vec = np.array(P)
    p = []
    for i in range(1, len(P_vec)):
        if P_vec[i] > P_vec[i-1]:
            p.append(i)
    p.append(6)
    return p

def EXPLoRaAT(sf_vec):
    sf_v = np.array(sf_vec)
    sf_o = ([0, 0, 0, 0, 0, 0])
    for i in range(0, len(sf_o)):

        sf_o[i] = sf_v[i]
    w = np.array([1.0, 1.83, 3.33, 6.67, 13.34, 24.04])
    q = np.array([1.0 / 1.0, 1.0 / 1.83, 1.0 / 3.33, 1.0 / 6.67, 1.0 / 13.34, 1.0 / 24.04])
    P = sf_v * w

    # Water Filling Algorithm
    old_p = 0
    p = 1
    while old_p != p:
        p_idx = local_peaks_indexes(P)
        p = old_p
        old_p = p_idx
        start = 0
        for i in range(0, len(p_idx)):
            count = (sum(P[start:(p_idx[i])] * q[start:(p_idx[i])])) / (sum(q[start:(p_idx[i])]))
            for j in range(start, p_idx[i]):
                P[j] = count
            start = p_idx[i]

    k_AT = P * q
    vec = ([0, 0, 0, 0, 0, 0])
    for i in range(0, len(k_AT)):
        vec[i] = round(k_AT[i])
    return vec


def EXPLoRaAT_func(Num):
    df = pd.read_csv('./data/OneGateway_' + str(Num) + '.csv')
    df['SF'] = 0

    sf_vec = [len(df), 0.0, 0.0, 0.0, 0.0, 0.0]
    sf_vec = EXPLoRaAT(sf_vec)

    sum0 = sum(sf_vec)
    sf_sens = [-120.75, -124.0, -127.5, -128.75, -128.75, -132.25]
    sf_set = [7, 8, 9, 10, 11, 12]

    if sum(sf_vec) != len(df):
        sf_vec[0] += len(df) - sum(sf_vec)

    for t in range(len(sf_set)):
        for i in range(sf_vec[t]):
            index = df[df['SF'] == 0]['RSSI'].idxmax(axis=1)
            df.loc[index, 'SF'] = sf_set[t]

    df.to_csv('./data/OneGateway_EXPLoRaAT_' + str(Num) + '.csv')