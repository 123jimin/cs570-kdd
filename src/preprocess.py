#!/usr/bin/env python

import csv, pandas, jellyfish, math
import numpy as np

from urlparse import urlparse

def getCSV(file_name):
	reader = csv.reader(open("../data/raw/%s.csv" % file_name, 'rb'))
	reader.next()
	return reader

def getUrl(Paper):
	global dict_Conference, dict_Journal
	url = None
	if Paper[2] > 0 and Paper[2] in dict_Conference:
		url = dict_Conference[Paper[2]][2]
	elif Paper[3] > 0 and Paper[3] in dict_Journal:
		url = dict_Journal[Paper[3]][2]
	return url

def getDomain(url):
	if url is None or url == "":
		return ""
	if url[0:5] != "http:" and url[0:6] != "https:":
		url = "http://"+url
	parsed_url = urlparse(url)
	if '.' not in parsed_url.netloc:
		return ""
	domain = parsed_url.netloc.split('.')[-1]
	if ':' in domain:
		domain = domain.split(':')[0]
	if len(domain) >= 10:
		return ""
	return domain.lower()

# Id: Title, Year, ConferenceId, JournalId, Keyword
dict_Paper = dict()
# Id: Name, Affiliation
dict_Author = dict()
# Id: ShortName, FullName, HomePage
dict_Conference = dict()
# Id: ShortName, FullName, HomePage
dict_Journal = dict()

dict_authorDomain = dict()
dict_authorDomainCount = dict()
dict_pairCount = dict()

dict_coPaper = dict()
dict_coAuthor = dict()
set_pairs = set()

print("Reading Author...")
csv_Author = getCSV("Author")
for row in csv_Author:
	dict_Author[int(row[0])] = row[1:]

print("Reading Paper...")
csv_Paper = getCSV("Paper")
for row in csv_Paper:
	PaperId, Title, Year, ConferenceId, JournalId, Keyword = row
	dict_Paper[int(PaperId)] = (Title, Year, int(ConferenceId), int(JournalId), Keyword)

print("Reading Valid & Test")
csv_Valid = getCSV("Valid")
for row in csv_Valid:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

csv_Train = getCSV("Train")
for row in csv_Train:
	AuthorId = int(row[0])
	for str_PaperId in row[1].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))
	for str_PaperId in row[2].split(' '):
		set_pairs.add((int(str_PaperId), AuthorId))

size_pairs = len(set_pairs)
print("Rows = %d" % size_pairs)

print("Reading Conference & Journal")
dict_domain = dict()
csv_Conference = getCSV("Conference")
for row in csv_Conference:
	dict_Conference[int(row[0])] = row[1:]
	domain = getDomain(row[3])
	if domain in dict_domain:
		dict_domain[domain] += 1
	else:
		dict_domain[domain] = 1

csv_Journal = getCSV("Journal")
for row in csv_Journal:
	dict_Journal[int(row[0])] = row[1:]
	domain = getDomain(row[3])
	if domain in dict_domain:
		dict_domain[domain] += 1
	else:
		dict_domain[domain] = 1

list_domain = dict_domain.keys()

print("Reading PaperAuthor...")
csv_PaperAuthor = getCSV("PaperAuthor")

print("Computing co-data...")
for row in csv_PaperAuthor:
	PaperId, AuthorId = int(row[0]), int(row[1])
	if (PaperId, AuthorId) in dict_pairCount:
		dict_pairCount[(PaperId, AuthorId)] += 1
	else:
		dict_pairCount[(PaperId, AuthorId)] = 1
	if AuthorId in dict_coPaper:
		dict_coPaper[AuthorId].append(PaperId)
	else:
		dict_coPaper[AuthorId] = [PaperId]
	if PaperId in dict_coAuthor:
		dict_coAuthor[PaperId].append(AuthorId)
	else:
		dict_coAuthor[PaperId] = [AuthorId]
	if PaperId in dict_Paper:
		Paper = dict_Paper[PaperId]
		url = getUrl(Paper)
		domain = getDomain(url)
		if AuthorId in dict_authorDomain:
			if domain in dict_authorDomain[AuthorId]:
				dict_authorDomain[AuthorId][domain] += 1
			else:
				dict_authorDomain[AuthorId][domain] = 1
			dict_authorDomainCount[AuthorId] += 1
		else:
			dict_authorDomain[AuthorId] = dict()
			dict_authorDomain[AuthorId][domain] = 1
			dict_authorDomainCount[AuthorId] = 1

print("Computing pair features...")
p_next, curr_ind = 5, 0
csv_Feature = csv.writer(open("../data/feature/feature_test.csv", 'wb'))
csv_Feature.writerow("PaperId AuthorId PairCount DomainId AuthorDomainCount DomainPercentage".split(' '))
for index in set_pairs:
	PaperId, AuthorId = index
	if index in dict_pairCount:
		pairCount = dict_pairCount[index]
	else:
		pairCount = 0
	DomainId = -1
	DomainPercentage = -1
	AuthorDomainCount = 0
	if PaperId in dict_Paper:
		Paper = dict_Paper[PaperId]
		url = getUrl(Paper)
		domain = getDomain(url)
		if domain != "" and domain in list_domain:
			DomainId = list_domain.index(domain)
		if AuthorId in dict_authorDomain:
			AuthorDomainCount = len(dict_authorDomain[AuthorId])
			if domain in dict_authorDomain[AuthorId]:
				DomainPercentage = (dict_authorDomain[AuthorId][domain] + 0.0) / dict_authorDomainCount[AuthorId]
	csv_Feature.writerow([PaperId, AuthorId, pairCount, DomainId, AuthorDomainCount, DomainPercentage])
	curr_ind +=1
	if curr_ind * 100 >= size_pairs * p_next:
		print("%d%%..." % p_next)
		p_next += 5

print("Done.")
