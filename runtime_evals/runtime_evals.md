# Performing runtime evaluations

Run time evalutaions were run on four datasets, which will be downloaded as part of this workflow. The datasets will be referred to as: IncF 300, IncF 1500, type blind 300, type blind 1500.


For IncF 300 and type blind 300, you will need 8 cores to be available. The original evluation was performed on a laptop. Perform the following sequence of commands:

1. Download the input files:
```
python download_from_plsdb.py incf 300
```
2. Unzip the output from the previous step, where `IncF_300.fna.gz` is the previously downloaded file:
```
gzip -d IncF_300.fna.gz
```
3. Seperate out entries in the fasta file into individual files in a common directory and remove descriptions, where `IncF_300.fna` is the previously unzipped fasta file:
```
python seperate_fastas.py incf 300 IncF_300.fna
```
4. Repeat 1-3 but replace `incf` with `type_blind`.
5. Generate the list of paths to the IncF fasta files by doing the following commands:
```
cd fastas_incf_300
ls -d -1 $PWD/*.fna > ../IncF_300_list.txt
cd ..
```
Repeat for the type blind dataset.
6. You should now have in one directory the following files: `cleaned_IncF_300.fna`, `cleaned_type_blind_300.fna`, `IncF_300_list.txt`, `type_blind_300_list.txt`, `taxonomy_IncF_300.tsv`, `taxonomy_type_blind_300.tsv` (note: the taxonomies are from PLSDB). Run the following script, where `pling_path` is the path to the directory where pling is stored:
```
python run_300.py cleaned_IncF_300.fna cleaned_type_blind_300.fna pling_path IncF_300_list.txt type_blind_300_list.txt
```
The run times will be printed to stdout.



For IncF 1500 and type blind 1500, perform the steps 1-5 described above, but replace `300` with `1500`. The original evaluation was performed by submitting jobs on a SLURM cluster, and run times were read from job information reports. The following commands were run:

1. pling without sourmash, with GLPK
IncF:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py IncF_1500_list.txt pling_smash_glpk_incf align --batch_size 200 --ilp_solver GLPK --forceall --cores 48
```
type blind:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py type_blind_1500_list.txt pling_smash_glpk_type_blind align --batch_size 200 --ilp_solver GLPK --forceall --cores 48
```

2. pling with sourmash, with GLPK
IncF:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py IncF_1500_list.txt pling_smash_glpk_incf align --batch_size 200 --sourmash --ilp_solver GLPK --forceall --cores 48
```
type blind:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py type_blind_1500_list.txt pling_smash_glpk_type_blind align --batch_size 200 --sourmash --ilp_solver GLPK --forceall --cores 48
```

3. pling with sourmash, with Gurobi
IncF:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py IncF_1500_list.txt pling_smash_glpk_incf align --batch_size 200 --sourmash --ilp_solver gurobi --forceall --cores 48
```
type blind:
```
PYTHONPATH=pling_path python pling_path/pling/run_pling.py type_blind_1500_list.txt pling_smash_glpk_type_blind align --batch_size 200 --sourmash --ilp_solver gurobi --forceall --cores 48
```

4. mge-cluster 48 cores
IncF:
```
mge_cluster --create --input IncF_1500_list.txt --min_cluster 2 --threads 48
```
type blind:
```
mge_cluster --create --input type_blind_1500_list.txt --min_cluster 2 --threads 48
```
