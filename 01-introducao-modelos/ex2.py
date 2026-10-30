# --- Problema 2 - Merenda das Crianças ---
import pyomo.environ as Pyo
from rep import resolver, relatorio

#--- Conjuntos ---
Itens = ['pao', 'pasta_amend', 'geleia', 'biscoito', 'leite', 'suco']

#-- Parâmetros ---
KCAL_fat = {'pao':10,
            'pasta_amend':75,
            'geleia':0,
            'biscoito':20,
            'leite':70,
            'suco':0}

KCAL_tot = {'pao':70,
            'pasta_amend':100,
            'geleia':50,
            'biscoito':60,
            'leite':150,
            'suco':100}

Vit_C = {'pao':0,
         'pasta_amend':0,
         'geleia':3,
         'biscoito':0,
         'leite':2,
         'suco':120}

Prote = {'pao':3,
         'pasta_amend':4,
         'geleia':0,
         'biscoito':1,
         'leite':8,
         'suco':1}

Custo = {'pao':0.05,
         'pasta_amend':0.04,
         'geleia':0.07,
         'biscoito':0.08,
         'leite':0.15,
         'suco':0.35}

#--- Modelagem Numérico ----
Modelo = Pyo.ConcreteModel()

#-[VD]-------------
Modelo.X_b = Pyo.Var(domain = Pyo.NonNegativeIntegers) # Inteira Não Negativa
Modelo.X_pb = Pyo.Var(domain = Pyo.NonNegativeReals)   # Real Não Negativa
Modelo.X_j = Pyo.Var(domain = Pyo.NonNegativeReals)   # Real Não Negativa
Modelo.X_gc = Pyo.Var(domain = Pyo.NonNegativeIntegers) # Inteira Não Negativa
Modelo.X_m = Pyo.Var(domain = Pyo.NonNegativeReals)   # Real Não Negativa
Modelo.X_s = Pyo.Var(domain = Pyo.NonNegativeReals)   # Real Não Negativa


#-[F.O.]-----------
Modelo.FO = Pyo.Objective(
    expr = (0.05*Modelo.X_b + 0.04*Modelo.X_pb + 0.07*Modelo.X_j +
           0.08*Modelo.X_gc + 0.15*Modelo.X_m + 0.35*Modelo.X_s),
    sense = Pyo.minimize
)

#---- Restrições -----

#--[KCal_MIN]
Modelo.Restricao_KCAL_Min = Pyo.Constraint(
    expr = (70*Modelo.X_b + 100*Modelo.X_pb + 50*Modelo.X_j +
           60*Modelo.X_gc + 150*Modelo.X_m + 100*Modelo.X_s) >= 400)

#--[KCal_MAX]
Modelo.Restricao_KCAL_Max = Pyo.Constraint(
    expr = (70*Modelo.X_b + 100*Modelo.X_pb + 50*Modelo.X_j +
           60*Modelo.X_gc + 150*Modelo.X_m + 100*Modelo.X_s) <= 600)

X_k = 70*Modelo.X_b + 100*Modelo.X_pb + 50*Modelo.X_j + 60*Modelo.X_gc + 150*Modelo.X_m + 100*Modelo.X_s

#--[KCal_fat]
Modelo.Restricao_KCAL_fat = Pyo.Constraint(
    expr = (10*Modelo.X_b + 75*Modelo.X_pb + 0*Modelo.X_j +
           20*Modelo.X_gc + 70*Modelo.X_m + 0*Modelo.X_s) <= 0.3*X_k)

#--[Vit_C]
Modelo.Restricao_Vit_C = Pyo.Constraint(
    expr = (0*Modelo.X_b + 0*Modelo.X_pb + 3*Modelo.X_j +
           0*Modelo.X_gc + 2*Modelo.X_m + 120*Modelo.X_s) >= 60)

#--[Proteina]
Modelo.Restricao_Prote = Pyo.Constraint(
    expr = (3*Modelo.X_b + 4*Modelo.X_pb + 0*Modelo.X_j +
           1*Modelo.X_gc + 8*Modelo.X_m + 1*Modelo.X_s) >= 12)

#--[Pão]
Modelo.Restricao_Pao = Pyo.Constraint(expr = (Modelo.X_b >= 2))

#--[Manteiga de Amendoin o Dobro da Geléia]
Modelo.Restricao_PB = Pyo.Constraint(expr = (Modelo.X_b - 2*Modelo.X_j >= 0))

#--[Líquido]
Modelo.Restricao_Liq = Pyo.Constraint(expr = (Modelo.X_m + Modelo.X_s >= 1))

#-- Otimizando a partir da função de relatório
print('Status = ', resolver(Modelo))
relatorio(Modelo)
KCAL_from_fat = (10*Pyo.value(Modelo.X_b) +
                          75*Pyo.value(Modelo.X_pb) +
                          0*Pyo.value(Modelo.X_j) +
                          20*Pyo.value(Modelo.X_gc) +
                          70*Pyo.value(Modelo.X_m) +
                          0*Pyo.value(Modelo.X_s))

KCAL_total =  (70*Pyo.value(Modelo.X_b) +
               100*Pyo.value(Modelo.X_pb) +
               50*Pyo.value(Modelo.X_j) +
               60*Pyo.value(Modelo.X_gc) +
               150*Pyo.value(Modelo.X_m) +
               100*Pyo.value(Modelo.X_s))

print(f'KCAL from fat = {KCAL_from_fat/KCAL_total}')