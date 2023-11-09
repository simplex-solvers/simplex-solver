import numpy as np
import math 

class PrimalTableau:
    def __init__(self, c, A, b, constraint, problem_type):
        self.problem_type = problem_type
        if self.problem_type == "min":
            self.c = c
        else:
            self.c = -c
        self.A = A
        self.b = b
        self.constraint = constraint
        self.M = 100
 

    def add_variables(self):
        m, _ = self.A.shape

        for i in range(m):
            constraint = self.constraint[i]

            if constraint == "<=":
                slack_variable = np.zeros(m)
                slack_variable[i] = 1 
                self.A = np.column_stack((self.A, slack_variable)) 
                self.c = np.append(self.c, 0) 

            elif constraint == ">=":
                surplus_variable = np.zeros(m)
                surplus_variable[i] = -1  
                self.A = np.column_stack((self.A, surplus_variable))  
                self.c = np.append(self.c, 0) 
                artificial_variable = np.zeros(m)
                artificial_variable[i] = 1  
                self.A = np.column_stack((self.A, artificial_variable)) 
                self.c = np.append(self.c, self.M)  

            elif constraint == "=":
                artificial_variable = np.zeros(m)
                artificial_variable[i] = 1  
                self.A = np.column_stack((self.A, artificial_variable)) 
                self.c = np.append(self.c, self.M)


    def create_tableau(self):
        combined_array = np.hstack((self.A, np.expand_dims(self.b, axis=1)))
        self.c = np.append(self.c, 0)

        for i, constraint in enumerate(self.constraint):
            if constraint == ">=" or constraint == "=":
                self.c = self.c - self.M * combined_array[i] #NumPy não aceita self.c -= self.M * combined_array[i] 
        
        tableau = np.vstack((self.c, combined_array))
        return tableau

