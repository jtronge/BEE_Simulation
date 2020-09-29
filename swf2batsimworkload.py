"""Convert a SWF file to a Batsim workload file.

Convert a SWF file on stdin to a Batsim workload file on stdout (in json).
"""
import argparse
import json
import random
import sys


MAX_RESOURCES = 64
MAX_GROUP_COUNT = 512

def parse_args():
    """Parse arguments and return them.

    Parse typical arguments and return them.
    """
    parser = argparse.ArgumentParser(
        description='Convert an SWF file to a Batsim workload file')
    parser.add_argument('-R', '--max-resources', type=int,
                        default=MAX_RESOURCES,
                        name='max_resources',
                        help='max resources jobs can use')
    parser.add_argument('-g', '--group-count', type=int, name='group_count',
                        default=MAX_GROUP_COUNT,
                        help=('max number of jobs in a "group" of jobs that '
                              'will start at the same time'))
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
                res = int(line[4])
                jobs.append({
                    'id': line[0],
                    'subtime': int(line[1]),
                    'walltime': int(line[3]),
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

    # TODO: Need to cap the resource usage size here - this may affect how the
    # jobs are later grouped and their subtimes as well

    # Convert list of jobs into a more useful workflow
    # TODO: Will need to play with this some more

    # Sort jobs into groups that will have the same 'subtime'. This will make
    # for a better workflow.
    # TODO: Perhaps use a 'next_subtime' estimate based on resource usage of group
    jobs.sort(key=lambda job: job['subtime'])
    groups = []
    new_jobs = []
    prev_subtime = 0
    prev_walltime = 0
    while jobs:
        cnt = random.randint(1, min(len(jobs), args.group_count))
        group = [jobs.pop(0) for i in range(cnt)]
        subtime = prev_subtime + prev_walltime
        group_walltime = 0
        for job in group:
            job['subtime'] = subtime
            group_walltime = max(group_walltime, job['walltime'])
        prev_subtime = subtime
        prev_walltime = group_walltime
        groups.append(group)
        new_jobs.extend(group)
    jobs = new_jobs

    # Dump the workload
    data = {
        'nb_res': nb_res,
        'jobs': jobs,
        'profiles': profiles,
    }
    json.dump(data, fp=sys.stdout, indent=4)

if __name__ == '__main__':
    main()
