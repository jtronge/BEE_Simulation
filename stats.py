"""Save a gantt chart of the simulation.

Save a gantt chart of the simulation.
"""
import csv
import matplotlib.pyplot as plt
import sys


with open('out/batsim_jobs.csv') as fp:
    reader = csv.DictReader(fp)
    jobs = [line for line in reader]

# TODO: This may not work with multiple scheduled jobs per node
resources = list(set(int(job['allocated_resources']) for job in jobs))
resources.sort()

workflow_start = min(float(job['starting_time']) for job in jobs)
total_time = max(float(job['finish_time']) for job in jobs) - workflow_start
print(workflow_start)
print(total_time)

fig, gnt = plt.subplots()

gnt.set_ylim(0.0, 50.0)
gnt.set_xlim(0.0, total_time)

gnt.set_title('BEE Scheduler Batsim Simulation (%s)'
              % (sys.argv[1] if len(sys.argv) > 1 else ''))
gnt.set_xlabel('Execution times')
gnt.set_ylabel('Nodes (resources)')

gnt.set_yticks([10 + i * 10 for i in range(len(resources))])
gnt.set_yticklabels([str(res) for res in resources])

gnt.grid(True)

# Set up a mapping from resources to job times
job_res = {res: [] for res in resources}
for job in jobs:
    # Zero the finish time
    starting_time = float(job['starting_time']) - workflow_start
    execution_time = float(job['execution_time'])
    job_res[int(job['allocated_resources'])].append((starting_time,
                                                     execution_time))

# Call broken_barh() to draw the jobs for each resource
for i, res in enumerate(sorted(job_res)):
    facecolors = ('blue', 'orange', 'red', 'green')
    gnt.broken_barh(job_res[res], (5 + i * 10, 9), facecolors=facecolors,
                    hatch='/', edgecolor='black')

plt.savefig('stats.png')
