import math
import numpy as np
from .simplex_algorithm import SimplexPrimal
from decimal import Decimal, ROUND_HALF_UP

class Node:
   def __init__(self, A, b, c, constraints, solution_variables, op_z, num_of_var):
      self.solution = solution_variables
      self.left_child = None
      self.right_child = None  
      self.constraints = constraints
      self.A = A
      self.b = b
      self.c = c
      self.z = op_z
      self.num_of_var = num_of_var

   def insert_constraint(self, i, value, constraint_type):
      """ Insere a nova restrição inteira do problema """
      new_constraint = np.zeros(self.num_of_var)
      new_constraint[i] = 1
      self.A = np.vstack((self.A, new_constraint))
      self.b = np.append(self.b, value)
      self.constraints = np.append(self.constraints, constraint_type)
      
      
   def is_feasible(self):
      """" Verifica se a solução encontrada não fere as restrições do problema """
      
      for i in range(len(self.A)):
         """Calcula o valor do "lado esquerdo" a partir do produto escaloar em que:
         1. self.A[i] seleciona uma linha específica (uma restrição específica) da matriz A.
         2. solution é um vetor que contém os valores das variáveis de decisão."""
         
         lhs = np.dot(self.A[i], self.solution)
         
         # Checa se alguma condiçâo não for satisfeita (torna o problema impossível)ca o tipo de restrição e se ela é satisfeita pela solução
         if self.constraints[i] == "<=" and np.around(lhs, 5) > self.b[i]:
            return False
         elif self.constraints[i] == ">=" and np.around(lhs, 5) < self.b[i]:
            return False
         elif self.constraints[i] == "=" and np.around(lhs, 5) != self.b[i]:
            return False

      # Se todas as condições forem satisfeitas retorna True, caso contre todas as restrições forem satisfeitas, a solução é viável
      return True
   
   
   def __str__(self):
      return f"Node(A={self.A}, b={self.b}, c={self.c}, constraints={self.constraints}, solution={self.solution}, z={self.z})"


class BranchAndBound:
   def __init__(self, problem_type, optimal_solution):
      self.root = None
      self.problem_type = problem_type
      if self.problem_type == "max":
         self.lower_bound = -math.inf
         self.upper_bound = optimal_solution
      elif self.problem_type == "min":
         self.lower_bound = optimal_solution
         self.upper_bound = math.inf

   def solve_pli(self, node):
      problem = SimplexPrimal(self.problem_type, node.num_of_var, node.c, node.A, node.b, node.constraints)
      solution, _ = problem.solve()
      node.z = solution['optimal_solution']
      node.solution = solution['solution']
      print(f"solução: {solution['solution']}, optimal_solution: {solution['optimal_solution']}")


   def branch(self, node):
      """Funçâo que ramifica e escolhe a variável a particionar 
      por ter maior resíduo, seguindo o critério de Dank """

      residue = -math.inf 
      print("Node solution: ", node.solution)      

      for i, value in enumerate(node.solution):
         if value != int(value) and value - int(value) > residue: 
            index, chosen_value = i, value if value - int(value) > residue else (index, chosen_value)
            residue = value - int(value) 

      print(f"Valor escolhido {chosen_value}")         
      node.left_child = self.insert_new_node(index, int(chosen_value), "<=", node)      
      node.right_child = self.insert_new_node(index, int(chosen_value) + 1, ">=", node)      


   def insert_new_node(self, i, value, constraint_type, node): 
      #Insere um novo nó 
      new_node = Node(node.A, node.b, node.c, node.constraints, [], 0, node.num_of_var) #Ajustar isso
      new_node.insert_constraint(i, value, constraint_type)
      return new_node


   def optimize(self, node):
      """A parada da recursividade são baseados em 3 critérios:
         1. Para quando o problema é impossível (fere as restrições dos outros prooblemas)
         2. Parar quando não se existe uma solução pelo simplex
         3. Parar quando for obtida uma solução inteira """
      
      print("-" * 50)
      print("Nó executado: ", node)
      
      if self.root == None: 
         self.root = node #Se não tem nó raiz, cria o primeiro     
      else:
         self.solve_pli(node) #Se não está na raiz resolve o problema

      if node.solution is None: 
         return

      if node.is_feasible() == False: 
         print("Impossível")
         return

      #Se a solução não possui todas variáveis inteiras, ramifica
      if any(value != int(value) for value in node.solution): 
         print("Valor não otimo: ", node.solution)
         self.branch(node) #Ramifica
         self.optimize(node.left_child) #Chamada de recursividade para o filho da esquerda
         self.optimize(node.right_child) #Chamada de recursividade para o filho direito
      
      #Todas as variáveis da solução problema possuem valor inteiro no nó
      else:
         #Compara o valor do z com o lower bound (maior valor)
         if node.z > self.lower_bound and self.problem_type == "max": 
            self.lower_bound = node.z
            self.best_solution = node.solution
            self.optimal_z = self.lower_bound
            return node 
         #Compara o valor do z com o upper bound (menor valor)
         elif node.z < self.upper_bound and self.problem_type == "min":
            self.upper_bound = node.z
            self.best_solution = node.solution
            self.optimal_z = self.upper_bound
            return node 
         else:
            return
         
      return  {
         'solution': self.best_solution,
         'optimal_solution': self.optimal_z
      }