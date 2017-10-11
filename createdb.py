
import csv, sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pagedata (Page varchar2,Frame number,Motor1 number,Motor2 number,Motor3 number,Motor4 number,Motor5 number,Motor6 number,Motor7 number,Motor8 number,Motor9 number,Motor10 number,Motor11 number,Motor12 number,Motor13 number,Motor14 number,Motor15 number,Motor16 number,Motor17 number,Motor18 number);") # use your column names here

with open('pagedata.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Page'],i['Frame'],i['Motor 1'],i['Motor 2'],i['Motor 3'],i['Motor 4'],i['Motor 5'],i['Motor 6'],i['Motor 7'],i['Motor 8'],i['Motor 9'],i['Motor 10'],i['Motor 11'],i['Motor 12'],i['Motor 13'],i['Motor 14'],i['Motor 15'],i['Motor 16'],i['Motor 17'],i['Motor 18']) for i in dr]

cur.executemany("INSERT INTO pagedata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()


con = sqlite3.connect("test.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS flowdata (Flow varchar2,PageID number,PageName varchar2,Speed number);") # use your column names here

with open('flowdata.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Flow'],i['PageID'],i['PageName'],i['Speed']) for i in dr]

cur.executemany("INSERT INTO flowdata VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()


