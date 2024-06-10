import argparse
from plsdbapi import query
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('inc_type', choices=["incf", "type_blind"])
parser.add_argument('size', choices=["300", "1500"])
args = parser.parse_args()

path = f"{args.inc_type}_samples_{args.size}.txt"

accessions = [el[0] for el in pd.read_csv(path, header=None).values]
isdownloaded = query.download_fasta(accessions)
if not isdownloaded:
    raise Exception("Download from PLSDB failed")
