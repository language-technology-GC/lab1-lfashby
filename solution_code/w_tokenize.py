#!/usr/bin/env python
from nltk.tokenize import word_tokenize


def main():
    with open("../data/tokenized.txt", "w") as sink:
        with open("../data/news.2009.en.shuffled.deduped", "r") as source:
            for line in source:
                # Could casefold, could try to remove punctuation/special characters.
                val = word_tokenize(line)
                print(f"{' '.join(val)}", file=sink)


if __name__ == "__main__":
    main()
