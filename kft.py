import cvxpy as cp
import numpy as np
import  get_values as data

"""[0.3        0.17333333 1.17432    2.28       0.042675   0.09
 0.035175   0.264      0.08810526 0.02295    0.195     ]

 [ 123.2    81.54 3049.2   180.6    31.16   73.2    45.75   88.     60.
  359.7   415.8 ]

 [[1.3 1.3 1.3 0.2 0.3 0.3 0.3 0.3 0.3 0.5 1. ]
 [1.3 1.3 0.2 1.3 0.3 0.3 0.3 0.3 0.3 0.5 1. ]
 [1.3 1.3 1.3 1.3 0.3 0.3 0.3 0.3 0.3 0.5 1. ]
 [1.  1.  1.  1.  0.1 0.1 0.1 0.1 0.1 0.2 0.5]]

 [[0.1 0.1 1.  1.  0.1 0.1 0.1 0.1 0.1 0.1 0.8]
 [0.1 0.1 1.  1.  0.1 0.1 0.1 0.1 0.1 0.1 0.8]
 [0.1 0.1 1.  1.  0.1 0.1 0.1 0.1 0.1 0.1 0.8]
 [0.1 0.1 1.  1.  0.1 0.1 0.1 0.1 0.1 0.1 0.8]]"""
p, c, r, b = data.get_data()
r=r.T
b=b.T
nb_of_products, nb_of_agents = r.shape
X = cp.Variable((nb_of_agents, nb_of_products), nonneg=True)
C = cp.Parameter()
C.value = 400

def Ua(X, a):
    return r[0][a]*cp.power(X[a][0] + X[a][1] + b[0][a], 0.5)\
         + r[2][a]*cp.power(X[a][2] + b[2][a], 0.5)\
         + r[3][a]*cp.power(X[a][3] + b[3][a], 0.5)\
         + r[4][a]*cp.power(X[a][4] + X[a][5] + X[a][6] + b[4][a], 0.5)\
         + r[7][a]*cp.power(2*X[a][7] + X[a][8] + b[7][a], 0.5)\
         + r[9][a]*cp.power(X[a][9] + b[9][a], 0.5)\
         + r[10][a]*cp.power(X[a][10] + b[10][a], 0.5)

def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)

objective = cp.Minimize(cp.sum(X@p))
constraints = [centered_Ua(X, 0)>=1, centered_Ua(X, 1)>=1, centered_Ua(X, 2)>=1, centered_Ua(X, 3)>=1, cp.sum(X@c) - C <=0]
prob = cp.Problem(objective, constraints)
res = prob.solve()
print("Satut du problème: ", prob.status)
print("Achats optimaux: ", X.value)
print("Prix minimisé: ", res)
print("Coefficient taxe carbone (lambda): ", constraints[-1].dual_value)