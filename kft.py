import cvxpy as cp
import numpy as np
import get_values as data

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
uamin=1
C.value = 18000

b = \
[\
[0.1,   0.1,    0.02,    1.0],
[0.1,   0.1,    0.00009,    1.0],
[1.0,   1.0,    0.1,    0.1],
[1.0,   1.0,    0.1,    0.1],
[0.1,   0.1,    0.1,    5.0],
[0.1,   0.1,    1,    0.1],
[0.1,   0.1,    1,    0.1],
[0.1,   0.1,    0.5,    4.0],
[0.8,   0.8,    0.1,    0.8]]
r = \
[
[1.3,   1.3,    0.1,    1.0],
[1.3,   1.3,    0.1,    1.0],
[1.3,   0.2,    0.4,    3.0],
[0.2,   1.3,    0.4,    1.0],
[0.3,   0.3,    0.1,    0.2],
[0.3,   0.3,    0.1,    1.0],
[0.3,   0.3,    0.15,    1.0],
[0.5,   0.5,    0.1,    0.2],
[1.0,   1.0,    0.1,    0.5]]


def Ua(X, a):
    puissance = 0.5
    multiplicateur = 1
    return multiplicateur*\
        (  r[0][a]*cp.power(X[a][0] + b[0][a], puissance)\
         + r[1][a]*cp.power(X[a][1] + b[1][a], puissance)\
         + r[2][a]*cp.power(X[a][2] + b[2][a], puissance)\
         + r[3][a]*cp.power(X[a][3] + b[3][a], puissance)\
         + r[4][a]*cp.power(X[a][4] + b[4][a], puissance)\
         + r[5][a]*cp.power(X[a][5] + b[5][a], puissance)\
         + r[6][a]*cp.power(X[a][6] + b[6][a], puissance)\
         + r[7][a]*cp.power(X[a][7] + b[7][a], puissance)\
         + r[8][a]*cp.power(X[a][8] + b[8][a], puissance))

def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)

objective = cp.Minimize(cp.sum(X@p))
#constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin, cp.sum(X@c) - C <=0]
constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin]
prob = cp.Problem(objective, constraints)
res = prob.solve()

#print("Satut du problème: ", prob.status)
print("Achats optimaux: \n", np.round(X.value, 3))
#print("Prix minimisé: ", res)
#print("Coût en gCO2:", cp.sum(X@c).value)
#print("Coefficient taxe carbone (lambda): ", constraints[-1].dual_value)
