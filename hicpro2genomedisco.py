import pandas as pd
import sys
import os
from itertools import combinations

sizes = pd.read_csv(sys.argv[1], sep="\t", header=None, names=["chr","start","end"])
sizes["start"] = sizes["start"].floordiv(10000).round().add(1).astype("int")

ends = []
chr = []
for index, row in sizes.iterrows():
	ends.append(row["start"])
	chr.append(row["chr"])

start = []
prev = 0
for i in ends:
	start.append(prev+1)
	prev += i
end = [start[x] + ends[x] - 1 for x in range(len(start))]

bins = {}
for i in range(len(chr)):
	bins[chr[i]] = [*range(start[i],end[i]+1,1)]
bins = pd.DataFrame([(k, v) for (k, L) in bins.items() for v in L], columns=["chr1", "bin1"])

df = pd.read_csv(sys.argv[2], sep="\t", header=None, names=["bin1","bin2","int"])
df = df.merge(bins, how="inner", on="bin1")
bins.rename(columns={"bin1":"bin2", "chr1":"chr2"}, inplace=True)
df = df.merge(bins, how="inner", on="bin2")
df = df[["chr1", "bin1", "chr2", "bin2", "int"]]
df.sort_values(["bin1","bin2"], inplace=True)

#n*(n+1)/2
bc = pd.DataFrame(columns=["bin1", "bin2"])
all_bins = [*range(1,max(bins["bin2"])+1)]
for j in combinations(all_bins, 2):
		bc.loc[len(bc.index)] = j
print(bc)
"""
# to save as hicrep format
for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"]:
	chrom = "".join(["Pf3D7_",i,"_v3"])
	df_sub = df[(df["chr1"] == chrom) & (df["chr2"] == chrom)]
	df_sub.drop(["chr1","chr2"], axis=1, inplace=True)
	df_sub.to_csv("".join(["hicrep/",os.path.basename(sys.argv[2]).replace(".matrix","".join(["_",chrom,".matrix"]))]), 
					sep="\t", header=False, index=False)

# to save as genomeDisco format
#df.to_csv(sys.argv[2].replace("matrix","gd"), sep="\t", header=False, index=False)
"""