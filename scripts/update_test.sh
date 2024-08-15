#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

# python evaluate_updates.py kron_13_stream_binary
# python evaluate_updates.py kron_15_stream_binary
# python evaluate_updates.py kron_16_stream_binary
# python evaluate_updates.py kron_17_stream_binary
# python evaluate_updates.py kron_18_stream_binary

# python evaluate_updates.py dnc_stream_binary
# python evaluate_updates.py tech_stream_binary
# python evaluate_updates.py enron_stream_binary
# python evaluate_updates.py dnc_streamified_binary
# python evaluate_updates.py tech_streamified_binary
# python evaluate_updates.py enron_streamified_binary
# python evaluate_updates.py dnc_ff_binary
# python evaluate_updates.py tech_ff_binary
# python evaluate_updates.py enron_ff_binary

# python evaluate_updates.py twitter_stream_binary
# python evaluate_updates.py stanford_stream_binary
# python evaluate_updates.py random2N_stream_binary
# python evaluate_updates.py randomNLOGN_stream_binary
# python evaluate_updates.py randomNSQRTN_stream_binary
# python evaluate_updates.py randomDIV_stream_binary

# python evaluate_updates.py erdos_0001_stream_binary
# python evaluate_updates.py erdos_001_stream_binary
# python evaluate_updates.py erdos_01_stream_binary
python evaluate_updates.py erdos_10_stream_binary
python evaluate_updates.py erdos_20_stream_binary
python evaluate_updates.py erdos_30_stream_binary
# python evaluate_updates.py erdos_40_stream_binary
# python evaluate_updates.py erdos_50_stream_binary
# python evaluate_updates.py erdos_60_stream_binary
# python evaluate_updates.py erdos_70_stream_binary
# python evaluate_updates.py erdos_80_stream_binary
# python evaluate_updates.py erdos_90_stream_binary
# python evaluate_updates.py erdos_100_stream_binary
