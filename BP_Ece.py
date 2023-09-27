import gurobipy as gp
from gurobipy import GRB
import random

# Define the number of vertices in your graph
n = 10  # Adjust the number of vertices as needed

# Initialize an empty adjacency matrix with zeros
W = [[0] * n for _ in range(n)]

# Generate random edge weights (assuming non-negative weights)
for i in range(n):
    for j in range(i+1, n):
        weight = random.uniform(0, 10)  # Adjust the range as needed
        # Ensure that edges are undirected by setting W[i][j] = W[j][i] = weight
        W[i][j] = W[j][i] = weight

# Create a Gurobi model
model = gp.Model("MaxCut")

# Define decision variables for each vertex with values -1 or 1
x = {}
for i in range(n):
    x[i] = model.addVar(vtype=GRB.BINARY, name=f'x_{i}')

# Set the objective to maximize the total cut weight
model.setObjective(0.25 * gp.quicksum(W[i][j] * (1 - x[i] * x[j]) for i in range(n) for j in range(i+1, n)), GRB.MAXIMIZE)

# Optimize the model
model.optimize()

# Retrieve the optimal solution (-1 or 1 for each vertex)
optimal_solution = [2 * x[i].X - 1 for i in range(n)]

# Process 'optimal_solution' to determine the partition or cut

# Close the Gurobi model
model.dispose()
