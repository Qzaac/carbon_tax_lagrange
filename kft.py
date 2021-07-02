import cvxpy as cp
import numpy as np
import get_values as data
import pandas as pd
import matplotlib.pyplot as plt

p, c, r, b = data.get_data()
r=r.T
b=b.T
nb_of_products, nb_of_agents = r.shape

X = cp.Variable((nb_of_agents, nb_of_products), nonneg=True)
C = cp.Parameter()
C.value = 5500
uamin=1


# --------------- Définition des fonctions d'utilité --------------- #
def Ua(X, a):
    S=0
    for i in range(nb_of_products):
        S+=r[i][a]*cp.power(X[a][i] + b[i][a], 0.5)
    return S

def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)

# --------------- Définition du problème --------------- #

objective = cp.Minimize(cp.sum(X@p))
constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin,\
               cp.sum(X@c) - C <=0,\
               X[:,0] + X[:,1] >= 1, X[0:,2] + X[0:,3] >= 0.5, X[0:,4]>=0.5, X[0:,5] + X[0:,6] >= 0.5, X[0:,7] >= 0.7, X[0:,8] >=1]
prob = cp.Problem(objective, constraints)
res = prob.solve()


print("Satut du problème: ", prob.status)
print("Achats optimaux: \n", np.round(X.value, 3))
print("Prix minimisé: ", res)
print("Coût en gCO2:", cp.sum(X@c).value)
print("Coefficient taxe carbone (lambda): ", constraints[4].dual_value)


# --------------- Affichage des achats --------------- #

L=[X.value[0][i] for i in range(9)]
M=[X.value[1][i] for i in range(9)]
N=[X.value[2][i] for i in range(9)]
O=[X.value[3][i] for i in range(9)]
dataframe = pd.DataFrame({'Agent 1':L,
                          'Agent 2':M,
                          'Agent 3':N,
                          'Agent 4':O,}, 
                          index =['Pain', 'Galette', 'Viande', 'Vegan', 'STO', 'Blanche','Indus.','Canettes', 'Frites'])
axis = dataframe.plot.bar(rot=0)
print(axis)
plt.xticks(fontsize=9)
plt.savefig('plot')
