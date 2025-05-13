# Power_Flow

Este projeto implementa uma ferramenta modular em Python para modelagem de redes elétricas e simulação de fluxo de potência. Ele utiliza dados extraídos de arquivos `.PWF` e constrói estruturas internas que representam barras, linhas de transmissão, cargas e geradores.

## 🧠 Funcionalidades

- Leitura de arquivos `.PWF` com dados do sistema elétrico.
- Construção automática de redes através do `PWF_Network_Builder`
- Modelagem orientada a objetos de:
  - Barras (Bus)
  - Linhas de transmissão (Line)
  - Cargas (Load)
  - Geradores (Generator)
  - Rede (Network) 
- Cálculo do Fluxo AC por Newton-Raphson

## 🗂️ Estrutura do Projeto

Power_Flow/
│
├── main.ipynb              # Notebook principal (executa leitura de arquivos .PWF)
├── Complete_Code.ipynb     # Todas as classes e exemplos combinados
├── exemples.ipynb          # Exemplos com sistemas 3Bus e 14Bus (dados no código)
│
├── Bus_model.py            # Classe Bus
├── Line_model.py           # Classe Line
├── Load_model.py           # Classe Load
├── Generator_model.py      # Classe Generator
├── Network_model.py        # Classe principal (constrói rede e calcula Ybus)
├── AC_PF.py                # Funções para cálculo de fluxo de potência AC
├── pwf_reader.py           # Leitura de arquivos .PWF
├── net_builder.py          # Constrói a rede automaticamente
│
├── pwf_systems/            # Diretório com arquivos .PWF
│   └── IEEE14.pwf          # Exemplo de sistema IEEE 14 barras
│
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto

## ▶️ Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Power_Flow.git
   cd Power_Flow

2. Crie um ambiente virtual (opcional):
    python -m venv venv
    source venv/bin/activate
    venv\Scripts\activate

3. Instale as dependências:
    pip install -r requirements.txt

4. Execute o arquivo principal:
    python main.py
    abra main.ipynb e altere o caminho do arquivo .PWF para o sistema desejado.
    caminho = 'pwf_systems/IEEE14.pwf'

