#!/usr/bin/env python

from __future__ import print_function
import ROOT

fname = 'ratios.root'
fname = 'new_ratios.root'

def print_preamb():
  with open('figure_preamb.txt') as f:
    lines = f.readlines()
    for l in lines:
      print(l.strip('\n').replace('ratios.root', fname))

def same_bins(s1, s2):
  if len(s1) < 1:
    return False
  if len(s2) < 1:
    return False
  return (s1.split('rmatrix__')[1].split('_hAng')[0] == s2.split('rmatrix__')[1].split('_hAng')[0])


fin = ROOT.TFile(fname)
hnames = []
for k in fin.GetListOfKeys():
  _hname = k.GetName()
  h = fin.Get(_hname)
  if h.GetEntries() > 250:
    hnames.append(_hname)

print(len(hnames))

last_hn = ''
for hn in hnames:
  if same_bins(hn, last_hn) is False:
    print_preamb()
  print('ratios.root : {} : p : title={}'.format(hn, hn))
  last_hn = hn
