# -*- coding: utf-8 -*-
"""
 extra-LoRaSim: simulate collisions in multi-gateway LoRaWAN network - User-defined data version LoRaSim.
 The original LoRaSim: https://www.lancaster.ac.uk/scc/sites/lora/lorasim.html
"""


import simpy
import random
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.patches import Rectangle
from datetime import datetime

# 125kHz时每种SF对应的接收灵敏度，only for ADR
sensiDict = {7:-126.5, 8:-127.25, 9:-131.25, 10:-132.75, 11:-134.5, 12:-133.25}

# check for collisions at base station
# Note: called before a packet (or rather node) is inserted into the list
sfCollideNum = 0
timingCollideNum = 0

def checkcollision(packet):
    global sfCollideNum
    global timingCollideNum

    col = 0 # flag needed since there might be several collisions for packet
    # lost packets don't collide
    if packet.lost:
       return 0
    if packetsAtBS[packet.bs]:
        for other in packetsAtBS[packet.bs]:
            if other.id != packet.nodeid:
                # simple collision
                sfCollide = sfCollision(packet, other.packet[packet.bs])
                timingCollide = timingCollision(packet, other.packet[packet.bs])
                if sfCollide and timingCollide:
                    # check who collides in the power domain
                    c = powerCollision(packet, other.packet[packet.bs])
                    # mark all the collided packets
                    # either this one, the other one, or both
                    for p in c:
                        p.collided = 1
                        if p == packet:
                            col = 1
        return col
    return 0


def sfCollision(p1, p2):
    if p1.sf == p2.sf:
        # p2 may have been lost too, will be marked by other checks
        return True
    return False


def timingCollision(p1, p2):
    # assuming p1 is the freshly arrived packet and this is the last check
    # we've already determined that p1 is a weak packet, so the only
    # way we can win is by being late enough (only the first n - 5 preamble symbols overlap)

    # assuming 8 preamble symbols
    Npream = 8

    # we can lose at most (Npream + 4.25) * Tsym of our preamble
    # Tpreamb = 2**p1.sf/(1.0*p1.bw) * (Npream + 4.25)
    Tpreamb = 2**p1.sf/(1.0*p1.bw) * (Npream + 4.25)
    Tpreamb = Tpreamb / 1000

    # check whether p2 ends in p1's critical section
    p2_end = p2.addTime + p2.rectime
    p1_cs = env.now + Tpreamb
    if p1_cs < p2_end:
        # p1 collided with p2 and lost
        return True
    return False


def powerCollision(p1, p2):
    powerThreshold = 6 # dB
    if abs(p1.rssi - p2.rssi) < powerThreshold:
        # packets are too close to each other, both collide
        # return both packets as casualties
        return (p1, p2)
    elif p1.rssi - p2.rssi < powerThreshold:
        # p2 overpowered p1, return p1 as casualty
        return (p1,)
    # p2 was the weaker packet, return it as a casualty
    return (p2,)

# this function computes the airtime of a packet
# according to LoraDesignGuide_STD.pdf
#
def airtime(sf,cr,pl,bw):
    H = 0        # implicit header disabled (H=0) or not (H=1)
    DE = 0       # low data rate optimization enabled (=1) or not (=0)
    Npream = 8   # number of preamble symbol (12.25  from Utz paper)

    if bw == 125 and sf in [11, 12]:
        # low data rate optimization mandated for BW125 with SF11 and SF12
        DE = 1
    if sf == 6:
        # can only have implicit header with SF6
        H = 1

    Tsym = (2.0**sf)/bw
    Tpream = (Npream + 4.25)*Tsym
    payloadSymbNB = 8 + max(math.ceil((8.0*pl-4.0*sf+28+16-20*H)/(4.0*(sf-2*DE)))*(cr+4),0)
    Tpayload = payloadSymbNB * Tsym
    return (Tpream + Tpayload) / 1000



#
# this function creates a BS
#
class myBS():
    def __init__(self, id, lng, lat, dist):
        # 网关id和坐标
        self.id = id
        self.x = lng
        self.y = lat
        self.dist = dist

#
# this function creates a node
#
class myNode():
    # 终端节点ID，发送间隔，数据包长度
    def __init__(self, id, lng, lat, sf, rssi, periods, packetlen):
        global bs

        self.id = id
        self.periods = periods  # TODO: 数据包发送间隔(按小时划分的数组)
        self.x = lng            # 坐标
        self.y = lat
        self.sf = sf
        self.rssi = rssi
        self.packet = []        # 数据包
        self.dist = []          # 终端节点与各个网关的距离列表
        self.node_recPackets = 0    # 当前节点发出的数据包中成功接收的个数
        self.sent = 0           # 当前节点发出数据包总数
        self.der = 0            # 当前节点的数据包交付率
       

        # create "virtual" packet for each BS
        # 模拟数据包发送，广播给每一个网关
        global nrBS
        for i in range(0,nrBS):
            d = np.sqrt((self.x-bs[i].x)*(self.x-bs[i].x)+(self.y-bs[i].y)*(self.y-bs[i].y))  * 96.81365
            self.dist.append(d)
            print("x", self.x, "y", self.y, "bsx", bs[i].x, "bsy", bs[i].y)
            self.packet.append(myPacket(self.id, self.sf, self.rssi, packetlen, self.dist[i], bs[i], i))


#
# this function creates a packet (associated with a node)
# it also sets all parameters, currently random
#
class myPacket():
    # 终端节点ID，数据包长度，终端节点与网关的距离，网关ID
    def __init__(self, nodeid, sf, rssi, plen, distance, bs, bs_id):
        global experiment
        global Ptx
        global GL


        self.bs = bs_id
        # new: base station ID
        self.nodeid = nodeid
        # randomize configuration values
        self.cr = 4
        self.bw = 125
        self.sf = sf
        # self.sf = random.randint(6,12)
        self.rssi = rssi
        # transmission range, needs update XXX
        self.pl = plen      # 数据包长度
        # frequencies: 500MHz
        self.freq = 500000000 

        self.rectime = airtime(self.sf,self.cr,self.pl,self.bw)
        # denote if packet is collided
        self.collided = 0
        self.processed = 0


        # 计算数据包是否可达(接收功率高于RSSI)
        # pass-loss
        Lpl = 120.8 + 35.7*math.log10(distance)
        Prx = Ptx - Lpl

        
        if (ADR == True):           # ADR mode:
            minairtime = airtime(7,4,20,self.bw)
            minsf = 7

            # 从最大的SF开始往最小的尝试
            for i in range(7, 13)[::-1]:
                if (Prx > sensiDict[i]):
                    self.sf = i
                    at = airtime(self.sf,4,20,self.bw)
                    if at < minairtime:
                        minairtime = at
                        minsf = self.sf

            self.rectime = minairtime
            self.sf = minsf
            if (minairtime == 9999):
                print ("does not reach base station")
               # exit(-1)
        else:
            self.lost = distance > bs.dist


#
# main discrete event loop, runs for each node
# a global list of packet being processed at the gateway
# is maintained
#
def transmit(env, node):
    while True:
        # 判断当前环境时间是哪个小时，设备的发包频率按小时划分
        hour = int(env.now // 60 * 60 % 24)

        print("【 progress: {}% 】".format((env.now / simtime) * 100))
        
        # 以指数分布的概率返回随机数random.expovariate(lambd)，lambd=1.0/期望的平均值
        # 如果lambd为正，返回的值范围从0到正无穷；如果lambd为负，返回的值范围从负无穷到0。如，顾客到达时间服从指数分布，时间间隔平均为10分钟，则lambd=1.0/10
        time_slot = node.periods[hour]
        time_slot = random.expovariate(1.0/float(time_slot)) if time_slot != 0 else 0

        if time_slot == 0 or time_slot >= 60 * 60:
            # 啥也不干，跳过这个小时
            yield env.timeout(60 * 60)
        else:
            yield env.timeout(time_slot)

            # time sending and receiving
            # packet arrives -> add to base station
            node.sent = node.sent + 1
            
            global packetSeq
            packetSeq = packetSeq + 1

            global nrBS
            for bs in range(0, nrBS):
               if (node in packetsAtBS[bs]):
                    print("ERROR: packet already in")
               else:
                    # adding packet if no collision
                    if (checkcollision(node.packet[bs])==1):
                        node.packet[bs].collided = 1
                    else:
                        node.packet[bs].collided = 0
                        
                    packetsAtBS[bs].append(node)
                    node.packet[bs].addTime = env.now
                    node.packet[bs].seqNr = packetSeq

            # take first packet rectime
            # 每个数据包的空中时间也纳入事件间隔中（假设有数据包在发送时不发送下一个）
            yield env.timeout(node.packet[0].rectime)

            # if packet did not collide, add it in list of received packets
            # unless it is already in
            rec_by_any_BS = False       # 此数据包被任何一个网关成功接收
            for bs in range(0, nrBS):
                if node.packet[bs].lost:
                    # 加入因接收功率不足无法成功接收的数据包队列
                    lostPackets.append(node.packet[bs].seqNr)
                else:
                    if node.packet[bs].collided == 0:
                        print("free: ",bs)
                        # 加入当前网关的成功接收数据包队列
                        packetsRecBS[bs].append(node.packet[bs].seqNr)
                        rec_by_any_BS = True
                        # 加入整个网络中成功接收的数据包队列
                        # 若recPackets队列为空直接添加，否则只有当队列最后一个序号和当前不同时添加（放置重复添加）
                        if (recPackets):
                            if (recPackets[-1] != node.packet[bs].seqNr):
                                recPackets.append(node.packet[bs].seqNr)
                        else:
                            recPackets.append(node.packet[bs].seqNr)
                    else:
                        print('collide node:{}, bs:{}'.format(node.id, bs))
                        # XXX only for debugging
                        # 加入因碰撞无法成功接收的数据包队列
                        collidedPackets.append(node.packet[bs].seqNr)
            if rec_by_any_BS:
                node.node_recPackets += 1

            # complete packet has been received by base station, can remove it
            for bs in range(0, nrBS):
                if (node in packetsAtBS[bs]):
                    packetsAtBS[bs].remove(node)
                    # reset the packet
                    node.packet[bs].collided = 0
                    node.packet[bs].processed = 0
            print("DER: ", len(recPackets)/float(packetSeq))



#
# ---------------------------------------------------  "main" program  -------------------------------------------
#

# 开始时间
start_time = datetime.now()

# 主要参数定义
ADR = False                     # ADR实验模式开关，不打开时使用输入的SF，否则自适应选择SF
simtime = 3600 * 24 * 7         # 总仿真时间：1week，单位：sec
nrBS = 85                       # 网络中的网关总数

# global stuff 终端、网关
nodes = []
packetsAtBS = []
env = simpy.Environment()


# max distance: 300m in city, 3000 m outside (5 km Utz experiment)
# also more unit-disc like according to Utz
# nr：总数
nrCollisions = 0    # 冲突总数
nrReceived = 0      # 成功接收总数
nrProcessed = 0     # 生成的数据包总数

# global value of packet sequence numbers 数据包序列号
packetSeq = 0

# list of received packets
recPackets=[]
collidedPackets=[]
lostPackets = []

# 计算接收功率的参数
Ptx = 14            # 发送功率
GL = 0              # 路径损耗参数：一般的增益和损耗


#sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])

# list of base stations
bs = []

# list of packets at each base station, init with 0 packets
# 解析网关数据
with open("data/new_gateways_dist.csv", "rb") as f:
    df_gateways = pd.read_csv(f, header = 0, names=['lng', 'lat', 'dist'])    
    f.close()

packetsAtBS = []
packetsRecBS = []
for i in range(0, len(df_gateways)):
    lng = df_gateways.loc[i]['lng']
    lat = df_gateways.loc[i]['lat']
    dist = df_gateways.loc[i]['dist']
    b = myBS(i, lng, lat, dist)
    bs.append(b)
    packetsAtBS.append([])
    packetsRecBS.append([])


# 生成每个终端节点并模拟数据包发送
# 从csv文件中解析每个终端节点的信息，包括【ID，avgSendTime，坐标，sf，packetlen（可以统一成全局变量）】，
with open("data/sensor_with_RSSI_SNR.csv", "rb") as f:
    df_sensors = pd.read_csv(f, header = 0, names=['sensor_id', 'lng', 'lat', 'newSF', 'oldSF', 'EXPLoRa_SF1', 'EXPLoRa_SF2',\
                                        'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', \
                                        'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', \
                                        'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'SNR', 'RSSI'])
    f.close()


sensor0_add_time = []
for i in range(0, len(df_sensors)):
    item = df_sensors.loc[i]
    lng = item['lng']
    lat = item['lat']
    sf = item['EXPLoRa_SF1']
    rssi = item['RSSI']

    # 每小时（60min）发n个包，每隔  60*(1/n)  min发一个包
    avgSendTime = list(item[5:])
    avgSendTime = list(map(lambda x:60 * 60 *(1/x) if x != 0 else 0, avgSendTime))


    node = myNode(i, lng, lat, sf, rssi, avgSendTime, 20)
    nodes.append(node)
    env.process(transmit(env, node))


# start simulation
# 模拟时间周期，和前面设备发送时间间隔统一单位
env.run(until=simtime)

print("sf collide: ", sfCollideNum)
print("timing collide: ", timingCollideNum)

# store nodes and basestation locations
# 存储终端设备的坐标和包交付率
df_nodes = pd.DataFrame(columns = ["id", "lng", "lat", 'sent', 'recv', "der"])
index = 0
for node in nodes:
    if node.sent == 0:
        curr_der = 1
    else:
        curr_der = node.node_recPackets/float(node.sent) 
    df_nodes.loc[index] = {'id': node.id, 'lng': node.x, 'lat': node.y, 'sent': node.sent, 'recv': node.node_recPackets, 'der': curr_der}
    index += 1
with open('data/new_der(EXPLoRa_SF1)_1week.csv', 'w') as file:
    df_nodes.to_csv(file, index = None, encoding ='utf-8')
    file.close()
   

# print stats and save into file
# print "nrCollisions ", nrCollisions
# print list of received packets
#print recPackets
print("nr received packets", len(recPackets))
print("nr collided packets", len(collidedPackets))
print("nr lost packets", len(lostPackets))

#print "sent packets: ", sent
#print "sent packets-collisions: ", sent-nrCollisions
#print "received packets: ", len(recPackets)
for i in range(0,nrBS):
    print("packets at BS",i, ":", len(packetsRecBS[i]))
print("sent packets: ", packetSeq)

# data extraction rate
der = len(recPackets)/float(packetSeq)
print("DER:", der)

end_time = datetime.now()
print("runtime_in_sec: ", (end_time - start_time).seconds)
