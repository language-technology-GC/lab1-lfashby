#!/bin/bash
set -eou pipefail

./w_tokenize.py
cut -f 1-2 ../data/ws353.tsv > ../data/cleaned.tsv

./ppmi.py --results_path="../data/results.tsv" --tok_path="../data/tokenized.txt" --pairs_path="../data/cleaned.tsv"
./compare.py --res_path="../data/results.tsv"

./word2vec.py --results_path="vec_results.tsv" --tok_path="tokenized.txt" --pairs_path="data/cleaned.tsv"
./compare.py --res_path="../data/vec_results.tsv"
