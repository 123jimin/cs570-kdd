#!/usr/bin/env python

import csv

from operator import itemgetter
from sklearn.externals import joblib

print("Loading data...")
csv_ValidSolution = csv.reader(open("../data/raw/ValidSolution.csv", 'r'))
csv_ValidSolution.next()
csv_Respond = csv.reader(open("../data/result/out_Valid.csv", 'r'))
csv_Respond.next()

csv_Wrong = csv.writer(open("../data/result/wrong_Valid.csv", 'wb'))
csv_Wrong.writerow("AuthorId FalsePositive FalseNegative".split(' '))

print("Computing score...")
total_score = 0.0
total_count = 0
for solution, respond in zip(csv_ValidSolution, csv_Respond):
	if solution[0] != respond[0]:
		raise Exception("AuthorID does not match!")
	list_Papers = solution[1].split(' ')
	set_Papers = set(list_Papers)
	list_responds = respond[1].split(' ')
	cur_score = 0.0
	count_find = 0
	list_falsePositive = list()
	list_falseNegative = list()
	len_answers = len([x for x in list_responds if x in set_Papers])
	for i in range(len(list_responds)):
		if list_responds[i] in set_Papers:
			count_find += 1
			cur_score += count_find / (i+1.0)
			if len(list_falsePositive) > 0:
				list_falseNegative.append(list_responds[i])
		else:
			if count_find < len_answers:
				list_falsePositive.append(list_responds[i])
	csv_Wrong.writerow((respond[0], ' '.join(list_falsePositive), ' '.join(list_falseNegative)))
	cur_score /= count_find
	total_score += cur_score
	total_count += 1

print("Score: %f" % (total_score / total_count))
