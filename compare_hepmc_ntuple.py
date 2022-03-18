from pyjetty.mputils import data_io as dio
import ROOT
import pyhepmc_ng
import fastjet as fj
import numpy as np
from array import array 


def logbins(xmin, xmax, nbins):
        lspace = np.logspace(np.log10(xmin), np.log10(xmax), nbins+1)
        arr = array('f', lspace)
        return arr


def get_particles_ntuple_file(fname):
	_fn = '/data/alice/ang/{}'.format(fname)
	print('[i] file', _fn)
	datafile = dio.DataFileIO(file_input=_fn, tree_name='tree_Particle_gen')
	print('[i] number of events:', len(datafile.df_events))
	for d in datafile.df_events:
		#print('n parts=', len(d.particles))
		yield d.particles


pdg = ROOT.TDatabasePDG()
def is_charged(p):
	return (pdg.GetParticle(p.pid).Charge() != 0)


pion_mass = 0.13957039
def get_particles_hepmc_file(fname, mass=-1):
	print('[i] file', fname)
	input_hepmc = pyhepmc_ng.ReaderAsciiHepMC2(fname)
	if input_hepmc.failed():
		print ("[error] unable to read from {}".format(args.input))
		sys.exit(1)
	hepmc_event = pyhepmc_ng.GenEvent()
	while not input_hepmc.failed():
		fjparts = []
		ev = input_hepmc.read_event(hepmc_event)
		if not input_hepmc.failed():	
			for i, p in enumerate(hepmc_event.particles):
				if p.status == 1 and not p.end_vertex and is_charged(p):
					psj = fj.PseudoJet(p.momentum.px, p.momentum.py,
														p.momentum.pz, p.momentum.e)
					if mass >= 0:
						psj.reset_PtYPhiM(psj.perp(), psj.rap(), psj.phi(), mass)
					# psj.set_user_index(i)
					fjparts.append(psj)
			yield fjparts

files_ntuples = [	'/rstorage/generators/herwig_alice/tree_gen/265216/260023/10/124/AnalysisResultsGen.root',
									'/rstorage/generators/herwig_alice/tree_gen/265216/260023/20/78/AnalysisResultsGen.root']

files_hepmc = [	'/data/alice/ang/rstorage/generators/herwig_alice/hepmc/260023/10/124/LHC_5020_MPI-S985111.hepmc',
							 	'/data/alice/ang/rstorage/generators/herwig_alice/hepmc/260023/20/78/LHC_5020_MPI-S617111.hepmc']

def report_counts():
	len_ntuple_events = []
	for parts in get_particles_ntuple_file(files_ntuples[0]):
		len_ntuple_events.append(len(parts))

	len_hepmc_events = []
	for parts in get_particles_hepmc_file(files_hepmc[0]):
		len_hepmc_events.append(len(parts))

# order not the same
# compare_nevents = zip(len_ntuple_events, len_hepmc_events)
# for c in compare_nevents:
# 	print(c)

class ComparisonHistograms(object):
	def __init__(self, foutname):
		self.fout = ROOT.TFile(foutname, 'recreate')
		self.eta 	= ROOT.TH1F('eta', 'eta;#eta_{particle}; #Delta N_{ntuple-hepmc}', 60, -2, 2)
		self.eta.Sumw2()
		self.perp =  ROOT.TH1F('perp', 'perp;p_{T,particle}; #Delta N_{ntuple-hepmc}', 100, logbins(0.1,600,100))
		self.perp.Sumw2()
		self.phi 	=  ROOT.TH1F('phi', 'phi;#varphi_{particle}; #Delta N_{ntuple-hepmc}', 72, 0, 2.*ROOT.TMath.Pi())
		self.phi.Sumw2()

		self.part_selector = fj.SelectorPtMin(0.150) & fj.SelectorPtMax(600.0) & fj.SelectorAbsEtaMax(0.9)

		_R = 0.4
		self.jet_def = fj.JetDefinition(fj.antikt_algorithm, _R)
		self.jet_selector = fj.SelectorPtMin(10.0) & fj.SelectorPtMax(600.0) & fj.SelectorAbsEtaMax(0.9 - _R)

		self.j_eta 	= ROOT.TH1F('j_eta', 'j_eta;#eta_{jet}; #Delta N_{ntuple-hepmc}', 60, -2, 2)
		self.j_eta.Sumw2()
		self.j_perp =  ROOT.TH1F('j_perp', 'j_perp;p_{T,jet}; #Delta N_{ntuple-hepmc}', 100, logbins(0.1,600,100))
		self.j_perp.Sumw2()
		self.j_phi 	=  ROOT.TH1F('j_phi', 'j_phi;#varphi_{jet}; #Delta N_{ntuple-hepmc}', 72, 0, 2.*ROOT.TMath.Pi())
		self.j_phi.Sumw2()

	def fill_histograms(self, particles, w=1.):
		for p in particles:
			self.eta.Fill(p.eta(), w)
			self.perp.Fill(p.perp(), w)
			self.phi.Fill(p.phi(), w)
		jets = self.jet_selector(self.jet_def(self.part_selector(particles)))
		for p in jets:
			self.j_eta.Fill(p.eta(), w)
			self.j_perp.Fill(p.perp(), w)
			self.j_phi.Fill(p.phi(), w)

	def close_file(self):
		self.fout.Write()
		self.fout.Close()
		print('[i] done with {} '.format(self.fout.GetName()))


for i in range(len(files_ntuples)):
	c_hists_nt = ComparisonHistograms(f'nt_ptetaphi_{i}.root')
	_ = [c_hists_nt.fill_histograms(parts, 1.) for parts in get_particles_ntuple_file(files_ntuples[i])]
	c_hists_nt.close_file()

	c_hists_hepmc = ComparisonHistograms(f'hepmc_ptetaphi_{i}.root')
	_ = [c_hists_hepmc.fill_histograms(parts, 1.) for parts in get_particles_hepmc_file(files_hepmc[i])]
	c_hists_hepmc.close_file()

	c_hists_hepmc = ComparisonHistograms(f'hepmc_ptetaphi_{i}_m0.root')
	_ = [c_hists_hepmc.fill_histograms(parts, 1.) for parts in get_particles_hepmc_file(files_hepmc[i], 0)]
	c_hists_hepmc.close_file()

	c_hists_hepmc = ComparisonHistograms(f'hepmc_ptetaphi_{i}_mpion.root')
	_ = [c_hists_hepmc.fill_histograms(parts, 1.) for parts in get_particles_hepmc_file(files_hepmc[i], pion_mass)]
	c_hists_hepmc.close_file()
