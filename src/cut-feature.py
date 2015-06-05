#!/usr/bin/env python

import csv

set_pairs = set()

def getCSV(file_name, header=True):
	reader = csv.reader(open("../data/%s.csv" % file_name, 'rb'))
	if header:
		reader.next()
	return reader

def cutFeaturePA(file_name, header=True, rev=False):
	print("Cutting feature %s..." % file_name)
	csv_in = getCSV("feature/%s" % file_name, False)
	csv_in_header = None
	set_keys = set()
	if header:
		csv_in_header = csv_in.next()
	csv_out = csv.writer(open("../data/feature/%s_cut.csv" % file_name, 'wb'))
	if header:
		csv_out.writerow(csv_in_header)
	for row in csv_in:
		is_in_pairs = False
		new_row = None
		if rev:
			new_row = [row[1], row[0]] + row[2:]
		else:
			new_row = row
		key = (int(new_row[0]), int(new_row[1]))
		if key in set_pairs and key not in set_keys:
			set_keys.add(key)
			csv_out.writerow(new_row)

csv_Valid = getCSV("raw/Valid")
for row in csv_Valid:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

csv_Train = getCSV("raw/Train")
for row in csv_Train:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))
	for str_PaperId in row[2].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

"""
cutFeaturePA("paperauthor_author_feature")
cutFeaturePA("feature2", rev=True)
cutFeaturePA("feature4", rev=True)
cutFeaturePA("feature_HBN", header=False)
"""

cutFeaturePA("feature5", rev=True)
