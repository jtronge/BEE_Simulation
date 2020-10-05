"""Generate a random workflow.

Generate a random workflow with a set of tasks that can be run.
"""
import json
import random
import sys


nb_res = random.randint(1, 32)
task_group_cnt = random.randint(1, 20)
task_cnt = random.randint(1, 20)

jobs = []
subtime = 0
for i in range(task_group_cnt):
    task_group = []
    usage_total = []
    for j in range(random.randint(1, task_cnt)):
        walltime = random.randint(1, 1000)
        res = random.randint(1, nb_res)
        jobs.append({
            'id': '%i-%i' % (i, j),
            'subtime': subtime,
            'walltime': walltime,
            'res': res,
            'profile': 'default',
        })
        usage_total.append((res, walltime))
    # TODO: Change the subtime here
    total_walltime = sum((res / nb_res) * walltime
                         for res, walltime in usage_total)
    max_walltime = max(walltime for res, walltime in usage_total)
    total_walltime = (total_walltime if total_walltime > max_walltime
                      else max_walltime)
    subtime += total_walltime + 40

data = {
    'nb_res': nb_res,
    'jobs': jobs,
    'profiles': {
        'default': {
            'type': 'parallel_homogeneous',
            'cpu': 6e6,
            'com': 1e6,
        },
    },
}
json.dump(data, fp=sys.stdout, indent=4)
