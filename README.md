# Workflow to reproduce all data and figures in pling paper

## Dependancies

You will have to ensure that you have:
- pling v1.0.3 (https://github.com/iqbal-lab-org/pling/releases/tag/v1.0.3)
- mash v2.3 (https://mash.readthedocs.io/en/latest/)
- (if you want to do all the run time evaluations) Gurobi

Please create a conda environment with the `env.yaml` file
```
conda create -n pling_paper -f env.yaml
```
and activate it
```
conda activate pling_paper
```
beforehand.

## Content

The commands to reproduce the clustering outputs from all tools for Russian doll and Addenbrookes plasmids are further below.

The remaining parts of the analysis from the paper are split into their own folder, with their own description file.

- For alignment visualisations from Figures 3, 4, 5, and Supp. Figures 3-7, please refer to `alignment_figs`.
- For distances from Figure 3 and Supp. Table 2, please refer to `psd.md`.
- For Figure 6, please refer to `tree_vis`.
- For Supp. Figure 1, please refer to `relative_core_genome`.
- For van Dongen distance calculation, please refer to `split_join`.
- For run time evaluations in Supp. Table 1, please refer to `runtime_evals`.

The total output for Russian doll and Addenbrookes plasmids is available [here](https://doi.org/10.6084/m9.figshare.26871001.v1)

## Cluster Russian doll plasmids

These need to be run with pling v2. Please run:
```
pling fastas/russian_doll.txt russian_doll_pling align
```
then for MOB-suite:
```
mob_typer --multi --infile fastas/russian_doll_seqs.fna --out_file russian_doll_mobtyper_results.txt
mob_cluster -m build -f fastas/russian_doll_seqs.fna -o reduced -p russian_doll_mobtyper_results.txt -t fastas/russian_doll_taxonomy.tsv
```
and finally for mge-cluster:
```
mge_cluster --create --input fastas/russian_doll.txt --prefix russian_doll --threads 4 --min_cluster 2
```

## Cluster Addenbrookes plasmids

Please run:
```
pling fastas/addenbrookes.txt addenbrookes_pling align --containment_distance 0.3
```
then for MOB-suite:
```
mob_typer --multi --infile fastas/addenbrookes_seqs.fna --out_file addenbrookes_mobtyper_results.txt
mob_cluster -m build -f fastas/addenbrookes_seqs.fna -o reduced -p addenbrookes_mobtyper_results.txt -t fastas/addenbrookes_taxonomy.tsv
```
and finally for mge-cluster:
```
mge_cluster --create --input fastas/addenbrookes.txt --prefix addenbrookes --threads 4 --min_cluster 2
```
