from flask import render_template, request
from simplexsolver import app
import numpy as np
from .simplex.primal_tableau import PrimalTableau
from .simplex.simplex_algorithm import SimplexAlgorithm
from .simplex.graphic_solution import create_graph

# #Veio do frontend
# c = np.array([0.4, 0.5])
# A = np.array([[0.3, 0.1], [0.5, 0.5], [0.6, 0.4]])
# b = np.array([2.7, 6, 6])
# constraints = ["<=", "=", ">="]
# problem_type = "min"
# num_of_var = c.shape[0]

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/tabular', methods=['POST'])
def tabular_solve():
    data = request.get_json()  
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    constraints = data['constraints']
    problem_type = data['problem_type']
    num_of_var = data['num_of_var']

    tableau = PrimalTableau(c, A, b, constraints, problem_type)
    final_tableau = tableau.create_tableau()

    problem = SimplexAlgorithm(final_tableau, problem_type, num_of_var)
    solution, all_tableaus = problem.solve()

    return {
        "solution": solution,
        "all_tableaus": [tableau for tableau in all_tableaus]
    }


@app.route('/grafico', methods=['POST'])
def graph_solve():
    data = request.get_json()  
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    constraints = data['constraints']
    problem_type = data['problem_type']
    num_of_var = data['num_of_var']

    tableau = PrimalTableau(c, A, b, constraints, problem_type)
    final_tableau = tableau.create_tableau()

    problem = SimplexAlgorithm(final_tableau, problem_type, num_of_var)
    
    solution, _ = problem.solve()

    if num_of_var == 2:
        create_graph(A, b, c, constraints, solution)

    return { "solution": solution }    
