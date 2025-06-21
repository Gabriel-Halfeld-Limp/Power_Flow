# CTDF-for-linear-load-methods

Implementação dos Current Transfer Distribution Factors (CTDF) de Sauer para análise de fluxos de potência em redes elétricas.

## Descrição

Este projeto contém uma implementação dos métodos de fluxo de potência AC e DC, além do cálculo dos fatores de distribuição de corrente (CTDFs) para diferentes sistemas de barras (IEEE 14 barras, Sauer 6, 11, etc). O código permite comparar resultados de fluxo de potência AC, DC e CTDF, além de analisar o impacto de perturbações de carga.

Os experimentos e gráficos principais estão organizados no notebook [`main.ipynb`](main.ipynb).

## Estrutura do Projeto

- `main.ipynb`: Notebook principal com exemplos, gráficos e análises.
- `requirements.txt`: Lista de dependências Python necessárias.
- `power/`: Implementação dos modelos elétricos, fluxo de potência e CTDF (Montado em Network e elementos calculados em Line).
- `systems/`: Definição dos sistemas de barras (IEEE14, Sauer6, Sauer11, etc).

## Instalação

1. **Clone o repositório:**

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd CTDF-for-linear-load-methods
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

## Como rodar

O projeto foi desenvolvido para ser executado em um ambiente Jupyter Notebook.

2. **Abra o arquivo [`main.ipynb`](main.ipynb).**

3. **Execute as células do notebook para reproduzir os experimentos, gráficos e análises.**

## Observações

- O notebook utiliza as bibliotecas `numpy`, `matplotlib`, `pandas` e outras listadas em [`requirements.txt`](requirements.txt).
- Os sistemas de barras estão definidos em [`systems/`](systems/) e os modelos elétricos em [`power/`](power/).
- Para adicionar novos sistemas ou métodos, basta seguir a estrutura dos arquivos existentes.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE) para mais detalhes.

---