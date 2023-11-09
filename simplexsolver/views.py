from flask import render_template, request
from simplexsolver import app
import numpy as np

c = np.array([0.4, 0.5])
A = np.array([[0.3, 0.1], [0.5, 0.5], [0.6, 0.4]])
b = np.array([2.7, 6, 6])
constraints = ["<=", "=", ">="]
problem_type = "min"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado')
def tabular_solve():
    return render_template('index.html')

@app.route('/grafico')
def graph_solve():
    return render_template('index.html')
