#!/usr/bin/env python

import csv, pandas, jellyfish, math
import numpy as np

def getCSV(file_name):
	reader = csv.reader(open("../data/raw/%s.csv" % file_name, 'rb'))
	reader.next()
	return reader

print("Preparing data storge...")
dict_coPaper = dict()
dict_coAuthor = dict()
set_pairs = set()

print("Reading Author...")
csv_Author = getCSV("Author")

print("Reading Paper...")
csv_Paper = getCSV("Paper")

print("Reading Valid & Test")
csv_Valid = getCSV("Valid")
for row in csv_Valid:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

csv_Train = getCSV("Train")
for row in csv_Train:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))
	for str_PaperId in row[2].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

size_pairs = len(set_pairs)

print("Reading PaperAuthor...")
csv_PaperAuthor = getCSV("PaperAuthor")

print("Computing co-data...")
for row in csv_PaperAuthor:
	break
	PaperId, AuthorId = int(row[0]), int(row[1])
	if AuthorId in dict_coPaper:
		dict_coPaper[AuthorId].append(PaperId)
	else:
		dict_coPaper[AuthorId] = [PaperId]
	if PaperId in dict_coAuthor:
		dict_coAuthor[PaperId].append(AuthorId)
	else:
		dict_coAuthor[PaperId] = [AuthorId]

print("Computing pair features...")
p_next, curr_ind = 5, 0
csv_Feature = csv.writer(open("../data/feature/feature_test.csv", 'wb'))
csv_Feature.writerow("PaperId AuthorId TestFeature1".split(' '))
for index in set_pairs:
	PaperId, AuthorId = index
	csv_Feature.writerow([PaperId, AuthorId, 42])
	curr_ind +=1
	if curr_ind * 100 >= size_pairs * p_next:
		print("%d%%..." % p_next)
		p_next += 5

print("Done.")
