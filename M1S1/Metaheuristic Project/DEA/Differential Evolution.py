# -*- coding: utf-8 -*-
"""
    To reach our implementations for all functions, follow the link:
    https://colab.research.google.com/drive/1kOkZt3da9oibP0H9RP2yFGzlt-mRY0IJ?usp=sharing
"""

import numpy as np
import matplotlib.pyplot as plt
import time

# Define the Schwefel function
def Schwefel(x):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x)) + 10 * len(x)

# Problem Definition
CostFunction = Schwefel

nVar = 20
VarSize = (nVar,)

VarMin = -5
VarMax = 5

# DE Parameters
MaxIt = 20000
nPop = 30
beta_min = 0.2
beta_max = 0.8
pCR = 0.2

# Initialization
pop = np.empty(nPop, dtype=object)
BestSol = {'Position': None, 'Cost': np.inf}
BestCost = np.zeros(MaxIt)

for i in range(nPop):
    pop[i] = {'Position': np.random.uniform(VarMin, VarMax, VarSize)}
    pop[i]['Cost'] = CostFunction(pop[i]['Position'])

    if pop[i]['Cost'] < BestSol['Cost']:
        BestSol = pop[i].copy()

# DE Main Loop
start_time = time.time()
all_costs = []

for it in range(MaxIt):
    for i in range(nPop):
        x = pop[i]['Position']
        A = np.random.permutation(nPop)
        A = A[A != i][:3]
        a, b, c = A

        beta = np.random.uniform(beta_min, beta_max, VarSize)
        y = pop[a]['Position'] + beta * (pop[b]['Position'] - pop[c]['Position'])
        y = np.maximum(y, VarMin)
        y = np.minimum(y, VarMax)

        j0 = np.random.randint(0, nVar)
        z = np.where(np.random.rand(*VarSize) <= pCR, y, x)
        z[j0] = y[j0]

        NewSol = {'Position': z}
        NewSol['Cost'] = CostFunction(NewSol['Position'])

        if NewSol['Cost'] < pop[i]['Cost']:
            pop[i] = NewSol.copy()
            if pop[i]['Cost'] < BestSol['Cost']:
                BestSol = pop[i].copy()

    BestCost[it] = BestSol['Cost']
    all_costs.append(BestCost[it])

# Calculate Statistics
best_min = np.min(all_costs)
worst_min = np.max(all_costs)
avg_min = np.mean(all_costs)
std_min = np.std(all_costs)

end_time = time.time()
comp_time = end_time - start_time

print(f'Best Minimum: {best_min}')
print(f'Worst Minimum: {worst_min}')
print(f'Average Minimum: {avg_min}')
print(f'Standard Deviation of Minimums: {std_min}')
print(f'Computational Time: {comp_time} seconds')

# Show Results
plt.figure()
plt.semilogy(BestCost, linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.grid()
plt.show()

