
nodes_my_PDR = [0.5903955743659812,0.47443566285930816,0.36547059928611686,0.2594249076753681,0.1965282505105514]
nodes_expSF_PDR = [0.41085613415710504,0.34166129010117097,0.24995621749624994,0.19968363630987873,0.15745236176820995]
nodes_expAT_PDR = [0.5828105605689556,0.4578974470160984,0.3069862468358709,0.2053728906618208,0.1432958867517746]
nodes_ADR_PDR = [0.4646524879083019,0.39235766247013665,0.32505163633109885,0.22573555339796444,0.16860553310118626]

packets_my_PDR = [0.8834651746092996, 0.8201539073902083, 0.7371392040044615, 0.5436756701912554, 0.3892481682785212, 0.2694831236919824]
packets_expSF_PDR = [0.8343364860991688, 0.739010919728646, 0.684865856974531, 0.4979320437770425, 0.3544027348254267, 0.24765035470606842]
packets_expAT_PDR = [0.8288985544326468, 0.7451783893985728, 0.6809331373989713, 0.4662598259962114, 0.3221363664918757, 0.2289321779920516]
packets_ADR_PDR = [0.8430795931157499, 0.7526318483509359, 0.599919001695902, 0.42300978010086365, 0.2946335627087023, 0.21220055992907888]

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