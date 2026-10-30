# --- Problema 19 - Companhia de Reflorestamento ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
Cidades = [1, 2, 3, 4]
Especies = ['Pinus', 'Carvalho', 'Nogueira', 'Araucaria']

#-- Parâmetros --

# Área disponível por cidade (em hectares)
Area_Disponivel = {1: 1500, 2: 1700, 3: 900, 4: 600}

# Produção Anual Esperada (em m³/ha)
Producao = {
    (1, 'Pinus'): 17, (1, 'Carvalho'): 14, (1, 'Nogueira'): 10, (1, 'Araucaria'): 9,
    (2, 'Pinus'): 15, (2, 'Carvalho'): 16, (2, 'Nogueira'): 12, (2, 'Araucaria'): 11,
    (3, 'Pinus'): 13, (3, 'Carvalho'): 12, (3, 'Nogueira'): 14, (3, 'Araucaria'): 8,
    (4, 'Pinus'): 10, (4, 'Carvalho'): 11, (4, 'Nogueira'): 8,  (4, 'Araucaria'): 6
}

# Renda Anual Esperada (em u.m./ha)
Renda = {
    (1, 'Pinus'): 16, (1, 'Carvalho'): 12, (1, 'Nogueira'): 20, (1, 'Araucaria'): 18,
    (2, 'Pinus'): 14, (2, 'Carvalho'): 13, (2, 'Nogueira'): 24, (2, 'Araucaria'): 20,
    (3, 'Pinus'): 17, (3, 'Carvalho'): 10, (3, 'Nogueira'): 28, (3, 'Araucaria'): 20,
    (4, 'Pinus'): 12, (4, 'Carvalho'): 11, (4, 'Nogueira'): 18, (4, 'Araucaria'): 17
}

# Usando os valores nominais da tabela 
Producao_Minima = {
    'Pinus': 225, 
    'Carvalho': 9, 
    'Nogueira': 4.8, 
    'Araucaria': 3.5
}

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[c, e] = Quantidade de área (em hectares) designada para a espécie 'e' no município 'c'
Modelo.X = Pyo.Var(Cidades, Especies, domain=Pyo.NonNegativeReals) #--> X_c,e >= 0

#[F.O.]
# O objetivo é maximizar a renda anual total esperada de todos os plantios
Modelo.FO = Pyo.Objective(expr = sum(Renda[c, e] * Modelo.X[c, e] for c in Cidades for e in Especies),
                          sense = Pyo.maximize)

#-- Restrições --

# 1. Restrição de Área: O somatório das áreas plantadas com qualquer espécie em uma cidade 
# não pode ultrapassar o limite de área daquela cidade.
Modelo.Restricao_Area = Pyo.ConstraintList()
for c in Cidades:
    Modelo.Restricao_Area.add(
        expr = sum(Modelo.X[c, e] for e in Especies) <= Area_Disponivel[c]
    )

# 2. Restrição de Produção: A soma da produção gerada de uma espécie em todas as cidades 
# deve ser no mínimo o valor de produção mínima exigido.
Modelo.Restricao_Producao = Pyo.ConstraintList()
for e in Especies:
    Modelo.Restricao_Producao.add(
        expr = sum(Producao[c, e] * Modelo.X[c, e] for c in Cidades) >= Producao_Minima[e]
    )

#-- Otimizando a partir da função de relatório
status = resolver(Modelo)
print('Status = ', status)

# Verificação de segurança: só roda o relatório se o solver achou uma solução viável
if str(status) == 'optimal' or str(status) == 'ok':
    relatorio(Modelo)
else:
    print("\nO solver não conseguiu gerar o relatório porque o modelo é matematicamente inviável (sem solução possível).")