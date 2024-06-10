# Distance calculations for PSD

## Examples A-C

Where `pling_path` is the path to the directory in which pling is, for example A please run:
```
PYTHONPATH=pling_path python pling_path/run_pling.py fastas/PSD_A.txt PSD_A align
mash dist fastas/russian_doll/pKPC_CAV1321-45.fna fastas/russian_doll/pKPC_CAV1668.fna > PSD_A_mash.dist
sourmash sketch dna --from-file fastas/PSD_A.txt -o PSD_A.sig
sourmash compare PSD_A.sig --max-containment --csv PSD_A.dist
```

For examples B and C do the same, just replace the inputs appropriately.

For example D, do the same for pling and sourmash as above, and then for mash run
```
mash dist fastas/russian_doll/pKPC_CAV1320.fna -l fastas/PSD_D.txt > PSD_D.dist
```
