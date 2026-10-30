# --- Problema 10 - Produção Alumilâminas S.A. ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
# Duas fábricas de produção
Fabricas = ['SP', 'RJ']
# Três tipos de lâminas de alumínio
Laminas = ['Fina', 'Media', 'Grossa']

#-- Parâmetros --
# Custo de produção diário por fábrica
Custo = {'SP': 100000, 'RJ': 200000}

# Contratos fechados de fornecimento (Demanda mínima em toneladas)
Demanda = {'Fina': 16, 'Media': 6, 'Grossa': 28}

# Capacidade produtiva diária (toneladas) de cada fábrica por tipo de lâmina
Producao = {
    ('SP', 'Fina'): 8, ('SP', 'Media'): 1, ('SP', 'Grossa'): 2,
    ('RJ', 'Fina'): 2, ('RJ', 'Media'): 1, ('RJ', 'Grossa'): 7
}

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[f] = Quantidade de dias que a fábrica 'f' deverá operar
# Como o problema pede resolução gráfica e modelagem linear padrão, as variáveis contínuas >= 0
Modelo.X = Pyo.Var(Fabricas, domain=Pyo.NonNegativeReals) #--> X_f >= 0

#[F.O.]
# Minimizar o custo total de operação para atender aos pedidos
Modelo.FO = Pyo.Objective(expr = sum(Custo[f] * Modelo.X[f] for f in Fabricas),
                          sense = Pyo.minimize)

#-- Restrições --
# Restrições de Demanda: garantir que a produção atenda os contratos fechados
Modelo.Restricao_Demanda = Pyo.ConstraintList()

for l in Laminas:
    # A soma da produção diária de ambas as fábricas multiplicada pelos dias operados
    # deve ser maior ou igual à demanda da respectiva lâmina
    Modelo.Restricao_Demanda.add(
        expr = sum(Producao[f, l] * Modelo.X[f] for f in Fabricas) >= Demanda[l]
    )

print('Status = ', resolver(Modelo))
relatorio(Modelo)