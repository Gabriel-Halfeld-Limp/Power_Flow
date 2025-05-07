net = Network()
# Criação das barras
buses = [
    Bus(net, id=1, bus_type='Slack', v=1.0, theta=0.0),
    Bus(net, id=2, bus_type='PV'), 
    Bus(net, id=3)
]
print(net.buses)
# Criação das linhas
lines = [
    Line(id=1, from_bus=buses[0], to_bus=buses[1], r=0.01938, x=0.05917, b_half=0.00264),
    Line(id=2, from_bus=buses[0], to_bus=buses[2], r=0.05403, x=0.22304, b_half=0.00264),
    Line(id=3, from_bus=buses[1], to_bus=buses[2], r=0.04699, x=0.19797, b_half=0.00219),
]
print(net.lines)
y = net.y_bus()
Y = pd.DataFrame(y)
Y
#Criação de Geradores:
generators = [
    Generator(id=1, bus=buses[0]), #Gerador Vtheta
    Generator(id=2, bus=buses[1]), #Compensador Síncrono
]

print(net.generators)
loads = [
    Load(id=1, bus=buses[1], pb=1000, p_input=240, q_input=120),
    Load(id=2, bus=buses[2], pb=1000, p_input=240, q_input=120)
]

print(net.loads)