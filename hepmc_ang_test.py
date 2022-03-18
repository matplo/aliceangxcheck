#!/usr/bin/env python

from __future__ import print_function

import fastjet as fj
import fjcontrib
import fjext

import tqdm
import argparse
import os
import sys
import numpy as np
from array import array 

import pyhepmc_ng
import ROOT
import math

# handy link https://arxiv.org/abs/2107.11303v1


def logbins(xmin, xmax, nbins):
        lspace = np.logspace(np.log10(xmin), np.log10(xmax), nbins+1)
        arr = array('f', lspace)
        return arr


def find_jets_hepmc(jet_def, jet_selector, hepmc_event):
	fjparts = []
	for i,p in enumerate(hepmc_event.particles):
		if p.status == 1 and not p.end_vertex:
			psj = fj.PseudoJet(p.momentum.px, p.momentum.py, p.momentum.pz, p.momentum.e)
			# psj.set_user_index(i)
			fjparts.append(psj)
	jets = jet_selector(jet_def(fjparts))
	return jets


pdg = ROOT.TDatabasePDG()
def is_charged(p):
	return (pdg.GetParticle(p.pid).Charge() != 0)


pion_mass = 0.13957039
def find_charged_jets_hepmc_pion_mass(jet_def, jet_selector, hepmc_event):
	fjparts = []
	for i, p in enumerate(hepmc_event.particles):
		if p.status == 1 and not p.end_vertex and is_charged(p):
			psj = fj.PseudoJet(p.momentum.px, p.momentum.py,
			                   p.momentum.pz, p.momentum.e)
			psj.reset_PtYPhiM(psj.perp(), psj.rap(), psj.phi(), pion_mass)
			# psj.set_user_index(i)
			fjparts.append(psj)
	jets = jet_selector(jet_def(fjparts))
	return jets

class HistogramStorage(object):
	def __init__(self, version='new'):
		self.hists = { 0: { 0: { -1 : 'object'} } }
		self.version = version
  
	def get(self, R, alpha, sd):
		hret = None
		try:
			hret = self.hists[R][alpha][sd]
		except:
			hname_new = 'h_ang_JetPt_Truth_R{}_{}'.format(R, alpha)
			hname_old = 'hAng_JetPt_tru_R{}_{}'.format(R, alpha)
			hname = None
			if self.version == 'new':
				hname = hname_new
			if self.version == 'old':
				hname = hname_old
			if sd > 0:
				hname += '_SD_zcut02_B0'
			try:
				_d = self.hists[R]
			except:
				self.hists[R] = {}
			try:
				_d = self.hists[R][alpha]
			except:
				self.hists[R][alpha] = {}

			if self.version == 'new':
				self.hists[R][alpha][sd] = ROOT.TH2F(hname, hname, 200, array('d', [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0, 120.0, 121.0, 122.0, 123.0, 124.0, 125.0, 126.0, 127.0, 128.0, 129.0, 130.0, 131.0, 132.0, 133.0, 134.0, 135.0, 136.0, 137.0, 138.0, 139.0, 140.0, 141.0, 142.0, 143.0, 144.0, 145.0, 146.0, 147.0, 148.0, 149.0, 150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0, 160.0, 161.0, 162.0, 163.0, 164.0, 165.0, 166.0, 167.0, 168.0, 169.0, 170.0, 171.0, 172.0, 173.0, 174.0, 175.0, 176.0, 177.0, 178.0, 179.0, 180.0, 181.0, 182.0, 183.0, 184.0, 185.0, 186.0, 187.0, 188.0, 189.0, 190.0, 191.0, 192.0, 193.0, 194.0, 195.0, 196.0, 197.0, 198.0, 199.0, 200.0]), 98, array('d', [0.0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.015000000000000001, 0.020000000000000004, 0.025, 0.030000000000000006, 0.035, 0.04000000000000001, 0.045000000000000005, 0.05000000000000001, 0.055000000000000014, 0.06000000000000001, 0.065, 0.07, 0.07500000000000001, 0.08, 0.085, 0.09000000000000001, 0.09500000000000001, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.16999999999999998, 0.18, 0.19, 0.2, 0.21000000000000002, 0.22, 0.22999999999999998, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.39999999999999997, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.5700000000000001, 0.5800000000000001, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8]))
			if self.version == 'old':
				self.hists[R][alpha][sd] = ROOT.TH2F(hname, hname, 195 , 5.0 , 200.0 , 160 , 0.0 , 0.8)
			hret = self.hists[R][alpha][sd]
			print('[i] creating {} histogram for R={} alpha={} SD={}'.format(hret.GetName(), R, alpha, sd))
		return hret


def main():
	parser = argparse.ArgumentParser(description='hepmc analysis - angularities', prog=os.path.basename(__file__))
	parser.add_argument('-i', '--input', help='input file', default='low', type=str, required=True)
	parser.add_argument('-o', '--output', help='output file', default='out.root', type=str, required=True)
	parser.add_argument('--hepmc', help='what format 2 or 3', default=2, type=int)
	parser.add_argument('--nev', help='number of events', default=10, type=int)
	args = parser.parse_args()	

	###
	# now lets read the HEPMC file and do some jet finding
	if args.hepmc == 3:
		input_hepmc = pyhepmc_ng.ReaderAscii(args.input)
	if args.hepmc == 2:
		input_hepmc = pyhepmc_ng.ReaderAsciiHepMC2(args.input)

	if input_hepmc.failed():
		print ("[error] unable to read from {}".format(args.input))
		sys.exit(1)

	# jet finder
	# print the banner first
	fj.ClusterSequence.print_banner()
	print()
	jet_R0s = [0.2, 0.4, 0.6]
	jet_defs = {}
	jet_selectors = {}
	for _R in jet_R0s:
		jet_defs[_R] = fj.JetDefinition(fj.antikt_algorithm, _R)
		jet_selectors[_R] = fj.SelectorPtMin(10.0) & fj.SelectorPtMax(500.0) & fj.SelectorAbsEtaMax(0.9 - _R)

	alphas = [1, 1.5, 2, 3]
	sds = [0, 1]

	fout = ROOT.TFile(args.output, 'recreate')
	fout.cd()
	hs_old = HistogramStorage('old')
	hs_new = HistogramStorage('new')
	for R in jet_R0s:
		for a in alphas:
			for sd in sds:
				h = hs_new.get(R, a, sd)
				h = hs_old.get(R, a, sd)

	kappa = 1.

	event_hepmc = pyhepmc_ng.GenEvent()
	pbar = tqdm.tqdm(range(args.nev))
	while not input_hepmc.failed():
		ev = input_hepmc.read_event(event_hepmc)
		if input_hepmc.failed():
			break
		for R in jet_R0s:
			# jets_hepmc = find_jets_hepmc(jet_defs[R], jet_selectors[R], event_hepmc)
			jets_hepmc = find_charged_jets_hepmc_pion_mass(jet_defs[R], jet_selectors[R], event_hepmc)
			for a in alphas:
				for sd in sds:
					for j in jets_hepmc:
						h_old = hs_old.get(R, a, sd)
						h_new = hs_new.get(R, a, sd)
						if sd > 0:
							gshop = fjcontrib.GroomerShop(j, 1.0, fj.cambridge_aachen_algorithm)
							j_sd_gshop = gshop.soft_drop(0, 0.2, 1.0)
							l = fjext.lambda_beta_kappa(j, j_sd_gshop.pair(), a, kappa, R)
							h_old.Fill(j_sd_gshop.pair().perp(), l)
							h_new.Fill(j_sd_gshop.pair().perp(), l)
						else:
							l = fjext.lambda_beta_kappa(j, a, kappa, R)
							h_old.Fill(j.perp(), l)
							h_new.Fill(j.perp(), l)

		pbar.update()
		if pbar.n >= args.nev:
			break

	pbar.close()

	fout.Write()
	fout.Close()
	print('[i] file written:', fout.GetName())
	return 

if __name__ == '__main__':
	main()
