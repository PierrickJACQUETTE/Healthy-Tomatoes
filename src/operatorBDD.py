from elasticsearch import helpers, Elasticsearch
import BDD as bdd
import csv

medianeVoteAverage = 5

def BDDfromCSV(csv_filename, tableTrain, tableTest, numberSeparation):
	es = bdd.BDD.get_instance();
	try :
		es.indices.delete(index=bdd.index)
	except :
		pass

	es.indices.create(index=bdd.index)
	print("now indexing...")

	with open(csv_filename) as csvfile:
		reader = csv.DictReader(csvfile)
		i = 2
		for row in reader:
			try:
				vote = float(row['vote_average'])
				if(vote > medianeVoteAverage and vote <= 10):
					row['SUCCESS'] = 1
				elif(vote <= 5 and vote >= 0):
					row['SUCCESS'] = 0
				else:
					newVote = vote%10
					row['vote_average'] = newVote
					row['SUCCESS'] = newVote
				if(i<numberSeparation):
					es.index(index=bdd.index, doc_type=tableTrain, body=row)
				else:
					es.index(index=bdd.index, doc_type=tableTest, body=row)
			except :
				print("Error row : ", i)
				pass
			i = i+1
			if(i%250 == 0):
				print("Add rows : ", i)

def BDDSearch(query):
	es = bdd.BDD.get_instance();
	res = es.search(index=bdd.index, doc_type=bdd.tableMovieTrain, body=query, size=4000)
	print("Got %d Hits:" % res['hits']['total'])
	return res

def BDDSearchAll():
	myquery={"query": {"match_all": {}}}
	return BDDSearch(myquery);

def BDDSearchCategorie(key, value):
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery);
