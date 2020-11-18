# Anmol Kapoor

# Step 1: Enter everything into the database
import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import sys, os

# source for variety of jobs
sp = BeautifulSoup(requests.get("https://www.joblist.com/b/all-jobs").text, 'html.parser')

# get all elements with job titles
departments = sp.find_all("ul", class_="css-3dvgnl")[2:-1]

titles = []
for dept in departments:
    for a_tag in dept.find_all("a"):
        titles.append(a_tag.text)

# define a method for creating a connection to giant.db
# I rarely get an error message, so I haven't really refined the except block
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

## empty the database if it already exists to repopulate it
if os.path.exists("giant.db"):
    os.remove("giant.db")
# create the connection and the table in the db
conn, curs = get_cnxn("giant.db")
curs.execute('create table giant_jobs (title nvarchar(120), yes_no bit)')
conn.commit()

# insert all data from joblist.com
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

# insert all data from output_non_jobs.txt
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

# Here we will add locations as false data, because apparently, we are getting that
cit_cn, cit_cu = get_cnxn("../cities.db")
cit_cu.execute("select distinct city from usa")
cities = [city[0] for city in cit_cu.fetchall()]
cit_cu.execute("select distinct state from usa")
states = [state[0] for state in cit_cu.fetchall()]
cities.append("Remote") # because of COVID situation

## handle the cities first
insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for city in cities:
    if city == cities[-1]:
        last = True
    cit = city.replace("'", "")
    insertion_cmd += f"('{cit}', '{0}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

## handle the states now
insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for state in states:
    if state == states[-1]:
        last = True
    stat = state.replace("'", "")
    insertion_cmd += f"('{stat}', '{0}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

cit_cu.close()
cit_cn.close()

# Here we will add job titles as true data, because apparently, we are getting too many positives
job_cn, job_cu = get_cnxn("../jobs.db")
job_cu.execute("select distinct title from jobs")
jobs = [job[0] for job in job_cu.fetchall()]

## handle the jobs first
insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for job in jobs:
    if job == jobs[-1]:
        last = True
    jo = job.replace("'", "")
    insertion_cmd += f"('{jo}', '{1}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

job_cu.close()
job_cn.close()

# now add some phrases that are common on job sites, but are not job titles
extra_false_phrases = [
    "Department",
    "All Departments",
    "Office",
    "All Offices",
    "Finance",
    "Current Job Openings",
    "Global Support",
    "Human Resources",
    "IT",
    "Marketing",
    "Product",
    "Product Designer",
    "Professional Services",
    "Research and Development",
    "Engineering",
    "Applications",
    "Cloud Engineering",
    "Data Infrastructure & Security",
    "Data Platforms",
    "Quality & Release",
    "Security",
    "Runtime",
    "SQL",
    "Sales",
    "Alliances",
    "Corporate Sales",
    "Customer & Product Strategy",
    "Sales Engineering",
    "Sales Operations",
    "Workplace",
    "Agriculture, Food, & Natural Resources",
	"Architecture & Construction",
	"Arts, Audio/Video Technology, and Communications",
	"Business, Management, & Administration",
	"Education & Training",
	"Government & Public Administration",
	"Health Science",
	"Hospitality & Tourism",
	"Information Technology",
	"Law, Public Safety, Corrections, & Security",
	"Manufacturing",
	"Marketing, Sales, & Service",
	"Science, Technology, Engineering, & Mathematics",
    "Technology",
	"Transportation, Distribution, & Logistics"
]

# Here we will add related to job titles as false data, because apparently, we are getting too many positives
insertion_cmd = "insert into giant_jobs(title, yes_no) values "
last = False
for phrase in extra_false_phrases:
    if phrase == extra_false_phrases[-1]:
        last = True
    phras = phrase.replace("'", "")
    insertion_cmd += f"('{phras}', '{0}')"
    if not last:
        insertion_cmd += ", "
curs.execute(insertion_cmd)
conn.commit()

# finally close the connection to giant.db
curs.close()
conn.close()
