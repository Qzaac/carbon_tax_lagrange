import cvxpy as cp
import numpy as np
#import cvxopt as co

nb_of_products = 7
nb_of_agents = 3

#Parameters needed to compute utility functions
rv = [1.62, 1.62, 1.62]
bv = [0.1, 0.1, 0.1]
rt = [1.2, 0.6, 0.4]
bt = [1, 1, 1]
rb = [0.5, 1.2, 0.6]
bb = [1, 1, 1]
rf = [0.2, 0.4, 0.1]
bf = [1, 1, 1]
rc = [0.2, 0.2, 0.1]
bc = [1, 1, 1]

p = cp.Parameter(nb_of_products, nonpos=False)
p.value = [77, 50, 35, 15, 3, 0, 2]
c = cp.Parameter(nb_of_products, nonpos=False)
c.value = [37, 92, 32, 8, 2, 0, 1]
C = cp.Parameter()
C.value = 1000


def Ua(X, a):
    return rv[a]*cp.power(X[a][0] + X[a][1] + bv[a], 0.5) + rt[a]*cp.power(X[a][2] + bt[a], 0.5) + rb[a]*cp.power(2*X[a][3] + X[a][4] \
           + bb[a], 0.5) + rf[a]*cp.power(X[a][5] + bf[a], 0.5) + rc[a]*cp.power(X[a][6] + bc[a], 0.5)


def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)


def dual(l):
    X = cp.Variable((nb_of_agents, nb_of_products), nonneg=True)
    objective = cp.Minimize(cp.sum(X@p) + l*(cp.sum(X@c) - C))
    utmin = 1
    constraints = [centered_Ua(X, 0)>=utmin, centered_Ua(X, 1)>=utmin, centered_Ua(X, 2)>=utmin ]
    prob1 = cp.Problem(objective, constraints)
    result = prob1.solve()
    
    print(prob1.status)
    print(X.value)
    print(result)
    
    return cp.sum(X@p) + l*(cp.sum(X@c) - C)

dual(-0.01)

"""
l=cp.Variable()
prob2 = cp.Problem(objective=cp.Maximize(dual(l)), constraints=[])
res = prob2.solve()
print(l.value())
print(res)
print(prob2.status)
"""