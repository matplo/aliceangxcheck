#!/usr/bin/env python

from __future__ import print_function
import ROOT
import argparse
import os

import dlist

def main(args):
	tc = ROOT.TCanvas('tc', 'tc') 
	dlists = []
	print('[i] processing file:', args.input)
	fin = ROOT.TFile(args.input)
	hlist = fin.GetListOfKeys()
	hprocessed = []
	for hn in hlist:
		hname = hn.GetName()
		if hname in hprocessed:
			continue
		hprocessed.append(hname)
		if 'hepmc' not in hname:
			continue
		h = fin.Get(hname)
		h.Scale(1./h.Integral())
		h.Sumw2()
		if h:
			hrmold = fin.Get(hname.replace('hepmc', 'rmatrix_old'))
			hrmold.Sumw2()
			hrmold.Scale(1./hrmold.Integral())
			hrmnew = fin.Get(hname.replace('hepmc', 'rmatrix_new'))
			hrmnew.Sumw2()
			hrmnew.Scale(1./hrmnew.Integral()/2.)
			print(h, hrmold, hrmnew)
			if hrmold and hrmnew:
				hl = dlist.dlist(h.GetName())
				hl.add(h, 'herwig mp', 'hist +l1 +k1 +f1001 +a20')
				hl.add(hrmold, 'rmatrix old', 'hist +l1 +k2 +f3350 +a50')
				hl.add(hrmnew, 'rmatrix new / 2.', 'hist +l1 +k4 +f3359 +a50')
				dlists.append(hl)

				hl1 = dlist.dlist(h.GetName())
				hl1.add(h, 'herwig mp', 'hist +k1')
				hl1.add(hrmold, 'rmatrix old', 'hist +k2')
				hlr = hl1.ratio_to(0, 'p +k9')
				# hlr = hl.ratio_to_href(h, 'p +k9')
				dlists.append(hlr)

		if len(dlists) > 1000:
			break

	for ifig, hl in enumerate(dlists):
		print('[i] drawing', hl.name)
		tc.cd()
		hl.tcanvas = tc
		if 'ratio' in hl.name:
			hl.draw('', 0, 5)
		else:
			hl.draw('', 0, 0.05)
		hl.self_legend(title=hl.name)
		foutname = args.output
		if ifig == 0:
			foutname = args.output + '('
		if ifig == len(dlists) - 1:
			foutname = args.output + ')'    
		hl.tcanvas.Print(foutname, 'pdf')
	
	fin.Close()  

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='project histograms', prog=os.path.basename(__file__))
	parser.add_argument('-i', '--input', help='input file',
											default='ang_projections.root', type=str)
	parser.add_argument('-o', '--output', help='output file',
											default='ang_projections.root.pdf', type=str)
	args = parser.parse_args()
	main(args)
