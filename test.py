import csv, sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()
cur.execute('SELECT * FROM pagedata where Page="1 Bow";')
print(cur.fetchall())
con.commit()
con.close()
