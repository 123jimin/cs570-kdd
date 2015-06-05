import math, csv

def getFeatureCSV(file_name, header=True):
	print("Reading %s..." % file_name)
	csv_file = csv.reader(open("../data/feature/%s.csv" % file_name, 'r'))
	if header:
		csv_file.next()
	return csv_file

dict_features_pa = dict()
dict_features_a = dict()
set_keys_tmp = set()

def addFeatures(file_name, header=True, rev=False):
	set_keys_tmp.clear()
	for row in getFeatureCSV(file_name, header):
		key = None
		if rev:
			key = (int(row[1]), int(row[0]))
		else:
			key = (int(row[0]), int(row[1]))
		if key not in set_keys_tmp:
			set_keys_tmp.add(key)
			if key not in dict_features_pa:
				dict_features_pa[key] = list()
			if file_name == "feature_test":
				# ignore pair feature
				dict_features_pa[key].extend(map(float, row[3:]))
			else:
				dict_features_pa[key].extend(map(float, row[2:]))

def normalizeFeatures(dict_features):
	print("Normalizing features...")
	num_rows = float(len(dict_features))
	sum_values = None
	sum_sq_values = None
	for key in dict_features:
		val = dict_features[key]
		if sum_values is None:
			sum_values = [0] * len(val)
			sum_sq_values = [0] * len(val)
		for i in xrange(len(val)):
			sum_values[i] += val[i]
			sum_sq_values[i] += val[i]**2
	
	sample_average = [0] * len(sum_values)
	sample_variance = [0] * len(sum_values)

	for i in xrange(len(sum_values)):
		sample_average[i] = sum_values[i] / num_rows 
		sample_variance[i] = sum_sq_values[i] / num_rows - sample_average[i] ** 2
		sample_variance[i] *= num_rows / (num_rows - 1.0)
		sample_variance[i] = math.sqrt(sample_variance[i])

	for key in dict_features:
		for i in xrange(len(sample_average)):
			if sample_variance[i] > 0.0:
				dict_features[key][i] = (dict_features[key][i] - sample_average[i]) / sample_variance[i]

set_keys_tmp.clear()

for row in getFeatureCSV("feature1"):
	if int(row[0]) not in set_keys_tmp:
		set_keys_tmp.add(int(row[0]))
		dict_features_a[int(row[0])] = map(float, row[1:])

addFeatures("paperauthor_author_feature_cut")
addFeatures("feature2_cut")
addFeatures("feature4_cut")
addFeatures("feature5_cut")
addFeatures("feature_HBN_cut", header=False)
addFeatures("feature_test")

normalizeFeatures(dict_features_pa)
normalizeFeatures(dict_features_a)

def getFeature(AuthorId, PaperId):
	key = (PaperId, AuthorId)
	if key not in dict_features_pa:
		raise Exception("key not in features")
	return dict_features_pa[key]
	if AuthorId not in dict_features_a:
		raise Exception("author not in features")
	return dict_features_pa[key] + dict_features_a[AuthorId]
