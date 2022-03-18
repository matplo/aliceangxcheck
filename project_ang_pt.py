#!/usr/bin/env python

from __future__ import print_function
import ROOT
import argparse
import os


hlist = [
	'hAng_JetPt_tru_R0.2_1',
	'hAng_JetPt_tru_R0.2_1_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.2_1.5',
	'hAng_JetPt_tru_R0.2_1.5_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.2_2',
	'hAng_JetPt_tru_R0.2_2_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.2_3',
	'hAng_JetPt_tru_R0.2_3_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.4_1',
	'hAng_JetPt_tru_R0.4_1_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.4_1.5',
	'hAng_JetPt_tru_R0.4_1.5_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.4_2',
	'hAng_JetPt_tru_R0.4_2_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.4_3',
	'hAng_JetPt_tru_R0.4_3_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.6_1',
	'hAng_JetPt_tru_R0.6_1_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.6_1.5',
	'hAng_JetPt_tru_R0.6_1.5_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.6_2',
	'hAng_JetPt_tru_R0.6_2_SD_zcut02_B0',
	'hAng_JetPt_tru_R0.6_3',
	'hAng_JetPt_tru_R0.6_3_SD_zcut02_B0']

def main(args):

	with open(args.input) as f:
		file_list = [l.strip('\n') for l in f.readlines()]

	for fn in file_list:
		print(fn)

	outh_list = []

	ptbins = [ [20, 40], [40, 60], [60, 80], [80, 100] ]
	for ptbin in ptbins:
		for fn in file_list:
			fin = ROOT.TFile(fn)
			for hn in hlist:
				if 'R0.6' in hn:
					continue
				h = fin.Get(hn)
				if h:
					print('projecting', h)
					ib1 = h.GetXaxis().FindBin(ptbin[0])
					ib2 = h.GetXaxis().FindBin(ptbin[1])
					srctype = 'rmatrix'
					if 'herwig' in fn:
						srctype = 'hepmc'
						try:
							srctype_mod = fn.split('260023')[1].split('LHC')[0].replace('/', '_')
						except:
							srctype_mod = fn.split('herwig_newMP')[1].split('.root')[0].replace('/', '_')
					else:
						try:
							srctype_mod = fn.split('260023')[1].split('AnalysisResults')[0].replace('/', '_')
						except:
							srctype_mod = fn.split('fromEzra')[1].split('_framework')[0].replace('/', '_')
					if '_new_' in srctype_mod:
						srctype_mod = srctype_mod.replace('_new', '')
					if '_old_' in srctype_mod:
						srctype_mod = srctype_mod.replace('_old', '')
						continue
					pname = '{}_{}_{}_{}_{}'.format(srctype, srctype_mod, ptbin[0], ptbin[1], h.GetName())
					# hpj.SetName(pname)
					hpj = h.ProjectionY(pname, ib1, ib2)
					hpj.SetDirectory(0)
					outh_list.append(hpj)
					# get and project the histogram
					# save it in the output with some prefix - mp or el
					# break
				pass
			fin.Close()

	fout = ROOT.TFile(args.output, 'recreate')
	fout.cd()
	for h in outh_list:
		h.Write()
	fout.Close()
	print('[i] file written:', fout.GetName())


def compare(args):
	outh_list = []

	fin = ROOT.TFile(args.input)
	for k in fin.GetListOfKeys():
		_hname = k.GetName()
		if 'rmatrix' in _hname:
			hrm = fin.Get(_hname)
			_hname_mc = _hname.replace('rmatrix', 'hepmc')
			hmc = fin.Get(_hname_mc)
			if not hmc:
				#_hname_mc = _hname.replace('rmatrix', 'hepmc').replace('_old', '')
				_hname_mc = _hname.replace('rmatrix', 'hepmc').replace('_old', '')
			hmc = fin.Get(_hname_mc)
			if not hmc:
				print('[w] not found', _hname_mc)
				continue
			hrm.Divide(hmc)
			outh_list.append(hrm)
			hrm.SetDirectory(0)
	fin.Close()
	fout = ROOT.TFile(args.output, 'recreate')
	fout.cd()
	for hrm in outh_list:
		hrm.Write()
	fout.Close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='project histograms', prog=os.path.basename(__file__))
	parser.add_argument('-i', '--input', help='input file', default='h2d_list.txt', type=str)
	parser.add_argument('-o', '--output', help='output file', default='ang_projections.root', type=str)
	parser.add_argument('--compare', help='make the comparisons', action='store_true', default=False)
	args = parser.parse_args()	
	if args.compare:
		compare(args)
	else:
		main(args)
	
