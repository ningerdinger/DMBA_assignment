import gurobipy as gp
from gurobipy import GRB
import random

# To Define the number of vertices in our graph
n = 10  

# Initializing an empty adjacency matrix with zeros
W = [[0] * n for _ in range(n)]

# Generate random edge weights (assuming non-negative weights)
for i in range(n):
    for j in range(n):
        weight = random.uniform(0, 10)  # Adjust the range as needed
        # Ensure that edges are undirected by setting W[i][j] = W[j][i] = weight
        W[i][j] = W[j][i] = weight

model = gp.Model("MaxCut")

# Defining binary decision variables for each vertex
x = {}
for i in range(n):
    x[i] = model.addVar(vtype=GRB.BINARY, name=f'x_{i}')

# Set the objective to maximize the total cut weight
model.setObjective(0.25*gp.quicksum(W[i][j] * (1 - x[i] * x[j]) for i in range(n) for j in range(n)), GRB.MAXIMIZE)

#to ensure that the decision variables are binary
for i in range(n):
    x[i].setAttr(GRB.Attr.VType, GRB.BINARY)

model.optimize()
optimal_solution = [x[i].X for i in range(n)]
model.dispose()
