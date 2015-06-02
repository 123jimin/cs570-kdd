#!/usr/bin/env python

import csv

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.externals import joblib

from feature import getFeature

classifier = RandomForestClassifier(50)
# classifier = KNeighborsClassifier(10)

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

classifier.fit(train_data, train_cat)

print("Saving model...")

joblib.dump(classifier, "../data/model/classifier")
