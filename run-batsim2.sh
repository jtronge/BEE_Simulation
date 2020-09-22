#!/bin/sh

ch-run batsim-img/oarteam.batsim-2020-09-14/ \
	-b .:/data \
	-c /data \
	/bin/batsim \
	-- \
	-p batsim/platforms/cluster512.xml \
	-w batsim/workloads/test_walltime.json \
	-e /data/out/batsim \
	--enable-compute-sharing
	# -p batsim/platforms/small_platform.xml \
	# -w batsim/workloads/test_one_computation_job.json \
