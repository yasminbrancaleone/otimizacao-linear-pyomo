# --- Problema - Aluguel de Armazém ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
Meses = [1, 2, 3, 4, 5]

# Lista de tuplas (mes_inicio, duracao) representando todas as opções válidas de aluguel.
Opcoes_Aluguel = [(i, j) for i in Meses for j in range(1, 6 - i + 1)]

#-- Parâmetros --
Demanda = {1: 30000, 2: 20000, 3: 40000, 4: 10000, 5: 50000} # Espaço necessário por mês em Sq. Ft.
Custo = {1: 65, 2: 100, 3: 135, 4: 160, 5: 190} # Custo por Sq. Ft. baseado no período do aluguel

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[i, j] = Quantidade de espaço alugado iniciando no mês 'i' com duração de 'j' meses
Modelo.X = Pyo.Var(Opcoes_Aluguel, domain=Pyo.NonNegativeReals) #--> X_i,j >= 0

#[F.O.]
# Minimizar o custo total de todos os contratos de aluguel firmados
Modelo.FO = Pyo.Objective(expr = sum(Custo[j] * Modelo.X[i, j] for (i, j) in Opcoes_Aluguel),
                          sense = Pyo.minimize)

#-- Restrições --
Modelo.Restricao_Demanda = Pyo.ConstraintList()

# Para cada mês 'm', a soma de todos os aluguéis ativos deve ser maior ou igual à demanda daquele mês.
for m in Meses:
    espaco_ativo = sum(Modelo.X[i, j] for (i, j) in Opcoes_Aluguel if i <= m and i + j - 1 >= m)
    Modelo.Restricao_Demanda.add(expr = espaco_ativo >= Demanda[m])

#-- Otimizando a partir da função de relatório
print('Status = ', resolver(Modelo))
relatorio(Modelo)