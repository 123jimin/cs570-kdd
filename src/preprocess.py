#!/usr/bin/env python

import csv

def getCSV(file_name):
	reader = csv.reader(open("../data/raw/%s.csv" % file_name, 'r'))
	reader.next() # ignore column titles
	return reader

csv_PaperAuthor = getCSV("PaperAuthor")

i = 0

for PaperId, AuthorId, Name, Affiliation in csv_PaperAuthor:
	pass
