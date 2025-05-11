
from dataclasses import dataclass, field
from typing import List, Optional, ClassVar
import numpy as np

@dataclass
class Bus:
    network: "Network"
    id: Optional[int] = None
    name: Optional[str] = None
    bus_type: str = "PQ"  # "slack", "PQ", "PV"
    v: float = 1.0 # in pu
    theta: float = 0.0 # in degrees
    Sb: float = 1.0 # Base power in MVA
    Sh: float = 0.0 # Shunt admittance connected to the bus

    # Relacionamentos
    loads: List["Load"] = field(default_factory=list)
    generators: List["Generator"] = field(default_factory=list)

    _id_counter: ClassVar[int] = 0

    def __post_init__(self):
        if self.id is None:
            self.id = Bus._id_counter
            Bus._id_counter += 1
        else:
            self.id = int(self.id)
            if self.id >= Bus._id_counter:
                Bus._id_counter = self.id + 1

        if self.name is None:
            self.name = f"Bus {self.id}"

        # Add the bus to the network
        self.network.buses.append(self)
    
    @property
    def theta_rad(self) -> float:
        return np.deg2rad(self.theta)
    
    @property
    def p(self) -> float:
        """Net active power injection (pu)"""
        return sum(g.p for g in self.generators) - sum(l.p for l in self.loads)

    @property
    def q(self) -> float:
        """Net reactive power injection (pu)"""
        return sum(g.q for g in self.generators) - sum(l.q for l in self.loads) 

    @property
    def shunt(self) -> complex:
        """Shunt admittance connected to the bus (pu)"""
        return (self.Sh*1j)/self.Sb
    
    # add_generator and add_load methods are used inside Generator and Load classes automatically. 
    # You just need to inform wich bus the generator or load is connected to.
    def add_generator(self, generator: 'Generator'):
        if generator not in self.generators:
            self.generators.append(generator)

    def add_load(self, load: 'Load'):
        if load not in self.loads:
            self.loads.append(load)

    def __repr__(self):
        return (f"Bus(id={self.id}, type={self.bus_type}, v={self.v:.3f} pu, "
                 f"theta={self.theta_rad:.3f} rad, p={self.p:.3f} pu, q={self.q:.3f} pu, "
                 f"shunt={self.shunt:.3f} pu, "
                 f"gen={len(self.generators)}, load={len(self.loads)})")
    

# Exemplo de uso da classe Bus
if __name__ == "__main__":
    # Exemplo fictício de uma classe Network, substitua por sua própria implementação
    class Network:
        def __init__(self):
            self.buses = []

    # Criando uma rede
    net = Network()

    # Criando instâncias de Bus
    bus1 = Bus(network=net, id=1, name="Bus 1", bus_type="PV", v=1.02, theta=0.0, Sb=100.0, Sh=0.0)
    bus2 = Bus(network=net, id=2, name="Bus 2", bus_type="PQ", v=1.0, theta=0.0, Sb=100.0, Sh=0.0)
    
    # Exibindo informações sobre os busses
    print(bus1)
    print(bus2)

    # Acessando a lista de buses na rede
    print(f"Buses in network: {net.buses}")