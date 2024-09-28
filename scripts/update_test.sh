#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

python3 evaluate_updates.py Household_lines_5_sym
python3 evaluate_updates.py CHEM_5_sym
python3 evaluate_updates.py grid_1000_10000_03_sym
python3 evaluate_updates.py Germany_sym
python3 evaluate_updates.py RoadUSA_sym
python3 evaluate_updates.py rmat_26
python3 evaluate_updates.py com-youtube_sym
python3 evaluate_updates.py as-skitter_sym
python3 evaluate_updates.py pokec_sym
python3 evaluate_updates.py wiki-topcats_sym
python3 evaluate_updates.py stackoverflow_sym
python3 evaluate_updates.py soc-LiveJournal1_sym
python3 evaluate_updates.py enwiki_sym
python3 evaluate_updates.py com-orkut_sym
python3 evaluate_updates.py twitter_sym
python3 evaluate_updates.py friendster_sym
