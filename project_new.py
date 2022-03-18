#!/usr/bin/env python

from __future__ import print_function
import ROOT
import argparse
import os


def main(args):

	with open(args.input) as f:
		file_list = [l.strip('\n') for l in f.readlines()]

	# for fn in file_list:
	# 	print(fn)

	outh_list = []

	ptbins = [[20, 40], [40, 60], [60, 80], [80, 100]]
	for fn in file_list:
		print('processing file:', fn)
		for ptbin in ptbins:
			fin = ROOT.TFile(fn)
			hlist = fin.GetListOfKeys()
			for hn in hlist:
				if 'R0.6' in hn:
					continue
				if ('hAng_JetPt_tru_' not in hn.GetName()) and ('h_ang_JetPt_Truth_' not in hn.GetName()):
					continue
				print (fn, hn.GetName())
				h = fin.Get(hn.GetName())
				if h:
					# print('projecting', h.GetName())
					ib1 = h.GetXaxis().FindBin(ptbin[0])
					ib2 = h.GetXaxis().FindBin(ptbin[1])
					srctype = 'rmatrix_'
					if 'herwig_' in fn:
						srctype = 'hepmc_'
					srctype += os.path.basename(fn).replace('.root', '').replace('new_','').replace('old_', '').replace('framework', '')
					if '_Truth_' in h.GetName():
						srctype += 'new'
					else:
						srctype += 'old'
					pname = '{}_{}_{}_{}'.format(srctype, ptbin[0], ptbin[1], h.GetName())
					# pname = pname.replace('h_ang_JetPt_Truth_', 'hAng_JetPt_tru_')
					pname = pname.replace('h_ang_JetPt_Truth_', '')
					pname = pname.replace('hAng_JetPt_tru_', '')
					print(h.GetName(), '->', pname)
					hpj = h.ProjectionY(pname, ib1, ib2)
					hpj.SetName(pname)
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
  return


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='project histograms', prog=os.path.basename(__file__))
	parser.add_argument('-i', '--input', help='input file',
	                    default='h2d_new_list.txt', type=str)
	parser.add_argument('-o', '--output', help='output file',
	                    default='ang_projections.root', type=str)
	parser.add_argument('--compare', help='make the comparisons',
	                    action='store_true', default=False)
	args = parser.parse_args()
	if args.compare:
		compare(args)
	else:
		main(args)
