#!/usr/bin/env python3

import sys
import os
import re
import sys
import os
import math
import re
import argparse
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
def gff_to_bed(gff_file):
    bed_file = os.path.splitext(gff_file)[0] + ".bed"

    with open(gff_file, 'r') as gff, open(bed_file, 'w') as bed:
        for line in gff:
            if line.startswith('#'):
                continue

            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue

            if fields[2] not in ["protein_coding_gene", "ncRNA_gene", "gene"]:
                continue

            chrom = fields[0]
            start = int(fields[3]) - 1
            end = int(fields[4])

            attributes = fields[8]
            name_match = re.search(r'ID=([^;]+)', attributes)
            name = name_match.group(1) if name_match else 'unknown'

            score = fields[5] if fields[5] != '.' else '0'
            strand = fields[6] if fields[6] in ['+', '-'] else '.'

            bed.write(f"{chrom}\t{start}\t{end}\t{name}\t{score}\t{strand}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: gff2bed.py input.gff")
        sys.exit(1)

    gff_file = sys.argv[1]
    gff_to_bed(gff_file)
    print(f"Converted {gff_file} to {os.path.splitext(gff_file)[0]}.bed successfully.")