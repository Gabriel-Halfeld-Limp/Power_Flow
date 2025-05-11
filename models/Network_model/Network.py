from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
import numpy as np

from Bus_model.Bus import Bus
from Line_model.Line import Line
from Load_model.Load import Load
from Generator_model.Generator import Generator

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
        for line in self.lines: #Adiciona os elementos de admitância da linha
            for (i, j), y in line.get_admittance_elements(bus_idx):
                ybus[i, j] += y
        
        for i, bus in enumerate(self.buses):
            ybus[i, i] += bus.shunt
    
        return ybus
        
    def get_G(self):
        return self.y_bus().real
    
    def get_B(self):
        return self.y_bus().imag
    
    def __repr__(self):
        return f"Network(id={self.id}, name={self.name})"