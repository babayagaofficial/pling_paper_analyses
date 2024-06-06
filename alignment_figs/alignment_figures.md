# Creating alignment plots in figures 4 and 5, and supp. figures 3-7

We modified Martin Hunt's script (https://github.com/martinghunt/bioinf-scripts/blob/master/python/multi_act_cartoon.py), to accept text files with a list of paths to fasta files -- this modified script can be found under `multi_act_cartoon.py`. Appropriately formated lists can be found under `clusters/cluster_lists` for all clusters from all tools. The directory `clusters/cluster_lists/russian_doll_alignments` contains lists for the alignments in figures 4 and 5. The script can be run with e.g.

```
python multi_act_cartoon.py figure_4_alignment ../clusters/cluster_lists/russian_doll_alignments/figure_4.txt --match_min_len_bases 200 --nucmer_min_id 80
```

Note that we run with the parameters `match_min_len_bases=200` and `nucmer_min_id=80` to reflect the parameters at which nucmer is run when integerising.
