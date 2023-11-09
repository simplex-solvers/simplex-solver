from flask import render_template, request
from simplexsolver import app
import numpy as np

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado')
def tabular_solve():
    return render_template('index.html')

@app.route('/grafico')
def graph_solve():
    return render_template('index.html')