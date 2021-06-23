import matplotlib.pyplot as plt
import numpy as np

def echelon(x,x0,val):
    if(x<x0):
        return 0
    else:
        return val

def utility_pain(x):
    return echelon(x,80,0.5)+echelon(x,160,0.2)+echelon(x,240,0.1)

x = np.linspace(0,300,num=1000)
y = np.zeros(1000)

for i in range(len(y)):
    y[i] = utility_pain(x[i])

plt.plot(x,y)
plt.show()

