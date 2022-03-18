#!/bin/bash

# test_file="/data/alice/ang/rstorage/generators/herwig_alice/hepmc/260023/20/78/LHC_5020_MPI-S617111.hepmc"
# echo "[i] counting events..."
# nev=$(grep "N " ${test_file} | wc -l)
# ./hepmc_ang_test.py -i ${test_file} -o test.root --nev ${nev} $@

#_files=$(cat ros_files_rivet.txt)
_files=$(cat test2_ros_files_rivet.txt)
for test_file in ${_files}
do
	echo "[i] counting events in ${test_file} ..."
	nev=$(grep "N " ${test_file} | wc -l)
	./hepmc_ang_test.py -i ${test_file} -o "${test_file}_hout.root" --nev ${nev} $@
done
