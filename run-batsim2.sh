#!/bin/sh

ch-run batsim-img/oarteam.batsim-2020-09-14/ \
	-b .:/data \
	-c /data \
	/bin/batsim \
	-- \
	-p batsim/platforms/cluster512.xml \
	-w synthetic_small-workload.json \
	-e /data/out/batsim \
	--enable-compute-sharing
	# -w ANL-Intrepid-2009-1-workload.json \
	# -w batsim/workloads/test_walltime.json \
	# -p new.xml \
	# -p ns3-big-cluster.xml \
	# -p batsim/platforms/cluster_locality_8x64.xml \
	# -p batsim/platforms/small_platform.xml \
	# -w batsim/workloads/test_one_computation_job.json \
	# -m algol \
