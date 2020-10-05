import pandas as pd
from itertools import product

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import WordNetError

brown_ic = wordnet_ic.ic('ic-brown.dat')


def compare_lin(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        try:
            curr = wn.lin_similarity(first_synset, second_synset, brown_ic)
        except WordNetError: # _lcs_ic() error
            continue
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def compare_jcn(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        try:
            curr = wn.jcn_similarity(first_synset, second_synset, brown_ic)
        except WordNetError: # _lcs_ic() error
            continue
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def compare_resnik(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        try:
            curr = wn.res_similarity(first_synset, second_synset, brown_ic)
        except WordNetError: # _lcs_ic() error
            continue
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def compare_wup(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        curr = wn.wup_similarity(first_synset, second_synset)
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def compare_lch(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        try:
            curr = wn.lch_similarity(first_synset, second_synset)
        except WordNetError: # Bespoke error within lch_similarity()
            continue
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def compare_path(first, second):
    highest = 0
    for first_synset, second_synset in product(
        wn.synsets(first), wn.synsets(second)
    ):
        curr = wn.path_similarity(first_synset, second_synset)
        # Check curr, avoids TypeError when path_similarity returns None
        # as when comparing Synset('dog.n.01') Synset('cat.v.01')
        if curr and curr > highest:
            highest = curr

    return highest if highest else float("NaN")


def comparison_gen():
    funcs = [
        compare_path,
        compare_lch,
        compare_wup,
        compare_resnik,
        compare_jcn,
        compare_lin
    ]
    for func in funcs:
        covered = 0
        human_sim_values = []
        comparison_sim_values = []
        with open("../data/ws353.tsv", "r") as source:
            for line in source:
                first_word, second_word, sim_value = line.rstrip().split("\t")
                res = func(first_word, second_word)
                # Check if res is NaN
                if res == res:
                    covered += 1
                human_sim_values.append(sim_value)
                comparison_sim_values.append(res)

        s1 = pd.Series(human_sim_values)
        s2 = pd.Series(comparison_sim_values)
        corr = s1.corr(s2, method="spearman")
        yield "{:.4f}".format(corr), covered


if __name__ == "__main__":
    for spr, total_covered in comparison_gen():
        print(spr, total_covered)

# path similarity -- correlation: 0.5735, coverage: 203
# Leacock-Chodorow similarity -- correlation: 0.5914, coverage: 203
# Wu-Palmer similarity -- correlation: 0.6141, coverage: 203
# Resnik similarity -- correlation: 0.6042, coverage: 192
# Jiang-Conrath similarity -- correlation: 0.5717, coverage: 202
# Lin similarity -- correlation: 0.5768, coverage: 192
