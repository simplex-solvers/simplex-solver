import numpy as np
import math
from abc import ABC, abstractmethod
import random

class SimplexBase(ABC):
   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      self.problem_type = problem_type
      self.tableau = np.array([])
      self.num_of_variables = num_of_variables
      self.all_iterations = []
      self.c = c #Função Objetivo
      self.A = A
      self.b = b
      self.constraint = constraint
      self.solution_dict = {}


   @abstractmethod
   def solve(self):
      pass
   

   def add_slack_variables(self, m, i):
      slack_variable = np.zeros(m)
      slack_variable[i] = 1
      self.A = np.column_stack((self.A, slack_variable))
      self.c = np.append(self.c, 0)


   @abstractmethod
   def add_variables(self):
      pass


   @abstractmethod
   def get_formated_initial_tableau(self):
      pass


   @abstractmethod
   def is_not_optimum(self):
      pass


   def get_pivot_value(self, i, j):
      return self.tableau[i][j]
   
   @abstractmethod
   def get_leaving_row(self, entering_column):
      pass


   @abstractmethod
   def get_entering_column(self):
      pass


   def update_tableau(self, leaving_row, entering_column, pivot_value):
      new_tableau = np.zeros_like(self.tableau)

      new_tableau[leaving_row] = np.round(self.tableau[leaving_row] / pivot_value, decimals=5)

      for index, row in enumerate(self.tableau):
         if leaving_row != index:
            multiplier = -row[entering_column]
            new_tableau[index] = np.round(multiplier * new_tableau[leaving_row] + self.tableau[index], decimals=5)
     
      self.all_iterations.append(new_tableau.tolist())
      self.tableau = new_tableau


   def get_solution(self):
      transposed = np.transpose(self.tableau)
      solution = []
     
      for _, row in enumerate(transposed):
         count_1 = np.count_nonzero(row == 1)
         count_0 = np.count_nonzero(row == 0)
         if count_1 == 1 and count_0 == len(row) - 1:
            index = np.argwhere(row==1)[0][0]
            basic_variable = np.round(self.tableau[index][-1], decimals=2)
            solution.append(basic_variable)  
         else:
            solution.append(0)

      return solution[:self.num_of_variables]


   def get_optimal_solution(self):
      optimal_value = np.round(self.tableau[0][-1], decimals=2)
     
      if optimal_value < 0:
          optimal_value = -optimal_value
     
      return optimal_value


class SimplexPrimal(SimplexBase):
   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      super().__init__(problem_type, num_of_variables, c, A, b, constraint)
      self.M = 100
      self.original_c = self.c.copy()


   def solve(self):
      self.get_formated_initial_tableau()

      while self.is_not_optimum():
         entering_column = self.get_entering_column()
         leaving_row = self.get_leaving_row(entering_column)
         pivot_value = self.get_pivot_value(leaving_row, entering_column)
         self.update_tableau(leaving_row, entering_column, pivot_value)
     
      self.solution_dict['solution'] = self.get_solution()
     
      if self.test_multiple_solutions():
         self.solution_dict['additional_solutions'] =  self.get_solution()
         self.solution_dict['multiple_solution'] = self.get_multiple_solution()
      
      self.solution_dict['optimal_solution'] = self.get_optimal_solution()

      return self.solution_dict, self.all_iterations


   def add_surplus_variables(self, m, i):
      surplus_variable = np.zeros(m)
      surplus_variable[i] = -1  
      self.A = np.column_stack((self.A, surplus_variable))  
      self.c = np.append(self.c, 0)
   

   def add_artificial_variables(self, m, i):
      artificial_variable = np.zeros(m)
      artificial_variable[i] = 1  
      self.A = np.column_stack((self.A, artificial_variable))
      self.c = np.append(self.c, self.M)


   def add_variables(self):
      m, _ = self.A.shape

      for i in range(m):
         constraint = self.constraint[i]
         if constraint == "<=":
               self.add_slack_variables(m, i)
         elif constraint == ">=":
               self.add_surplus_variables(m, i)
               self.add_artificial_variables(m, i)
         elif constraint == "=":
               self.add_artificial_variables(m, i)

   
   def get_formated_initial_tableau(self):     
      if self.problem_type == "max":
            self.c = -self.c

      self.add_variables()
      
      combined_array = np.hstack((self.A, np.expand_dims(self.b, axis=1)))
      self.c = np.append(self.c, 0)

      for i, constraint in enumerate(self.constraint):
         if constraint == ">=" or constraint == "=":
               self.c = self.c - self.M * combined_array[i]
     
      self.tableau = np.vstack((self.c, combined_array))
      self.all_iterations.append(self.tableau.tolist())


   def is_not_optimum(self):
      return any(self.objective_row[:-1] < 0)


   @property
   def objective_row(self):
      return self.tableau[0]


   def get_entering_column(self):
      objective_row = self.objective_row[:-1]
      return np.argmin(objective_row)


   def get_leaving_row(self, entering_column):
      pivot_column = (self.tableau[1:, entering_column])
      b_column = (self.tableau[1:, -1])
      min_ratio = math.inf
     
      for i, element in enumerate(pivot_column):
         if element > 0:
            ratio = b_column[i] / element
            if ratio < min_ratio:
               min_ratio = ratio
               leaving_row = i + 1

      return leaving_row


   def test_multiple_solutions(self):
      transposed = np.transpose(self.tableau)
      for i, row in enumerate(transposed):
         count_1 = np.count_nonzero(row == 1)
         count_0 = np.count_nonzero(row == 0)

         if self.tableau[0][i] == 0 and count_1 != 1 and count_0 != 0:
            leaving_row = self.get_leaving_row(i)
            pivot_value = self.get_pivot_value(leaving_row, i)
            self.update_tableau(leaving_row, i, pivot_value)
            return True
     
      return False
   
   def get_multiple_solution(self):
      B = self.solution_dict.get('solution')
      C = self.solution_dict.get('additional_solutions')
      alpha = random.uniform(0, 1)
      multiple_solution = []
      for i in range(len(B)):
         x = alpha * B[i] + (1 - alpha) * C[i]
         multiple_solution.append(round(x, 2))
      return multiple_solution


class SimplexDual(SimplexBase):

   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      super().__init__(problem_type, num_of_variables, c, A, b, constraint)


   def solve(self):
      self.get_formated_initial_tableau()


      while self.is_not_optimum():
         leaving_row = self.get_leaving_row()
         entering_column = self.get_entering_column(leaving_row)
         pivot_value = self.get_pivot_value(leaving_row, entering_column)
         self.update_tableau(leaving_row, entering_column, pivot_value)
     
      self.solution_dict['solution'] = self.get_solution()
      self.solution_dict['optimal_solution'] = self.get_optimal_solution()

      return self.solution_dict, self.all_iterations
   
   
   def add_variables(self):
      m, _ = self.A.shape

      for i in range(m):
         self.add_slack_variables(m, i)


   def get_formated_initial_tableau(self):
      self.add_variables()
      combined_array = np.hstack((self.A, np.expand_dims(self.b, axis=1)))
      self.c = np.append(-self.c, 0)
      self.tableau = np.vstack((self.c, combined_array))
      self.all_iterations.append(self.tableau.tolist())


   @property
   def b_column(self):
      return self.tableau[1:, -1]
   

   def is_not_optimum(self):
      return any(self.b_column < 0)


   def get_leaving_row(self):
      b_column = self.b_column
      leaving_row = np.argmin(b_column) + 1
      return leaving_row


   def get_entering_column(self, leaving_row):
      min_ratio = math.inf
      for i, element in enumerate(self.tableau[leaving_row, :-1]):
         if element < 0:
            ratio = self.tableau[0][i] / element
            if ratio < min_ratio:
               min_ratio = ratio
               entering_column = i
     
      return entering_column
     


