#!/usr/bin/env python

from __future__ import print_function

import sys

def main():
	if len(sys.argv) < 2:
		return

	lines = []
	with open('map_rivet_to_analysis.txt', 'r') as f:
		lines = f.readlines()

	ld = {}
	for l in lines:
		fname = '{}.dat'.format(l.split()[0])
		ld[fname] = l.split()[1]

	try:
		print(ld[sys.argv[1]])
	except:
		print('')

if __name__ == '__main__':
	main()
 
 
