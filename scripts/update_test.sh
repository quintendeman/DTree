#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

python evaluate_updates.py kron_13_stream_binary
python evaluate_updates.py kron_15_stream_binary
python evaluate_updates.py kron_16_stream_binary
python evaluate_updates.py kron_17_stream_binary
python evaluate_updates.py kron_18_stream_binary
python evaluate_updates.py dnc_stream_binary
python evaluate_updates.py tech_stream_binary
python evaluate_updates.py enron_stream_binary
python evaluate_updates.py dnc_streamified_binary
python evaluate_updates.py tech_streamified_binary
python evaluate_updates.py enron_streamified_binary
