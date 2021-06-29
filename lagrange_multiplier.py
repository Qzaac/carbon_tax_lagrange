import cvxpy as cp
import numpy as np
import get_values as data

#Parameter of the gradient rise
MAX_ITERS = 500
rho = 1.0

"""
#Pour KFT:
p, c, r, b = data.get_data()
r=r.T
b=b.T
nb_of_products, nb_of_agents = r.shape
##################################
"""

#Pour tester:
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

p = [77, 50, 35, 15, 3, 0, 2]
c = [37, 92, 32, 8, 2, 0, 1]
############################################

X = cp.Variable((nb_of_agents, nb_of_products), nonneg=True)
C = cp.Parameter()
C.value = 70
uamin=1

"""
#Pour KFT:
def Ua(X, a):
    return r[0][a]*cp.power(X[a][0] + X[a][1] + b[0][a], 0.5)\
         + r[2][a]*cp.power(X[a][2] + b[2][a], 0.5)\
         + r[3][a]*cp.power(X[a][3] + b[3][a], 0.5)\
         + r[4][a]*cp.power(X[a][4] + X[a][5] + X[a][6] + b[4][a], 0.5)\
         + r[7][a]*cp.power(2*X[a][7] + X[a][8] + b[7][a], 0.5)\
         + r[9][a]*cp.power(X[a][9] + b[9][a], 0.5)\
         + r[10][a]*cp.power(X[a][10] + b[10][a], 0.5)
"""

#Pour tester:
def Ua(X, a):
    return rv[a]*cp.power(X[a][0] + X[a][1] + bv[a], 0.5) + rt[a]*cp.power(X[a][2] + bt[a], 0.5) + rb[a]*cp.power(2*X[a][3] + X[a][4] \
           + bb[a], 0.5) + rf[a]*cp.power(X[a][5] + bf[a], 0.5) + rc[a]*cp.power(X[a][6] + bc[a], 0.5)
#####################################

def centered_Ua(X, a):
    return Ua(X, a) - Ua(np.zeros(X.shape), a)

l = cp.Parameter()
#initially, there is no tax at all:
l.value = 0

def mymax(n, m):
    if (m>=n):
        return m
    return n

for t in range(MAX_ITERS):
    print(t, "ieme ITERATION\n")
    #First, we solve the dual problem for a given value of l:
    objective = cp.Minimize(cp.sum(X@p) + l*(cp.sum(X@c) - C))
    #KFT: constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin]
    constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, cp.sum(X[:,:-1], axis=1)==1]
    prob = cp.Problem(objective, constraints)
    prob.solve()

    #Then, we update the value of l using x*(l) (previous l) given by prob.solve() (the government does this):
    #le gouvernement obeserve l'effet de l'imposition passée et acutalise la valeur de l'impôt
    rho = 1/np.sqrt((t+1))
    l.value = mymax(0, l.value + rho*(cp.sum(X@c).value - C).value)  
    print("Coefficient taxe carbone (lambda): ", l.value)
    

print("Achats optimaux: \n", np.round(X.value))
print("Prix minimisé: ", cp.sum(X@p).value)
print("Coût en gCO2:", cp.sum(X@c).value)
print("Coefficient taxe carbone (lambda): ", l.value)

