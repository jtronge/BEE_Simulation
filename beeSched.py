"""BEE Scheduler Batsim interface.

BEE Scheduler Batsim interface.
"""
import batsim.batsim as batsim
import json
import os
import procset
import requests
import subprocess
import time


PORT = 5200
JOB_CNT = 32
DEFAULT_MAX_RUNTIME = 128

class BeeSched(batsim.BatsimScheduler):
    """BEE Scheduler Interface class.

    Class interfacing with the BEE Scheduler and Batsim.
    """

    def __init__(self, *pargs, **kwargs):
        """BeeSched constructor.

        BeeSched constructor.
        """
        super().__init__(*pargs, **kwargs)
        # Needed for onNoMoreEvents
        self.submitted_jobs = []

    def onAfterBatsimInit(self):
        """Run after construction.

        Run after construction.
        """
        print('onAfterBatsimInit()')
        # self.submitted_jobs = []
        self.machines = [i for i in range(self.bs.nb_resources)]
        with open('resources.txt', 'w') as fp:
            print(self.machines, file=fp)

    def onSimulationBegins(self):
        """Simulation start.

        Simulation start.
        """
        os.chdir('BEE_Private/')
        self.proc = subprocess.Popen([
            'python', 'beeflow/scheduler/scheduler.py',
            '-p', str(PORT),
            '--no-config',
            # '--algorithm', 'sjf',
            '--algorithm', 'backfill',
            # '--use-mars',
            # '--mars-model', 'model/',
        ], shell=False)
        time.sleep(3)
        self.url = 'http://localhost:%s/bee_sched/v1' % PORT

    def onSimulationEnds(self):
        """Simulation end.

        Simulation end.
        """
        self.proc.terminate()

    def onJobSubmission(self, job):
        """Job submission.

        Job submission.
        """
        print('onJobSubmission()')
        print(job.job_state)
        self.submitted_jobs.append(job)
        if len(self.submitted_jobs) >= JOB_CNT:
            print('Scheduling...')
            self.schedule()

    def onJobCompletion(self, job):
        """Job completion.

        Job completion.
        """
        print('onJobCompletion()')

    def onNoMoreJobsInWorkloads(self):
        """No more jobs are ready to be scheduled.

        This is a NOTIFY sent by Batsim saying that there are no more jobs left
        to send over.
        """
        # Schedule jobs if any are submitted
        if self.submitted_jobs:
            self.schedule()

    def schedule(self):
        """Schedule submitted jobs.

        Schedule submitted jobs.
        """
        # TODO: Do the actual scheduling here
        ready = []
        rejects = []
        # Send resource list here
        resources = [{'id_': str(i), 'nodes': 1}
                     for i in range(len(self.machines))]

        with open('test_resources.json', 'w') as fp:
            json.dump(resources, fp=fp)

        r = requests.put(f'{self.url}/resources', json=resources)

        assert r.ok
        assert r.json() == ('created %i resource(s)' % len(resources))

        # Collect and schedule jobs here
        workflow_name = 'workflow'
        # TODO: Handle correct 'max_runtime' value
        tasks = [
            {
                'workflow_name': workflow_name,
                'task_name': str(i),
                'requirements': {
                    # 'max_runtime': (job.requested_time
                    #                 if job.requested_time > 0 else 1),
                    'max_runtime': (job.requested_time
                                    if job.requested_time > 0
                                    else DEFAULT_MAX_RUNTIME),
                    'nodes': job.requested_resources,
                },
            }
            for i, job in enumerate(self.submitted_jobs)
            if job.job_state == batsim.Job.State.SUBMITTED
        ]
        r = requests.put(f'{self.url}/workflows/{workflow_name}/jobs',
                         json=tasks)
        assert r.ok
        data = r.json()

        # Sort the task data by start_time
        data.sort(key=lambda task: task['allocations'][0]['start_time']
                                    if task['allocations'] else 0)

        last_time = 0
        # TODO: This loop may need to be redesigned in order to work effectively
        # with the scheduler
        for task in data:
            i = int(task['task_name'])
            job = self.submitted_jobs[i]
            if task['allocations']:
                # Set the allocation properly
                # TODO: This only works for single allocations
                alloc = [self.machines[int(alloc['id_'])] for alloc in task['allocations']]
                with open('alloc.txt', 'w') as fp:
                    print(alloc, file=fp)
                # Allocations must be sorted
                alloc.sort()
                job.allocation = procset.ProcSet(*alloc)
                # Schedule tasks that need to run
                start_time = int(task['allocations'][0]['start_time'])

                task_map = [(i, job.id) for i, job in enumerate(self.submitted_jobs)]
                with open('task_map.json', 'w') as fp:
                    json.dump(task_map, fp=fp, indent=4)
                with open('tasks.json', 'w') as fp:
                    json.dump(data, fp=fp, indent=4)
                with open('resources.json', 'w') as fp:
                    json.dump(resources, fp=fp, indent=4)

                if last_time != start_time and ready:
                    self.bs.execute_jobs(ready)
                    ready.clear()
                time = start_time - last_time
                if time > 0:
                    # Add 0.01 to avoid overlap
                    self.bs.consume_time(time + 0.01)
                last_time = start_time
                ready.append(job)
            else:
                rejects.append(job)
        if rejects:
            self.bs.reject_jobs(rejects)
        if ready:
            #start_time = (int(data[-1]['allocations'][0]['start_time'])
            #              if data[-1]['allocations'] else last_time)
            #time = start_time - last_time
            if time > 0:
                self.bs.consume_time(time)
            self.bs.execute_jobs(ready)
            ready.clear()

        # Clear old jobs
        self.submitted_jobs.clear()
