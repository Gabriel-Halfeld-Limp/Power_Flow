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