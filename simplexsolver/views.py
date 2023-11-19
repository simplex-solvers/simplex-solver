from flask import render_template, request
from simplexsolver import app
import numpy as np
from .simplex.simplex_algorithm import SimplexPrimal, SimplexDual
from .simplex.graphic_solution import create_graph
from .simplex.dual_validator import primal_to_dual, change_constraints

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
    problem_form = data['problem_form']

    if problem_form == "primal":
        problem = SimplexPrimal(problem_type, num_of_var, c, A, b, constraints)
        solution, all_tableaus = problem.solve()

    elif problem_form == "dual":              
        if problem_type =="max":
            A, b, c, constraints, problem_type = primal_to_dual(A, b, c, problem_type)
            A, b, constraints = change_constraints(A, b, constraints)
            
        if "=" in constraints or ">=" in constraints:
            A, b, constraints = change_constraints(A, b, constraints)

        problem = SimplexDual(problem_type, num_of_var, c, A, b, constraints)
        solution, all_tableaus = problem.solve()

    for tableau in all_tableaus:
        print(tableau)

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

    problem = SimplexPrimal(problem_type, num_of_var, c, A, b, constraints)
    
    solution, _ = problem.solve()

    if num_of_var == 2:
        graph_html = create_graph(A, b, c, constraints, solution)

    return render_template('graph.html', graph_html=graph_html)
   
