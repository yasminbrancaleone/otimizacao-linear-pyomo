# --- Problema 20 - Designação de Leitos e Quartos do Hospital ----------
import pyomo.environ as Pyo
from rep import resolver, relatorio

#-- Conjuntos --
# Tipos de quartos: 1 leito, 2 leitos e 3 leitos
Tipos = [1, 2, 3] 

#-- Parâmetros --
Leitos = {1: 1, 2: 2, 3: 3}
Area = {1: 10, 2: 14, 3: 17} # Área em m² por quarto

# Mão de obra (esforço): pacientes em quartos de 2 e 3 leitos exigem 
# apenas 80% da mão de obra que o paciente do quarto individual.
# Esforço por quarto = (Número de leitos) * (Fator de esforço do paciente)
Esforco = {1: 1 * 1.0, 2: 2 * 0.8, 3: 3 * 0.8}

# Arrecadação: O recebimento por paciente é inversamente proporcional à 
# capacidade do quarto. Sendo 'k' uma constante de valor, a receita 
# por paciente é (k / capacidade). A receita total do quarto é:
# capacidade * (k / capacidade) = k.
# Logo, a receita por quarto é constante para todos (usaremos o valor 1 para k).
Arrecadacao = {1: 1, 2: 1, 3: 1}

#--- Modelagem ---
Modelo = Pyo.ConcreteModel()

#[V.D]
# X[t] = Quantidade de quartos do tipo 't' a serem construídos
# Utilizando Reais Não Negativos para programação linear padrão (LP relaxada). 
# *Nota: Na vida real quartos são números inteiros, mas mantemos o padrão dos exercícios.
Modelo.X = Pyo.Var(Tipos, domain=Pyo.NonNegativeReals) #--> X_t >= 0

#-- Restrições --

# 1. Restrição Máxima de Quartos: O total a construir não pode ultrapassar 70
Modelo.Restricao_Total_Quartos = Pyo.Constraint(
    expr = sum(Modelo.X[t] for t in Tipos) <= 70
)

# 2. Restrição Mínima de Leitos: Deverão ser oferecidos pelo menos 120 leitos
Modelo.Restricao_Min_Leitos = Pyo.Constraint(
    expr = sum(Leitos[t] * Modelo.X[t] for t in Tipos) >= 120
)

# 3. Restrições de Proporção: A percentagem de quartos de 1 leito deve ser restrita 
# entre 15% e 30% do total de quartos construídos
Modelo.Restricao_Perc_Min = Pyo.Constraint(
    expr = Modelo.X[1] >= 0.15 * sum(Modelo.X[t] for t in Tipos)
)

Modelo.Restricao_Perc_Max = Pyo.Constraint(
    expr = Modelo.X[1] <= 0.30 * sum(Modelo.X[t] for t in Tipos)
)


#[F.O.] - Definindo as 4 Funções Objetivo do problema
# (a) Minimizar o esforço da mão de obra
Modelo.FO_a = Pyo.Objective(expr = sum(Esforco[t] * Modelo.X[t] for t in Tipos), sense=Pyo.minimize)

# (b) Maximizar a arrecadação global
Modelo.FO_b = Pyo.Objective(expr = sum(Arrecadacao[t] * Modelo.X[t] for t in Tipos), sense=Pyo.maximize)

# (c) Maximizar o número de leitos
Modelo.FO_c = Pyo.Objective(expr = sum(Leitos[t] * Modelo.X[t] for t in Tipos), sense=Pyo.maximize)

# (d) Minimizar o espaço necessário
Modelo.FO_d = Pyo.Objective(expr = sum(Area[t] * Modelo.X[t] for t in Tipos), sense=Pyo.minimize)

# Desativando todas as F.O. inicialmente para controlar a execução via loop
Modelo.FO_a.deactivate()
Modelo.FO_b.deactivate()
Modelo.FO_c.deactivate()
Modelo.FO_d.deactivate()


#-- Otimizando a partir da função de relatório para cada cenário
objetivos_cenarios = {
    'A - Minimizar Esforço da Mão de Obra': Modelo.FO_a,
    'B - Maximizar Arrecadação Global': Modelo.FO_b,
    'C - Maximizar o Número de Leitos': Modelo.FO_c,
    'D - Minimizar o Espaço Necessário': Modelo.FO_d
}

for nome, fo_ativa in objetivos_cenarios.items():
    print(f"\n{'='*60}\nCenário: {nome}\n{'='*60}")
    
    # Ativa apenas a Função Objetivo do cenário atual
    fo_ativa.activate() 
    
    status = resolver(Modelo)
    print('Status = ', status)
    
    if str(status) == 'optimal' or str(status) == 'ok':
        relatorio(Modelo)
    else:
        print("\nO solver não encontrou solução viável para este cenário.")
        
    # Desativa a F.O. atual para a próxima iteração do loop
    fo_ativa.deactivate()