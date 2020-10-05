#!/bin/sh

ch-run batsim-img/oarteam.batsim-2020-09-14/ \
	-b .:/data \
	-c /data \
	/bin/batsim \
	-- \
	-p platforms/cluster512.xml \
	-w ANL-Intrepid-2009-1-small.json \
	-e /data/out/batsim \
	--enable-compute-sharing
	# -p platforms/cluster16.xml \
	# -w SDSC-SP2-1998-4.2-cln.json \
	# -w synthetic_small-test-workload-3.json \
	# -w synthetic_small-test-workload.json \
	# -p batsim/platforms/cluster512.xml \
	# -p batsim/platforms/small_platform.xml \
	# -w HPC2N-test-workload.json \
	# -p batsim/platforms/cluster_locality_8x16.xml \
	# -p batsim/platforms/cluster512.xml \
	# --enable-compute-sharing
	# -w HPC2N-2002-2.2-cln.json \
	# -w ANL-Intrepid-2009-1-workload.json \
	# -w synthetic_small-workload.json \
	# -w ANL-Intrepid-2009-1-workload.json \
	# -w batsim/workloads/test_walltime.json \
	# -p new.xml \
	# -p ns3-big-cluster.xml \
	# -p batsim/platforms/cluster_locality_8x64.xml \
	# -w batsim/workloads/test_one_computation_job.json \
	# -m algol \
