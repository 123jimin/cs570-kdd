#!/usr/bin/env python

import csv

from operator import itemgetter
from sklearn.externals import joblib

print("Loading data...")
csv_ValidSolution = csv.reader(open("../data/raw/ValidSolution.csv", 'r'))
csv_ValidSolution.next()
csv_Answer = csv.reader(open("../data/result/out_Valid.csv", 'r'))
csv_Answer.next()

print("Computing score...")
total_score = 0.0
total_count = 0
for solution, answer in zip(csv_ValidSolution, csv_Answer):
	if solution[0] != answer[0]:
		raise Exception("AuthorID does not match!")
	set_Papers = set(solution[1].split(' '))
	list_answers = answer[1].split(' ')
	cur_score = 0.0
	count_find = 0
	for i in range(len(list_answers)):
		if list_answers[i] in set_Papers:
			count_find += 1
			cur_score += count_find / (i+1.0)
	cur_score /= len(set_Papers)
	total_score += cur_score
	total_count += 1

print("Score: %f" % (total_score / total_count))
