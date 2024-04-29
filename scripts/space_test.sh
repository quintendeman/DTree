#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results
mkdir -p results/space_results

run_mem_test() {
	python evaluate_space.py $1 &
	scripts/mem_record.sh evaluate_space.py 2 results/space_results/$1_mem.txt
	wait
}

run_mem_test "kron_13_stream_binary"
run_mem_test "kron_15_stream_binary"
run_mem_test "kron_16_stream_binary"
run_mem_test "kron_17_stream_binary"
run_mem_test "kron_18_stream_binary"
run_mem_test "dnc_stream_binary"
run_mem_test "tech_stream_binary"
run_mem_test "enron_stream_binary"
run_mem_test "dnc_streamified_binary"
run_mem_test "tech_streamified_binary"
run_mem_test "enron_streamified_binary"
