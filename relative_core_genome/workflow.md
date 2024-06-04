# Core genome calculation and plot generation

```
snakemake --config tool="pling" --cores 1
snakemake --config tool="MOB_secondary" --cores 1
snakemake --config tool="mge_cluster" --cores 1--keep-going
```

Note that for mge-cluster ggcaller fails on cluster 22 due to a segmentation fault, so this cluster was left out of further analysis.

Then to calculate the median relative core genome size and make the plots do:
```
python get_core_sizes.py
```
