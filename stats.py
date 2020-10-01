"""Save a gantt chart of the simulation.

Save a gantt chart of the simulation.
"""
import csv
import matplotlib.pyplot as plt
import sys


# Limit the size of the schedule
MAX_RESOURCES = 16
MAX_TIME = 1200000

with open('out/batsim_jobs.csv') as fp:
    reader = csv.DictReader(fp)
    jobs = [line for line in reader]

jobs = [job for job in jobs if job['final_state'] == 'COMPLETED_SUCCESSFULLY']

# TODO: This may not work with multiple scheduled jobs per node
resources = []
first_time = min(float(job['starting_time']) for job in jobs)
for job in jobs:
    allocs = job['allocated_resources'].split()
    allocs = [alloc.split('-') for alloc in allocs]
    allocs = [(int(alloc[0]), int(alloc[1]) + 1) if len(alloc) > 1
              else (int(alloc[0]), int(alloc[0]) + 1) for alloc in allocs]
    job['allocated_resources'] = allocs
    resources.extend(i for alloc in allocs for i in range(*alloc))
    # Normalize the times
    job['starting_time'] = float(job['starting_time']) - first_time

resources = list(set(resources))
resources.sort()
resources = resources[:MAX_RESOURCES]

# workflow_start = min(float(job['starting_time']) for job in jobs)
# total_time = max(float(job['finish_time']) for job in jobs) - workflow_start
total_time = max(float(job['finish_time']) for job in jobs) - first_time
total_time = MAX_TIME if total_time > MAX_TIME else total_time

fig, gnt = plt.subplots()

gnt.set_ylim(0.0, 50.0)
gnt.set_xlim(0.0, total_time)

gnt.set_title('BEE Scheduler Batsim Simulation %s'
              % (f'({sys.argv[1]})' if len(sys.argv) > 1 else ''))
gnt.set_xlabel('Execution times')
gnt.set_ylabel('Nodes (resources)')

gnt.set_yticks([10 + i * 10 for i in range(len(resources))])
gnt.set_yticklabels([str(res) for res in resources])

gnt.grid(True)

# Set up a mapping from resources to job times
job_res = {res: [] for res in resources}
for job in jobs:
    if job['starting_time'] > MAX_TIME:
        continue
    starting_time = job['starting_time']
    execution_time = float(job['execution_time'])
    requested_time = float(job['requested_time'])
    for alloc in job['allocated_resources']:
        if alloc[1] > MAX_RESOURCES:
            # break
            alloc = (alloc[0], MAX_RESOURCES)
        for i in range(*alloc):
            print('starting_time', starting_time)
            # job_res[i].append((starting_time, execution_time))
            job_res[i].append((starting_time, requested_time))

# Call broken_barh() to draw the jobs for each resource
for i, res in enumerate(sorted(job_res)):
    facecolors = ('blue', 'orange', 'red', 'green')
    gnt.broken_barh(job_res[res], (5 + i * 10, 9), facecolors=facecolors,
                    hatch='/', edgecolor='black')

plt.savefig('stats.png')
