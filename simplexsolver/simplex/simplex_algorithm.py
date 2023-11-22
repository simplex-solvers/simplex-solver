import numpy as np
import math
from abc import ABC, abstractmethod

class SimplexBase(ABC):
   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      self.problem_type = problem_type
      self.tableau = np.array([])
      self.num_of_variables = num_of_variables
      self.all_iterations = []
      self.c = c
      self.A = A
      self.b = b
      self.constraint = constraint

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
   def get_pivot_row(self, entering_column):
      pass

   @abstractmethod
   def get_entering_column(self):
      pass

   def update_tableau(self, pivot_row, entering_column, pivot_value):
      new_tableau = np.zeros_like(self.tableau)

      new_tableau[pivot_row] = np.round(self.tableau[pivot_row] / pivot_value, decimals=5)

      for index, row in enumerate(self.tableau):
         if pivot_row != index:
            multiplier = -row[entering_column]
            new_tableau[index] = np.round(multiplier * new_tableau[pivot_row] + self.tableau[index], decimals=5)
      
      self.all_iteracions.append(new_tableau.tolist())
      self.tableau = new_tableau

   def get_solution(self):
      transposed = np.transpose(self.tableau)
      solution = []
      
      for _, row in enumerate(transposed):
         count_1 = np.count_nonzero(row == 1)
         count_0 = np.count_nonzero(row == 0)

         if count_1 == 1 and count_0 == len(row) - 1: 
            index = np.argwhere(row==1)[0][0]
            op_value = np.round(self.tableau[index][-1], decimals=2)
            solution.append(op_value) 
         else:
            solution.append(0)

      solution = (solution[:self.num_of_variables])
      return solution



class SimplexPrimal(SimplexBase):
   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      super().__init__(problem_type, num_of_variables, c, A, b, constraint)
      self.M = 100


   def solve(self):
      self.get_formated_initial_tableau()

      while self.is_not_optimum():
         #Passo a passo do algoritmo
         entering_column = self.get_entering_column()
         pivot_row = self.get_pivot_row(entering_column)
         pivot_value = self.get_pivot_value(pivot_row, entering_column)
         self.update_tableau(pivot_row, entering_column, pivot_value)
      
      return self.get_solution(), self.all_iteracions


   def add_slack_variables(self, m, i):
      slack_variable = np.zeros(m)
      slack_variable[i] = 1 
      self.A = np.column_stack((self.A, slack_variable)) 
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
      self.add_variables()

      if self.problem_type == "max":
            self.c = -self.c

      combined_array = np.hstack((self.A, np.expand_dims(self.b, axis=1)))
      self.c = np.append(self.c, 0)

      for i, constraint in enumerate(self.constraint):
         if constraint == ">=" or constraint == "=":
               self.c = self.c - self.M * combined_array[i] 
      
      self.tableau = np.vstack((self.c, combined_array))
      self.all_iteracions.append(self.tableau.tolist())


   def is_not_optimum(self):
      return any(self.objective_row[:-1] < 0)


   @property
   def objective_row(self):
      return self.tableau[0]


   def get_entering_column(self):
      objective_row = self.objective_row[:-1] #Array Numpy
      return np.argmin(objective_row)


   def get_pivot_row(self, entering_column):
      pivot_column = (self.tableau[1:, entering_column])
      b_column = (self.tableau[1:, -1])
      ratios = [] 
      
      for i, element in enumerate(pivot_column):
         if element <= 0:
            ratios.append(math.inf)
         else:
            ratios.append(b_column[i] / element)
      
      pivot_row = ratios.index(min(ratios)) + 1 
      return pivot_row


class SimplexDual(SimplexBase):

   def __init__(self, problem_type, num_of_variables, c, A, b, constraint):
      super().__init__(problem_type, num_of_variables, c, A, b, constraint)

   def solve(self):
      self.get_formated_intial_tableau()

      while self.is_not_optimum():
         #Passo a passo do algoritmo
         pivot_row = self.get_pivot_row()
         entering_column = self.get_entering_column(pivot_row)
         pivot_value = self.get_pivot_value(pivot_row, entering_column)
         self.update_tableau(pivot_row, entering_column, pivot_value)    
      return self.get_solution(), self.all_iteracions
   
   
   def add_variables(self):
      m, _ = self.A.shape

      for i in range(m):
         self.add_slack_variables(m, i)


   def get_formated_intial_tableau(self):
      self.add_variables()
      combined_array = np.hstack((self.A, np.expand_dims(self.b, axis=1)))
      self.c = np.append(-self.c, 0)
      self.tableau = np.vstack((self.c, combined_array))
      self.all_iteracions.append(self.tableau.tolist())


   @property
   def b_column(self):
      return self.tableau[1:, -1]
   

   def is_not_optimum(self):
      return any(self.b_column < 0)


   def get_pivot_row(self):
      b_column = self.b_column
      pivot_row = np.argmin(b_column) + 1
      return pivot_row


   def get_entering_column(self, pivot_row):
      ratios = []

      for i, element in enumerate(self.tableau[pivot_row, :-1]):
         if element >= 0:
            ratios.append(math.inf)
         else:
            ratios.append(self.tableau[0][i] / element)
      
      entering_column = ratios.index(min(ratios))
      return entering_column



