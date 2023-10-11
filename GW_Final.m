% Define the number of nodes and edges in the graph
n = 20; % Number of nodes
m = 100; % Number of edges 

% Generate a random graph with edge weights
edges = randi([1, n], m, 2); % Random edges between nodes
weights = rand(m, 1); % Random edge weights

% Create the weight matrix W
W = zeros(n, n);
for i = 1:m
    W(edges(i, 1), edges(i, 2)) = weights(i);
    W(edges(i, 2), edges(i, 1)) = weights(i);
end

% Step 1: Solve the SDP relaxation of Max-Cut
X = sdpvar(n, n, 'symmetric');
constraints = [X >= 0, diag(X) == 1];
objective = -trace(W * X); % Maximize the cut

% Attempt to solve the SDP with SeDuMi
options = sdpsettings('solver', 'sedumi', 'verbose', 2); % Use SeDuMi solver
result = optimize(constraints, objective, options);

% Check if the optimization was successful
if result.problem == 0
    X_opt = value(X);

    % Step 2: Decompose X into U
    [U, ~, ~] = svd(X_opt);
    rankX = rank(X_opt);
    U = U(:, 1:rankX);

    % Step 3: Perform Goemans-Williamson rounding
    r = randn(rankX, 1);
    r = r / norm(r); % Normalize r to have norm 1
    x = sign(U' * r);

    % Calculate the cut value based on the rounding
    cut_value = 0.25 * x' * (diag(W) - W) * x;

    % Define the two sets based on the rounding
    set1 = find(x == 1); % Vertices in Set 1
    set2 = find(x == -1); % Vertices in Set 2

    fprintf('Optimal Max-Cut Value: %.4f\n', -value(objective));
    fprintf('Rounded Max-Cut Value: %.4f\n', cut_value);
    fprintf('Set 1: %s\n', mat2str(set1));
    fprintf('Set 2: %s\n', mat2str(set2));
else
    fprintf('Failed to solve the SDP relaxation. Solver error: %s\n', result.info);
end