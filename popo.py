from gurobipy import *
model=Model("SimpleLP")
x1 = model.addVar(vtype="C", name = "x1")
x2 = model.addVar(vtype="C", name = "x2")
model.addConstr(2*x1 + 3*x2 <= 18)
model.addConstr(4*x1 + 3*x2 <= 24)
model.addConstr(x1 >= 0)
model.addConstr(x2 >= 0)
model.setObjective(8*x1 + 7*x2, GRB.MAXIMIZE)
model.update()
model.optimize()
print
print("Optimal value=", model.ObjVal)
print("x1=", x1.X)
print("x2=", x2.X)
