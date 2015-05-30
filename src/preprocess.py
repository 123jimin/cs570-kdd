#!/usr/bin/env python

import csv, pandas, jellyfish, math
import numpy as np

def getCSV(file_name, index=None):
	data = pandas.read_csv("../data/raw/%s.csv" % file_name,
		compression = None,
		index_col = index
	)
	return data

print("Preparing data storge...")
dict_coPaper = dict()
dict_coAuthor = dict()
set_pairs = set()

print("Reading Author...")
csv_Author = getCSV("Author", 0)

print("Reading Paper...")
csv_Paper = getCSV("Paper", 0)

print("Reading Valid & Test")
csv_Valid = csv.reader(open("../data/raw/Valid.csv", 'r'))
csv_Valid.next()
for row in csv_Valid:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

csv_Train = csv.reader(open("../data/raw/Train.csv", 'r'))
csv_Train.next()
for row in csv_Train:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))
	for str_PaperId in row[2].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

size_pairs = len(set_pairs)

print("Reading PaperAuthor...")
csv_PaperAuthor = getCSV("PaperAuthor", [0, 1])

size_PaperAuthor = len(csv_PaperAuthor.values)
p_next = 5
curr_ind = 0

print("Computing co-data...")
for index in csv_PaperAuthor.index:
	if index[0] != index[0] or index[1] != index[1]:
		raise Exception("Row %d: invalid" % curr_ind)
	if index[1] in dict_coPaper:
		dict_coPaper[index[1]].append(index[0])
	else:
		dict_coPaper[index[1]] = [index[0]]
	if index[0] in dict_coAuthor:
		dict_coAuthor[index[0]].append(index[1])
	else:
		dict_coAuthor[index[0]] = [index[1]]
	curr_ind +=1
	if curr_ind * 100 >= size_PaperAuthor * p_next:
		print("%d%%..." % p_next)
		p_next += 5

p_next = 1
curr_ind = 0

print("Computing pair features...")
for index in set_pairs:
	curr_ind +=1
	if curr_ind * 100 >= size_pairs * p_next:
		print("%d%%..." % p_next)
		p_next += 1

print("Writing results to file...")
# TODO

print("Done.")
