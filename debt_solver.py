from ortools.linear_solver import pywraplp

class DebtSolver:
    """
    A class to solve debt allocation problems. Given a dictionary of expenses, the solver will
    determine how much each person owes or is owed in order to even out the expenses.
    """
    def __init__(self, expenses):
        """
        Initializes the DebtSolver with a dictionary of expenses.

        Args:
            expenses: A dictionary of expenses where the keys are the names of the people and the
                      values are the amounts they spent.
        """
        self.expenses, self.per_capita_expense = self.round_cents(expenses)
        self.debts = {k: max(0, self.per_capita_expense*(k.count("+")+1)-v) for k,v in self.expenses.items()}
        self.loans = {k: max(0, v-self.per_capita_expense*(k.count("+")+1)) for k,v in self.expenses.items()}

        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        
        # Create variables
        self.variables = {}
        for person_i in self.expenses.keys():
            for person_j in self.expenses.keys():
                name = f"x_{person_i}_{person_j}"
                self.variables[name] = self.solver.IntVar(0, 1, name)
                name = f"z_{person_i}_{person_j}"
                self.variables[name] = self.solver.IntVar(0, self.solver.infinity(), name)

        # Add constraints
        for person_j in self.expenses.keys():
            self.solver.Add(sum(self.variables[f"z_{person_i}_{person_j}"] for person_i in self.expenses.keys()) == self.loans[person_j])
        for person_i in self.expenses.keys():
            self.solver.Add(sum(self.variables[f"z_{person_i}_{person_j}"] for person_j in self.expenses.keys()) == self.debts[person_i])
        for person_i in self.expenses.keys():
            for person_j in expenses.keys():
                self.solver.Add(999999999.0 * self.variables[f"x_{person_i}_{person_j}"] - self.variables[f"z_{person_i}_{person_j}"] >= 0)

        # Set objective
        objective = self.solver.Sum(self.variables[f"x_{person_i}_{person_j}"] for person_i in self.expenses.keys() for person_j in self.expenses.keys())
        self.solver.Minimize(objective)

    def solve(self):
        """
        Solves the debt allocation problem and returns a string representation of the solution.
        
        Returns:
            A string representation of the solution. If a solution is found, it will be in the form
            "*Debts:*\n\n[person] owes [person]: [amount]\n[person] owes [person]: [amount]\n...".
            If a solution is not found, it will return "I couldn't find a solution to the problem.".
        """
        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            message = "*Debts:*\n\n"
            for person_i in self.expenses.keys():
                for person_j in self.expenses.keys():
                    debt = self.variables[f"z_{person_i}_{person_j}"].solution_value()
                    if debt > 0:
                        message = f"{message}{person_i} owes {person_j}: ${int(debt)}\n"
            return message.rstrip('\n')
        else:
            return "Couldn't find a solution to the problem."

    @staticmethod
    def round_cents(expenses):
        """
        Rounds the expenses to the nearest dollar and returns the rounded expenses and the per-capita
        expense.

        Args:
            expenses: A dictionary of expenses where the keys are the names of the people and the
                      values are the amounts they spent.

        Returns:
            A tuple containing the rounded expenses as a dictionary and the per-capita expense as an
            integer.
        """
        # Round the per-capita expense to the nearest dollar
        n_people = sum([1+k.count("+") for k in expenses])
        per_capita_expense = round(sum(expenses.values())/n_people)

        # Calculate the difference between the total expenses and the per-capita expense
        diff = sum(expenses.values())-(per_capita_expense*n_people)
        
        # Sort the expenses in decreasing order by value
        expenses = sorted(list(expenses.items()), key=lambda x: x[1], reverse=True)
        
        # Adjust the largest expense to compensate for the difference
        expenses[0] = (expenses[0][0], expenses[0][1]-diff)
        
        # Return the rounded expenses and per-capita expense
        return dict(expenses), per_capita_expense

if __name__ == "__main__": 
    expenses = {
        "Person 1": 40967,
        "Person 2+Person 3": 40967, 
        "Person 4+Person 5": 40967,
        "Person 6": 12000,
        "Person 7": 0
    }
    result = DebtSolver(expenses).solve()
    print(result)