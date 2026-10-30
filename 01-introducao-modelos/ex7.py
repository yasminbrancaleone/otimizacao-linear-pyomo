# --- Problema 7 - Escala de Operadores ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
Operadores = ['K. C.', 'D. H.', 'H. B.', 'S. C.', 'K. S.', 'N. K.']
Dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']

#-- Parâmetros --
# Taxa salarial por hora ($/hora)
Custo = {'K. C.': 25, 'D. H.': 26, 'H. B.': 24, 'S. C.': 23, 'K. S.': 28, 'N. K.': 30}

# Disponibilidade máxima de horas por dia para cada operador
Disponibilidade = {
    ('K. C.', 'Seg'): 6, ('K. C.', 'Ter'): 0, ('K. C.', 'Qua'): 6, ('K. C.', 'Qui'): 0, ('K. C.', 'Sex'): 6,
    ('D. H.', 'Seg'): 0, ('D. H.', 'Ter'): 6, ('D. H.', 'Qua'): 0, ('D. H.', 'Qui'): 6, ('D. H.', 'Sex'): 0,
    ('H. B.', 'Seg'): 4, ('H. B.', 'Ter'): 8, ('H. B.', 'Qua'): 4, ('H. B.', 'Qui'): 0, ('H. B.', 'Sex'): 4,
    ('S. C.', 'Seg'): 5, ('S. C.', 'Ter'): 5, ('S. C.', 'Qua'): 5, ('S. C.', 'Qui'): 0, ('S. C.', 'Sex'): 5,
    ('K. S.', 'Seg'): 3, ('K. S.', 'Ter'): 0, ('K. S.', 'Qua'): 3, ('K. S.', 'Qui'): 8, ('K. S.', 'Sex'): 0,
    ('N. K.', 'Seg'): 0, ('N. K.', 'Ter'): 0, ('N. K.', 'Qua'): 0, ('N. K.', 'Qui'): 6, ('N. K.', 'Sex'): 2
}

# Horas mínimas garantidas por semana
# Estudantes de licenciatura (K. C., D. H., H. B., S. C.) e mestrado/doutoramento (K. S., N. K.)
Horas_Minimas_Semanais = {
    'K. C.': 8, 'D. H.': 8, 'H. B.': 8, 'S. C.': 8, 
    'K. S.': 7, 'N. K.': 7                          
}

# Demanda diária: a instalação funciona das 8 A.M. às 10 P.M. (14 horas por dia)
Demanda_Diaria = 14

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[o, d] = Número de horas que o operador 'o' é designado para trabalhar no dia 'd'
Modelo.X = Pyo.Var(Operadores, Dias, domain=Pyo.NonNegativeReals) #--> X_o,d >= 0

#[F.O.]
# Minimizar o custo total salarial da semana
Modelo.FO = Pyo.Objective(expr = sum(Custo[o] * Modelo.X[o, d] for o in Operadores for d in Dias),
                          sense = Pyo.minimize)

#-- Restrições --

# 1. Cobertura diária: Exatamente 1 operador de plantão (totalizando 14 horas de operação por dia)
Modelo.Restricao_Cobertura = Pyo.ConstraintList()
for d in Dias:
    Modelo.Restricao_Cobertura.add(expr = sum(Modelo.X[o, d] for o in Operadores) == Demanda_Diaria)

# 2. Disponibilidade máxima: Cada operador possui um limite de horas que pode trabalhar por dia
Modelo.Restricao_Disponibilidade = Pyo.ConstraintList()
for o in Operadores:
    for d in Dias:
        Modelo.Restricao_Disponibilidade.add(expr = Modelo.X[o, d] <= Disponibilidade[o, d])

# 3. Horas mínimas: Cada operador tem um nível mínimo de horas por semana para manter o conhecimento
Modelo.Restricao_Horas_Minimas = Pyo.ConstraintList()
for o in Operadores:
    Modelo.Restricao_Horas_Minimas.add(expr = sum(Modelo.X[o, d] for d in Dias) >= Horas_Minimas_Semanais[o])

#-- Otimizando a partir da função de relatório
print('Status = ', resolver(Modelo))
relatorio(Modelo)