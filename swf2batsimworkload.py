"""Convert a SWF file to a Batsim workload file.

Convert a SWF file on stdin to a Batsim workload file on stdout (in json).
Also filters the workload in order to prepare for a better simulation.
"""
import argparse
import json
import random
import sys


MAX_RESOURCES = 64
MAX_GROUP_COUNT = 32
MAX_TOTAL_TASKS = 1024

def parse_args():
    """Parse arguments and return them.

    Parse typical arguments and return them.
    """
    parser = argparse.ArgumentParser(
        description='Convert an SWF file to a Batsim workload file')
    parser.add_argument('-R', '--max-resources', type=int,
                        default=MAX_RESOURCES,
                        dest='max_resources',
                        help='max resources jobs can use')
    # We want to cap the total tasks to reduce simulation time
    parser.add_argument('-T', '--max-total-tasks', type=int,
                        dest='max_total_tasks', default=MAX_TOTAL_TASKS,
                        help='max number of tasks in entire workload')
    return parser.parse_args()

def main():
    args = parse_args()

    # nb_res = 1
    jobs = []
    profiles = {
        # This profile should work no matter the number of machines requested
        'default': {
            'type': 'parallel_homogeneous',
            'cpu': 6e6,
            'com': 1e6,
        },
    }

    # Parse the input
    for line in sys.stdin:
        line = line.split()
        try:
            # Get workload properties
            #if line[1] == 'MaxNodes:':
            #    nb_res = int(line[2])
            # Get jobs
            if line[0] != ';':
                # Set defaults on negative fields
                res = int(line[4])
                res = res if res > 0 else 1
                walltime = int(line[3])
                walltime = walltime if walltime > 0 else 1
                jobs.append({
                    'id': line[0],
                    # 'subtime': int(line[1]),
                    'subtime': 0,
                    'walltime': walltime,
                    # TODO: This may be taking the incorrect value for 'res'
                    # (it's labeled as 'number_of_allocated_processors' in
                    # Betis' code, and request_number_of_nodes is set to -1)
                    'res': res,
                    'profile': 'default',
                })
        except IndexError:
            continue

    # Remove jobs with too many resources
    jobs = [job for job in jobs if job['res'] <= args.max_resources]
    nb_res = args.max_resources

    # Remove extra jobs
    jobs = jobs[:args.max_total_tasks]

    # Dump the workload
    data = {
        'nb_res': nb_res,
        'jobs': jobs,
        'profiles': profiles,
    }
    json.dump(data, fp=sys.stdout, indent=4)

if __name__ == '__main__':
    main()
