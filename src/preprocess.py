#!/usr/bin/env python

import psycopg2

copaper = dict()
coauthor = dict()

conn = psycopg2.connect("dbname=kdd2013authorpaperidentification user=postgres password=postgres")
cur = conn.cursor()
cur.execute("""SELECT paperid, authorid FROM paperauthor;""")

print("Filling copapers and coauthors...")
for row in cur.fetchall():
	if row[1] in copaper:
		copaper[row[1]].append(row[0])
	else:
		copaper[row[1]] = [row[0]]
	if row[0] in coauthor:
		coauthor[row[0]].append(row[1])
	else:
		coauthor[row[0]] = [row[1]]

print("Done.")

cur.close()
conn.close()
