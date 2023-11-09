import numpy as np
import math

class SimplexAlgorithm:
   def __init__(self, tableau, problem_type, num_of_variables):
      self.tableau = tableau
      self.problem_type = problem_type
      self.num_of_variables = num_of_variables
      self.all_iteracions = []


   def solve(self):
      while self.is_not_optimum():
         #Passo a passo do algoritmo
         entering_column = self.get_entering_column()
         pivot_row = self.get_pivot_row(entering_column)
         pivot_value = self.get_pivot_value(pivot_row, entering_column)
         self.update_tableau(pivot_row, entering_column, pivot_value)
      
      return self.get_solution(), self.all_iteracions

   def is_not_optimum(self):
      return any(self.objective_row[:-1] < 0)


   @property
   def objective_row(self):
      return self.tableau[0]


   def get_pivot_value(self, i, j):
      return self.tableau[i][j]
   

   def get_entering_column(self):
      objective_row = self.objective_row
      entering_column = None
      min_coefficient = math.inf

      for i, coefficient in enumerate(objective_row[:-1]):
         if coefficient < min_coefficient:
               min_coefficient = coefficient
               entering_column = i
               
      return entering_column


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
