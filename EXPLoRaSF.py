import pandas as pd

def EXPLoRaSF_func(Num):
    D = Num
    sf_sens = [-120.75, -124.0, -127.5, -128.75, -128.75, -132.25]
    sf_set = [7, 8, 9, 10, 11, 12]
    df = pd.read_csv('./data/OneGateway_' + str(Num) + '.csv')
    df['SF'] = 0
    l = len(sf_set)
    for t in range(len(sf_set)):
        cnt = sum(df['RSSI'] > sf_sens[t])
        if cnt > D / l:
            z = int(D / l)
        else:
            z = cnt

        for i in range(z):
            index = df[df['SF'] == 0]['RSSI'].idxmax(axis=1)
            df.loc[index, 'SF'] = sf_set[t]
            D -= 1
        l -= 1

    df.to_csv('./data/OneGateway_EXPLoRaSF_' + str(Num) + '.csv')
