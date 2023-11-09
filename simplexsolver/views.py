from flask import render_template, request
from simplexsolver import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def solve():
    return 'Solução do problema.'
