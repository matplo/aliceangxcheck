#!/bin/bash

files=$(find . -name "*.dat" | sort)
echo ${files}

subdir10="fromJames/rivet-plots-10"
subdir20="fromJames/rivet-plots-20"

mkdir -p ./comp_pdfs

for fn in ${files}
do
	if [[ "${fn}" =~ .*"${subdir10}".* ]]; then
		sdir10=""
		sdir20="#ignore"
		sdir="10"
	fi

	if [[ "${fn}" =~ .*"${subdir20}".* ]]; then
		sdir10="#ignore"
		sdir20=""
		sdir="20"
	fi

	fnbase=$(basename ${fn})
	hname_replacement=$(./map_rivet_name_to_hname.py ${fnbase})
	replacements="-r sdir10:${sdir10} -r sdir20:${sdir20} -r fname:${fnbase} -r hname:${hname_replacement}"
	gui_draw_select.py ${replacements} --preent pdf1 --quit rivet_root.draw --wname ${fnbase}
	# gui_draw_select.py ${replacements} rivet_root.draw --wname ${fnbase}
	cp -v ${fnbase}*.pdf ./comp_pdfs/${sdir}_${fnbase}.pdf
	mv -v ${fnbase}*.pdf ${fn}.pdf
	# break
done
