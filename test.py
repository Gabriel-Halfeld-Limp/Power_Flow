from power import *

caminho = 'pwf_systems/IEEE14.pwf'

builder = PWF_Network_Builder(caminho)
net = builder.build_network()

print(net.buses)