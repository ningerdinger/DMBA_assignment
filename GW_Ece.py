import numpy as np
import networkx as nx
import cvxopt
import cvxopt.solvers

# Create a random graph (you can replace this with your own graph)
G = nx.erdos_renyi_graph(n=10, p=0.4)

# Number of nodes in the graph
n = len(G.nodes())

# Create a matrix for the SDP relaxation
X = cvxopt.solvers.sdp(n * (n + 1) // 2)

# Objective: Maximize sum of X[i, j] for all edges (i, j)
c = cvxopt.matrix(-1.0, (n, n))
for i in range(n):
    c[i * (n + 1)] = 0.0  # Diagonal elements are not included

# Constraints
A = []  # List to hold constraint matrices
for i, j in G.edges():
    row = np.zeros((n, n))
    row[i, j] = -1
    row[j, i] = -1
    A.append(cvxopt.matrix(row))
b = cvxopt.matrix(-1.0, (len(A), 1))

# Add constraints to the SDP relaxation
for Ai in A:
    X.A = X.A + [Ai]

# Solve the SDP relaxation
cvxopt.solvers.options['show_progress'] = False
cvxopt.solvers.options['maxiters'] = 1000
solution = cvxopt.solvers.sdp(c, Gq=A, h=b)

# Extract the solution matrix from the SDP solution
X_optimal = np.array(solution['x']).reshape(n, n)

# Random rounding step
import random

random.seed(42)  # Set a seed for reproducibility
cut = []
for i in range(n):
    if random.random() < (1 + X_optimal[i, i]) / 2:
        cut.append(i)

# Calculate the cut size
cut_size = sum(1 for edge in G.edges() if edge[0] in cut and edge[1] not in cut)

print("Cut Size:", cut_size)
print("Cut Nodes:", cut)

