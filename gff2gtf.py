#!/usr/bin/env python3

## Converts GFF to GTF format if a GTF file is unavailable for a user's organism of interest.

import sys
import pandas as pd
import csv

with open(sys.argv[1], 'r') as f:
	lines = f.readlines()
	num = [i for i, l in enumerate(lines) if l.startswith("##")]
df = pd.read_csv(sys.argv[1], sep="\t", header=None, skiprows = num)
df = df[(df[2] == "protein_coding_gene") | (df[2] == "pseudogene") | (df[2] == "ncRNA_gene") | (df[2] == "gene") | (df[2] == "lnc_RNA")]
df[2] = "transcript"
df = df.sort_values(by=[0,3]).reset_index().drop("index", axis=1)
transcript_ID = df[8].str.split("=", expand = True)[1].str.split(";", expand = True)
transcript_ID[0] = transcript_ID[0].str.replace("exon_", "")
gene_ID = transcript_ID[0].str.split(".", expand = True)
df[8] = "transcript_id \"" + transcript_ID[0] + "\"; gene_id \"" + gene_ID[0] + "\""
df.to_csv(sys.argv[1].replace(".gff",".gtf"), sep="\t", header=False, index=False, quoting=csv.QUOTE_NONE)
