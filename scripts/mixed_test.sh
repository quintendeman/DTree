#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements
mkdir -p results

# Test run
python evaluate_mixed.py kron_13_query10_binary

# Full sweep
python evaluate_mixed.py kron_13_query10_binary
python evaluate_mixed.py kron_15_query10_binary
python evaluate_mixed.py kron_16_query10_binary
python evaluate_mixed.py kron_17_query10_binary
# python evaluate_mixed.py kron_18_query10_binary

python evaluate_mixed.py dnc_query10_binary
python evaluate_mixed.py tech_query10_binary
python evaluate_mixed.py enron_query10_binary

python evaluate_mixed.py twitter_query10_binary
python evaluate_mixed.py stanford_query10_binary
python evaluate_mixed.py random2N_query10_binary
python evaluate_mixed.py randomNLOGN_query10_binary
python evaluate_mixed.py randomNSQRTN_query10_binary
python evaluate_mixed.py randomDIV_query10_binary

# Fixed-forest
python evaluate_mixed.py kron_13_ff_query10_binary
python evaluate_mixed.py kron_15_ff_query10_binary
python evaluate_mixed.py kron_16_ff_query10_binary
python evaluate_mixed.py kron_17_ff_query10_binary
# python evaluate_mixed.py kron_18_ff_query10_binary

python evaluate_mixed.py dnc_ff_query10_binary
python evaluate_mixed.py tech_ff_query10_binary
python evaluate_mixed.py enron_ff_query10_binary

python evaluate_mixed.py twitter_ff_query10_binary
python evaluate_mixed.py stanford_ff_query10_binary
python evaluate_mixed.py random2N_ff_query10_binary
python evaluate_mixed.py randomNLOGN_ff_query10_binary
python evaluate_mixed.py randomNSQRTN_ff_query10_binary
python evaluate_mixed.py randomDIV_ff_query10_binary
