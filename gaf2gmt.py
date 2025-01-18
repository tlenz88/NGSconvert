#!/usr/bin/env python

import sys
import csv

lst = dict()

with open(sys.argv[1], 'r') as f:
	gaf = csv.reader(f, delimiter='\t')
	for i in gaf:
		gene = i[1]
		GO = i[3]
		if GO not in lst.keys():
			lst[GO] = '\t.\t' + gene
		else:
			if gene not in lst[GO]:
				lst[GO] += '\t' + gene

with open(sys.argv[2], 'r') as g:
	GO_sets = csv.reader(g, delimiter='\t')
	for i in GO_sets:
		GO = i[0]
		annotation = i[1].replace(" ", "_")
		if GO in lst.keys():
			lst[annotation] = lst[GO]
			del(lst[GO])

with open(sys.argv[1].replace(".gaf", ".gmt"), 'w+') as f:
	for key in lst.keys():
		f.write("%s%s\n" % (key, lst[key]))