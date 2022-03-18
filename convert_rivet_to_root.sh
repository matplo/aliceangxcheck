#!/bin/bash

files=$(find /Users/ploskon/tmp/angularities/fromJames/rivet-plots-10/ALICE_2021_I1891385 -name "*.dat")
files20=$(find /Users/ploskon/tmp/angularities/fromJames/rivet-plots-20/ALICE_2021_I1891385 -name "*.dat")
for fn in ${files} ${files20}
do
	if [ -e "${fn}.root" ] 
		then
			echo "[w] converted file exists ${fn}.root"
		else
			echo "[i] converting ${fn}"
			./convert_rivet_datfile.py -i $fn
	fi
done
