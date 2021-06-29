import cvxpy as cp
import numpy as np
np.random.seed(1)

# Initialize data.
MAX_ITERS = 10
rho = 1.0
n = 20
m = 10
A = np.random.randn(m,n)
b = np.random.randn(m)

# Initialize problem.
x = cp.Variable(shape=n)
f = cp.norm(x, 1)

# Solve with CVXPY.
cp.Problem(cp.Minimize(f), [A*x == b]).solve()
print("Optimal value from CVXPY: {}".format(f.value))

# Solve with method of multipliers.
resid = A*x - b
y = cp.Parameter(shape=(m)); y.value = np.zeros(m)
aug_lagr = f + y.T*resid + (rho/2)*cp.sum_squares(resid)
for t in range(MAX_ITERS):
    cp.Problem(cp.Minimize(aug_lagr)).solve()
    y.value += rho*resid.value

print("Optimal value from method of multipliers: {}".format(f.value))