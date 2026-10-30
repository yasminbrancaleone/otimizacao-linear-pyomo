# --- Problema 1 - Fundição ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
Insumos = ['Lingote', 'Grafite', 'Sucata']

#-- Parâmetros -- Composições de Carbono e Silício (Dict) ---
Carbono = {'Lingote': 0.0050, 'Grafite':0.90, 'Sucata':0.090}
Silicio = {'Lingote': 0.14, 'Grafite':0.00, 'Sucata':0.27}

Custo = {'Lingote':90, 'Grafite':180, 'Sucata':25}
Estoque = {'Lingote':5, 'Grafite':5, 'Sucata':12}

Demanda = 10
Carbono_Minimo = 0
Carbono_Maximo = 0.095
Silicio_Minimo = 0.19
Silicio_Maximo = 0.20

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
Modelo.X = Pyo.Var(Insumos, domain=Pyo.NonNegativeReals) #--> X_i >= 0

#[F.O.]
Modelo.FO = Pyo.Objective(expr = sum(Custo[i] * Modelo.X[i] for i in Insumos),
                          sense = Pyo.minimize)

#-- Restrições --

Modelo.Restricao_Demanda = Pyo.Constraint(expr =
                                          sum(Modelo.X[i] for i in Insumos) ==  Demanda)

Modelo.Restricao_C_Max = Pyo.Constraint(expr = sum(Carbono[i] * Modelo.X[i]
                                                   for i in Insumos) <= Carbono_Maximo * Demanda)
Modelo.Restricao_C_Min = Pyo.Constraint(expr = sum(Carbono[i] * Modelo.X[i]
                                                   for i in Insumos) >= Carbono_Minimo * Demanda)
Modelo.Restricao_Si_Max = Pyo.Constraint(expr = sum(Silicio[i] * Modelo.X[i]
                                                    for i in Insumos) <= Silicio_Maximo * Demanda)
Modelo.Restricao_Si_Min = Pyo.Constraint(expr = sum(Silicio[i] * Modelo.X[i]
                                                    for i in Insumos) >= Silicio_Minimo * Demanda)

Modelo.Restricao_Estoque = Pyo.ConstraintList()
for i in Insumos:
  Modelo.Restricao_Estoque.add(Modelo.X[i] <= Estoque[i])

#-- Otimizando a partir da função de relatório
print('Status = ', resolver(Modelo))
relatorio(Modelo)