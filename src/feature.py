import math, csv, numpy

numpy.set_printoptions(threshold='nan')

from scipy import linalg

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

def normalizeFeatures(dict_features, feature_name):
	print("Normalizing feature %s..." % feature_name)
	num_rows = float(len(dict_features))
	sum_values = None
	sum_sq_values = None
	first_val = None
	val_changed = None
	for key in dict_features:
		val = dict_features[key]
		if sum_values is None:
			sum_values = [0] * len(val)
			sum_sq_values = [0] * len(val)
			first_val = val
			val_changed = [False] * len(val)
		for i in xrange(len(val)):
			if numpy.isnan(val[i]) or numpy.isinf(val[i]):
				val[i] = 0
			sum_values[i] += val[i]
			sum_sq_values[i] += val[i]**2
			if val[i] != first_val[i]:
				val_changed[i] = True
	
	sample_average = [0] * len(sum_values)
	sample_variance = [0] * len(sum_values)

	print("# of constant features: %d of %d" % (len([1 for x in val_changed if not x]), len(sample_average)))

	for i in xrange(len(sum_values)):
		sample_average[i] = sum_values[i] / num_rows 
		sample_variance[i] = sum_sq_values[i] / num_rows - sample_average[i] ** 2
		sample_variance[i] *= num_rows / (num_rows - 1.0)
		sample_variance[i] = math.sqrt(sample_variance[i])

	for key in dict_features:
		result_feature = []
		for i in xrange(len(sample_average)):
			if val_changed[i]:
				f_val = dict_features[key][i]
				result_feature.append((f_val - sample_average[i]) / sample_variance[i])
		dict_features[key] = numpy.array(result_feature)


set_keys_tmp.clear()

for row in getFeatureCSV("feature1"):
	if int(row[0]) not in set_keys_tmp:
		set_keys_tmp.add(int(row[0]))
		dict_features_a[int(row[0])] = map(float, row[1:])

addFeatures("paperauthor_author_feature_cut")
addFeatures("feature2_cut")
addFeatures("feature4_cut")
addFeatures("feature6_cut")
addFeatures("feature_HBN_cut", header=False)
addFeatures("feature_test")

print("Merging features...")
for key, val in dict_features_pa.iteritems():
	dict_features_pa[key].extend(dict_features_a[key[1]])

dict_features_a.clear()

normalizeFeatures(dict_features_pa, "PaperAuthor")
# normalizeFeatures(dict_features_a, "Author")

print("Doing PCA...")
S = 0
for key in dict_features_pa:
	row = dict_features_pa[key]
	xx = numpy.array(row).reshape((len(row), 1))
	S += numpy.dot(xx, numpy.transpose(xx))

eigval, eigvec = linalg.eigh(S)
eigvec = numpy.transpose(eigvec)

zeig = sorted(zip(eigval, eigvec), cmp=lambda x,y: 1 if abs(y[0])>abs(x[0]) else -1)

evecs = numpy.array([b for a,b in zeig])
evals = numpy.array([a for a,b in zeig])

print(evals)
print(evecs)

cut_features = 3

print("Projecting... (# of features = %d)" % cut_features)
for key in dict_features_pa:
	x = dict_features_pa[key]
	y = []
	for i in xrange(cut_features):
		y.append(numpy.dot(x, evecs[i].reshape(len(x))))
	dict_features_pa[key] = numpy.array(y)

def getFeature(AuthorId, PaperId):
	key = (PaperId, AuthorId)
	return dict_features_pa[key]
