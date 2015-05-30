#!/usr/bin/env python

import csv

from operator import itemgetter

from sklearn.externals import joblib
from feature import getFeature

print("Loading model...")
classifier = joblib.load("../data/model/classifier")

print("Computing...")
valid_data = list()
csv_Valid = csv.reader(open("../data/raw/Valid.csv", 'r'))
csv_Valid.next()
list_Valid = list(csv_Valid)
size_Valid = len(list_Valid)
out_lines = ["AuthorId,PaperIds"]
p_next = 5
curr_ind = 0
for row in list_Valid:
	AuthorId = int(row[0])
	paper_prob = list()
	for str_PaperId in row[1].split(' '):
		PaperId = int(str_PaperId)
		feature = getFeature(AuthorId, PaperId)
		paper_prob.append((str_PaperId, classifier.predict_proba([feature])[0][1]))
	paper_prob.sort(key=itemgetter(1), reverse=True)
	paper_list = map(itemgetter(0), paper_prob)
	out_lines.append("%d,%s" % (AuthorId, ' '.join(paper_list)))
	curr_ind +=1
	if curr_ind * 100 >= size_Valid * p_next:
		print("%d%%..." % p_next)
		p_next += 5

print("Done.")
