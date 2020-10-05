#!/bin/bash
set -eou pipefail

./w_tokenize.py
cut -f 1-2 ../data/ws353.tsv > ../data/cleaned.tsv

../ppmi.py --results_path="../data/results_window.tsv" --tok_path="../data/tokenized.txt" --pairs_path="../data/cleaned.tsv" --window=30
./compare.py --res_path="../data/results_window.tsv"

../word2vec.py --results_path="../data/vec_aug_results.tsv" --tok_path="../data/tokenized.txt" --pairs_path="../data/cleaned.tsv" --size=200 --iter=6 --window=15
./compare.py --res_path="../data/vec_aug_results.tsv"
