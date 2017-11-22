from elasticsearch import helpers, Elasticsearch
import BDD as bdd
import csv

def BDDfromCSV(csv_filename, table):
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
			try :
				es.index(index=bdd.index,doc_type=table,body=row)
			except :
				print("Error row : ", i)
				pass
			i = i+1
			if(i%250 == 0):
				print("Add rows : ", i)

def BDDSearch(query):
	es = bdd.BDD.get_instance();
	res = es.search(index=bdd.index, body=query)
	print("Got %d Hits:" % res['hits']['total'])
	return res;

def BDDSearchAll():
	myquery={"query": {"match_all": {}}}
	return BDDSearch(myquery);

def BDDSearchCategorie(key, value):
	myquery={"_source": ["title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery);

