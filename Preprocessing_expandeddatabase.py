import os
from os.path import join
import argparse
import pandas as pd

from smiles_embeddings import *
from protein_embeddings import *


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_val_path",
        type=str,
        required=True,
        help="Path, where train, test, and validation dataset are as csv files",
    )
    parser.add_argument(
        "--outpath",
        type=str,
        required=True,
        help="Path, where the protein and SMILES embeddings should be saved.",
    )
    parser.add_argument(
        "--prot_emb_no",
        default=2000,
        type=int,
        help="Number of protein sequences in one dictionary.",
    )
    parser.add_argument(
        "--smiles_emb_no",
        default=2000,
        type=int,
        help="Number of SMILES strings in one dictionary.",
    )
    return parser.parse_args()


args = get_arguments()


# Find all training and validation dataframes
dataframes = [
    dataframe
    for dataframe in os.listdir(args.train_val_path)
    if dataframe.endswith(".csv") and os.path.isfile(join(args.train_val_path, dataframe))
]

if len(dataframes) == 0:
    raise ValueError("No CSV files found in train_val_path: %s" % args.train_val_path)

df = pd.concat(
    [pd.read_csv(join(args.train_val_path, dataframe)) for dataframe in dataframes],
    ignore_index=True,
)


# Remove rows with missing protein sequences or SMILES
df = df.dropna(subset=["Protein sequence", "SMILES"])

# Make sure everything is string
df["Protein sequence"] = df["Protein sequence"].astype(str)
df["SMILES"] = df["SMILES"].astype(str)


# Get all Protein Sequences and SMILES strings
all_sequences = list(set(df["Protein sequence"]))
all_smiles = list(set(df["SMILES"]))

print(
    "No. of different sequences: %s, No. of different SMILES strings: %s"
    % (len(all_sequences), len(all_smiles))
)


try:
    os.mkdir(args.outpath)
except:
    pass


print("Calculating protein embeddings:")
calculate_protein_embeddings(all_sequences, args.outpath, args.prot_emb_no)

print("Calculating SMILES embeddings:")
calculate_smiles_embeddings(all_smiles, args.outpath, args.smiles_emb_no)