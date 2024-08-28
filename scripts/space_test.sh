#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results
mkdir -p results/space_results

run_mem_test() {
	python3 evaluate_space.py $1 &
	scripts/mem_record.sh evaluate_space.py 120 results/space_results/$1_mem.txt
	wait
}

run_mem_test com-youtube_sym
# run_mem_test as-skitter_sym
# run_mem_test pokec_sym
# run_mem_test wiki-topcats_sym
# run_mem_test stackoverflow_sym
# run_mem_test soc-LiveJournal1_sym
# run_mem_test enwiki_sym
# run_mem_test com-orkut_sym
# run_mem_test twitter_sym
# run_mem_test friendster_sym
