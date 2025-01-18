#!/usr/bin/env python3

import sys
import os
import pandas as pd

def assign_args(args):
    for i in range(1, len(args)):
        df = pd.read_csv(sys.argv[i], sep = '\t', header = None)
        if df.shape[1] == 7:
            tsv = df.copy()
            matrix_output = ''.join([os.path.splitext(sys.argv[i])[0], '.matrix'])
            bed_output = ''.join([os.path.splitext(sys.argv[i])[0], '_abs.bed'])
        elif df.shape[1] == 2:
            sizes = df.copy()
    return tsv, sizes, matrix_output, bed_output

def filter_chroms(tsv, sizes):
    return tsv[tsv[0].isin(sizes[0]) & tsv[3].isin(sizes[0])]

def find_chrom_starts(sizes, res):
    starts = sizes.copy()
    starts[1] = sizes[1] // res + 1
    starts[1] = starts[1].cumsum()
    starts[1] = starts[1].shift(periods = 1, fill_value = 0)
    return starts

def convert2hicpro(tsv, starts, res):
    tsv[2] = tsv[2] // res + (tsv[2] % res > 0)
    tsv[5] = tsv[5] // res + (tsv[5] % res > 0)
    tsv = pd.merge(tsv, starts, how = 'left', left_on = [0], right_on = [0])
    tsv = pd.merge(tsv, starts, how = 'left', left_on = [3], right_on = [0])
    tsv.columns = range(tsv.shape[1])
    tsv[10] = tsv[2] + tsv[7]
    tsv[11] = tsv[5] + tsv[9]
    tsv = tsv[[10, 11, 6]]
    return tsv

def generate_bed(sizes, res):
    dfs = []
    for chr in sizes.itertuples():
        dfs.append(pd.DataFrame({0: chr[1], 1: list(range(0, chr[2], res)), 2: list(range(res, chr[2], res)) + [chr[2]]}))
    bed = pd.concat(dfs, ignore_index = True)
    bed[3] = list(range(1, bed.shape[0] + 1))
    return bed

def main():
    tsv, sizes, matrix_output, bed_output = assign_args(sys.argv)
    tsv = filter_chroms(tsv, sizes)
    res = tsv.iloc[0, 2] - tsv.iloc[0, 1]
    starts = find_chrom_starts(sizes, res)
    tsv = convert2hicpro(tsv, starts, res)
    tsv.to_csv(matrix_output, sep = '\t', doublequote = False, index = False, header = False)
    bed = generate_bed(sizes, res)
    bed.to_csv(bed_output, sep = '\t', doublequote = False, index = False, header = False)

if __name__ == '__main__':
    main()
