import pandas as pd
import numpy as np
import random

def findMIS(Matrix, df, SF):
    while len(df[df['degree'] == 0]) > 0:
        MinDegreeIndex = -1
        MinDegree = len(df) + 1
        for i in range(len(df)):
            if df.loc[i, 'SF'] == 0 and df.loc[i, 'degree'] < MinDegree and df.loc[i, 'flag'] == 1:
                MinDegreeIndex = i
                MinDegree = df.loc[i, 'degree']

        if MinDegreeIndex == -1:
            break
        # Set SF and clear neighbors
        df.loc[MinDegreeIndex, 'SF'] = SF
        if SF > 7:
            print("#", SF)
        for i in range(len(df)):
            if df.loc[MinDegreeIndex, 'degree'] == 0:
                break
            if Matrix[MinDegreeIndex][i] == 1:
                Matrix[MinDegreeIndex][i] = 0
                Matrix[i][MinDegreeIndex] = 0
                df.loc[MinDegreeIndex, 'degree'] -= 1
                df.loc[i, 'degree'] -= 1
                df.loc[MinDegreeIndex, 'flag'] = 0
                df.loc[i, 'flag'] = 0




def SetSF(Num, hour, X, X_Num):
    df = pd.read_csv("./data/OneGateway_" + str(Num) + ".csv")
    df['SF'] = 0
    df['degree'] = 0
    df['flag'] = 1
    df.idxmax(axis=1)

    # find node to allocate SF
    i = 7
    while len(df[df['SF'] == 0]) > 0:
        print(i)
        count = 0
        if i == 13:
            for j in range(len(df)):
                if df.loc[j, 'SF'] == 0:
                    df.loc[j, 'SF'] = random.randint(7, 12)
                    count += 1
            print("count:" + str(count))
            break
        df['degree'] = 0
        df['flag'] = 1
        Matrix = np.zeros((Num, Num))
        for j in range(len(df)):
            if df.loc[j, 'SF'] != 0:
                continue
            for k in range(j, len(df)):
                if df.loc[k, 'SF'] != 0 or k == j:
                    continue

                CollideFactorNum = 0
                for h in range(hour):
                    CollideFactor = 2 * df.loc[j, 'lambda' + str(h)] * df.loc[k, 'lambda' + str(h)] * 0.3 / 3600
                    if CollideFactor > X:
                        CollideFactorNum += 1
                if CollideFactorNum >= X_Num:
                    Matrix[j][k] = 1
                    Matrix[k][j] = 1
                    df.loc[j, 'degree'] += 1
                    df.loc[k, 'degree'] += 1
        findMIS(Matrix, df, i)
        i += 1
    df.drop(columns=['degree', 'flag'], axis=1, inplace=True)
    df.to_csv("./data/OneGateway_" + str(Num) + ".csv", index=False)


# df = SetSF(100, 4.5)
# df.drop(columns=['degree', 'flag'], axis=1, inplace=True)
# print(df)
