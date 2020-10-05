#!/usr/bin/env python
import argparse
import pandas as pd

from typing import List


def isolate_group(path_to_results: str, to_match: List[str]):
    with open(path_to_results, "r") as res_source:
        for line in res_source:
            first, second, val = line.strip().split("\t")
            res_group = [first.casefold(), second.casefold()]
            res_group.sort()
            if res_group == to_match:
                return val

    return float("NaN")


def main(args: argparse.Namespace):
    covered = 0
    ppmi_vals = []
    human_vals = []

    with open("../data/ws353.tsv", "r") as source:
        for line in source:
            first, second, human_val = line.strip().split("\t")
            group = [first.casefold(), second.casefold()]
            group.sort()

            ppmi_val = isolate_group(args.res_path, group)
            if ppmi_val == ppmi_val:
                covered += 1

            human_vals.append(human_val)
            ppmi_vals.append(ppmi_val)

    s1 = pd.Series(human_vals)
    s2 = pd.Series(ppmi_vals)
    corr = s1.corr(s2, method="spearman")
    return "{:.4f}".format(corr), covered


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--res_path", required=True
    )
    print(main(parser.parse_args()))
