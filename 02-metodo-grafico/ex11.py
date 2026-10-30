# --- Problema 11 - Produção da Pizzaria ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
# Produtos fabricados pela pizzaria
Produtos = ['Pizza', 'Calzone']

#-- Parâmetros --
# Receita de venda por unidade (R$)
Receita = {'Pizza': 18.00, 'Calzone': 22.00}

# Consumo de queijo por unidade (em gramas)
Queijo = {'Pizza': 40, 'Calzone': 60}

# Tempo de produção por unidade (em horas)
# O pizzaiolo faz 16 pizzas por hora (1/16 de hora por pizza) ou 9 calzones por hora (1/9 de hora por calzone)
Tempo_Producao = {'Pizza': 1/16, 'Calzone': 1/9}

# Disponibilidades diárias
# A pizzaria tem 3 pizzaiolos que trabalham 8 horas por dia (3 * 8 = 24 horas totais)
Horas_Disponiveis = 3 * 8 

# O total de queijo disponível é de 5 kg (5000 gramas) por dia
Queijo_Disponivel = 5000

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[p] = Quantidade de unidades produzidas e vendidas do produto 'p' diariamente
Modelo.X = Pyo.Var(Produtos, domain=Pyo.NonNegativeReals) #--> X_p >= 0

#[F.O.]
# O objetivo é maximizar a receita total diária
Modelo.FO = Pyo.Objective(expr = sum(Receita[p] * Modelo.X[p] for p in Produtos),
                          sense = Pyo.maximize)

#-- Restrições --

# 1. Restrição de tempo de trabalho: O tempo total gasto não pode exceder as horas disponíveis de todos os pizzaiolos
Modelo.Restricao_Tempo = Pyo.Constraint(
    expr = sum(Tempo_Producao[p] * Modelo.X[p] for p in Produtos) <= Horas_Disponiveis
)

# 2. Restrição de queijo: O consumo de queijo não pode exceder os 5 kg (5000 g) disponíveis
Modelo.Restricao_Queijo = Pyo.Constraint(
    expr = sum(Queijo[p] * Modelo.X[p] for p in Produtos) <= Queijo_Disponivel
)

print('Status = ', resolver(Modelo))
relatorio(Modelo)