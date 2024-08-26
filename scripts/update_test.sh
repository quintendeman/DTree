#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

python evaluate_updates.py com-youtube_sym
python evaluate_updates.py as-skitter_sym
python evaluate_updates.py pokec_sym
python evaluate_updates.py wiki-topcats_sym
python evaluate_updates.py stackoverflow_sym
python evaluate_updates.py soc-LiveJournal1_sym
python evaluate_updates.py enwiki_sym
python evaluate_updates.py com-orkut_sym
python evaluate_updates.py twitter_sym
python evaluate_updates.py friendster_sym
