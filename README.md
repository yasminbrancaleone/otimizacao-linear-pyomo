# Otimização Linear com Pyomo

Este repositório reúne uma coleção de exercícios e modelos de otimização linear implementados em Python com a biblioteca Pyomo. Os exemplos cobrem desde introdução à modelagem até métodos gráficos, problemas de maior porte e formulações relacionadas ao método simplex.

## Objetivo

O projeto tem como foco praticar a formulação e a solução de problemas de programação linear usando:

- variáveis de decisão;
- restrições;
- função objetivo;
- solver GLPK via Pyomo;
- relatórios de solução com valores das variáveis e das restrições.

## Estrutura do projeto

```text
otimizacao-linear-pyomo/
├── README.md
├── rep.py
├── requirements.txt
├── 01-introducao-modelos/
│   ├── ex1.py
│   ├── ex2.py
│   ├── ex3.py
│   ├── ex5.py
│   └── ex7.py
├── 02-metodo-grafico/
│   ├── ex10.py
│   ├── ex11.py
│   └── ex12.py
├── 03-problemas-grande-porte/
│   ├── ex18.py
│   ├── ex19.py
│   └── ex20.py
├── 04-metodo-simplex/
│   ├── ex22.py
│   └── ex23.py
└──
```

## Arquivos principais

### `rep.py`

Arquivo utilitário compartilhado por todos os exercícios. Ele define:

- `resolver(m, tee=False)`: resolve o modelo usando o solver GLPK;
- `relatorio(m, casas=4, mostrar_zeros=False)`: imprime a função objetivo, as variáveis de decisão e as restrições com seus valores de LHS e RHS.

Esse arquivo centraliza a rotina de solução e facilita a leitura dos resultados em cada exercício.

### `requirements.txt`

Lista as dependências do projeto.

```txt
pyomo>=6.7.0
```

## Como executar

1. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
```

2. Ative o ambiente:

- Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

- Linux/macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute qualquer exemplo:

```bash
python .\01-introducao-modelos\ex1.py
```

## Observação sobre o GLPK

Os scripts usam o solver GLPK, configurado em `rep.py` com um caminho Windows específico:

```python
Pyo.SolverFactory("glpk", executable=r"C:\glpk\winglpk-4.65\glpk-4.65\w64\glpsol.exe")
```

Se a instalação do GLPK estiver em outro local no seu computador, ajuste esse caminho antes de executar os modelos.

## Conteúdo por pasta

### 01 - Introdução aos modelos

Nesse conjunto são modelados problemas clássicos de mistura, produção e alocação, como:

- mistura de materiais com limites de composição;
- dieta/merenda com requisitos nutricionais;
- aluguel de espaço em armazém;
- composição de ligas metálicas;
- escala de operadores e cobertura de demanda.

Exercícios nesta pasta:

- `ex1.py` — problema de fundição com composição de carbono e silício;
- `ex2.py` — problema de merenda das crianças;
- `ex3.py` — aluguel de armazém;
- `ex5.py` — mistura de ligas metálicas;
- `ex7.py` — escala de operadores.

### 02 - Método gráfico

São exemplos que representam problemas de produção e otimização com duas variáveis, muitas vezes utilizados para ilustrar a interpretação geométrica da solução.

Arquivos:

- `ex10.py` — produção de lâminas de alumínio;
- `ex11.py` — produção de pizza e calzone;
- `ex12.py` — produção de paraquedas e asa-delta.

### 03 - Problemas de grande porte

Os scripts desta pasta tratam de modelos mais extensos, com múltiplas variáveis, restrições e cenários de decisão.

Arquivos:

- `ex18.py` — resgate em ilha com itens essenciais;
- `ex19.py` — reflorestamento com cidades, espécies e produção mínima;
- `ex20.py` — dimensionamento de quartos e leitos em hospital, com múltiplos objetivos.

### 04 - Método simplex

Nesta pasta, os exercícios focam em formulações na forma padrão e canônica do simplex, além do uso de variáveis de folga, excesso e artificiais.

Arquivos:

- `ex22.py` — forma padrão e resolução via Pyomo;
- `ex23.py` — forma canônica com variáveis artificiais.

## Considerações gerais

- Os modelos são resolvidos como problemas lineares (LP) ou, em alguns casos, como relaxações lineares e variações inteiras.
- Há exemplos com maximização e minimização de objetivos.
- A bibliografia do conteúdo está implícita nos próprios enunciados dos exercícios, com nomes e contextos específicos em cada problema.
- O código segue uma convenção simples e didática, com comentários em português para facilitar o entendimento acadêmico.

## Recomendação de uso

Use este repositório como material de estudo para:

- aprender a modelar problemas em Pyomo;
- compreender a estrutura de um problema de otimização linear;
- praticar a identificação de variáveis, restrições e funções objetivo;
- comparar diferentes formas de representação (padrão, canônica, com folga/excesso);
- interpretar os resultados gerados pelo solver.

## Licença

Este projeto foi desenvolvido para fins educacionais e de estudo. 