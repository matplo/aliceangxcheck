from pyjetty.mputils import data_io as dio

files = ['/rstorage/generators/herwig_alice/tree_gen/265216/260023/20/78/AnalysisResultsGen.root',
         '/rstorage/generators/herwig_alice/tree_gen/265216/260023/10/124/AnalysisResultsGen.root']

for fn in files:
    _fn = '/data/alice/ang/{}'.format(fn)
    print('[i] file', _fn)
    datafile = dio.DataFileIO(file_input=_fn, tree_name='tree_Particle_gen')
    print('[i] number of events:', len(datafile.df_events))
    for d in datafile.df_events:
        print('n parts=', len(d.particles))