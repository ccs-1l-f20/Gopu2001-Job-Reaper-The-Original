# Anmol Kapoor

# Step 1: Enter everything into the database
import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import sys, os

sp = BeautifulSoup(requests.get("https://www.joblist.com/b/all-jobs").text, 'html.parser')

departments = sp.find_all("ul", class_="css-3dvgnl")[2:-1]
print("total sections:", len(departments))

titles = []
for dept in departments:
    for a_tag in dept.find_all("a"):
        titles.append(a_tag.text)

def get_cnxn(src):
    conn, curs = None, None
    try:
        conn = sql.connect(src)
        curs = conn.cursor()
    except sql.Error as e:
        print(e)
        if os.path.exists(src):
            curs.close()
            conn.close()
        sys.exit(1)
    return conn, curs

if os.path.exists("giant.db"):
    os.remove("giant.db")
conn, curs = get_cnxn("giant.db")
curs.execute('create table giant_jobs (title nvarchar(120), yes_no bit)')
conn.commit()

insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for title in titles:
    if title == titles[-1]:
        last = True
    insertion_cmd += f"('{title}', '{1}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

with open("output_non_jobs.txt", mode="r", encoding="utf-8") as file:
    content = file.readlines()

insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for line in content:
    if line == content[-1]:
        last = True
    title = line.replace("'", "")
    insertion_cmd += f"('{title}', '{0}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

curs.close()
conn.close()
