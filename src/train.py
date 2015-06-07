#!/usr/bin/env python

import csv, time
from operator import itemgetter

import numpy
from scipy import linalg

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

t_start = time.time()
from feature import getFeature

t_feature = time.time()

print("Load t = %d seconds" % (t_feature - t_start))

# classifier = AdaBoostClassifier(DecisionTreeClassifier(), 30)
# classifier = RandomForestClassifier(50)
# classifier = KNeighborsClassifier(3)
classifier = SVC(C=0.025, kernel='linear', gamma=0.0)
# classifier = DecisionTreeClassifier(max_depth=9)
# classifier = GradientBoostingClassifier(n_estimators=300, max_depth=5)
# classifier = AdaBoostClassifier(GradientBoostingClassifier(n_estimators=100, max_depth=5), 10)

print("Reading Train.csv...")
train_data = list()
train_cat = list()
def addTrainPairs(AuthorId, PaperId, category):
	train_data.append(getFeature(AuthorId, PaperId))
	train_cat.append(category)
csv_Train = csv.reader(open("../data/raw/Train.csv", 'r'))
csv_Train.next()
for row in csv_Train:
	AuthorId = int(row[0])
	for str_ConfirmedPaperId in row[1].split(' '):
		addTrainPairs(AuthorId, int(str_ConfirmedPaperId), 1)
	for str_DeletedPaperId in row[2].split(' '):
		addTrainPairs(AuthorId, int(str_DeletedPaperId), 0)

print("Training...")

t_begin_train = time.time()
classifier.fit(train_data, train_cat)
t_end_train = time.time()

print("Fit t = %d seconds" % (t_end_train - t_begin_train))

print("Saving model...")

joblib.dump(classifier, "../data/model/classifier")

## test

print("Loading model...")
classifier = joblib.load("../data/model/classifier")

print("Computing...")
valid_data = list()
csv_Valid = csv.reader(open("../data/raw/Valid.csv", 'r'))
csv_Valid.next()
list_Valid = list(csv_Valid)
size_Valid = len(list_Valid)
out_file = file("../data/result/out_Valid.csv", 'w')
out_file.write("AuthorId,PaperIds\n")
p_next = 5
curr_ind = 0
t_begin_valid = time.time()
for row in list_Valid:
	AuthorId = int(row[0])
	paper_prob = list()
	for str_PaperId in row[1].split(' '):
		PaperId = int(str_PaperId)
		feature = getFeature(AuthorId, PaperId)
		paper_prob.append((str_PaperId, classifier.predict_proba([feature])[0][1]))
	paper_prob.sort(key=itemgetter(1), reverse=True)
	paper_list = map(itemgetter(0), paper_prob)
	out_file.write("%d,%s\n" % (AuthorId, ' '.join(paper_list)))
	curr_ind +=1
	if curr_ind * 100 >= size_Valid * p_next:
		print("%d%%..." % p_next)
		p_next += 5
t_end_valid = time.time()

print("Valid t = %d seconds" % (t_end_valid - t_begin_valid))

out_file.close()
print("Done.")
