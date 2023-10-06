from flask import render_template, request
from simplexsolver import app

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/resultado', methods=['POST'])
def solve():
    return 'Solução do problema.'
