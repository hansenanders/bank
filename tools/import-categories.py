#!/usr/bin/env python3
import argparse
import sqlite3
import json
import sys


parser = argparse.ArgumentParser(description='import categories to sqlitedb.')
parser.add_argument(
    '-d', '--sqlite-db-file', required=True, action='store', help='path to SQLiteDB')
parser.add_argument('--data-file', required=True, help='data file path')
args = parser.parse_args()


db = sqlite3.connect(args.sqlite_db_file)
data = json.load(args.data_file)

cur = db.cursor()
for d in data:
    try:
        query = '''INSERT INTO categories (name, type) VALUES ("{}", "{}")'''.format(d, data[d])
        print(query)
        cur.execute(query)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


cur.execute("SELECT * FROM categories")
data = cur.fetchall()
print(data)

db.close()
