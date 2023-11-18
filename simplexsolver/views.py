from flask import render_template, request
from simplexsolver import app
import numpy as np
from .simplex.primal_tableau import PrimalTableau
from .simplex.simplex_algorithm import SimplexPrimal
from .simplex.graphic_solution import create_graph

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
    formated_tableau = tableau.get_formated_tableau()

    problem = SimplexPrimal(formated_tableau, problem_type, num_of_var)
    solution, all_tableaus = problem.solve()


    for tableau in all_tableaus:
        print(tableau)
        print()

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
    formated_tableau = tableau.get_formated_tableau()

    problem = SimplexPrimal(formated_tableau, problem_type, num_of_var)
    
    solution, _ = problem.solve()

    if num_of_var == 2:
        graph_html = create_graph(A, b, c, constraints, solution)

    return render_template('graph.html', graph_html=graph_html)
   
