#!/usr/bin/env python

import os
import astropy.io
from astropy.io import ascii

dir = '/Users/ploskon/tmp/angularities/fromJames/rivet-plots-10/ALICE_2021_I1891385'
fname = 'd01-x01-y01.dat'
dfname = os.path.join(dir, fname)

print('reading', dfname)
data = astropy.io.ascii.read(dfname)

print(data)
