import networkx as nx
import random
import cvxpy as cp
import numpy as np
import sys

# Create a random graph with weights for the edges
n = 10  # Change this to the desired number of nodes
G = nx.Graph()

for i in range(n):
    for j in range(i + 1, n):
        weight = random.uniform(0, 1)  # Random edge weight between 0 and 1
        G.add_edge(i, j, weight=weight)

# Create an n x n matrix variable
X = cp.Variable((n, n), symmetric=True)

# Define the SDP relaxation constraints
constraints = [X >> 0]  # X must be positive semidefinite

# Extract edge weights from the graph G
edge_weights = [G[i][j]["weight"] for i in range(n) for j in range(i + 1, n)]

# Define the objective function (Maximize sum of edge weights)
objective = cp.Maximize(cp.sum([edge_weights[i] * X[i, j] for i in range(n) for j in range(i + 1, n)]))

# Create the problem
prob = cp.Problem(objective, constraints)

# Define solver options for SCS
solver_opts = {
    # Specify the maximum number of iterations
    "max_iters": 1000,
    # Specify a custom tolerance level (e.g., 1e-6)
    "eps": 1e-6,
}

try:
    # Solve the problem with solver options
    prob.solve(solver=cp.SCS, **solver_opts)
except cp.SolverError as e:
    print("SolverError:", e)
    sys.exit(1)

# Check if the problem was successfully solved
if prob.status != cp.OPTIMAL:
    print("Optimization problem did not converge to optimal solution.")
    sys.exit(1)

# Get the optimal solution
X_optimal = X.value

# Calculate the maximized objective value
maximized_value = sum([edge_weights[i] * X_optimal[i, j] for i in range(n) for j in range(i + 1, n)])
print("Maximized Objective Value:", maximized_value)

# Perform randomized rounding
np.random.seed(42)  # Set a seed for reproducibility
random_vector = np.random.randn(n)
partition = [1 if np.dot(random_vector, X_optimal[i]) >= 0 else -1 for i in range(n)]

# Print the partition
print("Partition:", partition)
