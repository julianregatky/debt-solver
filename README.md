# DebtSolver

A tool to solve debt allocation problems. Given a dictionary of expenses, the solver will determine how much each person owes or is owed in order to even out the expenses.

## Mathematical Formulation

The debt allocation problem can be formulated as an integer linear programming problem as follows:

Let $n$ be the number of people, $E_i$ be the amount spent by person $i$, and $D_i$ be the amount that person $i$ owes. The problem can be written as:

$$
\begin{aligned}
    \text{minimize} \quad & \sum_{i=1}^{n} \sum_{j=1}^{n} x_{i,j} \\
    \text{subject to} \quad & \sum_{i=1}^{n} z_{i,j} = L_j \quad & \forall j \in \{1, \dots, n\} \\
                            & \sum_{j=1}^{n} z_{i,j} = D_i \quad & \forall i \in \{1, \dots, n\} \\
                            & Mx_{i,j} - z_{i,j} \ge 0 \quad & \forall i, j \in \{1, \dots, n\} \\
                            & x_{i,j}, z_{i,j} \in \mathbb{Z} \quad & \forall i, j \in \{1, \dots, n\} \\
\end{aligned}
$$

where $L_j$ is the amount that person $j$ is owed, and $x_{i,j}$ and $z_{i,j}$ are binary and integer variables, respectively. The first constraint ensures that each person gets back the amount that they are owed, and the second constraint ensures that each person pays back their debts. The third constraint is a big-M constraint that ensures that a debt is only assigned if it is non-zero.

The third constraint is known as a big-M constraint, where $M$ is a large positive constant. This constraint is used to ensure that a debt is only assigned if it is non-zero. Specifically, if $x_{i,j} = 1$, then the debt $z_{i,j}$ must be non-zero, and if $x_{i,j} = 0$, then the debt $z_{i,j}$ must be zero. The large value of $M$ ensures that the constraint is always satisfied when $x_{i,j} = 1$.

## Usage

To use the DebtSolver, first install OR-Tools:

```bash
pip install ortools
```

Then, create an instance of the `DebtSolver` class with a dictionary of expenses and call the `solve` method.

```python
import collections
from debt_solver import DebtSolver

expenses = collections.OrderedDict(zip(['Person A', 'Person B', 'Person C'], [100, 50, 0]))
result = DebtSolver(expenses).solve()
```