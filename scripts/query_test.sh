#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

python evaluate_queries.py kron_13_stream_binary
python evaluate_queries.py kron_15_stream_binary
python evaluate_queries.py kron_16_stream_binary
python evaluate_queries.py kron_17_stream_binary
python evaluate_queries.py kron_18_stream_binary
python evaluate_queries.py dnc_stream_binary
python evaluate_queries.py tech_stream_binary
python evaluate_queries.py enron_stream_binary
python evaluate_queries.py dnc_streamified_binary
python evaluate_queries.py tech_streamified_binary
python evaluate_queries.py enron_streamified_binary
