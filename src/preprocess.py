#!/usr/bin/env python

import pandas, jellyfish, math
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
list_features = list()

print("Reading Author...")
csv_Author = getCSV("Author", 0)
#for row in csv_Author.values:
	# Id, Name, Affiliation
	#pass

print("Reading Paper...")
csv_Paper = getCSV("Paper", 0)
#for row in csv_Paper.values:
	# Id, Title, Year, ConferenceId, JournalId, Keyword
	#pass

print("Reading PaperAuthor...")
csv_PaperAuthor = getCSV("PaperAuthor", [0, 1])

size_PaperAuthor = len(csv_PaperAuthor.values)
p_next = 5
curr_ind = 0
non_existing_author = 0
non_existing_paper = 0

print(csv_PaperAuthor.head(10))

print("Computing co-data...")
for index in csv_PaperAuthor.index:
	# PaperId, AuthorId, Name, Affiliation
	if index[0] != index[0] or index[1] != index[1]:
		raise Exception("Row %d: invalid" % curr_ind)
	if index[1] in dict_coPaper:
		dict_coPaper[index[1]].append(index[0])
	else:
		if index[1] not in csv_Author.index:
			non_existing_author += 1
		dict_coPaper[index[1]] = [index[0]]
	if index[0] in dict_coAuthor:
		dict_coAuthor[index[0]].append(index[1])
	else:
		if index[0] not in csv_Paper.index:
			non_existing_paper += 1
		dict_coAuthor[index[0]] = [index[1]]
	curr_ind +=1
	if curr_ind * 100 >= size_PaperAuthor * p_next:
		print("%d%%..." % p_next)
		p_next += 5

print("Author/Paper not in CSV: %d/%d" % (non_existing_author, non_existing_paper))

p_next = 1
curr_ind = 0

print("Computing pair features...")
for index in csv_PaperAuthor.index:
	coPaper = dict_coPaper[index[1]]
	coAuthor = dict_coAuthor[index[0]]

	features = (
		1, 2, 3
	)

	list_features.append(features)

	curr_ind +=1
	if curr_ind * 100 >= size_PaperAuthor * p_next:
		print("%d%%..." % p_next)
		p_next += 1

print("Writing results to file...")
print(len(list_features))

print("Done.")
