#!/usr/bin/env python3
import csv
import json
from flask import (
    Flask, render_template, send_file, jsonify)

TEMPLATE = 'index.html'
CATEGORYS = 'categorys.json'
app = Flask(__name__)


@app.route('/')
def render():
    return render_template(TEMPLATE)

@app.route('/data', methods=['POST'])
def data():
    return send_file('anders-sep.csv',
                     mimetype='text/csv',
                     attachment_filename='data.csv',
                     as_attachment=True)

@app.route('/data/categorys', methods=['POST'])
def data_categorys():
    with open(CATEGORYS, 'r') as f:
        d = json.load(f)
    return jsonify(d)
    

if __name__ == "__main__":
    app.run()

