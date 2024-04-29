#!/bin/bash

declare base_dir="$(dirname $(dirname $(realpath $0)))"

cd ${base_dir}
pip install -r requirements.txt

mkdir -p results

python evaluate_queries.py kron_13
python evaluate_queries.py kron_15
python evaluate_queries.py kron_16
python evaluate_queries.py kron_17
python evaluate_queries.py kron_18
python evaluate_queries.py dnc
python evaluate_queries.py tech
python evaluate_queries.py enron
python evaluate_queries.py dnc_streamified
python evaluate_queries.py tech_streamified
python evaluate_queries.py enron_streamified
