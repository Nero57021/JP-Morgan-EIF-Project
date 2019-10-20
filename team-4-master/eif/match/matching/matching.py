import networkx as nx
from networkx.algorithms import bipartite
from math import inf
from itertools import chain
from heapq import nsmallest

# match the students with jobs
def match(jobs, students, interview_limit):
  B = make_graph(jobs, students)
  return get_matches(B, jobs.keys(), interview_limit)

# create a biparte graph with the student, jobs, and the weight between each node
def make_graph(jobs, students):
  B = nx.Graph()
  B.add_nodes_from(jobs.keys(), bipartite=0)
  B.add_nodes_from(students.keys(), bipartite=1)
  B.add_weighted_edges_from( compute_weights(jobs, students) )
  return B

# find the weight between each student and jobs
def compute_weights(jobs, students):
  weights = []
  func = lambda job, student: get_distance(job, student[1], student[0], students)
  for job in jobs:
    job_weights = list(map(lambda s: func(job, s), enumerate(jobs[job])))
    weights.append(job_weights)

  return list(chain.from_iterable(weights))

# find the weight by getting the absolute value of the difference of the indices
def get_distance(job_id, student_id, rank, students):
  try:
    job_rank = students[student_id].index(job_id)
  except ValueError:
    job_rank = inf

  return (job_id, student_id, abs(rank - job_rank - 1))

# return the matches running a minheap to fill the additional positions
def get_matches(graph, jobs, interview_max):
  matches = {}
  for job in jobs:
    match = nsmallest(interview_max, graph[job].items(), key=lambda w: w[1]['weight'])
    cleaned = list(map(lambda m: m[0], match))
    matches[job] = cleaned

  return matches