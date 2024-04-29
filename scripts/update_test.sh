#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements.txt
mkdir -p results

python evaluate_updates.py kron_13
python evaluate_updates.py kron_15
python evaluate_updates.py kron_16
python evaluate_updates.py kron_17
python evaluate_updates.py kron_18
python evaluate_updates.py dnc
python evaluate_updates.py tech
python evaluate_updates.py enron
python evaluate_updates.py dnc_streamified
python evaluate_updates.py tech_streamified
python evaluate_updates.py enron_streamified
