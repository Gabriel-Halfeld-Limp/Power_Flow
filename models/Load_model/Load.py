from dataclasses import dataclass
from typing import Optional, ClassVar
from PowerDevice import PowerDevice  # <- Importando de outro arquivo

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