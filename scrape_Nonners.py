# Anmol Kapoor

with open('non_jobs.txt', mode='r', encoding='utf8') as file:
    content = file.readlines()

non_jobs = []
for line in content:
    if line.strip() != '' and line.strip() not in non_jobs:
        non_jobs.append(line.strip())
x = ''
for i in non_jobs: x += i + '\n'

o_file = open("output_non_jobs.txt", mode="w", encoding='utf8')
o_file.write(x)
o_file.close()
