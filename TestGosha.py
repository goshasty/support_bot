# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect('test.db')  #do try
cur = con.cursor()
d = 1
cur.execute('SELECT * FROM companies WHERE main_subcategory_id = (?)', [d])
res = cur.fetchall()
print(res)
con.close
