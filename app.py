#!/usr/bin/env python3
import csv
import json
import sqlite3
import argparse
from flask import (Flask, render_template, jsonify, g)

TEMPLATE = 'index.html'
app = Flask(__name__)

parser = argparse.ArgumentParser(description='import bank data to sqlitedb.')
parser.add_argument('-d', '--db-file', required=True, action='store', help='path to SQLiteDB')
args = parser.parse_args()

DATABASE = args.db_file

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def db_fetchall(query):
    cursor = get_db().cursor()
    cursor.execute(query)
    return cursor.fetchall()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def render():
    return render_template(TEMPLATE)


@app.route('/data/transactions', methods=['POST'])
def get_transactions():
    query = "SELECT * from transactions"
    transactions = db_fetchall(query)

    response = {}
    for (name, date, value) in transactions:
        response[str(name)] = dict(date=date,
                                   value=value)
    print
    return jsonify(response)

@app.route('/data/categories', methods=['POST'])
def get_categories():
    query = "SELECT * from categories"
    categories = db_fetchall(query)

    response = {}
    for (name, value) in categories:
        response[str(name)] = value

    return jsonify(response)

if __name__ == "__main__":
    app.run()
