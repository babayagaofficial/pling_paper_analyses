from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inc_type', choices=["incf", "type_blind"])
parser.add_argument('size', choices=["300", "1500"])
parser.add_argument('input_file', help="Unzipped fasta file from PLSDB download")
args = parser.parse_args()

output_dir = Path(f"fastas_{args.inc_type}_{args.size}")
output_dir.mkdir(parents=True, exist_ok=True)

with open(f"cleaned_{args.input_file}", "w") as cleaned:
    for record in SeqIO.parse(Path(args.input_file), "fasta"):
        sep_record = SeqRecord(record.seq, record.id, description="")
        with open(f"./{output_dir}/{record.id}.fna", "w") as output_handle:
            SeqIO.write(sep_record, output_handle, "fasta")
        SeqIO.write(sep_record, cleaned, "fasta")
