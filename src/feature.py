import csv

def getFeatureCSV(file_name, header=True):
	print("Reading %s..." % file_name)
	csv_file = csv.reader(open("../data/feature/%s.csv" % file_name, 'r'))
	if header:
		csv_file.next()
	return csv_file

dict_features_pa = dict()
dict_features_a = dict()

set_keys = set()

for row in getFeatureCSV("paperauthor_author_feature"):
	key = (int(row[0]), int(row[1]))
	if key not in set_keys:
		set_keys.add(key)
		dict_features_pa[key] = map(float, row[2:])

set_keys.clear()

for row in getFeatureCSV("feature1"):
	if int(row[0]) not in set_keys:
		set_keys.add(int(row[0]))
		dict_features_a[int(row[0])] = map(float, row[1:])

set_keys.clear()

for row in getFeatureCSV("feature2"):
	key = (int(row[1]), int(row[0]))
	if key in dict_features_pa and key not in set_keys:
		set_keys.add(key)
		dict_features_pa[key].extend(map(float, row[2:]))

set_keys.clear()

for row in getFeatureCSV("feature4"):
	key = (int(row[1]), int(row[0]))
	if key in dict_features_pa and key not in set_keys:
		set_keys.add(key)
		dict_features_pa[key].extend(map(float, row[2:]))

set_keys.clear()

for row in getFeatureCSV("feature_HBN", False):
	key = (int(row[0]), int(row[1]))
	if key in dict_features_pa and key not in set_keys:
		set_keys.add(key)
		dict_features_pa[key].extend(map(float, row[2:]))

set_keys.clear()
n = 0
o = None
k = None

for row in getFeatureCSV("feature_test"):
	key = (int(row[0]), int(row[1]))
	# dict_features_pa[key] = [int(row[2])]
	dict_features_pa[key].extend(map(float, row[3:]))
	if n == 0:
		o = dict_features_pa[key]
		n = len(o)
		k = key
	elif n != len(dict_features_pa[key]):
		print("%d %d" % (n, len(dict_features_pa[key])))
		print(k)
		print(o)
		print(key)
		print(dict_features_pa[key])
		raise Exception("Feature lengths differ")

def getFeature(AuthorId, PaperId):
	key = (PaperId, AuthorId)
	if key not in dict_features_pa:
		raise Exception("key not in features")
	return dict_features_pa[key]
	if AuthorId not in dict_features_a:
		raise Exception("author not in features")
	return dict_features_pa[key] + dict_features_a[AuthorId]
