import cvxpy as cp
import numpy as np
import get_values as data

#Paramètres de la montée de gradient
MAX_ITERS = 50
rho = 1.0


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


#On resoud le probleme une premiere fois sans taxe carbone
objective = cp.Minimize(cp.sum(X@p))
constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin,\
               X[:,0] + X[:,1] >= 1, X[0:,2] + X[0:,3] >= 0.5, X[0:,4]>=0.5, X[0:,5] + X[0:,6] >= 0.5, X[0:,7] >= 0.7, X[0:,8] >=1]
prob = cp.Problem(objective, constraints)
prob.solve()
previous = cp.sum(X@p).value

#on utilise le gradient de la fonction duale pour déterminer une meilleur valeur de taxe
lprevious = 0
print(cp.sum(X@c).value, C.value)
l = max(0, rho*(cp.sum(X@c) - C).value)
#for some reason, cvxpy despises high values of l
while(l>1000):
    l=l/2

for t in range(MAX_ITERS):
    print("\nITERATION numéro", t)
    #on calcule la fonction duale pour la valeur de la taxe actuelle
    objective = cp.Minimize(cp.sum(X@p) + l*(cp.sum(X@c) - C))
    constraints = [centered_Ua(X, 0)>=uamin, centered_Ua(X, 1)>=uamin, centered_Ua(X, 2)>=uamin, centered_Ua(X, 3)>=uamin,\
               X[:,0] + X[:,1] >= 1, X[0:,2] + X[0:,3] >= 0.5, X[0:,4]>=0.5, X[0:,5] + X[0:,6] >= 0.5, X[0:,7] >= 0.7, X[0:,8] >=1]
    prob = cp.Problem(objective, constraints)
    prob.solve()
    next = (cp.sum(X@p) + l*(cp.sum(X@c) - C)).value

    l = max(0, l + rho*(cp.sum(X@c) - C).value)
    while(l>1000):
        l=l/2
        
    #condition pour la recherche linéaire
    if(previous - next > 10**(-2)*cp.abs(cp.sum(X@c).value - C).value):
        print("BAD IDEAAA! previous - next :", previous - next)
        rho = rho/2
        l=lprevious
    #si le saut a apporté une amélioration, on actualise la valeur de previous
    previous = next 
    
    print("rho", rho)
    print("Coefficient taxe carbone (lambda): ", l)
    

print("Achats optimaux: \n", np.round(X.value, 3))
print("Prix minimisé: ", cp.sum(X@p).value)
print("Coût en gCO2:", cp.sum(X@c).value)
print("Coefficient taxe carbone (lambda): ", l)
