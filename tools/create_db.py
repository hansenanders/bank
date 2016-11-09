#!/usr/bin/env python3

import sqlite3

DB_NAME  = 'bank.db'
conn = sqlite3.connect(DB_NAME)
print("Opened database (%s) successfully" % DB_NAME)



print
conn.execute('''CREATE TABLE categories
(NAME TEXT DEFAULT NULL,
TYPE TEXT DEFAULT NULL
);''')

conn.execute('''CREATE TABLE transactions
(
  NAME TEXT DEFAULT NULL,
  DATE TEXT DEFAULT NULL,
  VALUE REAL DEFAULT NULL
);''')

conn.close()

