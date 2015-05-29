#!/usr/bin/env python

import pandas

def getCSV(file_name):
	data = pandas.read_csv("../data/raw/%s.csv" % file_name, compression=None)
	return data.values

dict_coPaper = dict()
dict_coAuthor = dict()

print("Reading Paper...")
csv_Paper = getCSV("Paper")
for row in csv_Paper:
	# Id, Title, Year, ConferenceId, JournalId, Keyword
	pass

print("Reading Author...")
csv_Author = getCSV("Author")
for row in csv_Author:
	# Id, Name, Affiliation
	pass

print("Reading PaperAuthor...")
csv_PaperAuthor = getCSV("PaperAuthor")

p_next = 5
curr_ind = 0

print("Computing co-data...")
for row in csv_PaperAuthor:
	# PaperId, AuthorId, Name, Affiliation
	if row[1] in dict_coPaper:
		dict_coPaper[row[1]].append(row[0])
	else:
		dict_coPaper[row[1]] = [row[0]]
	if row[0] in dict_coAuthor:
		dict_coAuthor[row[0]].append(row[1])
	else:
		dict_coAuthor[row[0]] = [row[1]]
	curr_ind +=1
	if curr_ind * 100 >= csv_PaperAuthor.size * p_next:
		print("%d%%..." % p_next)
		p_next += 5

print("Computing pair features...")
print("Done.")
