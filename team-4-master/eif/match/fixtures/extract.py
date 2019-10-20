import os
import json

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

students = {}
jobs = {}

with open(os.path.join(__location__, 'data.json')) as json_file:
    data = json.load(json_file)
    for p in data:
        print(p['fields'])
        if(p['model'] == 'match.StudentJob'):
            if not students or [p.pk] != None:
                students[p.pk][p['fields'].rank] = p['fields'].job
            else:
                students[p.pk] = [0,0,0,0,0]
                students[p.pk][p['fields'].rank] = p['fields'].job
        if(p['model'] == 'match.JobStudent'):
            if jobs[p.k] != None:
                jobs[p.pk][p['fields'].rank] = p['fields'].students
            else:
                jobs[p.pk][p['fields'].rank] = [0,0,0,0,0]
                jobs[p.pk][p['fields'].rank] = p['fields'].students
                

print(students)
print(jobs)
