import argparse
import time
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("fasta_file_IncF", help="Unzipped fasta of all IncF plasmids from PLSDB")
parser.add_argument("fasta_file_random", help="Unzipped fasta of all type blind plasmids from PLSDB")
parser.add_argument("pling_path", help="Path to pling")
parser.add_argument("genomes_list_IncF", help="Text file of paths to fasta files of IncF plasmids")
parser.add_argument("genomes_list_type_blind", help="Text file of paths to fasta files of type blind plasmids")
args = parser.parse_args()


def run_mob(infile, taxonomy, typer_out, cluster_out):
    start_time = time.time()
    subprocess.check_output(f"mob_typer --multi --infile {infile} --out_file {typer_out} -n 8", shell=True)
    subprocess.check_output(f"mob_cluster -m build -f {infile} -o MOB_out -p {typer_out} -t {taxonomy} -o {cluster_out} --num_threads 8", shell=True)
    run_time_mob = time.time() - start_time
    return run_time_mob

def run_pling(pling_path, genomes_list, out_dir, gurobi):
    if gurobi:
        solver = "--ilp_solver gurobi"
    else:
        solver = "--ilp_solver GLPK"
    start_time = time.time()
    subprocess.check_output(f"PYTHONPATH={pling_path} python {pling_path}/pling/run_pling.py {genomes_list} {out_dir} align --sourmash --batch_size 200 --cores 8 {solver}", shell=True)
    run_time = time.time() - start_time
    return run_time

mob_incf = run_mob(args.fasta_file_IncF, "taxonomy_IncF_300.tsv", "typer_IncF_300.txt", "MOB_IncF_300")
mob_type_blind = run_mob(args.fasta_file_random, "taxonomy_type_blind_300.tsv", "typer_type_blind_300.txt", "MOB_type_blind_300")
pling_incf_glpk = run_pling(args.pling_path, args.genomes_list_IncF, "pling_IncF_300", False)
pling_blind_glpk = run_pling(args.pling_path, args.genomes_list_type_blind, "pling_type_blind_300", False)
pling_incf_gurobi = run_pling(args.pling_path, args.genomes_list_IncF, "pling_gurobi_IncF_300", True)
pling_blind_gurobi = run_pling(args.pling_path, args.genomes_list_type_blind, "pling_gurobi_type_blind_300", True)
print("MOB-suite on IncF 300:", mob_incf)
print("MOB-suite on type blind 300:", mob_type_blind)
print("pling w GLPK on IncF 300:", pling_incf_glpk)
print("pling w GLPK on type blind 300:", pling_blind_glpk)
print("pling w Gurobi on IncF 300:", pling_incf_gurobi)
print("pling w Gurobi on type blind 300:", pling_blind_gurobi)
