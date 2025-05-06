from __future__ import annotations
import numpy as np
import math
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Dict
import pandas as pd


@dataclass
class Bus:
    network: "Network"
    id: Optional[int] = None
    name: Optional[str] = None
    bus_type: str = "PQ"  # "slack", "PQ", "PV"
    v: float = 1.0 # in pu
    theta: float = 0.0 # in degrees

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
                 f"gen={len(self.generators)}, load={len(self.loads)})")
    
@dataclass
class PowerDevice:
    bus: Bus
    name: Optional[str] = None
    pb: float = 1.0
    p_input: float = 0.0
    q_input: float = 0.0
    p_max_input: float = float('inf')
    p_min_input: float = 0.0
    q_max_input: Optional[float] = None
    q_min_input: Optional[float] = None
    cost_a_input: float = 0.0
    cost_b_input: float = 0.0
    cost_c_input: float = 0.0

    _counter: int = field(default=0, init=False, repr=False)

    @property
    def p(self) -> float:
        return self.p_input / self.pb
    
    @property
    def q(self) -> float:
        return self.q_input / self.pb

    @property
    def p_max(self) -> float:
        return self.p_max_input / self.pb
    
    @property
    def p_min(self) -> float:
        return self.p_min_input / self.pb
    
    @property
    def q_max(self) -> Optional[float]:
        return self.q_max_input / self.pb if self.q_max_input is not None else None

    @property
    def q_min(self) -> Optional[float]:
        return self.q_min_input / self.pb if self.q_min_input is not None else None

    @property
    def cost_a(self) -> float:
        return self.cost_a_input * self.pb
    
    @property
    def cost_b(self) -> float:
        return self.cost_b_input * self.pb
    
    @property
    def cost_c(self) -> float:
        return self.cost_c_input * self.pb
    
@dataclass
class Generator(PowerDevice):
    id: Optional[int] = None
    _id_counter: ClassVar[int] = 0
    def __post_init__(self):
        if self.id is None:
            self.id = Generator._id_counter
            Generator._id_counter += 1
        else:
            self.id = int(self.id)
            if self.id >= Generator._id_counter:
                Generator._id_counter = self.id + 1

        if self.name is None:
            self.name = f"Generator {self.id}"
            
        self.bus.add_generator(self)
        self.network = self.bus.network
        self.network.generators.append(self)

    def __repr__(self):
        return (f"Generator(id={self.id}, bus={self.bus.id}, p={self.p:.3f}, q={self.q:.3f}, "
                f"p_range=[{self.p_min:.3f},{self.p_max:.3f}], q_range=[{self.q_min},{self.q_max}])")

@dataclass
class Load(PowerDevice):
    id: Optional[int] = None

    _id_counter: ClassVar[int] = 0

    def __post_init__(self):
        if self.id is None:
            self.id = Load._id_counter
            Load._id_counter += 1
        else:
            self.id = int(self.id)
            if self.id >= Load._id_counter:
                Load._id_counter = self.id + 1

        if self.name is None:
            self.name = f"Load {self.id}"
            
        self.bus.add_load(self)
        self.network = self.bus.network
        self.network.loads.append(self)

    def __repr__(self):
        return (f"Load(id={self.id}, bus={self.bus.id}, p={self.p:.3f}, q={self.q:.3f}, "
                f"p_range=[{self.p_min:.3f},{self.p_max:.3f}], q_range=[{self.q_min},{self.q_max}])")

@dataclass
class Line:
    from_bus: Bus
    to_bus: Bus
    id: Optional[int] = None
    name: Optional[str] = None
    pb: float = 1.0
    vb: float = 1.0
    r: float = 0.0
    x: float = 0.01
    b_half: float = 0.0
    flux_max: float = float('inf')
    tap_ratio: float = 1.0
    tap_phase: float = 0.0

    _id_counter: ClassVar[int] = 0  # ID counter for lines

    def __post_init__(self):
        # Set default values if not provided
        if self.id is None:
            self.id = Line._id_counter
            Line._id_counter += 1
        else:
            self.id = int(self.id)
            if self.id >= Line._id_counter:
                Line._id_counter = self.id + 1

        if self.name is None:
            self.name = f"Line {self.id}"
        else:
            self.name = str(self.name)

        if self.from_bus.network != self.to_bus.network:
            raise ValueError("Both buses must belong to the same network.")
        
        self.network = self.from_bus.network #Add network to line
        self.network.lines.append(self) #Add line to network

    @property
    def zb(self) -> float:
        """Impedância base (pu)"""
        return self.vb**2 / self.pb

    @property
    def resistance(self) -> float:
        """Resistência da linha (pu)"""
        return self.r / self.zb

    @property
    def reactance(self) -> float:
        """Reatância da linha (pu)"""
        return self.x / self.zb

    @property
    def shunt_admittance_half(self) -> float:
        """Admitância shunt (half) (pu)"""
        return self.b_half / self.zb

    @property
    def impedance(self) -> complex:
        """Impedância da linha (ohms)"""
        return complex(self.resistance, self.reactance)

    @property
    def admittance(self) -> complex:
        """Admitância da linha (S)"""
        return 1 / self.impedance

    @property
    def tap_phase_rad(self) -> float:
        """Fase de tap em radianos"""
        return np.deg2rad(self.tap_phase)

    def get_admittance_elements(self, bus_index: Dict[str, int]):
        """Gera os elementos de admitância baseados nos parâmetros da linha"""
        y = self.admittance
        b = self.shunt_admittance_half * 1j
        a = self.tap_ratio * np.exp(1j * self.tap_phase_rad)
        i = bus_index[self.from_bus.id]
        j = bus_index[self.to_bus.id]
        if self.tap_ratio != 1.0 or self.tap_phase != 0.0:
            Yff = y / (a * np.conj(a)) + b
            Yft = -y / np.conj(a)
            Ytf = -y / a
            Ytt = y + b
        else:
            Yff = y + b
            Yft = -y
            Ytf = -y
            Ytt = y + b
        return [((i, i), Yff), ((i, j), Yft), ((j, i), Ytf), ((j, j), Ytt)]

    def __repr__(self):
        return (f"Line(id={self.name}, Barra para:{self.from_bus.id}, Barra de:{self.to_bus.id}, r={self.resistance:.4f}, x={self.reactance:.4f})")
    
@dataclass
class Network:
    id: Optional[int] = None
    name: Optional[str] = None
    buses: List[Bus] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    loads: List[Load] = field(default_factory=list)
    generators: List[Generator] = field(default_factory=list)

    def y_bus(self) -> np.ndarray:
        """
        Returns the Y bus matrix of the network.
        """
        n = len(self.buses)
        bus_idx = {bus.id: i for i, bus in enumerate(self.buses)}
        ybus = np.zeros((n, n), dtype=complex)
        for line in self.lines:
            for (i, j), y in line.get_admittance_elements(bus_idx):
                ybus[i, j] += y
        return ybus
        
    def get_G(self):
        return self.y_bus().real
    
    def get_B(self):
        return self.y_bus().imag
    
    def __repr__(self):
        return f"Network(id={self.id}, name={self.name})"


# Exemplo de uso: Cálculo da matriz Ybarra para um sistema de 3 barras
if __name__ == "__main__":
    net = Network()
    # Criação das barras
    buses = [
        Bus(net, id=1, bus_type='Slack'),
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
    print(Y)

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