import csv

def getFeatureCSV(file_name, header=True):
	print("Reading %s..." % file_name)
	csv_file = csv.reader(open("../data/feature/%s.csv" % file_name, 'r'))
	if header:
		csv_file.next()
	return csv_file

dict_features_pa = dict()
dict_features_a = dict()

for row in getFeatureCSV("paperauthor_author_feature"):
	key = (int(row[0]), int(row[1]))
	dict_features_pa[key] = map(float, row[2:])

for row in getFeatureCSV("feature1"):
	dict_features_a[int(row[0])] = map(float, row[1:])

for row in getFeatureCSV("feature_HBN", False):
	key = (int(row[0]), int(row[1]))
	dict_features_pa[key].extend(map(float, row[2:]))

def getFeature(AuthorId, PaperId):
	key = (PaperId, AuthorId)
	if key not in dict_features_pa:
		raise Exception("key not in features")
	if AuthorId not in dict_features_a:
		raise Exception("author not in features")
	return dict_features_pa[(PaperId, AuthorId)] + dict_features_a[AuthorId]
