#!/usr/bin/env python3

import ROOT
import argparse
import os
import sys
from array import array

def bins_same_size(h, axis=0):
	bw = None
	if axis == 0:
		tax = h.GetXaxis()
	if axis == 1:
		tax = h.GetYaxis()
	if axis == 2:
		tax = h.GetZaxis()
	for ib in range(1, tax.GetNbins()+1):
		_bw = tax.GetBinWidth(ib)
		if bw is None:
			bw = _bw
			continue
		if bw != _bw:
			return False
		bw = _bw
	return True


def list_histograms(fname, match_hist):
	fin = ROOT.TFile(fname)

	skipped = []
	for k in fin.GetListOfKeys():
		_hname = k.GetName()
		if match_hist in _hname or match_hist == '':
			# print(_hname)
			h = fin.Get(_hname)
			if h.InheritsFrom("THn"):
				skipped.append(h.GetName())
				continue
			bin_same_size = bins_same_size(h, 0) and bins_same_size(h, 1) and bins_same_size(h, 2)
			if bin_same_size is True:
				print('h=ROOT.TH2F("'+h.GetName()+'",', '"'+h.GetTitle()+'",', 
							h.GetNbinsX(), ',', h.GetXaxis().GetXmin(), ',', h.GetXaxis().GetXmax(), ',',
							h.GetNbinsY(), ',', h.GetYaxis().GetXmin(), ',', h.GetYaxis().GetXmax(), ')')
			else:
				low_edgesX = array('d', [0. for _ in range(h.GetNbinsX() + 1)])
				low_edgesX[-1] = h.GetXaxis().GetXmax()
				h.GetXaxis().GetLowEdge(low_edgesX)
				# print ('X axis:', h.GetXaxis().GetNbins(), len(low_edgesX), h.GetXaxis().GetXmax(), low_edgesX[-1])
				low_edgesY = array('d', [0. for _ in range(h.GetNbinsY() + 1)])
				low_edgesY[-1] = h.GetYaxis().GetXmax()
				h.GetYaxis().GetLowEdge(low_edgesY)
				# print ('Y axis:', h.GetYaxis().GetNbins(), len(low_edgesY), h.GetYaxis().GetXmax(), low_edgesY[-1])
				print('h=ROOT.TH2F("'+h.GetName()+'",', '"'+h.GetTitle()+'",',
          h.GetNbinsX(), ',', low_edgesX, ',',
          h.GetNbinsY(), ',', low_edgesY)

	print('[w] skipped THns', skipped)

def main():
	parser = argparse.ArgumentParser(description='hepmc analysis - angularities', prog=os.path.basename(__file__))
	parser.add_argument('-i', '--input', help='input file', default='', type=str, required=True)
	parser.add_argument(
		'-n', '--hname', help='histogram name pattern (e.g., h_ang_JetPt_Truth_R0. or hAng_JetPt_tru_R0.', default='', type=str)
	args = parser.parse_args()

	# fname = "/Users/ploskon/tmp/angularities/fromEzra/10_124_new_framework.root"
	fname = args.input
	if os.path.exists(fname):
		list_histograms(fname, args.hname)
	else:
		print('[e] input file not found', file=sys.stderr)


if __name__ == '__main__':
	main()
