# --- Problema 5 - Mistura de Ligas Metálicas ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
Ligas = [1, 2, 3, 4, 5]

#-- Parâmetros -- Propriedades das ligas (em proporção decimal) ---
# Valores extraídos da tabela de propriedades das ligas[cite: 2]
Estanho = {1: 0.60, 2: 0.25, 3: 0.45, 4: 0.20, 5: 0.50} # Porcentagem de tin
Zinco = {1: 0.10, 2: 0.15, 3: 0.45, 4: 0.50, 5: 0.40} # Porcentagem de zinco
Chumbo = {1: 0.30, 2: 0.60, 3: 0.10, 4: 0.30, 5: 0.10} # Porcentagem de chumbo

Custo = {1: 22, 2: 20, 3: 25, 4: 24, 5: 27} # Custo ($/lb)[cite: 2]

# Proporções desejadas para a nova liga[cite: 2]
Req_Estanho = 0.40
Req_Zinco = 0.35
Req_Chumbo = 0.25

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[i] = Proporção da liga 'i' a ser utilizada na mistura final
Modelo.X = Pyo.Var(Ligas, domain=Pyo.NonNegativeReals) #--> X_i >= 0

#[F.O.]
# Minimizar o custo total da mistura (para 1 unidade da nova liga)
Modelo.FO = Pyo.Objective(expr = sum(Custo[i] * Modelo.X[i] for i in Ligas),
                          sense = Pyo.minimize)

#-- Restrições --

# A soma das proporções de todas as ligas deve resultar em 100% da nova mistura 
Modelo.Restricao_Proporcao_Total = Pyo.Constraint(expr = 
                                                  sum(Modelo.X[i] for i in Ligas) == 1)

# Restrição de composição de Estanho (Tin) na nova liga
Modelo.Restricao_Estanho = Pyo.Constraint(expr = 
                                          sum(Estanho[i] * Modelo.X[i] for i in Ligas) == Req_Estanho)

# Restrição de composição de Zinco (Zinc) na nova liga
Modelo.Restricao_Zinco = Pyo.Constraint(expr = 
                                        sum(Zinco[i] * Modelo.X[i] for i in Ligas) == Req_Zinco)

# Restrição de composição de Chumbo (Lead) na nova liga
Modelo.Restricao_Chumbo = Pyo.Constraint(expr = 
                                         sum(Chumbo[i] * Modelo.X[i] for i in Ligas) == Req_Chumbo)

#-- Otimizando a partir da função de relatório
print('Status = ', resolver(Modelo))
relatorio(Modelo)