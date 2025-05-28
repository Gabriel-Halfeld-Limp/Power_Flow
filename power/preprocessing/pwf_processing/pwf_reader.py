import pandas as pd

class PWF_Reader:
    """
    Class for reading PWF (Power Flow) files and extracting system data into DataFrames.
    """
    def __init__(self, caminho_arquivo):
        self.caminho = caminho_arquivo
        self.df_bar = None      # DataFrame for DBAR block (bus data)
        self.df_lin = None      # DataFrame for DLIN block (line data)
        self.df_dcte = None     # DataFrame for DCTE block (system constants)
        self.df_titu = None     # DataFrame for TITU block (system title)
        self.df_dglt = None     # DataFrame for DGLT block (voltage limits)
        self.nome_sistema = None
        self._ler_arquivo()     # Read and parse the file

    def _ler_arquivo(self):
        # Read all lines from the file
        with open(self.caminho, 'r') as f:
            linhas = f.readlines()

        i = 0
        while i < len(linhas):
            linha = linhas[i]

            # Detect and read TITU block (system name/title)
            if linha.strip().startswith('TITU'):
                self._ler_titu(linhas, i)
                i += len(self.df_titu)  # Move past the TITU block
                continue

            # Detect and read DCTE block (system parameters/constants)
            if linha.strip().startswith('DCTE'):
                self._ler_dcte(linhas, i)
                i += 1  # Move past the DCTE block
                continue

            # Detect and read DBAR block (bus data)
            if linha.strip().startswith('DBAR'):
                self._ler_dbar(linhas, i)
                i += len(self.df_bar)  # Move past the DBAR block
                continue

            # Detect and read DLIN block (line data)
            if linha.strip().startswith('DLIN'):
                self._ler_dlin(linhas, i)
                i += len(self.df_lin)  # Move past the DLIN block
                continue

            # Detect and read DGLT block (voltage limits per generator)
            if linha.strip().startswith('DGLT'):
                self._ler_dglt(linhas, i)
                i += 1  # Move past the DGLT block
                continue

            i += 1

    def _ler_titu(self, linhas, i):
        """ Read TITU block (system title) """
        i += 1  # Skip to the line with the system name
        self.nome_sistema = linhas[i].strip()  # Remove asterisks and whitespace
        self.df_titu = pd.DataFrame({'Nome do Sistema': [self.nome_sistema]})

    def _ler_dcte(self, linhas, i):
        """ Read DCTE block (system constants) """
        dados_dcte = {}
        i += 2  # Skip header line with (Mn)(Val)
        
        while i < len(linhas):
            linha = linhas[i].strip()
            if linha.startswith("9999"):  # End of block
                break
            
            j = 0
            # Read key-value pairs in fixed-width format
            while j + 5 < len(linha):
                chave = linha[j:j+4].strip()
                valor = linha[j+5:j+12].strip()
                try:
                    dados_dcte[chave] = float(valor)
                except ValueError:
                    dados_dcte[chave] = valor  # Keep as string if not a float
                j += 12  # Move to next key-value pair

            i += 1

        self.df_dcte = pd.DataFrame([dados_dcte])

    def _ler_dbar(self, linhas, i):
        """ Read DBAR block (bus data) """
        i += 2  # Skip headers
        dados_barras = []
        while not linhas[i].strip().startswith('99999'):  # End of block
            l = linhas[i]
            dados_barras.append({
                'NUM': int(l[0:6]),
                'TPO': int(l[7]),
                'NOME': l[10:22].strip(),
                'V': float(l[24:28]) / 1000,
                'A': float(l[28:32]) if l[28:32].strip() else 0.0,
                'PG': float(l[32:37]) if l[32:37].strip() else 0.0,
                'QG': float(l[37:42]) if l[37:42].strip() else 0.0,
                'QN': float(l[42:47]) if l[42:47].strip() else 0.0,
                'QM': float(l[47:52]) if l[47:52].strip() else 0.0,
                'BC': float(l[52:58]) if l[52:58].strip() else 0.0,
                'PL': float(l[58:63]) if l[58:63].strip() else 0.0,
                'QL': float(l[63:68]) if l[63:68].strip() else 0.0,
                'SH': float(l[68:73]) if l[68:73].strip() else 0.0,
                'ARE': float(l[73:76]) if l[73:76].strip() else 0.0
            })
            i += 1
        self.df_bar = pd.DataFrame(dados_barras)
        type_map = {
            2: "Slack",
            1: "PV",
            0: "PQ"
        }
        self.df_bar["TPO"] = self.df_bar["TPO"].replace(type_map)

    def _ler_dlin(self, linhas, i):
        """ Read DLIN block (line data) """
        i += 2  # Skip headers
        dados_linhas = []
        while not linhas[i].strip().startswith('99999'):  # End of block
            l = linhas[i]
            dados_linhas.append({
                'DE': int(l[0:5]),
                'PARA': int(l[11:15]),
                'R%': float(l[20:26]) if l[20:26].strip() else 0.0,
                'X%': float(l[26:32]) if l[26:32].strip() else 0.0,
                'B': float(l[32:38]) if l[32:38].strip() else 0.0,
                'TAP': float(l[38:43]) if l[38:43].strip() else 1.0,
                'TAP_MIN': float(l[42:48]) if l[43:48].strip() else 0.0,
                'TAP_MAX': float(l[48:53]) if l[48:53].strip() else 0.0,
                'PHS': float(l[53:58]) if l[53:55].strip() else 0,
                'Bc' : float(l[58:64]) if l[55:61].strip() else 0.0,
                'Cn' : float(l[64:68]) if l[61:67].strip() else 0.0,
                'Ce' : float(l[68:72]) if l[67:73].strip() else 0.0,
                'Ns' : float(l[72:74]) if l[70:73].strip() else 0.0,
            })
            i += 1
        self.df_lin = pd.DataFrame(dados_linhas)

    def _ler_dglt(self, linhas, i):
        """ Read DGLT block (voltage limits per generator) """
        dados_dglt = []
        i += 1  # Skip header line
        
        while i < len(linhas):
            linha = linhas[i].strip()
            if linha.startswith("9999") or linha.upper().startswith("FIM"):  # End of block
                break

            partes = linha.split()
            if len(partes) >= 3:
                try:
                    g = int(partes[0])
                    vmn = float(partes[1])
                    vmx = float(partes[2])
                    dados_dglt.append({'G': g, 'Vmn': vmn, 'Vmx': vmx})
                except ValueError:
                    pass  # Ignore or handle parsing error

            i += 1

        self.df_dglt = pd.DataFrame(dados_dglt)