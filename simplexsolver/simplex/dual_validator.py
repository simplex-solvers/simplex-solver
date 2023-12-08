import numpy as np

def primal_to_dual(A, b, c, problem_type):
    A = np.transpose(A)
    b, c = c, b
    constraints = []
    for _ in b:
        constraints.append(">=")
    problem_type = "min"
    num_of_var = c.shape[0]

    return A, b, c, constraints, problem_type, num_of_var


def change_constraints(A, b, constraints):
   new_A = []
   new_b = []
   new_constraints = []

   actions = {
       "<=": lambda i: (new_A.append(A[i]), new_b.append(b[i]), new_constraints.append("<=")),
       "=": lambda i: (new_A.append(A[i]), new_b.append(b[i]), new_constraints.append("<="), new_A.append(-A[i]), new_b.append(-b[i]), new_constraints.append("<=")),
       ">=": lambda i: (new_A.append(-A[i]), new_b.append(-b[i]), new_constraints.append("<="))
   }

   for i, constraint in enumerate(constraints):
       action = actions.get(constraint)
       if action is not None:
           action(i)

   new_A = np.array(new_A)
   new_b = np.array(new_b)
   return new_A, new_b, new_constraints