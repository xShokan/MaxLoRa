
nodes_my_PDR = [0.5903955743659812,0.47443566285930816,0.36547059928611686,0.2594249076753681,0.1965282505105514]
nodes_expSF_PDR = [0.41085613415710504,0.34166129010117097,0.24995621749624994,0.19968363630987873,0.15745236176820995]
nodes_expAT_PDR = [0.5828105605689556,0.4578974470160984,0.3069862468358709,0.2053728906618208,0.1432958867517746]
nodes_ADR_PDR = [0.4646524879083019,0.39235766247013665,0.32505163633109885,0.22573555339796444,0.16860553310118626]

packets_my_PDR = [0.5903955743659812, 0.43066404268700925, 0.4305859718782619, 0.31917541470842303, 0.31606004523956405]
packets_expSF_PDR = [0.41085613415710504, 0.30318489755452743, 0.3079245916077757, 0.24157594608605495, 0.23671746137433228]
packets_expAT_PDR = [0.5828105605689556, 0.4083674123967605, 0.4189073050951504, 0.2931407836596143, 0.29128353329246576]
packets_ADR_PDR = [0.4646524879083019, 0.28748825211461937, 0.28710344966146306, 0.18461494269382128, 0.18741444154646456]

print((sum(nodes_my_PDR) - sum(nodes_expAT_PDR)) / sum(nodes_expAT_PDR))
print((sum(nodes_my_PDR) - sum(nodes_expSF_PDR)) / sum(nodes_expSF_PDR))
print((sum(nodes_my_PDR) - sum(nodes_ADR_PDR)) / sum(nodes_ADR_PDR))
print("##################")

print((sum(packets_my_PDR) - sum(packets_expAT_PDR)) / sum(packets_expAT_PDR))
print((sum(packets_my_PDR) - sum(packets_expSF_PDR)) / sum(packets_expSF_PDR))
print((sum(packets_my_PDR) - sum(packets_ADR_PDR)) / sum(packets_ADR_PDR))
print("##################")

for i in range(5):
    print((nodes_my_PDR[i] - nodes_expAT_PDR[i]) / nodes_expAT_PDR[i])
print("##################")

for i in range(5):
    print((packets_my_PDR[i] - packets_expAT_PDR[i]) / packets_expAT_PDR[i])
print("##################")

for i in range(5):
    print((nodes_my_PDR[i] - nodes_ADR_PDR[i]) / nodes_ADR_PDR[i])
print("##################")

for i in range(5):
    print((packets_my_PDR[i] - packets_ADR_PDR[i]) / packets_ADR_PDR[i])