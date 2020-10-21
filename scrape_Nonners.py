# Anmol Kapoor

with open('non_jobs.txt', mode='r', encoding='utf8') as file:
    content = file.readlines()

non_jobs = []
for cont in content:
    if cont.strip() != '' and cont not in non_jobs:
        non_jobs.append(cont.strip())
x = ''
for i in non_jobs: x += i + '\n'

