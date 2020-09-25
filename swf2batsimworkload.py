"""Convert a SWF file to a Batsim workload file.

Convert a SWF file on stdin to a Batsim workload file on stdout (in json).
"""
import json
import sys


def main():
    nb_res = 1
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
            if line[1] == 'MaxNodes:':
                nb_res = int(line[2])
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

    # TODO: Need to cap the resource usage size here

    # Dump the workload
    data = {
        'nb_res': nb_res,
        'jobs': jobs,
        'profiles': profiles,
    }
    json.dump(data, fp=sys.stdout, indent=4)

if __name__ == '__main__':
    main()
