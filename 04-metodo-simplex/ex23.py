# --- Exercício 23 em Forma Canônica via Pyomo ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

def resolver_item(modelo, nome_item, base_inicial, artificiais):
    print(f"\n{'='*60}\nResolução do Item ({nome_item}) - Forma Canônica\n{'='*60}")
    print(f"Base Inicial: {base_inicial}")
    print(f"Variáveis Artificiais: {artificiais}\n")
    
    status = resolver(modelo)
    print('Status = ', status)
    if str(status) == 'optimal' or str(status) == 'ok':
        relatorio(modelo)
    else:
        print("\nModelo sem solução viável ou ilimitado.")

# ---------------------------------------------------------------
# Item (a)
# ---------------------------------------------------------------
Modelo_a = Pyo.ConcreteModel()

#[V.D] Variáveis originais + Folga + Artificial
Modelo_a.x1 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_a.x2 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_a.s1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Folga
Modelo_a.a1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Artificial

#[F.O.]
Modelo_a.FO = Pyo.Objective(expr = Modelo_a.x1 + Modelo_a.x2, sense = Pyo.maximize)

#-- Restrições na Forma Canônica --
Modelo_a.R1 = Pyo.Constraint(expr = Modelo_a.x1 - 5 * Modelo_a.x2 + Modelo_a.a1 == 10)
Modelo_a.R2 = Pyo.Constraint(expr = Modelo_a.x1 + 2 * Modelo_a.x2 + Modelo_a.s1 == 50)

# Garantir que a variável artificial saia da solução final se houver viabilidade
Modelo_a.a1.fix(0)

resolver_item(Modelo_a, 'a', base_inicial=['a1', 's1'], artificiais=['a1'])


# ---------------------------------------------------------------
# Item (b)
# ---------------------------------------------------------------
Modelo_b = Pyo.ConcreteModel()

#[V.D] Variáveis originais + Excesso/Folga + Artificiais
Modelo_b.x1 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_b.x2 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_b.e1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Excesso
Modelo_b.s1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Folga
Modelo_b.e2 = Pyo.Var(domain=Pyo.NonNegativeReals) # Excesso
Modelo_b.a1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Artificial 1
Modelo_b.a2 = Pyo.Var(domain=Pyo.NonNegativeReals) # Artificial 2

#[F.O.]
Modelo_b.FO = Pyo.Objective(expr = 24 * Modelo_b.x1 + 12 * Modelo_b.x2, sense = Pyo.minimize)

#-- Restrições na Forma Canônica --
Modelo_b.R1 = Pyo.Constraint(expr = 3 * Modelo_b.x1 + 2 * Modelo_b.x2 - Modelo_b.e1 + Modelo_b.a1 == 4)
Modelo_b.R2 = Pyo.Constraint(expr = 2 * Modelo_b.x1 - 4 * Modelo_b.x2 + Modelo_b.s1 == 26)
Modelo_b.R3 = Pyo.Constraint(expr = Modelo_b.x2 - Modelo_b.e2 + Modelo_b.a2 == 3)

Modelo_b.a1.fix(0)
Modelo_b.a2.fix(0)

resolver_item(Modelo_b, 'b', base_inicial=['a1', 's1', 'a2'], artificiais=['a1', 'a2'])


# ---------------------------------------------------------------
# Item (c)
# ---------------------------------------------------------------
Modelo_c = Pyo.ConcreteModel()

#[V.D] Variáveis originais + Folga/Excesso + Artificial
Modelo_c.x1 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_c.x2 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_c.s1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Folga
Modelo_c.e1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Excesso
Modelo_c.a1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Artificial

#[F.O.]
Modelo_c.FO = Pyo.Objective(expr = 10 * Modelo_c.x1 - Modelo_c.x2, sense = Pyo.maximize)

#-- Restrições na Forma Canônica --
Modelo_c.R1 = Pyo.Constraint(expr = 6 * Modelo_c.x1 + Modelo_c.x2 + Modelo_c.s1 == 10)
Modelo_c.R2 = Pyo.Constraint(expr = Modelo_c.x2 - Modelo_c.e1 + Modelo_c.a1 == 6)

Modelo_c.a1.fix(0)

resolver_item(Modelo_c, 'c', base_inicial=['s1', 'a1'], artificiais=['a1'])


# ---------------------------------------------------------------
# Item (d)
# ---------------------------------------------------------------
Modelo_d = Pyo.ConcreteModel()

#[V.D] Variáveis originais + Folga/Excesso + Artificial
Modelo_d.x1 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_d.x2 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_d.x3 = Pyo.Var(domain=Pyo.NonNegativeReals)
Modelo_d.s1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Folga
Modelo_d.e1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Excesso
Modelo_d.a1 = Pyo.Var(domain=Pyo.NonNegativeReals) # Artificial

#[F.O.]
Modelo_d.FO = Pyo.Objective(expr = 3 * Modelo_d.x1 + 3 * Modelo_d.x2 - 2 * Modelo_d.x3, sense = Pyo.maximize)

#-- Restrições na Forma Canônica --
Modelo_d.R1 = Pyo.Constraint(expr = 6 * Modelo_d.x1 + 3 * Modelo_d.x2 - Modelo_d.x3 + Modelo_d.s1 == 10)
Modelo_d.R2 = Pyo.Constraint(expr = 0.25 * Modelo_d.x2 + Modelo_d.x3 - Modelo_d.e1 + Modelo_d.a1 == 20)

Modelo_d.a1.fix(0)

resolver_item(Modelo_d, 'd', base_inicial=['s1', 'a1'], artificiais=['a1'])