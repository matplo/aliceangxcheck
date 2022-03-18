#!/usr/bin/env python

from __future__ import print_function
import os
import argparse
import ROOT


def main():
	parser = argparse.ArgumentParser(description='ratio of contents of two files', prog=os.path.basename(__file__))
	parser.add_argument('-i1', '--input1', help='input file1 for file1/file2', default='', type=str, required=True)
	parser.add_argument('-i2', '--input2', help='input file2 for file1/file2', default='', type=str, required=True)
	parser.add_argument('-o', '--output', help='output for file1/file2', default='', type=str, required=True)
	args = parser.parse_args()

	fout = ROOT.TFile(args.output, 'recreate')
	fin1 = ROOT.TFile(args.input1)
	fin2 = ROOT.TFile(args.input2)
	skipped = []
	for k1 in fin1.GetListOfKeys():
		_hname = k1.GetName()
		h1 = fin1.Get(_hname)
		if h1.InheritsFrom('THn'):
			skipped.append(h1.GetName())
			continue
		if not h1.InheritsFrom('TH1'):
			skipped.append(h1.GetName())
			continue
		h2 = fin2.Get(_hname)
		fout.cd()
		hr = h1.Clone('{}_div_{}'.format(h1.GetName(), h2.GetName()))
		hr.SetTitle('{}_div_{}'.format(h1.GetName(), h2.GetName()))
		hr.Sumw2()
		hr.Divide(h2)
		hr.Write()
		grratio = ROOT.TGraphAsymmErrors(h1, h2, 'pois')
		grratio.SetTitle(h1.GetName()+'_ratio_gr')
		grratio.SetName(h1.GetName()+'_ratio_gr')
		grratio.Write()
	fout.Write()
	print('[w] skipped THns', skipped)


if __name__ == '__main__':
	main()
