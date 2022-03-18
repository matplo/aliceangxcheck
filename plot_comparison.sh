./ratio_2_files.py -i1 hepmc_ptetaphi_0.root -i2 nt_ptetaphi_0.root -o ratio_file_0.root
./ratio_2_files.py -i1 hepmc_ptetaphi_0_m0.root -i2 nt_ptetaphi_0.root -o ratio_file_0_m0.root
./ratio_2_files.py -i1 hepmc_ptetaphi_0_mpion.root -i2 nt_ptetaphi_0.root -o ratio_file_0_mpion.root

./ratio_2_files.py -i1 hepmc_ptetaphi_1.root -i2 nt_ptetaphi_1.root -o ratio_file_1.root
./ratio_2_files.py -i1 hepmc_ptetaphi_1_m0.root -i2 nt_ptetaphi_1.root -o ratio_file_1_m0.root
./ratio_2_files.py -i1 hepmc_ptetaphi_1_mpion.root -i2 nt_ptetaphi_1.root -o ratio_file_1_mpion.root

gui_draw_select.py compare_part_nt_hepmc.draw --wname 10_124 -r file:10/124 -r fnumber:0 --preent pdf1 --quit
gui_draw_select.py compare_part_nt_hepmc.draw --wname 20_78 -r file:20/78 -r fnumber:1 --preent pdf1 --quit
