#!/usr/bin/python3.8
# Anmol Kapoor
'''
Intermediary Part 1 in this project is a tool to create a database that
combines all of the other databases in the 'jobs' folder.
'''

import sqlite3 as sql
import sys
from os import chdir, listdir, path, remove

def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
        cur = conn.cursor()
    except sql.Error as e:
        print(e)
        if path.exists('jobs.db'):
            main_curs.close()
            main_cnxn.close()
            remove('jobs.db')
        sys.exit(1)
    return conn, cur

main_cnxn, main_curs = create_connection('jobs.db')
main_curs.execute("select name from sqlite_master where type='table' and name = 'jobs'")
if 'jobs' in main_curs.fetchone():
    main_curs.execute('drop table jobs')
    main_cnxn.commit()
main_curs.execute('create table jobs (title nvarchar(120), yes_no bit)')
main_cnxn.commit()

for database_file in listdir('jobs/'):
    next_cnxn, next_curs = create_connection('jobs/' + database_file)
    next_curs.execute('select title from co_jobs')
    job_opportunities = next_curs.fetchall()
    for title in job_opportunities:
        insertion_cmd = f"insert into jobs(title, yes_no) values ('{title[0]}', '1')"
        main_curs.execute(insertion_cmd)
        main_cnxn.commit()
    print("Added data from", database_file)

nj_file = open('output_non_jobs.txt', mode='r', encoding='utf8')
for line in nj_file.readlines():
    n_job = line.strip()[0:120]
    if "'" in n_job:
        n_job = n_job.replace("'", "")
    insertion_cmd = f"insert into jobs(title, yes_no) values ('{n_job}', '0')"
    main_curs.execute(insertion_cmd)
    main_cnxn.commit()
print("Added data from NON JOBS")

main_curs.close()
main_cnxn.close()
