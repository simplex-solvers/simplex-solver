from flask import render_template, request
from simplexsolver import app
import numpy as np
import logging
from .simplex.primal_tableau import PrimalTableau
from .simplex.simplex_algorithm import SimplexAlgorithm
from .simplex.graphic_solution import create_graph

#Veio do frontend
c = np.array([0.4, 0.5])
A = np.array([[0.3, 0.1], [0.5, 0.5], [0.6, 0.4]])
b = np.array([2.7, 6, 6])
constraints = ["<=", "=", ">="]
problem_type = "min"
num_of_variables = c.shape[0]

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/resultado')
def tabular_solve():
    tableau = PrimalTableau(c, A, b, constraints, problem_type)
    tableau.add_variables()
    final_tableau = tableau.create_tableau()

    problem = SimplexAlgorithm(final_tableau, problem_type, num_of_variables)
    solution, all_tableaus = problem.solve()

    print(solution)
   
    for i in range(len(all_tableaus)):
        print(all_tableaus[i])
    
    return 'OK'

@app.route('/grafico')
def graph_solve():
    tableau = PrimalTableau(c, A, b, constraints, problem_type)
    tableau.add_variables()
    final_tableau = tableau.create_tableau()

    problem = SimplexAlgorithm(final_tableau, problem_type, num_of_variables)
    
    solution, _ = problem.solve()

    if num_of_variables == 2:
        create_graph(A, b, c, constraints, solution)
    return 'OK'
