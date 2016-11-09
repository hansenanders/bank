#!/usr/bin/env python3

import argparse
import sqlite3
import json
import sys
import datetime
import csv
import re

parser = argparse.ArgumentParser(description='import bank data to sqlitedb.')
parser.add_argument(
    '-d', '--sqlite-db-file', required=True, action='store', help='path to SQLiteDB')
parser.add_argument('-c', '--csv-file', required=True, help='path to CSV with transaction data')
args = parser.parse_args()

db = sqlite3.connect(args.sqlite_db_file)

def wash(name, date, value):
    assert name != None, 'name is None'
    assert date != None, 'date is None'
    assert value != None, 'value is None'

    date = date
    name = re.sub(r'Kort.+p\s[0-9]+\s', '', name)
    value = float(value.replace('.', '').replace(',', '.'))

    try:
        value = int(value)
    except:
        value = float(value)*1000
        print('Fail to convert to Int, trying float. %s' % value)

    return name, date, value

def insert(name=None, date=None, value=None):
    assert name != None, 'name is None'
    assert date != None, 'date is None'
    assert value != None, 'value is None'
    
    cur = db.cursor()
    try:
        query = """
        INSERT INTO 
        transactions (name, date, value) 
        VALUES 
        ('{name}', '{date}', '{value}')
        """.format(name=name, date=date, value=value)
        print(query)
        cur.execute(query)
    except Exception as e:
        print(e)
        db.rollback()


        print()
with open(args.csv_file) as f:
    rows = csv.DictReader(f)
    for row in rows:
        print(row)
        name = row.get('Transaktion')
        date = row.get('Datum')
        value = row.get('Belopp')
        name, date, value = wash(name, date, value)
        insert(name=name, date=date, value=value)

db.commit()
db.close()
#print('Added %s new rows to bankdb.transactions' % len(rows))

