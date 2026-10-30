# ---------------------------------------------------------------
# rep.py -- resolucao e relatorio organizado (sem log do solver)
# ---------------------------------------------------------------
import pyomo.environ as Pyo

def resolver(m, tee=False):
    res = Pyo.SolverFactory("glpk", executable=r"C:\glpk\winglpk-4.65\glpk-4.65\w64\glpsol.exe").solve(m, tee=tee)
    return res.solver.termination_condition

def relatorio(m, casas=4, mostrar_zeros=False):
    """Imprime F.O., variaveis de decisao e LHS/RHS de cada restricao."""
    obj = next(m.component_data_objects(Pyo.Objective, active=True))
    print("F.O. = %.*f" % (casas, Pyo.value(obj)))
    print("\nVariaveis de decisao:")
    for v in m.component_data_objects(Pyo.Var):
        if v.value is None:
            continue
        if mostrar_zeros or abs(v.value) > 1e-9:
            print("  %-22s = %.*f" % (v.name, casas, v.value))
    print("\nRestricoes (LHS  sentido  RHS):")
    for c in m.component_data_objects(Pyo.Constraint, active=True):
        lhs = Pyo.value(c.body)
        if c.equality:
            print("  %-22s %14.*f  =   %.*f" % (c.name, casas, lhs, casas, Pyo.value(c.upper)))
        else:
            if c.upper is not None:
                print("  %-22s %14.*f  <=  %.*f" % (c.name, casas, lhs, casas, Pyo.value(c.upper)))
            if c.lower is not None:
                print("  %-22s %14.*f  >=  %.*f" % (c.name, casas, lhs, casas, Pyo.value(c.lower)))