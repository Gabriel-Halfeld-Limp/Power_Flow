import numpy as np
from dataclasses import dataclass
from typing import Optional, ClassVar, Dict
from Bus_model import Bus

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
        return (f"Line(id={self.name}, Barra para:{self.from_bus.id}, Barra de:{self.to_bus.id}, r={self.resistance:.4f}, x={self.reactance:.4f}, tap_ratio={self.tap_ratio:.4f}, tap_phase={self.tap_phase:.4f}, b_half={self.shunt_admittance_half:.4f})")