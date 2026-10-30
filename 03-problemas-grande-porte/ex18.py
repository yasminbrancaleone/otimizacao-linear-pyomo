# --- Problema 18 - Resgate na Ilha ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
# Itens essenciais para a sobrevivência do grupo
Itens = ['Alimento', 'Agua', 'Municao', 'Remedios']

#-- Parâmetros --
# O grupo necessita de quantidades específicas máximas de cada item
Necessidade = {'Alimento': 6, 'Agua': 4, 'Municao': 2, 'Remedios': 2}

# Valores de importância (peso para a sobrevivência)
# Munição e remédios = 4x Alimentos e 2x Água. 
# Se definirmos Alimento = 1, então Água = 2, Munição = 4 e Remédios = 4.
Importancia = {'Alimento': 1, 'Agua': 2, 'Municao': 4, 'Remedios': 4}

# Capacidade máxima de transporte do helicóptero em número de caixas
Capacidade_Helicoptero = 7

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[i] = Quantidade de caixas do item 'i' a serem enviadas
# Como são caixas físicas indivisíveis, utilizamos o domínio de números inteiros não negativos
Modelo.X = Pyo.Var(Itens, domain=Pyo.NonNegativeIntegers) #--> X_i >= 0 e Inteiro

#[F.O.]
# O objetivo é maximizar o valor de sobrevivência da carga de socorro enviada
Modelo.FO = Pyo.Objective(expr = sum(Importancia[i] * Modelo.X[i] for i in Itens),
                          sense = Pyo.maximize)

#-- Restrições --

# 1. Restrição de Capacidade: O helicóptero só pode transportar até 7 caixas no total
Modelo.Restricao_Capacidade = Pyo.Constraint(
    expr = sum(Modelo.X[i] for i in Itens) <= Capacidade_Helicoptero
)

# 2. Restrição de Necessidade Máxima: Não faz sentido enviar mais caixas do que o grupo necessita de cada item
Modelo.Restricao_Necessidade = Pyo.ConstraintList()
for i in Itens:
    Modelo.Restricao_Necessidade.add(
        expr = Modelo.X[i] <= Necessidade[i]
    )

print('Status = ', resolver(Modelo))
relatorio(Modelo)