#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements.txt
mkdir -p results
mkdir -p results/space_results

run_mem_test() {
	python evaluate_updates.py $1 &
	./../scripts/mem_record.sh mpi_dynamicCC_tests 2 ./../results/mpi_space_results/$1_mem.txt
	wait
}

run_mem_test "kron_13"
# run_mem_test "kron_15"
# run_mem_test "kron_16"
# run_mem_test "kron_17"
# run_mem_test "kron_18"
# run_mem_test "dnc"
# run_mem_test "tech"
# run_mem_test "enron_streamified"
# run_mem_test "dnc_streamified"
# run_mem_test "tech_streamified"
