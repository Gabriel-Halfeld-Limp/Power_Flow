
net = Network()

buses = [                                                 
    Bus(net, id= 1, bus_type='Slack', v=1.060, theta=0.0),
    Bus(net, id= 2, bus_type=   'PV', v=1.045, theta=0.0),
    Bus(net, id= 3, bus_type=   'PV', v=1.010, theta=0.0),
    Bus(net, id= 4, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id= 5, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id= 6, bus_type=   'PV', v=1.070, theta=0.0),
    Bus(net, id= 7, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id= 8, bus_type=   'PV', v=1.090, theta=0.0),
    Bus(net, id= 9, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id=10, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id=11, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id=12, bus_type=   'PQ', v=1.000, theta=0.0),
    Bus(net, id=13, bus_type=   'PQ', v=1.000, theta=0.0), 
    Bus(net, id=14, bus_type=   'PQ', v=1.000, theta=0.0) 
]

loads = [                                                           
    Load(id= 1, bus=buses[ 1], pb=100, p_input=21.70, q_input=12.70),
    Load(id= 2, bus=buses[ 2], pb=100, p_input=94.20, q_input=19.00),
    Load(id= 3, bus=buses[ 3], pb=100, p_input=47.80, q_input=-3.90),
    Load(id= 4, bus=buses[ 4], pb=100, p_input= 7.60, q_input= 1.60),
    Load(id= 5, bus=buses[ 5], pb=100, p_input=11.20, q_input= 7.50),
    Load(id= 6, bus=buses[ 8], pb=100, p_input=29.50, q_input=16.60),
    Load(id= 7, bus=buses[ 9], pb=100, p_input= 9.00, q_input= 5.80),
    Load(id= 8, bus=buses[10], pb=100, p_input= 3.50, q_input= 1.80),
    Load(id= 9, bus=buses[11], pb=100, p_input= 6.10, q_input= 1.60),
    Load(id=10, bus=buses[12], pb=100, p_input=13.50, q_input= 5.80),
    Load(id=11, bus=buses[13], pb=100, p_input=14.90, q_input= 5.00)
]

#Criação de Geradores:                                        
generators = [                                                
    Generator(id=1, bus=buses[0]),                            
    Generator(id=2, bus=buses[1], pb=100, p_input=40.00),     
    Generator(id=3, bus=buses[2]),                            
    Generator(id=4, bus=buses[4]),                            
    Generator(id=5, bus=buses[5]),                            
    Generator(id=6, bus=buses[7]) 
]

lines = [                                                                                                   
    Line(id= 1, from_bus=buses[ 0], to_bus=buses[ 1], r=0.01938, x=0.05917, b_half=0.0264),                 
    Line(id= 2, from_bus=buses[ 0], to_bus=buses[ 4], r=0.05403, x=0.22304, b_half=0.0246),                 
    Line(id= 3, from_bus=buses[ 1], to_bus=buses[ 2], r=0.04699, x=0.19797, b_half=0.0219),                 
    Line(id= 4, from_bus=buses[ 1], to_bus=buses[ 3], r=0.05811, x=0.17632, b_half=0.0170),                 
    Line(id= 5, from_bus=buses[ 1], to_bus=buses[ 4], r=0.05695, x=0.17388, b_half=0.0173),                 
    Line(id= 6, from_bus=buses[ 2], to_bus=buses[ 3], r=0.06701, x=0.17103, b_half=0.0064),                 
    Line(id= 7, from_bus=buses[ 3], to_bus=buses[ 4], r=0.01335, x=0.04211, b_half=0.0   ),                 
    Line(id= 8, from_bus=buses[ 3], to_bus=buses[ 6], r=0.0    , x=0.20912, b_half=0.0    ,tap_ratio=0.978),
    Line(id= 9, from_bus=buses[ 3], to_bus=buses[ 8], r=0.0    , x=0.55618, b_half=0.0    ,tap_ratio=0.969),
    Line(id=10, from_bus=buses[ 4], to_bus=buses[ 5], r=0.0    , x=0.25202, b_half=0.0    ,tap_ratio=0.932),
    Line(id=11, from_bus=buses[ 5], to_bus=buses[10], r=0.09498, x=0.19890, b_half=0.0),                    
    Line(id=12, from_bus=buses[ 5], to_bus=buses[11], r=0.12291, x=0.25581, b_half=0.0),                    
    Line(id=13, from_bus=buses[ 5], to_bus=buses[12], r=0.06615, x=0.13027, b_half=0.0),                    
    Line(id=14, from_bus=buses[ 6], to_bus=buses[ 7], r=0.0    , x=0.17615, b_half=0.0),                    
    Line(id=15, from_bus=buses[ 6], to_bus=buses[ 8], r=0.0    , x=0.11001, b_half=0.0),                    
    Line(id=16, from_bus=buses[ 8], to_bus=buses[ 9], r=0.03181, x=0.08450, b_half=0.0),                    
    Line(id=17, from_bus=buses[ 8], to_bus=buses[13], r=0.12711, x=0.27038, b_half=0.0),                    
    Line(id=18, from_bus=buses[ 9], to_bus=buses[10], r=0.08205, x=0.19207, b_half=0.0),                    
    Line(id=19, from_bus=buses[11], to_bus=buses[12], r=0.22092, x=0.19988, b_half=0.0),                    
    Line(id=20, from_bus=buses[12], to_bus=buses[13], r=0.17093, x=0.34802, b_half=0.0),                    
]