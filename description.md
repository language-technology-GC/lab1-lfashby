Part 1: WordNet
---------------
Results:  
- *path similarity* -- correlation: 0.5735, coverage: 203
- *Leacock-Chodorow similarity* -- correlation: 0.5914, coverage: 203
- *Wu-Palmer similarity* -- correlation: 0.6141, coverage: 203
- *Resnik similarity* -- correlation: 0.6042, coverage: 192
- *Jiang-Conrath similarity* -- correlation: 0.5717, coverage: 202
- *Lin similarity* -- correlation: 0.5768, coverage: 192

[Code](solution_code/wordnet_sim.py)

Approach:   
I placed each of NLTK's synset similarity methods into their own function so I could play around with them individually -- despite the fact that doing so meant there would be quite a bit of reused code in [wordnet_sim.py](solution_code/wordnet_sim.py).  
I imported `product` from `itertools` and used it to find the synset pair with the highest similarity score for each pair of words. The similiarity score was set to `NaN` if no similarity score could be calculated for any of the synsets associated with the two words. For each pair of words, I added the highest similarity score (or `NaN`) and the human similarity score to separate lists and computed the Spearman Correlation Coefficient from those lists using `pandas` (because I couldn't get `scipy`'s `spearmanr nan_policy` argument to do anything.)


Part 2: PPMI
-------------

Results:
- Default settings -- correlation: -0.0732, coverage: 175
- Window set to 30 -- correlation: -0.0684, coverage: 185


Approach:  
I wrote a small [bash script](solution_code/run_ppmi_and_vec.sh) to run `ppmi.py` and [compute](solution_code/compare.py) the correlation and coverage of the [results](data/results.tsv) (and larger window [results](data/results_window.tsv)). The bash script also runs a [tokenization script](solution_code/w_tokenize.py) and produces a 2-column [copy](data/cleaned.tsv) of [ws353.tsv](data/ws353.tsv). I ran the tokenization script on the 2009 data from WMT news crawl. I could have tried to experiment with cleaning up the news crawl data a bit and seeing what effect that had, but it took so long to run the tokenization and ppmi steps that I didn't go for it. My attempts to add add-alpha smoothing we're not successful.


Part 3: Word2Vec similarity
---------------------------
Results:
- Default settings -- correlation: 0.6495, coverage: 203
- 'Boosted' settings -- correlation: 0.6733 coverage: 203

Approach:  
Similar to running `ppmi.py`, a call to `word2vec.py` was made in the previously mentioned [bash script](solution_code/run_ppmi_and_vec.sh) and the [results](data/vec_results.tsv) were compared using the same [script](solution_code/compare.py) - even though sorting was not necessary in this case. I also ran `word2vec.py` with double the dimensionality of the word vectors (`size=200`), double the iterations (`iter=6`) and a window size of 15. This led to a higher correlation with the human judgments than the default settings, though it is difficult to tell whether any particular hyperparameter modification led to this slight improvement. (In the future I should only change one hyperparameter at a time!) I don't think it was wise to increase the `window` size to 15 - for the purposes of assigning similarity values I think a window size of 15 is too much context. 


Part 4: Summary
---------------
Ultimately, the Word2Vec similarity values had the greatest correlation with the human judgments and achieved total coverage. The NLTK WordNet similarity methods performed admirably, and had generally good coverage - though it would have been interesting to vary the 'Information Content' table to see how that modified the correlation and coverage scores for the Resnik, Lin, and JCN methods. (Regarding NLTK and WordNet, has anyone developed some way of automatically assigning the appropriate synset to a word given the context that it appears in?) The PPMI approach was not encouraging. Increasing the window size helped increase coverage, but the correlation score remained very near to 0. 
