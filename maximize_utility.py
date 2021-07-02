import cvxpy as cp
import numpy as np
import get_values as data

p, c, r, b = data.get_data()
r=r.T
b=b.T
nb_of_products, nb_of_agents = r.shape

X = cp.Variable((nb_of_agents, nb_of_products), nonneg=True)
C = cp.Parameter()
C.value = 5500
P0 = cp.Parameter()
P0.value = 2
P1 = cp.Parameter()
P1.value = 3
P2 = cp.Parameter()
P2.value = 2
P3 = cp.Parameter()
P3.value = 4

# --------------- Définition des fonctions d'utilité --------------- #
def Ua(X, a):
    S=0
    for i in range(nb_of_products):
        S+=r[i][a]*cp.power(X[a][i] + b[i][a], 0.5)
    return S

def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)


objective = cp.Maximize(0.2*centered_Ua(X, 0) + 0.1*centered_Ua(X, 1) + 0.4*centered_Ua(X, 2) + 0.3*centered_Ua(X, 3))
constraints = [X[0]@p - P0 <=0, X[1]@p - P1 <=0, X[2]@p - P2 <=0, X[3]@p - P3 <=0,\
                 cp.sum(X@c) - C <=0,\
                X[:,0] + X[:,1] >= 1, X[0:,2] + X[0:,3] >= 0.5, X[0:,4]>=0.5, X[0:,5] + X[0:,6] >= 0.5, X[0:,7] >= 0.7, X[0:,8] >=1]
prob = cp.Problem(objective, constraints)
res=prob.solve()


print("Satut du problème: ", prob.status)
print("Achats optimaux: \n", np.round(X.value, 3))
print("Utilité moyenne (pondérée) maximisée: ", res)
print("Utilité agent 1:", centered_Ua(X, 0).value)
print("Utilité agent 2:", centered_Ua(X, 1).value)
print("Utilité agent 3:", centered_Ua(X, 2).value)
print("Utilité agent 4:", centered_Ua(X, 3).value)
print("Coût en gCO2:", cp.sum(X@c).value)
print("Budget:", cp.sum(X@p).value)
print("Coefficient contrainte carbone (utilité/gCO2): ", constraints[1].dual_value)
print("Coefficient contrainte budget agent 1", constraints[0].dual_value)
print("Coefficient contrainte budget agent 2", constraints[1].dual_value)
print("Coefficient contrainte budget agent 3", constraints[2].dual_value)
print("Coefficient contrainte budget agent 4", constraints[3].dual_value)
