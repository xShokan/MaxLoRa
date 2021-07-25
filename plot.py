import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({"font.size":15})
plt.rc('font',family='Times New Roman')

nodes = [200, 300, 400, 500, 600]

nodes_my_PDR = [0.5903955743659812,0.47443566285930816,0.36547059928611686,0.2594249076753681,0.1965282505105514]
nodes_expSF_PDR = [0.41085613415710504,0.34166129010117097,0.24995621749624994,0.19968363630987873,0.15745236176820995]
nodes_expAT_PDR = [0.5828105605689556,0.4578974470160984,0.3069862468358709,0.2053728906618208,0.1432958867517746]
nodes_ADR_PDR = [0.4646524879083019,0.39235766247013665,0.32505163633109885,0.22573555339796444,0.16860553310118626]

packets = ["0", "1", "2", "3", "4"]
packets_my_PDR = [0.5903955743659812, 0.43066404268700925, 0.4305859718782619, 0.31917541470842303, 0.31606004523956405]
packets_expSF_PDR = [0.41085613415710504, 0.30318489755452743, 0.3079245916077757, 0.24157594608605495, 0.23671746137433228]
packets_expAT_PDR = [0.5828105605689556, 0.4083674123967605, 0.4189073050951504, 0.2931407836596143, 0.29128353329246576]
packets_ADR_PDR = [0.4646524879083019, 0.28748825211461937, 0.28710344966146306, 0.18461494269382128, 0.18741444154646456]

plt.cla()

plt.figure(figsize=(7,5))
plt.plot(nodes, nodes_my_PDR, color='#c0504d',linewidth=1.5, linestyle='-', label='MaxLoRa', marker='s')
plt.plot(nodes, nodes_expSF_PDR, color='#4f81bd',linewidth=1.5, linestyle='--', label='EXPLoRa-SF', marker='o')
plt.plot(nodes, nodes_expAT_PDR, color='#9bbb59', linewidth=1.5, linestyle=':', label='EXPLoRa-AT', marker='^')
plt.plot(nodes, nodes_ADR_PDR, color='#8064a2', linewidth=1.5, linestyle='-.', label='ADR', marker='+')
plt.xlabel("Numbers of sensors")
plt.ylabel("PDR")
plt.legend()

plt.savefig('./SimulationResult1.eps',dpi=600,format='eps')

plt.cla()

plt.figure(figsize=(7,5))
plt.plot(packets, packets_my_PDR, color='#c0504d',linewidth=1.5, linestyle='-', label='MaxLoRa', marker='s')
plt.plot(packets, packets_expSF_PDR, color='#4f81bd',linewidth=1.5, linestyle='--', label='EXPLoRa-SF', marker='o')
plt.plot(packets, packets_expAT_PDR, color='#9bbb59', linewidth=1.5, linestyle=':', label='EXPLoRa-AT', marker='^')
plt.plot(packets, packets_ADR_PDR, color='#8064a2', linewidth=1.5, linestyle='-.', label='ADR', marker='+')
plt.xlabel("Hour")
plt.ylabel("PDR")
plt.legend()

plt.savefig('./SimulationResult2.eps',dpi=600,format='eps')