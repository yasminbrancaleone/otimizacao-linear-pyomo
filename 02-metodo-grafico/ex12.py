# --- Problema 12 - Esportes Radicais S.A. ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
# Produtos fabricados pela empresa
Produtos = ['Paraquedas', 'Asa_delta']

# Linhas de montagem
Linhas = ['Linha_1', 'Linha_2']

#-- Parâmetros --
# Lucro unitário de cada produto (R$)
Lucro = {'Paraquedas': 60.00, 'Asa_delta': 40.00}

# Tempo disponível por semana em cada linha (em horas)
Disponibilidade = {'Linha_1': 100, 'Linha_2': 42}

# Tempo de processamento necessário de cada produto em cada linha (em horas)
Tempo_Processamento = {
    ('Linha_1', 'Paraquedas'): 10, ('Linha_1', 'Asa_delta'): 10,
    ('Linha_2', 'Paraquedas'): 3,  ('Linha_2', 'Asa_delta'): 7
}

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[p] = Quantidade de unidades produzidas semanalmente do produto 'p'
Modelo.X = Pyo.Var(Produtos, domain=Pyo.NonNegativeReals) #--> X_p >= 0

#[F.O.]
# O objetivo é maximizar o lucro total da produção
Modelo.FO = Pyo.Objective(expr = sum(Lucro[p] * Modelo.X[p] for p in Produtos),
                          sense = Pyo.maximize)

#-- Restrições --
Modelo.Restricao_Capacidade = Pyo.ConstraintList()

# O tempo total gasto em cada linha não pode exceder as horas semanais disponíveis para a fabricação dos produtos
for l in Linhas:
    Modelo.Restricao_Capacidade.add(
        expr = sum(Tempo_Processamento[l, p] * Modelo.X[p] for p in Produtos) <= Disponibilidade[l]
    )

print('Status = ', resolver(Modelo))
relatorio(Modelo)