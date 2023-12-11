from flask import render_template, request
from simplexsolver import app
import numpy as np
from .simplex.simplex_algorithm import SimplexPrimal, SimplexDual
from .simplex.graphic_solution import create_graph
from .simplex.dual_validator import primal_to_dual, change_constraints
from .simplex.branch_and_bound import Node, BranchAndBound

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solver():
    num_of_var = int(request.form.get('qntdCamp'))
    qntrest = int(request.form.get('qntdRestr'))
    problem_type = request.form.get('tipoProblema')
    problem_form = request.form.get('solucao')
    constraints = request.form.getlist('constr[]')
    Oc = request.form.getlist('campo[]')
    OA = request.form.getlist('campoR[]')
    Ob = request.form.getlist('resp[]')

    Sc = [float(x) for x in Oc]
    SA = [float(x) for x in OA]
    Sb = [float(x) for x in Ob]

    FA = [SA[i:i+num_of_var] for i in range(0, len(OA), num_of_var)]
    
    data = {
        "num_of_var": num_of_var,
        "qrest": qntrest,
        "problem_type": problem_type,
        "problem_form": problem_form,
        "constraints": constraints,
        "c": Sc,
        "A": FA,
        "b": Sb
    }

    # data = request.get_json()
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])

    # print(c)
    # print(A)
    # print(b)

    # constraints = data['constraints']
    # problem_type = data['problem_type']
    # num_of_var = data['num_of_var']
    # problem_form = data['problem_form']

    if problem_form == "graph":
        problem = SimplexPrimal(problem_type, num_of_var, c, A, b, constraints)
        solution, _ = problem.solve()
        if num_of_var == 2:
            graph_html = create_graph(A, b, c, constraints, solution)
        return render_template('graph.html', graph_html=graph_html)
    
    elif problem_form == "integer":
        problem = SimplexPrimal(problem_type, num_of_var, c, A, b, constraints)
        solution, all_tableaus = problem.solve()
        root = Node(A, b, c, constraints, solution['solution'], solution['optimal_solution'], num_of_var) 
        bb = BranchAndBound(problem_type, solution['optimal_solution'])
        solution = bb.optimize(root)  
        print("Melhor solução inteira: ", solution)

    elif problem_form == "primal":
        problem = SimplexPrimal(problem_type, num_of_var, c, A, b, constraints)
        solution, all_tableaus = problem.solve()

    elif problem_form == "dual":
        if problem_type == "max":
            A, b, c, constraints, problem_type, num_of_var = primal_to_dual(
               A, b, c, problem_type)
            A, b, constraints = change_constraints(A, b, constraints)

        if "=" in constraints or ">=" in constraints:
            A, b, constraints = change_constraints(A, b, constraints)

        problem = SimplexDual(problem_type, num_of_var, c, A, b, constraints)
        solution, all_tableaus = problem.solve()
    
    

    for tableau in all_tableaus:
        print(tableau)

    tableaus = {
        "solution": solution,
        "all_tableaus": [tableau for tableau in all_tableaus]
    }
    
    if problem_form == "primal":
        return render_template('tabularSimplex.html', json_data=tableaus, qntVar = num_of_var)
    elif problem_form == "dual":
        return render_template('dualSimplex.html', json_data=tableaus, qntVar = num_of_var)
    elif problem_form == "integer":
        return render_template('integerSolution.html', json_data=tableaus, qntVar = num_of_var, qntRest=qntrest, data=data)

@app.route('/grafico', methods=['POST'])
def graph_solve():
    # Pega os dados do fomrulario
    # num_of_var = int(request.form.get('qntdCamp'))
    # qntrest = int(request.form.get('qntdRestr'))
    # problem_type = request.form.get('tipoProblema')
    # problem_form = request.form.get('solucao')
    # constraints = request.form.getlist('constr[]')
    # Oc = request.form.getlist('campo[]')
    # OA = request.form.getlist('campoR[]')
    # Ob = request.form.getlist('resp[]')

    # Sc = [float(x) for x in Oc]
    # SA = [float(x) for x in OA] # Converte string para float
    # Sb = [float(x) for x in Ob]

    # FA = [SA[i:i+num_of_var] for i in range(0, len(OA), num_of_var)] # Coloca em uma array de ayyars

    # data = {
    #     "num_of_var": num_of_var,
    #     "qrest": qntrest,
    #     "problem_type": problem_type,
    #     "problem_form": problem_form,
    #     "constraints": constraints,
    #     "c": Sc,
    #     "A": FA,
    #     "b": Sb
    # }

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

@app.route("/teste")
def teste():
    return render_template("base.html")