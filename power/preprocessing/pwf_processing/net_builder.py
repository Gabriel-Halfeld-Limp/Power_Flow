from .pwf_reader import PWF_Reader
from power.models.electricity_models import *

class PWF_Network_Builder:
    """
    Class for building a network from PWF (Power Flow) data.
    """

    def __init__(self, caminho_arquivo):
        self.reader = PWF_Reader(caminho_arquivo)
        self.net_name = self.reader.nome_sistema
        self.df_bar = self.reader.df_bar
        self.df_lin = self.reader.df_lin
        self.df_dcte = self.reader.df_dcte
        self.df_titu = self.reader.df_titu
        self.df_dglt = self.reader.df_dglt
        self.Sb = self.df_dcte['BASE'].values[0]
        self.bus_dict = {} # Dictionary to store bus objects and its ID
        self.net = Network(name=self.net_name)
    
    def build_buses(self):
        """
        Build bus objects from the DBAR block.
        """
        self.buses = []
        for _, row in self.df_bar.iterrows():
            bus = Bus(
                network = self.net,
                id = row['NUM'],
                name = row['NOME'],
                bus_type = row['TPO'],
                v = row['V'],
                theta = row['A'],
                Sb = self.Sb,
                Sh = row['SH'],
            )
            self.buses.append(bus)
            self.bus_dict[bus.id] = bus # Add bus to the dictionary
        
        return self.net
        
    def build_lines(self):
        """
        Build line objects from the DLIN block.
        """
        self.lines = []
        line_counter = 1 # Counter to assign unique IDs to lines
        for _, row in self.df_lin.iterrows():
            frombus = self.bus_dict[row['DE']]
            tobus = self.bus_dict[row['PARA']]

            line = Line(
                from_bus = frombus,
                to_bus = tobus,
                id = line_counter,
                name = f"Line {line_counter}",
                r = row['R%']/self.Sb,
                x = row['X%']/self.Sb,
                b_half = (row['B'] * 0.5)/self.Sb,
                tap_ratio = row['TAP'],
                tap_phase = row['PHS'],
            )
            self.lines.append(line)
            line_counter += 1
        
        return self.net
    
    def build_generators(self):
        """
        Build generator objects from the DGLT block.
        """
        self.generators = []
        gen_counter = 1  # Counter to assign unique IDs to generators

        for _, row in self.df_bar.iterrows():
            # Verifica se há geração (considerando todos os campos)
            if any(row[key] != 0 for key in ['PG', 'QG', 'QM', 'QN']):
                bus = self.bus_dict[row['NUM']]
                generator = Generator(
                    bus=bus,
                    id=gen_counter,
                    name=f"Generator {gen_counter}",
                    pb = self.Sb,
                    p_input=row['PG'],
                    q_input=row['QG'],
                    q_max_input=row['QM'],
                    q_min_input=row['QN'],
                )
                self.generators.append(generator)
                gen_counter += 1
        return self.net
    
    def build_loads(self):
        """
        Build load objects from the DTITU block.
        """
        self.loads = []
        load_counter = 1  # Counter to assign unique IDs to loads

        for _, row in self.df_bar.iterrows():
            # Verifica se há carga
            if row['PL'] != 0 or row['QL'] != 0:
                bus = self.bus_dict[row['NUM']]
                load = Load(
                    bus=bus,
                    id=load_counter,
                    name=f"Load {load_counter}",
                    pb = self.Sb,
                    p_input=row['PL'],
                    q_input=row['QL'],
                )
                self.loads.append(load)
                load_counter += 1
        return self.net

    def build_network(self):
        """
        Build the network by calling the methods to build buses, lines, generators, and loads.
        """
        self.build_buses()
        self.build_lines()
        self.build_generators()
        self.build_loads()
        return self.net