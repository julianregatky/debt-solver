# Debt Solver

A tool to solve debt allocation problems. Given a dictionary of expenses, the solver will determine how much each person owes or is owed in order to even out the expenses while minimizing the number of transactions.

## Mathematical Formulation

The debt allocation problem can be formulated as an integer linear programming problem as follows:

Let $n$ be the number of people, $L_j$ be the amount that person $j$ is owed and $D_i$ be the amount that person $i$ owes. The problem can be written as:

$$
\begin{aligned}
    \text{minimize} \quad & \sum_{i=1}^{n} \sum_{j=1}^{n} x_{i,j} \\
    \text{subject to} \quad & \sum_{i=1}^{n} z_{i,j} = L_j \quad & \forall j \in \{1, \dots, n\} \\
                            & \sum_{j=1}^{n} z_{i,j} = D_i \quad & \forall i \in \{1, \dots, n\} \\
                            & Mx_{i,j} - z_{i,j} \ge 0 \quad & \forall i, j \in \{1, \dots, n\} \\
                            & x_{i,j}, z_{i,j} \in \mathbb{Z} \quad & \forall i, j \in \{1, \dots, n\} \\
\end{aligned}
$$

where $x_{i,j}$ and $z_{i,j}$ are binary and integer variables, respectively. The first constraint ensures that each person gets back the amount that they are owed, and the second constraint ensures that each person pays back their debts. The third constraint is a big-M constraint that ensures that a debt is only assigned if it is non-zero.

## Usage

To use the DebtSolver, first install OR-Tools:

```bash
pip install ortools
```

Then, create an instance of the `DebtSolver` class with a dictionary of expenses and call the `solve` method.

```python
from debt_solver import DebtSolver

expenses = {"Person A": 100, "Person B": 50, "Person C": 0, "Person D": 18}
result = DebtSolver(expenses).solve()
```
